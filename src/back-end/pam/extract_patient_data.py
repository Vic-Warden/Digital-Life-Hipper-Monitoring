import mysql.connector

# Connexion to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="superstronkrootpw",
    database="hipperdb"
)

cursor = connection.cursor()

# Test
patient_id = 1
start_date = "2025-06-01"
end_date = "2025-06-30"

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

cursor.execute(query)

for row in cursor.fetchall():
    print(row)


cursor.close()
connection.close()
