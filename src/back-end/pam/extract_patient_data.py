import mysql.connector

# Connection to the database
connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="superstronkrootpw",
    database="hipperdb"
)

cursor = connection.cursor()

# Test
patient_id = 1
start_date = "2025-05-19"
end_date = "2025-05-25"

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