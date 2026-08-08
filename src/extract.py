"""
STEP 1 OF ETL: EXTRACT

This file grabs raw data from wherever it lives (a CSV file and
an Excel file, in our case) and loads it into pandas DataFrames so the
rest of the pipeline can work with it.

Dataset used: LA Retail Sales -- real daily sales records from 10
grocery/retail stores in Los Angeles for September 2024 (store,
product category, units sold, dollar sales, zip code, promotion flag).

To imitate a real job -- where data often comes from more than one
export -- the same dataset has been split into two real files, like
two POS export batches from the same month:
  - data/raw/sales_sept_1_15.csv    (Sept 1-15, CSV export)
  - data/raw/sales_sept_16_30.xlsx  (Sept 16-30, Excel export)
"""

import pandas as pd

# Folder where our raw input files live
RAW_DATA_FOLDER = "data/raw"

#Reads a CSV file and returns it as a pandas DataFrame.

def extract_csv(file_name="sales_sept_1_15.csv"):
    file_path = f"{RAW_DATA_FOLDER}/{file_name}"
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} rows from {file_name}")
    return df


# Reads an Excel file and returns it as a pandas DataFrame.

def extract_excel(file_name="sales_sept_16_30.xlsx"):
    file_path = f"{RAW_DATA_FOLDER}/{file_name}"
    df = pd.read_excel(file_path)
    print(f"Extracted {len(df)} rows from {file_name}")
    return df


""" Runs both extractors and combines the two DataFrames into one,
    since they both contain the same type of data (just different dates).
"""
def extract_all():
    
    csv_data = extract_csv()
    excel_data = extract_excel()

    combined = pd.concat([csv_data, excel_data], ignore_index=True)
    print(f"Combined total: {len(combined)} rows")
    return combined


# This lets us test this file by itself: "python src/extract.py"
if __name__ == "__main__":
    data = extract_all()
    print(data.head())
