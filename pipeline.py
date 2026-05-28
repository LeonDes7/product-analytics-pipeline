import subprocess
import os
import sys
from prefect import flow, task

CREDENTIALS_PATH = "gcp_credentials.json"
BUCKET_NAME = "product-analytics-raw-data"
PROJECT_ID = "amazing-thought-494110-b8"
DATASET_ID = "product_analytics"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

# Task Decorator: Converts a native Python function into an uncoupled, observable unit of execution logic tracked by Prefect
@task(name="Generate Events")
def generate_events():
    """Triggers the programmatic synthetic user generation phase."""
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
    """Stages the generated file metrics into our decoupled cloud object storage repository infrastructure layer."""
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
    """Triggers bulk loading mechanisms to transition external assets straight into target relational database systems."""
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
    """Compiles SQL modeling matrices and instantly enforces internal structural unit quality test assertions."""
    print("Running dbt...")
    result = subprocess.run(
        ["dbt", "run", "--project-dir", "dbt_project"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")

    print("Running dbt tests...")
    # Pipeline Observability Guardrail: Run automated regressions across active schema definitions
    result = subprocess.run(
        ["dbt", "test", "--project-dir", "dbt_project"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt tests failed: {result.stderr}")
    print("dbt complete")

# Flow Decorator: Serves as the high-level orchestration graph container managing state transitions and workflow logic dependencies
@flow(name="Product Analytics Pipeline", log_prints=True)
def product_analytics_pipeline():
    """
    Linear Sequential Execution Flow Strategy: Enforces target data lineage ordering boundaries.
    Ensures data generation finishes before cloud lake storage routing, which blocks until warehouse loading begins.
    """
    generate_events()
    upload_to_gcs()
    load_to_bigquery()
    run_dbt()

if __name__ == "__main__":
    # Programmatic Entry Execution Point
    product_analytics_pipeline()