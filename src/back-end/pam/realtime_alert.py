import time
import os
from database import Database
from anomaly_detection import calculate_median, detect_anomalies
from dotenv import load_dotenv

load_dotenv()

db = Database(
    host=os.getenv('MYSQL_HOST'),
    port=int(os.getenv('MYSQL_PORT')),
    user=os.getenv('MYSQL_ROOT_USER'),
    password=os.getenv('MYSQL_ROOT_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)

# Paramètres globaux
THRESHOLD_PERCENT = 30  
SLEEP_INTERVAL = 5      

def get_last_timestamp():
    query = "SELECT MAX(timestamp) FROM Data;"
    result = db.do_query(query)
    return result[0][0] if result else None

def get_patient_id(device_id):
    query = "SELECT patient_id_device FROM Device WHERE id = %s;"
    result = db.do_query(query, (device_id,))
    return result[0][0] if result else None

def get_recent_activity(patient_id, days=30):
    query = """
        SELECT DATE(timestamp) as date, steps
        FROM Data
        JOIN Device ON Data.device_id = Device.id
        WHERE Device.patient_id_device = %s
        ORDER BY timestamp DESC
        LIMIT %s;
    """
    result = db.do_query(query, (patient_id, days))
    return [{"date": row[0], "steps": row[1]} for row in result] if result else []

def monitor():
    print("[INFO] Real-time monitoring started... (Ctrl+C to stop)")
    last_checked = get_last_timestamp()

    while True:
        query = "SELECT id, device_id, timestamp, steps FROM Data WHERE timestamp > %s ORDER BY timestamp ASC;"
        new_entries = db.do_query(query, (last_checked,))

        if new_entries:
            for entry in new_entries:
                _, device_id, timestamp, steps = entry

                patient_id = get_patient_id(device_id)
                if not patient_id:
                    continue

                activity_data = get_recent_activity(patient_id)

                if len(activity_data) < 5:
                    continue 

                steps_list = [item['steps'] for item in activity_data]
                median = calculate_median(steps_list)

                anomalies = detect_anomalies(activity_data, median, THRESHOLD_PERCENT)

                last_date = timestamp.date()
                anomaly_today = next((anomaly for anomaly in anomalies if anomaly['date'] == last_date), None)

                if anomaly_today:
                    print(f"[ALERT] Patient {patient_id}: {last_date} | Baseline: {int(median)}, Steps: {steps} (Deviation: -{anomaly_today['deviation_percent']}%)")

            last_checked = new_entries[-1][2]

        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    monitor()
