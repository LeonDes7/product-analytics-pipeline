import os
from google.cloud import bigquery

# --- GCP Target Warehousing Directives ---
CREDENTIALS_PATH = "gcp_credentials.json"
PROJECT_ID = "amazing-thought-494110-b8"  
DATASET_ID = "product_analytics"
BUCKET_NAME = "product-analytics-raw-data"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

def create_dataset(client):
    """Idempotent Logical Data Schema Separation: Generates target data warehouse space if not present."""
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {DATASET_ID} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US" # Regional Storage Alignment: Enforces storage proximity match with our GCS bucket layer
        client.create_dataset(dataset)
        print(f"Dataset {DATASET_ID} created")

def load_table(client, table_id, gcs_uri, schema):
    """Executes high-performance cloud serverless bulk data loading configurations."""
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_id}"
    
    # Configuration Tuning Layer
    job_config = bigquery.LoadJobConfig(
        schema=schema,                                         # Explicit Schema Enforcement
        skip_leading_rows=1,                                   # Strips raw text header indicators
        source_format=bigquery.SourceFormat.CSV,               # Parser identification
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE # Idempotency Rule: Overwrites target partition blocks to enable reliable reruns
    )
    
    # Asynchronous Job Submission: Dispatches extraction instructions to BigQuery cloud system workers
    load_job = client.load_table_from_uri(
        gcs_uri,
        table_ref,
        job_config=job_config
    )
    load_job.result() # Synchronous Blocking Hook: Pauses python state machine tracking until BigQuery processing closes completely
    
    table = client.get_table(table_ref)
    print(f"Loaded {table.num_rows} rows into {table_ref}")

def main():
    print("Connecting to BigQuery...")
    client = bigquery.Client(project=PROJECT_ID)

    print("Creating dataset...")
    create_dataset(client)

    print("Loading events table...")
    # Explicit Schema Definitions: Declares column tracking criteria to neutralize unstructured column injection corruptions
    events_schema = [
        bigquery.SchemaField("event_id", "STRING"),
        bigquery.SchemaField("user_id", "STRING"),
        bigquery.SchemaField("event_type", "STRING"),
        bigquery.SchemaField("event_timestamp", "TIMESTAMP"), # Automatically parses textual strings to standardized native dates
        bigquery.SchemaField("platform", "STRING"),
        bigquery.SchemaField("page", "STRING"),
        bigquery.SchemaField("session_id", "STRING"),
        bigquery.SchemaField("country", "STRING"),
    ]
    load_table(
        client,
        "raw_events",
        f"gs://{BUCKET_NAME}/raw/events.csv",
        events_schema
    )

    print("Loading users table...")
    users_schema = [
        bigquery.SchemaField("user_id", "STRING"),
        bigquery.SchemaField("signup_date", "DATE"),
        bigquery.SchemaField("platform", "STRING"),
        bigquery.SchemaField("country", "STRING"),
        bigquery.SchemaField("plan", "STRING"),
        ]
    load_table(
        client,
        "raw_users",
        f"gs://{BUCKET_NAME}/raw/users.csv",
        users_schema
    )

    print("Done!")

if __name__ == "__main__":
    main()