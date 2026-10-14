
import pandas as pd
from pathlib import Path

# File paths
input_file = Path("output/books_data.csv")
output_file = Path("output/research_report.xlsx")

# Check whether the input file exists
if not input_file.exists():
    raise FileNotFoundError(
        f"Input file not found: {input_file}. "
        "Run test_scraper.py first."
    )

# Load extracted data
df = pd.read_csv(input_file)

# -----------------------------
# 1. SUMMARY REPORT
# -----------------------------

summary_data = {
    "Metric": [
        "Total Records",
        "Distinct Titles",
        "Average Price (GBP)",
        "Minimum Price (GBP)",
        "Maximum Price (GBP)",
        "Missing Cells",
        "Exact Duplicate Rows",
        "Duplicate Title Rows"
    ],
    "Value": [
        len(df),
        df["Title"].nunique(),
        round(df["Price_GBP"].mean(), 2),
        round(df["Price_GBP"].min(), 2),
        round(df["Price_GBP"].max(), 2),
        int(df.isna().sum().sum()),
        int(df.duplicated().sum()),
        int(df.duplicated(subset=["Title"], keep=False).sum())
    ]
}

summary_df = pd.DataFrame(summary_data)

# -----------------------------
# 2. DATA QUALITY REPORT
# -----------------------------

quality_df = pd.DataFrame({
    "Column": df.columns,
    "Missing_Values": [
        int(df[column].isna().sum())
        for column in df.columns
    ],
    "Data_Type": [
        str(df[column].dtype)
        for column in df.columns
    ]
})

# Add validation checks
checks_df = pd.DataFrame({
    "Check": [
        "Dataset is not empty",
        "Required fields are present",
        "Prices are numeric and non-negative",
        "Source URLs are populated",
        "No exact duplicate rows"
    ],
    "Passed": [
        not df.empty,
        all(
            column in df.columns
            for column in [
                "Title", "Price_GBP",
                "Availability", "Rating", "Source_URL"
            ]
        ),
        (
            pd.api.types.is_numeric_dtype(df["Price_GBP"])
            and df["Price_GBP"].notna().all()
            and df["Price_GBP"].ge(0).all()
        ),
        df["Source_URL"].notna().all()
        and df["Source_URL"].astype(str).str.strip().ne("").all(),
        not df.duplicated().any()
    ]
})

# -----------------------------
# 3. RATING DISTRIBUTION
# -----------------------------

rating_order = ["One", "Two", "Three", "Four", "Five"]

rating_df = (
    df["Rating"]
    .value_counts()
    .reindex(rating_order, fill_value=0)
    .rename_axis("Rating")
    .reset_index(name="Book_Count")
)

# -----------------------------
# 4. EXPORT TO EXCEL
# -----------------------------

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(
        writer, sheet_name="Books Data", index=False
    )

    summary_df.to_excel(
        writer, sheet_name="Summary", index=False
    )

    quality_df.to_excel(
        writer, sheet_name="Data Quality", index=False
    )

    checks_df.to_excel(
        writer, sheet_name="Validation Checks", index=False
    )

    rating_df.to_excel(
        writer, sheet_name="Rating Distribution", index=False
    )

print("Excel report generated successfully.")
print("Records included:", len(df))
print("Validation checks passed:",
      int(checks_df["Passed"].sum()), "of", len(checks_df))
print("Report saved to:", output_file.resolve())
