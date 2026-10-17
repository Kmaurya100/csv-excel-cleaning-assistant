## Live Website

[Open csv-excel-cleaning-assistant](https://csv-excel-cleaning-assistant-6pkgrn5ntzlwp67wqfzn8q.streamlit.app/))

# Data Cleaning Assistant
A Streamlit-based web app for cleaning and preparing CSV or Excel datasets before analysis or reporting.

## Overview

This application helps users:
- Upload CSV and Excel files
- Inspect dataset structure and quality metrics
- Rename columns
- Convert column data types
- Detect and remove duplicate rows
- Handle missing values with multiple strategies
- Identify outliers using the IQR method
- Visualize distributions and correlations
- Download the cleaned dataset as CSV or Excel

## Features

### Data Upload
- Supports `.csv`, `.xlsx`, and `.xls` files
- Loads the dataset directly into the app

### Dataset Overview
- Displays row count, column count, missing values, and duplicate count
- Shows a preview of the first 10 rows

### Column Management
- Rename columns interactively
- Convert columns to:
  - `int`
  - `float`
  - `str`
  - `datetime`

### Data Quality Diagnostics
- Lists missing value counts and percentages per column
- Highlights columns requiring cleanup

### Cleaning Tools
- Remove duplicate rows
- Drop rows with missing values
- Fill missing values with a constant
- Impute numeric columns using the mean and categorical columns using the mode
- Remove outliers using the IQR-based rule

### Visualization
- Histogram for numeric columns
- Correlation heatmap for multiple numeric columns

### Export
- Download cleaned data as:
  - CSV
  - Excel workbook

## Project Structure

- `app.py` – main Streamlit application
- `requirements.txt` – Python dependencies
- `sample_data.csv` – example dataset for testing the app

## Requirements

Python 3.9+ is recommended.

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Start the application with:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

## Example Usage

1. Upload a CSV or Excel file from the sidebar.
2. Review the dataset overview and missing-value diagnostics.
3. Rename columns or convert data types if needed.
4. Apply duplicate removal and missing-value handling.
5. Review visualizations and clean outliers if necessary.
6. Download the cleaned dataset in your preferred format.

## Dependencies

This project uses:
- `streamlit`
- `pandas`
- `openpyxl`
- `matplotlib`
- `seaborn`

## License

This project is provided as a local utility for data cleaning tasks. Add your preferred license here if you plan to distribute it publicly.
