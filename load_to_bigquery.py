import os
from google.cloud import bigquery

# --- Config ---
CREDENTIALS_PATH = "gcp_credentials.json"
PROJECT_ID = "amazing-thought-494110-b8"  # your project ID from the error message
DATASET_ID = "product_analytics"
BUCKET_NAME = "product-analytics-raw-data"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

def create_dataset(client):
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {DATASET_ID} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Dataset {DATASET_ID} created")

def load_table(client, table_id, gcs_uri, schema):
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    load_job = client.load_table_from_uri(
        gcs_uri,
        table_ref,
        job_config=job_config
    )
    load_job.result()
    table = client.get_table(table_ref)
    print(f"Loaded {table.num_rows} rows into {table_ref}")

def main():
    print("Connecting to BigQuery...")
    client = bigquery.Client(project=PROJECT_ID)

    print("Creating dataset...")
    create_dataset(client)

    print("Loading events table...")
    events_schema = [
        bigquery.SchemaField("event_id", "STRING"),
        bigquery.SchemaField("user_id", "STRING"),
        bigquery.SchemaField("event_type", "STRING"),
        bigquery.SchemaField("event_timestamp", "TIMESTAMP"),
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