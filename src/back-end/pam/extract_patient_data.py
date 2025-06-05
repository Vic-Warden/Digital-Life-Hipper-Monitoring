import mysql.connector

import csv

# Connection to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="superstronkrootpw",
    database="hipperdb",
    collation='utf8mb4_unicode_ci' # I have no idea why is needed but it's working now
)

cursor = connection.cursor()

# Test the extraction from the data base with some start and end date 
patient_id = 1
start_date = "2025-06-01"
end_date = "2025-06-10"

# The Data I want to extract from the database
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
# The executable
cursor.execute(query)

results = cursor.fetchall()

# This means we can keep a record of the 7 days for analysis in cvs' file
with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Steps', 'PAM Score', 'Zone'])
    for row in results:
        writer.writerow(row)

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()