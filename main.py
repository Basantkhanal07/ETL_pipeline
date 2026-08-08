
import sys
import os

# Make sure Python can find the files inside the "src" folder
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from extract import extract_all
from transform import transform_all
from load import load_all
from generate_report import generate_report_all


def run_pipeline():
    print("\n STEP 1: EXTRACT ")
    raw_data = extract_all()

    print("\n STEP 2: TRANSFORM ")
    clean_data = transform_all(raw_data)

    print("\n STEP 3: LOAD ")
    load_all(clean_data)

    print("\n STEP 4: REPORT ")
    generate_report_all()

    print("\nPipeline finished successfully!")


if __name__ == "__main__":
    run_pipeline()
