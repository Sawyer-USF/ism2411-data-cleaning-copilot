# ism2411-data-cleaning-copilot

This mini-project cleans a messy sales dataset with Python. The script standardizes column names, trims whitespace from text fields, fills missing numeric values, removes invalid negative values, and exports a cleaned CSV that is easier to analyze.

## Project Structure

```text
ism2411-data-cleaning-copilot/
├── data/
│   ├── raw/
│   │   └── sales_data_raw.csv
│   └── processed/
│       └── sales_data_clean.csv
├── src/
│   └── data_cleaning.py
├── README.md
└── reflection.md
```

## How to Run

1. Open a terminal in the project root.
2. Run `python src/data_cleaning.py`
3. Check `data/processed/sales_data_clean.csv` for the cleaned output.

## Notes

The assignment prompt references a course-provided raw CSV. That file was not available in this workspace, so the repo currently includes a stand-in messy sales dataset with the same expected structure so the pipeline runs end to end. If you have the official course file, replace `data/raw/sales_data_raw.csv` and rerun the script.
