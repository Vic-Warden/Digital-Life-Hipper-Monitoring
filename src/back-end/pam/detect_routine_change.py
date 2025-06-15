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


