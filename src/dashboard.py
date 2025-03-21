import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import data_pipeline

# Page config
st.set_page_config(page_title="Event Analytics Dashboard", layout="wide")

# Title
st.title("📊 Analytics Dashboard")

# Run pipeline
with st.spinner("Running analytics pipeline..."):
    data_pipeline.run_pipeline()
    time.sleep(2)

# Timestamp
st.write(f"🕒 **Last update:** {pd.Timestamp.now():%Y-%m-%d %H:%M:%S}")

# Load processed CSVs
top_events = pd.read_csv("data/top_events.csv")
least_popular = pd.read_csv("data/least_popular_event_types.csv")

# Layout
col1, col2 = st.columns(2)

# 📊 Column 1 - Top Consulted Events
with col1:
    st.subheader("🎯 Top Consulted Events")
    st.metric("Total Consultations", int(top_events["count"].sum()))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(top_events["title"], top_events["count"], color="royalblue")
    ax.set_xlabel("Event")
    ax.set_ylabel("Consultations")
    ax.set_title("Top 5 Events")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    st.write("📋 **Detailed View**")
    st.dataframe(top_events)

# 📉 Column 2 - Least Popular Event Types
with col2:
    st.subheader("📉 Least Popular Event Types")
    st.metric("Total (Least Popular)", int(least_popular["count"].sum()))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(least_popular["event_type"], least_popular["count"], color="tomato")
    ax.set_xlabel("Consultations")
    ax.set_ylabel("Event Type")
    ax.set_title("Bottom 5 Event Types")
    st.pyplot(fig)

    st.write("📋 **Detailed View**")
    st.dataframe(least_popular)

# Footer
st.markdown("---")
st.write("📊 **Dashboard powered by Supabase & Streamlit**")
