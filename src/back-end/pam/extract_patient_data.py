import mysql.connector

import csv

from anomaly_detection import calculate_median, detect_anomalies, export_to_json

# Establish connection to the MySQL database.
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="superstronkrootpw",
    database="hipperdb",
    collation='utf8mb4_unicode_ci' # Full UTF-8 support for international characters.
)

# Create a cursor object to interact with the database.
cursor = connection.cursor()

# Define parameters for the data extraction.
patient_id = 1
start_date = "2025-06-01"
end_date = "2025-06-10"

# SQL query to retrieve patient activity data within the specified date range.
query = f"""
    SELECT 
        DATE(timestamp) AS date,
        steps,
        PAM_score,
        zone
    FROM Data
    JOIN Device ON Data.device_id = Device.id
    WHERE Device.patient_id_device = {patient_id}
      AND DATE(timestamp) BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY date ASC;
"""
# Execute the SQL query.
cursor.execute(query)

results = cursor.fetchall()

data = [{"date": row[0], "steps": row[1]} for row in results]
steps_list = [entry['steps'] for entry in data]

median = calculate_median(steps_list)

anomalies = detect_anomalies(data, median, threshold_percent=20)

export_to_json(median, anomalies, threshold_percent=20)

# Write the extracted data to a CSV file for further analysis.
with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Steps', 'PAM Score', 'Zone'])
    for row in results:
        writer.writerow(row)

# Attempt to print rows after fetchall(), but fetchall() already consumed the results.
# This loop will not print anything and can be removed for clarity.
for row in cursor.fetchall():
    print(row)

# Close the cursor and database connection to free resources.
cursor.close()
connection.close()