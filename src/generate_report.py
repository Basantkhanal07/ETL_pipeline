"""
STEP 4: REPORTING

This file reads the clean data back OUT of PostgreSQL (to prove
the database actually works), then create:
1. A simple text summary report
2. A couple of basic charts (saved as PNG images)

This step shows the pipeline data is actually usable for analysis --
not just sitting in a database doing nothing.
"""

import pandas as pd
import matplotlib.pyplot as plt
from db_config import get_engine


# Reads the whole table back from PostgreSQL into a DataFrame.

def read_from_postgres(table_name="sales"):
    engine = get_engine()
    df = pd.read_sql_table(table_name, engine)
    print(f"Read {len(df)} rows back from PostgreSQL table '{table_name}'")
    return df


# Writes a plain-text summary of the dataset. Simple, readable, no fancy libraries.

def write_summary_report(df, output_path="reports/summary_report.txt"):
    lines = []
    lines.append("LA RETAIL SALES - SUMMARY REPORT (September 2024)")
    lines.append("=" * 50)
    lines.append(f"Total transactions: {len(df)}")
    lines.append(f"Total revenue: ${df['dollar_sales'].sum():,.2f}")
    lines.append(f"Total units sold: {int(df['unit_sales'].sum())}")
    lines.append(f"Average sale amount: ${df['dollar_sales'].mean():.2f}")
    lines.append("")
    lines.append("Revenue by product category:")
    lines.append(df.groupby("product_category")["dollar_sales"].sum().round(2).sort_values(ascending=False).to_string())
    lines.append("")
    lines.append("Revenue by store:")
    lines.append(df.groupby("store_name")["dollar_sales"].sum().round(2).sort_values(ascending=False).to_string())
    lines.append("")
    lines.append("Transactions with a promotion active:")
    lines.append(df["promotion_flag"].value_counts().to_string())
    lines.append("")
    lines.append("Sale size breakdown:")
    lines.append(df["sale_size"].value_counts().to_string())

    report_text = "\n".join(lines)

    with open(output_path, "w") as f:
        f.write(report_text)

    print(f"Saved text report to {output_path}")
    print("\n" + report_text)

#Creates two simple charts and saves them as PNG files in reports.

def make_charts(df):

    # Chart 1: Bar chart - total revenue per product category
    revenue_by_category = df.groupby("product_category")["dollar_sales"].sum().sort_values(ascending=False)
    plt.figure(figsize=(6, 4))
    revenue_by_category.plot(kind="bar", color="seagreen")
    plt.title("Total Revenue by Product Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue ($)")
    plt.tight_layout()
    plt.savefig("reports/revenue_by_category.png")
    plt.close()
    print("Saved chart: reports/revenue_by_category.png")

    # Chart 2: Line chart - daily revenue trend across September
    daily_revenue = df.groupby(df["date"].dt.date)["dollar_sales"].sum()
    plt.figure(figsize=(7, 4))
    daily_revenue.plot(kind="line", marker="o", color="darkorange")
    plt.title("Daily Revenue - September 2024")
    plt.xlabel("Date")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("reports/daily_revenue_trend.png")
    plt.close()
    print("Saved chart: reports/daily_revenue_trend.png")


def generate_report_all():
    df = read_from_postgres()
    write_summary_report(df)
    make_charts(df)


# This lets us test this file by itself: "python src/generate_report.py"
if __name__ == "__main__":
    generate_report_all()
