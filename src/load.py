"""
STEP 3 OF ETL: LOAD

This file takes the clean data and saves it into our PostgreSQL
database, so it can be queried with SQL or used by reporting tools.

We also save a local copy as a CSV in data/processed/, which is handy
for quickly checking the output without opening the database.
"""

import pandas as pd
from db_config import get_engine

# Saves the DataFrame into a PostgreSQL table
def load_to_postgres(df, table_name="sales"):
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into PostgreSQL table '{table_name}'")

# Also saves a local copy of the clean data.

def save_processed_csv(df, file_name="clean_sales.csv"):
    output_path = f"data/processed/{file_name}"
    df.to_csv(output_path, index=False)
    print(f"Saved a local copy to {output_path}")


def load_all(df):
    save_processed_csv(df)
    load_to_postgres(df)


# This lets us test this file by itself: "python src/load.py"
if __name__ == "__main__":
    from extract import extract_all
    from transform import transform_all

    raw_data = extract_all()
    clean_data = transform_all(raw_data)
    load_all(clean_data)
