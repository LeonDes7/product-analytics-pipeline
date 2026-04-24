import os
from google.cloud import storage

# --- Config ---
CREDENTIALS_PATH = "gcp_credentials.json"
BUCKET_NAME = "product-analytics-raw-data"
LOCAL_DATA_PATH = "data/raw/"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

def create_bucket(client, bucket_name):
    try:
        bucket = client.get_bucket(bucket_name)
        print(f"Bucket {bucket_name} already exists")
        return bucket
    except Exception:
        bucket = client.create_bucket(bucket_name, location="US")
        print(f"Bucket {bucket_name} created")
        return bucket

def upload_files(client, bucket_name, local_path):
    bucket = client.bucket(bucket_name)
    for filename in os.listdir(local_path):
        if filename.endswith(".csv"):
            local_file = os.path.join(local_path, filename)
            blob = bucket.blob(f"raw/{filename}")
            blob.upload_from_filename(local_file)
            print(f"Uploaded {filename} to gs://{bucket_name}/raw/{filename}")

def main():
    print("Connecting to GCP...")
    client = storage.Client()

    print("Creating bucket...")
    create_bucket(client, BUCKET_NAME)

    print("Uploading files...")
    upload_files(client, BUCKET_NAME, LOCAL_DATA_PATH)

    print("Done!")

if __name__ == "__main__":
    main()