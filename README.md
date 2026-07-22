# Medical Device Recall Analysis

## Overview
A data pipeline and analysis of FDA medical device recall data, built to practice SQL,
Python, and data quality investigation skills relevant to MedTech data analysis.

## Why I Built This
I was interested in strengthening my SQL/Python fundamentals for a data analyst role
in the MedTech space, and wanted a project relevant to the industry — FDA's public
recall data (via the openFDA API) offered a realistic, messy dataset to work with.

## What It Does
1. **Fetches** device recall records from the openFDA API
2. **Loads** the data into a local SQLite database
3. **Analyzes** recall patterns via SQL — root causes, resolution times, volume trends
4. **Visualizes** key findings as charts

## How to Run It
```bash
pip install requests pandas matplotlib
python3 fetch_recalls.py      # pulls data, saves to CSV
python3 load_to_db.py         # loads CSV into SQLite
python3 analysis.py           # runs SQL queries, prints findings
python3 charts.py             # generates charts in /charts
```

## Key Findings
- **Root causes**: [top 2-3 causes and their counts]
- **Resolution time**: recalls take an average of X days to resolve; this varies
  meaningfully by root cause (Y days to Z days across the top 10 causes)
- **Volume over time**: recall volume is fairly steady year-to-year (~18-20/year),
  with two notable exceptions:
  - 2018 saw a spike to ~32 recalls, driven primarily by 2 firms accounting for
    18 recalls — not an industry-wide trend

## Data Quality Notes
- One record had a malformed year value ("0012") in `event_date_initiated`,
  clearly a data entry error. This record was excluded from date-based calculations.
- Other long-duration outliers (up to ~11 years) were retained, as they appear to
  reflect genuinely long recall processes rather than data errors.
- Records prior to 2003 were excluded from the volume-by-year analysis due to
  sparse historical coverage in the source data.

## Data Source
[openFDA Device Recalls API](https://open.fda.gov/apis/device/recall/)

## Built With
Python, SQLite, pandas, matplotlib
