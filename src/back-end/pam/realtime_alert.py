import time
import os
import sys
from dotenv import load_dotenv

# Add the path to the app directory to import modules 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app')))

# Import custom modules for database interaction and anomaly detection logic
from database import Database
from anomaly_detection import calculate_median, detect_anomalies

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../database/.env'))

load_dotenv()

# Connection to the MySQL database
db = Database(
    host=os.getenv('MYSQL_HOST'),
    port=int(os.getenv('MYSQL_PORT')),
    user=os.getenv('MYSQL_ROOT_USER'),
    password=os.getenv('MYSQL_ROOT_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)

# Define the global threshold for detecting anomalies
THRESHOLD_PERCENT = 30  

# Define the interval for checking new activity data
SLEEP_INTERVAL = 5      

def get_last_timestamp():
    """
    Retrieve the most recent timestamp from the Data table.
    This is used to only fetch new records after the last checked time.
    """
    query = "SELECT MAX(timestamp) FROM Data;"
    result = db.do_query(query)
    return result[0][0] if result else None

def get_patient_id(device_id):
    """
    Retrieve the patient ID associated with a given device ID.
    """
    query = "SELECT patient_id_device FROM Device WHERE id = %s;"
    result = db.do_query(query, (device_id,))
    return result[0][0] if result else None

def get_recent_activity(patient_id, days=30):
    """
    Retrieve the most recent activity data (steps) for the specified patient.
    Defaults to the last 30 entries.
    """
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
    """
    Main loop that continuously monitors for new activity data.
    Detects anomalies in real-time and prints alerts to the console.
    """
    print("[INFO] Real-time monitoring started... (Ctrl+C to stop)")
    last_checked = get_last_timestamp()

    while True:
        # Query for new entries added after the last checked timestamp
        query = "SELECT id, device_id, timestamp, steps FROM Data WHERE timestamp > %s ORDER BY timestamp ASC;"
        new_entries = db.do_query(query, (last_checked,))

        if new_entries:
            for entry in new_entries:
                _, device_id, timestamp, steps = entry

                # Retrieve the associated patient ID
                patient_id = get_patient_id(device_id)
                if not patient_id:
                    continue
                
                 # Fetch recent activity history for the patient
                activity_data = get_recent_activity(patient_id)

                if len(activity_data) < 5:
                    continue 

                steps_list = [item['steps'] for item in activity_data]
                
                # Extract the steps count for median calculation
                median = calculate_median(steps_list)
                # Detect anomalies
                anomalies = detect_anomalies(activity_data, median, THRESHOLD_PERCENT)

                # Check if the latest data point is an anomaly
                last_date = timestamp.date()
                anomaly_today = next((anomaly for anomaly in anomalies if anomaly['date'] == last_date), None)

                if anomaly_today:
                    print(f"[ALERT] Patient {patient_id}: {last_date} | Baseline: {int(median)}, Steps: {steps} (Deviation: -{anomaly_today['deviation_percent']}%)")

            # Update the last checked timestamp
            last_checked = new_entries[-1][2]

        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    monitor()
