# ETL Pipeline: LA Retail Sales Data

A end-to-end ETL (Extract, Transform, Load) pipeline
built with Python, Pandas, and PostgreSQL.

## What this project does

1. **Extract** — reads real retail sales data from a CSV file and an Excel file
2. **Transform** — cleans column names, fills missing sales numbers, fixes
   inconsistent category text, fixes bad zip codes, converts dates, and
   engineers new columns (price per unit, day of week, sale size)
3. **Load** — saves the clean data into a PostgreSQL database (and a local
   backup CSV)
4. **Report** — reads the data back from PostgreSQL and generates a text
   summary report plus two charts

## About the dataset

This project uses a **real LA (Los Angeles) retail sales dataset** — daily sales records
for September 2024 from 10 grocery/retail stores across Los Angeles
(store, product category, units sold, dollar sales, zip code, and whether
a promotion was running). It's genuinely messy in the ways real business
data usually is:

- A few missing sales numbers
- Inconsistent category text (`Household` vs `household`)
- A placeholder/bad zip code (`900XX`)
- Dates stored as plain text

To simulate a real job (where data usually comes in more than one
export/batch), the same real dataset was split into two files by date:

- `data/raw/sales_sept_1_15.csv` — first half of the month (CSV export)
- `data/raw/sales_sept_16_30.xlsx` — second half of the month (Excel export)

No fake/made-up data is used anywhere in this project.

## Project structure

```
etl-pipeline/
├── data/
│   ├── raw/            <- original CSV + Excel files (input)
│   └── processed/      <- cleaned data gets saved 
├── reports/            <- summary report + charts get saved here
├── src/
│   ├── db_config.py       <- database connection settings
│   ├── extract.py         <- Step 1: Extract
│   ├── transform.py       <- Step 2: Transform
│   ├── load.py            <- Step 3: Load
│   └── generate_report.py <- Step 4: Report
├── main.py                <- run this file to run the whole pipeline
├── requirements.txt
├── .env
└── .gitignore
```

---

## Setup Instructions (do these in order)

### 1. Install Python (3.13 or newer)
Check if you already have it:
```
python3 --version
```
If not installed, download it from https://www.python.org/downloads/

### 2. Install PostgreSQL
Download and install from https://www.postgresql.org/download/
(Windows/Mac/Linux installers are all on that page.) During setup, it
will ask you to create a password for the default `postgres` user —
remember whatever you type.

Check it's installed and running:
```
psql --version
```

### 3. Create the project database
Open a terminal and run:
```
psql -U postgres
```
Then, inside the `psql` prompt, type:
```sql
CREATE DATABASE etl_project;
\q
```

### 4. Download this project and open a terminal in its folder

### 5. Create a virtual environment (keeps this project's packages separate)
```
python3 -m venv venv
```
Activate it:
- Mac/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

### 6. Install the required Python packages
```
pip install -r requirements.txt
```

### 7. Set up your database credentials
Copy `.env.example` to a new file called `.env`:
```
cp .env.example .env
```
Open `.env` in a text editor and fill in the password you set in Step 3
(and any other values that don't match your setup).

### 8. Run the pipeline
```
python main.py
```

That's it! You should see progress messages for each step (Extract →
Transform → Load → Report), and afterward you'll find:
- Clean data inside your `etl_project` PostgreSQL database (table: `sales`)
- A backup CSV in `data/processed/clean_sales.csv`
- A text report in `reports/summary_report.txt`
- Two charts in `reports/` as `.png` images

### 9. (Optional) Check the data yourself with SQL
```
psql -U postgres -d etl_project -c "SELECT * FROM sales LIMIT 5;"
```

---

## Using Git & GitHub for this project

If you haven't already, set up Git:
```
git init
git add .
git commit -m "Initial commit: ETL pipeline"
```

Then create a new (empty) repository on GitHub and push:
```
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

**Important:** the `.env` file (which has your real password) is already
listed in `.gitignore`, so it will never be uploaded to GitHub. Only
`.env.example` (with no real password) gets uploaded — that's on purpose.

## Running individual steps (optional, for testing)

Each script can also be run on its own to see just that step:
```
python src/extract.py
python src/transform.py
python src/load.py
python src/generate_report.py
```

## Possible next steps (to extend this project later)
- Schedule `main.py` to run automatically every day (e.g. with `cron` or
  Windows Task Scheduler)
- Add more data validation checks in `transform.py`
- Try a bigger/different dataset from [Kaggle](https://www.kaggle.com/datasets)
- Build a small dashboard on top of the PostgreSQL data (e.g. with Streamlit)
