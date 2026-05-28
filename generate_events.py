import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

fake = Faker()
# Reproducibility Anchors: Explicitly seed random number generators to ensure identical data distributions across multiple local trial runs
random.seed(42)
np.random.seed(42)

# --- Operational Testing Scale Configuration ---
NUM_USERS = 10000
NUM_DAYS = 90
START_DATE = datetime(2025, 1, 1)
OUTPUT_PATH = "data/raw/events.csv"

# --- Categorical Enums with Realistic Weights to Simulate Organic Product Telemetry ---
EVENT_TYPES = ["signup", "login", "view_page", "click_feature", "upgrade_plan", "churn"]
EVENT_WEIGHTS = [0.05, 0.35, 0.30, 0.20, 0.05, 0.05]

PLATFORMS = ["mobile", "web", "tablet"]
PLATFORM_WEIGHTS = [0.50, 0.40, 0.10]

PAGES = ["home", "dashboard", "settings", "pricing", "profile", "explore"]

def generate_users(n):
    """Generates synthetic dimension table records representing customer signup metrics."""
    users = []
    for i in range(n):
        signup_date = START_DATE + timedelta(days=random.randint(0, NUM_DAYS - 1))
        users.append({
            "user_id": f"user_{i+1:05d}",
            "signup_date": signup_date,
            "platform": random.choices(PLATFORMS, weights=PLATFORM_WEIGHTS)[0],
            "country": fake.country_code(),
            "plan": random.choices(["free", "pro", "enterprise"], weights=[0.70, 0.25, 0.05])[0]
        })
    return pd.DataFrame(users)

def generate_events(users_df):
    """Generates synthetic fact table records representing asynchronous user transaction event logging."""
    events = []
    for _, user in users_df.iterrows():
        # Generates varying transactional event volumes per user ID to mirror active vs passive usage
        num_events = random.randint(5, 50)
        user_start = user["signup_date"]

        for _ in range(num_events):
            # Enforces relational consistency: Events cannot happen chronologically prior to user registration date
            event_date = user_start + timedelta(
                days=random.randint(0, NUM_DAYS),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            events.append({
                "event_id": fake.uuid4(), # High-entropy synthetic primary business key
                "user_id": user["user_id"], # Foreign key mapping back to users matrix
                "event_type": random.choices(EVENT_TYPES, weights=EVENT_WEIGHTS)[0],
                "event_timestamp": event_date,
                "platform": user["platform"],
                "page": random.choice(PAGES),
                "session_id": fake.uuid4(), # Grouping dimension tracking discrete browser contexts
                "country": user["country"]
            })

    return pd.DataFrame(events)

def main():
    os.makedirs("data/raw", exist_ok=True)

    print("Generating users...")
    users_df = generate_users(NUM_USERS)
    users_df.to_csv("data/raw/users.csv", index=False)
    print(f"Generated {len(users_df)} users")

    print("Generating events...")
    events_df = generate_events(users_df)
    # Sort logs chronologically to mirror real sequential application logging systems
    events_df = events_df.sort_values("event_timestamp").reset_index(drop=True)
    events_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(events_df)} events")
    print(f"Files saved to data/raw/")

if __name__ == "__main__":
    main()