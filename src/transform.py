"""
STEP 2 OF ETL: TRANSFORM

This file takes the raw, messy sales data and cleans it up so
it's ready to be stored in a database and used for reports.

What we do here, in order:
1. Clean up column names (make them consistent, lowercase, no spaces)
2. Remove exact duplicate rows
3. Fill missing sales numbers
4. Fix inconsistent text (e.g. "Household" vs "household")
5. Fix the bad zip code value ("900XX")
6. Convert the date column to a real date type
7. Feature engineering (create new, useful columns)
8. Validate the final data (basic sanity checks)
"""

import pandas as pd

# Renaming the inconsistent column names to lowercase_with_underscores for consistency and easier SQL queries.

def clean_column_names(df):    
    df = df.rename(columns={
        "Unit sales": "unit_sales",
        "DOLLAR SALES": "dollar_sales",
    })
    print("Renamed columns to: unit_sales, dollar_sales")
    return df

# Removing Duplicate Rows: Drops rows that are 100% identical to another row.

def remove_duplicates(df):
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Removed {before - after} duplicate rows")
    return df

# Handling Missing Values: Fills in missing values for 'unit_sales' and 'dollar_sales' with the average of their respective columns.

def fill_missing_values(df):
    
    missing_units = df["unit_sales"].isna().sum()
    missing_dollars = df["dollar_sales"].isna().sum()

    avg_units = df["unit_sales"].mean()
    avg_dollars = df["dollar_sales"].mean()

    df["unit_sales"] = df["unit_sales"].fillna(round(avg_units))
    df["dollar_sales"] = df["dollar_sales"].fillna(round(avg_dollars, 2))

    print(f"Filled {missing_units} missing 'unit_sales' with average ({round(avg_units)})")
    print(f"Filled {missing_dollars} missing 'dollar_sales' with average ({round(avg_dollars, 2)})")
    return df

# Standardizing Text: Ensures that the 'product_category' column has consistent casing by converting all values to title case.

def standardize_text(df):
    
    before_unique = df["product_category"].nunique()
    df["product_category"] = df["product_category"].str.strip().str.title()
    after_unique = df["product_category"].nunique()

    print(f"Standardized 'product_category': {before_unique} unique values -> {after_unique}")
    return df


# Fixing Zip Codes: Replaces the placeholder zip code '900XX' with 'unknown' to indicate that the real value is not available.

def fix_zip_codes(df):
    
    bad_zip_count = (df["store_zip"] == "900XX").sum()
    df["store_zip"] = df["store_zip"].replace("900XX", "unknown")

    print(f"Marked {bad_zip_count} invalid zip codes ('900XX') as 'unknown'")
    return df


# Converting Date Column: Changes the 'date' column from text to a proper date type for easier analysis and manipulation.

def convert_date_column(df):
    
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%y")
    print("Converted 'date' column to proper date type")
    return df


def add_features(df):
    
    # Price per unit -- useful for comparing value across categories
    df["price_per_unit"] = (df["dollar_sales"] / df["unit_sales"]).round(2)

    # Day of week name, e.g. "Monday"
    df["day_of_week"] = df["date"].dt.day_name()

    # Simple weekend flag
    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])

    # Sales size category based on dollar amount
    df["sale_size"] = pd.cut(
        df["dollar_sales"],
        bins=[0, 50, 150, 100000],
        labels=["small", "medium", "large"],
    )

    print("Added new columns: price_per_unit, day_of_week, is_weekend, sale_size")
    return df


# Check to ensure data are valid before we load them into the database. 
def validate_data(df):
    
    assert df["unit_sales"].isna().sum() == 0, "Still have missing unit_sales!"
    assert df["dollar_sales"].isna().sum() == 0, "Still have missing dollar_sales!"
    assert df["unit_sales"].min() >= 0, "Found negative unit_sales!"
    assert df["dollar_sales"].min() >= 0, "Found negative dollar_sales!"
    assert df.duplicated().sum() == 0, "Still have duplicate rows!"

    print("Validation passed: no missing values, no negative sales, no duplicates")
    return df


# Run all the transform steps in order
def transform_all(df):
    df = clean_column_names(df)
    df = remove_duplicates(df)
    df = fill_missing_values(df)
    df = standardize_text(df)
    df = fix_zip_codes(df)
    df = convert_date_column(df)
    df = add_features(df)
    df = validate_data(df)
    return df


# This lets us test this file by itself: "python src/transform.py"
if __name__ == "__main__":
    from extract import extract_all

    raw_data = extract_all()
    clean_data = transform_all(raw_data)
    print(clean_data.head())
