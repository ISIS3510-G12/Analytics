from supabase import create_client
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_data(table_name):
    """Fetch data from Supabase and return as DataFrame"""
    response = supabase.table(table_name).select("*").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame()

def generate_top_events(df_actions, df_recommendations):
    """Generate top 5 most consulted events"""
    df_events = df_actions[df_actions["action_type"] == "consult_event"]
    df_merged = df_events.merge(df_recommendations, left_on="event_id", right_on="id", how="left")
    event_counts = df_merged["title"].value_counts().reset_index()
    event_counts.columns = ["title", "count"]
    return event_counts.head(5)

def generate_least_popular_event_types(df_actions, df_recommendations):
    """Generate bottom 5 event types by consultation"""
    df_events = df_actions[df_actions["action_type"] == "consult_event"]
    df_merged = df_events.merge(df_recommendations, left_on="event_id", right_on="id", how="left")
    event_type_counts = df_merged["type"].value_counts().reset_index()
    event_type_counts.columns = ["event_type", "count"]
    return event_type_counts.sort_values(by="count").head(5)

def run_pipeline():
    """Run analytics pipeline (only analysis)"""
    print("🔄 Running analytics pipeline...")

    # Fetch only needed tables
    df_actions = fetch_data("user_actions")
    df_recommendations = fetch_data("recommendations")

    # Run analytics
    top_events = generate_top_events(df_actions, df_recommendations)
    least_popular = generate_least_popular_event_types(df_actions, df_recommendations)

    # Save results
    os.makedirs("data", exist_ok=True)
    top_events.to_csv("data/top_events.csv", index=False)
    least_popular.to_csv("data/least_popular_event_types.csv", index=False)

    print("✅ Analytics CSVs created.")

if __name__ == "__main__":
    run_pipeline()
