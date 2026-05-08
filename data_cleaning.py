"""Clean a messy sales dataset and save a recruiter-ready processed CSV."""

import csv
from pathlib import Path
from statistics import median
from typing import Any, Dict, List, Optional


# This function loads the raw CSV into a list of dictionaries so the cleaning
# pipeline can work with each row in a simple, explicit Python structure.
def load_data(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


# This function standardizes headers by trimming extra spaces, converting text
# to lowercase, and replacing spaces with underscores for easier access in code.
def clean_column_names(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    cleaned_rows: List[Dict[str, str]] = []

    for row in rows:
        cleaned_row = {}
        for column_name, value in row.items():
            normalized_name = column_name.strip().lower().replace(" ", "_")
            cleaned_row[normalized_name] = value
        cleaned_rows.append(cleaned_row)

    return cleaned_rows


# This function trims whitespace in text fields and fills missing numeric values
# after converting invalid entries to None so the dataset is usable downstream.
def handle_missing_values(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    cleaned_rows: List[Dict[str, Any]] = []

    for row in rows:
        cleaned_row = dict(row)
        cleaned_row["product_name"] = str(cleaned_row["product_name"]).strip()
        cleaned_row["category"] = str(cleaned_row["category"]).strip()
        cleaned_row["price"] = parse_float(cleaned_row["price"])
        cleaned_row["quantity"] = parse_int(cleaned_row["quantity"])
        cleaned_rows.append(cleaned_row)

    valid_prices = [row["price"] for row in cleaned_rows if row["price"] is not None]
    valid_quantities = [row["quantity"] for row in cleaned_rows if row["quantity"] is not None]

    price_fill_value = float(median(valid_prices)) if valid_prices else 0.0
    quantity_fill_value = int(round(median(valid_quantities))) if valid_quantities else 0

    for row in cleaned_rows:
        if row["price"] is None:
            row["price"] = round(price_fill_value, 2)
        if row["quantity"] is None:
            row["quantity"] = quantity_fill_value

    return cleaned_rows


# This function removes rows with negative prices or quantities because those
# values are clear data entry errors in a sales dataset.
def remove_invalid_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned_rows = [
        row for row in rows if float(row["price"]) >= 0 and int(row["quantity"]) >= 0
    ]
    return cleaned_rows


def parse_float(value: Any) -> Optional[float]:
    text = str(value).strip()
    if not text:
        return None

    try:
        return round(float(text), 2)
    except ValueError:
        return None


def parse_int(value: Any) -> Optional[int]:
    text = str(value).strip()
    if not text:
        return None

    try:
        return int(float(text))
    except ValueError:
        return None


def save_clean_data(rows: List[Dict[str, Any]], file_path: Path) -> None:
    if not rows:
        return

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def preview_rows(rows: List[Dict[str, Any]], limit: int = 5) -> str:
    return "\n".join(str(row) for row in rows[:limit])


if __name__ == "__main__":
    # Build project-relative paths so the script works when run from the repo root.
    project_root = Path(__file__).resolve().parents[1]
    raw_path = project_root / "data" / "raw" / "sales_data_raw.csv"
    cleaned_path = project_root / "data" / "processed" / "sales_data_clean.csv"

    # Load the messy CSV so we can apply each cleaning step in sequence.
    df_raw = load_data(str(raw_path))

    # Standardize the headers first so later cleaning code can refer to columns reliably.
    df_clean = clean_column_names(df_raw)

    # Clean text fields and handle missing numeric values so the dataset is complete enough to use.
    df_clean = handle_missing_values(df_clean)

    # Remove negative prices and quantities because they represent invalid sales records.
    df_clean = remove_invalid_rows(df_clean)

    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    save_clean_data(df_clean, cleaned_path)

    print("Cleaning complete. First few rows:")
    print(preview_rows(df_clean))
