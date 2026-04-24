import subprocess
import os
import sys
from prefect import flow, task

CREDENTIALS_PATH = "gcp_credentials.json"
BUCKET_NAME = "product-analytics-raw-data"
PROJECT_ID = "amazing-thought-494110-b8"
DATASET_ID = "product_analytics"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

@task(name="Generate Events")
def generate_events():
    print("Generating events...")
    result = subprocess.run(
        [sys.executable, "generate_events.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Event generation failed: {result.stderr}")
    print("Events generated successfully")

@task(name="Upload to GCS")
def upload_to_gcs():
    print("Uploading to GCS...")
    result = subprocess.run(
        [sys.executable, "upload_to_gcs.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"GCS upload failed: {result.stderr}")
    print("Upload complete")

@task(name="Load to BigQuery")
def load_to_bigquery():
    print("Loading to BigQuery...")
    result = subprocess.run(
        [sys.executable, "load_to_bigquery.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"BigQuery load failed: {result.stderr}")
    print("BigQuery load complete")

@task(name="Run dbt")
def run_dbt():
    print("Running dbt...")
    result = subprocess.run(
        ["dbt", "run", "--project-dir", "dbt_project"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")

    print("Running dbt tests...")
    result = subprocess.run(
        ["dbt", "test", "--project-dir", "dbt_project"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt tests failed: {result.stderr}")
    print("dbt complete")

@flow(name="Product Analytics Pipeline", log_prints=True)
def product_analytics_pipeline():
    generate_events()
    upload_to_gcs()
    load_to_bigquery()
    run_dbt()

if __name__ == "__main__":
    product_analytics_pipeline()