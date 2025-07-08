import pandas as pd
from datetime import datetime

def init_data():
    try:
        return pd.read_csv("mood_log.csv", parse_dates=["Date"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Mood", "Note"])

def add_mood_entry(data, mood_score, note=""):
    new_entry = pd.DataFrame([{
        "Date": datetime.today().normalize(),
        "Mood": mood_score,
        "Note": note
    }])
    data = pd.concat([data, new_entry], ignore_index=True)
    data.drop_duplicates(subset="Date", keep="last", inplace=True)
    data.to_csv("mood_log.csv", index=False)
    return data

def analyze_trends(data):
    data = data.sort_values("Date")
    data["7-day avg"] = data["Mood"].rolling(window=7).mean()
    return data

def detect_patterns(data):
    weekday_avg = data.groupby(data["Date"].dt.day_name())["Mood"].mean()
    print("\n Average mood by weekday:")
    print(weekday_avg.sort_values())
    return weekday_avg

def detect_anomalies(data, threshold=2.0):
    mean = data["Mood"].mean()
    std = data["Mood"].std()
    data["Anomaly"] = (abs(data["Mood"] - mean) > threshold * std)
    anomalies = data[data["Anomaly"] == True]
    if not anomalies.empty:
        print("\n Mood Anomalies Detected:")
        print(anomalies[["Date", "Mood", "Note"]])
    return anomalies


def recommend_care(data):
    last_week = data[data["Date"] > (data["Date"].max() - pd.Timedelta(days=7))]
    if len(last_week) < 3:
        return "Not enough recent data for care recommendation."
    avg_mood = last_week["Mood"].mean()
    if avg_mood <= 3:
        return " You're consistently feeling low. Consider talking to a therapist."
    elif avg_mood <= 5:
        return " Slight dip in mood. Practice self-care and monitor."
    else:
        return " Mood looks stable. Keep it up!"

def main():
    data = init_data()

    try:
        mood = int(input("Rate your mood today (1-10): "))
        note = input("Any notes? (Optional): ")
        if mood < 1 or mood > 10:
            raise ValueError("Mood must be between 1 and 10.")
    except ValueError as e:
        print("❌ Invalid input:", e)
        return

    data = add_mood_entry(data, mood, note)
    data = analyze_trends(data)
    detect_patterns(data)
    detect_anomalies(data)

    recommendation = recommend_care(data)
    print("\nCare Insight:", recommendation)

if __name__ == "__main__":
    main()
