
import logging
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# -----------------------------
# CONFIGURATION
# -----------------------------

BASE_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path("output")
LOG_DIR = Path("logs")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "books_data.csv"
LOG_FILE = LOG_DIR / "scraper.log"


# -----------------------------
# LOGGING
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


# -----------------------------
# HTTP SESSION WITH RETRIES
# -----------------------------

session = requests.Session()

retry_strategy = Retry(
    total=3,
    connect=3,
    read=3,
    status=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    respect_retry_after_header=True
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


# -----------------------------
# EXTRACT ONE PAGE
# -----------------------------

def extract_page(url):
    """Fetch one page and extract its book records."""

    response = session.get(url, timeout=(5, 20))
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    book_elements = soup.select("article.product_pod")

    if not book_elements:
        raise ValueError(f"No book records found on {url}")

    records = []

    for book in book_elements:
        try:
            title = book.h3.a["title"]

            price_text = book.select_one(
                ".price_color"
            ).get_text(strip=True)

            price_text = (
                price_text.replace("Â", "")
                .replace("£", "")
                .strip()
            )

            price = float(price_text)

            availability = book.select_one(
                ".availability"
            ).get_text(" ", strip=True)

            rating_classes = book.select_one(
                "p.star-rating"
            )["class"]

            rating = next(
                (item for item in rating_classes
                 if item in ["One", "Two", "Three", "Four", "Five"]),
                None
            )

            if not title or price < 0 or rating is None:
                raise ValueError("Invalid book data")

            records.append({
                "Title": title,
                "Price_GBP": price,
                "Availability": availability,
                "Rating": rating,
                "Source_URL": url
            })

        except (AttributeError, KeyError, TypeError, ValueError) as error:
            logger.warning(
                "Skipping an invalid record on %s: %s",
                url,
                error
            )

    if not records:
        raise ValueError(f"No valid records extracted from {url}")

    return records, soup


# -----------------------------
# SCRAPE ALL PAGES
# -----------------------------

def scrape_all_pages():
    current_url = BASE_URL
    page_number = 1
    all_records = []
    failed_pages = []

    while current_url:
        logger.info(
            "Processing page %s: %s",
            page_number,
            current_url
        )

        try:
            page_records, soup = extract_page(current_url)
            all_records.extend(page_records)

            logger.info(
                "Extracted %s records from page %s",
                len(page_records),
                page_number
            )

            next_link = soup.select_one("li.next a")

            if next_link:
                current_url = urljoin(
                    current_url,
                    next_link["href"]
                )
                page_number += 1
            else:
                current_url = None

            if current_url:
                time.sleep(0.5)

        except (
            requests.RequestException,
            ValueError
        ) as error:
            logger.error(
                "Page %s failed: %s",
                page_number,
                error
            )

            failed_pages.append({
                "Page_Number": page_number,
                "URL": current_url,
                "Error": str(error)
            })

            # Stop rather than silently skipping a page.
            break

    return all_records, page_number, failed_pages


# -----------------------------
# SAVE RESULTS
# -----------------------------

def main():
    records, pages_processed, failed_pages = scrape_all_pages()

    if failed_pages:
        logger.error(
            "Scraping incomplete. Failed pages: %s",
            len(failed_pages)
        )

        failure_file = OUTPUT_DIR / "failed_pages.csv"
        pd.DataFrame(failed_pages).to_csv(
            failure_file,
            index=False,
            encoding="utf-8-sig"
        )

        logger.error("Failure details saved to %s", failure_file)
        logger.error("The existing main CSV has not been overwritten.")
        return

    if not records:
        logger.error("No records extracted. Nothing was saved.")
        return

    df = pd.DataFrame(records)

    # Remove only fully identical rows.
    df = df.drop_duplicates().reset_index(drop=True)

    # Basic final validation.
    required_columns = [
        "Title", "Price_GBP", "Availability",
        "Rating", "Source_URL"
    ]

    if df[required_columns].isna().any().any():
        logger.error("Missing required values detected.")
        return

    df.to_csv(
        CSV_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info("Scraping completed successfully.")
    logger.info("Pages processed: %s", pages_processed)
    logger.info("Records saved: %s", len(df))
    logger.info("Distinct titles: %s", df["Title"].nunique())
    logger.info("CSV saved to: %s", CSV_FILE.resolve())
    logger.info("Log saved to: %s", LOG_FILE.resolve())


if __name__ == "__main__":
    main()
