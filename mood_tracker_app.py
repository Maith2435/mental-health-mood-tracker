import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

DATA_FILE = "mood_log.csv"

def init_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["date", "mood", "note"])
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

def add_entry(mood, note):
    df = init_data()
    new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), mood, note]],
                             columns=["date", "mood", "note"])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)

def show_graph():
    df = init_data()
    if df.empty:
        st.info("No mood data available.")
        return
    df["date"] = pd.to_datetime(df["date"])
    st.line_chart(df.set_index("date")["mood"])

def detect_anomalies():
    df = init_data()
    if len(df) < 2:
        return ""
    avg = df["mood"].astype(float).mean()
    if avg < 4:
        return " You're feeling low. Consider talking to a friend or professional."
    elif avg <= 6:
        return "Mood is fluctuating. Practice self-care."
    else:
        return "Mood is stable. Keep it up!"

# Streamlit UI
st.title("Mental Health Mood Tracker")
st.write("Log your daily mood and visualize patterns.")
mood = st.slider("Rate your mood today (1 = low, 10 = high):", 1, 10, 5)
note = st.text_input("Any notes? (optional)")
if st.button("Submit"):
    add_entry(mood, note)
    st.success("Mood entry added!")
st.header("Mood Trend")
show_graph()
st.header("Mood Analysis")
insight = detect_anomalies()
if insight:
    st.info(insight)