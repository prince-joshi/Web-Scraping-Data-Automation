# Web Scraping and Research Data Automation

A Python data automation project that extracts 1,000 book records from a paginated practice website, validates the dataset, and generates a multi-sheet Excel research report.

---

## About the Project

Collecting data from multiple web pages manually can be repetitive and time-consuming. This project automates the collection of structured data from the Books to Scrape practice website, cleans and validates the extracted records, and generates an Excel report for further analysis.

The workflow demonstrates **web scraping, pagination handling, data cleaning, validation, logging, CSV exports, and automated Excel reporting** using Python.

---

## Dataset

- **Source:** [Books to Scrape](https://books.toscrape.com/)
- **Records:** 1,000 book records extracted across 50 pages
- **Features:**
  - `Title` — Book title
  - `Price` — Book price converted to a numeric value
  - `Availability` — Stock availability displayed on the website
  - `Rating` — Book rating extracted from the website
  - `Source_URL` — URL of the page containing the book
- **Output:** `output/books_data.csv`
- **Report:** `output/research_report.xlsx`

**Data handling:** Exact duplicate rows are removed while records with the same title but different source URLs or prices are retained.

---

## Workflow

1. Connected to the website using Python Requests
2. Parsed HTML content using BeautifulSoup
3. Extracted book titles, prices, availability, ratings, and source URLs
4. Implemented pagination to process all 50 pages
5. Added request timeouts and retry handling for temporary HTTP errors
6. Added logging to record scraping progress and parsing issues
7. Converted book prices into numeric values for analysis
8. Removed exact duplicate rows without automatically discarding records with matching titles
9. Validated required columns, prices, source URLs, and duplicate records
10. Exported the extracted dataset to CSV using Pandas
11. Generated an Excel report with summary metrics, data-quality checks, validation results, and rating distribution

---

## Tech Stack

- **Python** — Core scripting and automation
- **Requests** — HTTP requests and website access
- **BeautifulSoup** — HTML parsing and data extraction
- **Pandas** — Data cleaning, validation, and CSV export
- **OpenPyXL** — Excel report generation
- **Microsoft Excel** — Reviewing the generated research report

---

## Key Results

- Extracted **1,000 book records** across 50 pages
- Processed **20 records per page** on the source website
- Identified **999 distinct book titles**, with one title appearing in more than one record
- Generated a structured CSV dataset containing five fields
- Created an Excel report with **five worksheets**
- Passed **5 out of 5 implemented validation checks** during the report-generation run
- Added retry handling, request timeouts, and execution logs to improve reliability

_These results describe the current run against the practice website. The validation checks assess the rules implemented in the scripts and do not guarantee the accuracy of the source website's information._

---

## Validation Checks

| **Check**               | **Purpose**                                           |
| ----------------------- | ----------------------------------------------------- |
| Non-empty dataset       | Confirms that records were extracted                  |
| Required columns        | Checks that expected fields are present               |
| Non-negative prices     | Identifies invalid negative prices                    |
| Source URL completeness | Checks that source URLs are populated                 |
| Exact duplicate rows    | Checks that fully identical records have been removed |

---

## Excel Report

The generated `research_report.xlsx` contains five worksheets:

| **Worksheet**         | **Description**                                        |
| --------------------- | ------------------------------------------------------ |
| `Books Data`          | Extracted book records                                 |
| `Summary`             | Record counts, price statistics, and duplicate metrics |
| `Data Quality`        | Missing values and column-level information            |
| `Validation Checks`   | Results of the implemented validation rules            |
| `Rating Distribution` | Distribution of book ratings                           |

---

## Files

| **File**                      | **Description**                                                |
| ----------------------------- | -------------------------------------------------------------- |
| `test_scraper.py`             | Main web-scraping script with pagination, retries, and logging |
| `generate_report.py`          | Generates the multi-sheet Excel report                         |
| `requirements.txt`            | Python dependencies required to run the project                |
| `.gitignore`                  | Excludes the virtual environment and other unnecessary files   |
| `output/books_data.csv`       | Extracted dataset                                              |
| `output/research_report.xlsx` | Generated Excel research report                                |

---

## How to Run

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Real-Estate-Data-Automation
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the scraper

```bash
python test_scraper.py
```

### 5. Generate the Excel report

```bash
python generate_report.py
```

The CSV dataset and Excel report are saved in the `output/` directory.

---

## Limitations and Future Improvements

- The current implementation uses a practice website rather than a real-estate listing source.
- Automated recovery and resumption from a failed page are not yet implemented.
- Future improvements include adapting the workflow to permitted real-estate or location-research data sources, adding geospatial distance calculations, and generating location-based research summaries.

---

## Responsible Data Collection

This project uses a practice website for learning and demonstration. For other sources, data collection should comply with the website's terms, access restrictions, and applicable privacy requirements.

---

## Author

Prince Joshi  
Aspiring Data Analyst
