# Product Analytics Pipeline

## Overview
An end-to-end cloud data pipeline that simulates, ingests, transforms, and visualizes product usage data using GCP, dbt, and Prefect.

## Architecture
Event Generator → GCP Cloud Storage → BigQuery → dbt → Looker Studio

## Tech Stack
- **Ingestion:** Python, GCP Cloud Storage
- **Warehouse:** Google BigQuery
- **Transformation:** dbt (6 models, 14 data quality tests)
- **Orchestration:** Prefect
- **Visualization:** Looker Studio

## Data Models
- `stg_events` — cleaned event data
- `stg_users` — cleaned user data
- `mart_dau_mau` — Daily/Monthly Active Users
- `mart_retention` — Cohort retention analysis
- `mart_funnel` — Funnel conversion rates
- `mart_platform_breakdown` — Usage by platform

## Dashboard
[View Live Dashboard](<https://datastudio.google.com/reporting/84dce0fb-cb7f-49f0-a948-333c1de7df2c>)

## How to Run
1. Clone the repo
2. Add `gcp_credentials.json` to root folder
3. Install dependencies: `pip install -r requirements.txt`
4. Run pipeline: `python pipeline.py`