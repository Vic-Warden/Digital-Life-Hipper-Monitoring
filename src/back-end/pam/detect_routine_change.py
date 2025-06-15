import os
import mysql.connector
import pandas as pd
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Connection MySQL
load_dotenv(dotenv_path='../database/.env')

db_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "hipperdb"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}

try:
    connection = mysql.connector.connect(**db_config)
    print("Database Connected")
except mysql.connector.Error as err:
    print("Database Connection error:", err)
    exit(1)

cursor = connection.cursor(dictionary=True)


# Load usual_slots
try:
    with open("usual_slots.json", "r") as f:
        routine_data = json.load(f)
        usual_slots = routine_data.get("usual_slots", [])
except FileNotFoundError:
    print("File not found")
    usual_slots = []

print(f"\nPatterns detected : {usual_slots}")

if not usual_slots:
    print("Any patterns detected")
    exit(0)


# Load activity
end_date = datetime.now().date()
start_date = end_date - timedelta(days=7)

query = """
SELECT DATE(timestamp) AS date, HOUR(timestamp) AS hour, SUM(steps) AS total_steps
FROM Data
WHERE timestamp BETWEEN %s AND %s
GROUP BY date, hour
ORDER BY date, hour;
"""
cursor.execute(query, (start_date, end_date))
rows = cursor.fetchall()
df = pd.DataFrame(rows)

if df.empty:
    print("No result")
    exit(0)

# Matrice
pivot_df = df.pivot_table(
    index="date",
    columns="hour",
    values="total_steps",
    fill_value=0
)

pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)

print("\nMatrice generated :")
print(pivot_df)

# Detect if the patient is inactive during 3 days in a row
ALERT_THRESHOLD_DAYS = 3  

alerts = []

for slot_hour in usual_slots:
    if slot_hour not in pivot_df.columns:
        print(f"⚠️ Le créneau {slot_hour}h n'existe pas dans les données.")
        continue

    # Retrieve the series of activities for this time slot
    activity_series = pivot_df[slot_hour]

    # Mark each day as active or inactive
    is_active = activity_series > 0

    # Detecting sequences of inactive days
    inactive_streak = []
    current_streak = []

    for date, active in is_active.items():
        if not active:
            current_streak.append(str(date))
        else:
            if len(current_streak) >= ALERT_THRESHOLD_DAYS:
                inactive_streak.append(current_streak)
            current_streak = []

    # Checks one last time at the end of the series
    if len(current_streak) >= ALERT_THRESHOLD_DAYS:
        inactive_streak.append(current_streak)

    # Add to report if there are alerts
    for streak in inactive_streak:
        alerts.append({
            "hour_slot": slot_hour,
            "inactive_days": streak
        })

# Print result
print("\nResults of routine breaks :")
if alerts:
    print(json.dumps(alerts, indent=2))
else:
    print("Any routine breaks")


connection.close()
