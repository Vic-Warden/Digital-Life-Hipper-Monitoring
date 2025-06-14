import os
import mysql.connector
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Load variables from the .env file
load_dotenv(dotenv_path='../database/.env')

# Retrieve MySQL connection parameters
db_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "hipperdb"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}

# Connection to the database
try:
    connection = mysql.connector.connect(**db_config)
    print("Success")
except mysql.connector.Error as err:
    print("error", err)
    exit(1)
    
cursor = connection.cursor(dictionary=True)

# Define the analysis period
end_date = datetime.now().date()
start_date = end_date - timedelta(days=7)

# Run the query
query = """
SELECT HOUR(timestamp) AS hour_slot, SUM(steps) as total_steps
FROM Data
WHERE timestamp BETWEEN %s AND %s
GROUP BY hour_slot
ORDER BY hour_slot;
"""
cursor.execute(query, (start_date, end_date))
rows = cursor.fetchall()

# Convert to DataFrame
df = pd.DataFrame(rows)

# Show times with more activity
print("\nAverage steps per hour (over 7 days) :")
print(df)

def detect_usual_slots(df, threshold=200):
    """
    Identifies hours with average activity above the given threshold
    Returns a structured JSON
    """
    usual_slots = df[df['total_steps'] > threshold]['hour_slot'].tolist()

    result = {
        "usual_slots": usual_slots,
        "threshold": threshold,
        "total_hours_analyzed": df.shape[0],
        "slots_details": df.to_dict(orient='records')
    }

    return result

connection.close()