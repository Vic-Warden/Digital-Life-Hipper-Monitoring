# Learning Journal
This file contains the learning journal with the learning story's of Bryan van Riesen. 

## Learning story
As a student I want to learn how the communication with the hipper device functions and how that can be implemented, so that I can use this information to communicate with the hipper divce 

### Learned
To communicate with the Hipper device, I use Bluetooth Low Energy (BLE) protocols wich is specified in the [Pam BLE Specs file](../assets/Pam_BLE_Spec_V1_8.pdf). The device supports both standard and custom BLE services. This allows me to communicate with the device with a specific set of codes. 

The device has an activity service (UUID 0x2100) that provides data from the device's activity. To make sure this data is saved on the device, I send the 2102 command to the device. This prepares the data that can then be requested using the 2103 command. 

I implemented a part of this communication by making a BLE connection with the hipper device and then writing the 2102 command to make a request to the device. 

This implementation shows my understanding of the BLE communication with the hipper device and that I understand how to use the device. 

## Learning story
As a student I want to learn how I can pull raw data from the hipper monitor so that we can create datasets using the raw accelerometer data.

### Learned
The code used for pulling raw data does not work with the regular hipper monitor and its software that it has. The device can only make use of the standard communication with sending the steps and regular data it is supposed to send. Looking at the code that was sent by the developer that he used to pull raw data, he uses different bits to communicate with the device. Using some simple test code written in open_ble_services.py, we can see that the device has the following services:
<pre>
Service 00001801-0000-1000-8000-00805f9b34fb:
  Characteristic 00002a05-0000-1000-8000-00805f9b34fb, properties: ['indicate']
  Characteristic 00002b29-0000-1000-8000-00805f9b34fb, properties: ['read', 'write']
  Characteristic 00002b2a-0000-1000-8000-00805f9b34fb, properties: ['read']
Service 00001800-0000-1000-8000-00805f9b34fb:
  Characteristic 00002a00-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a01-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a04-0000-1000-8000-00805f9b34fb, properties: ['read']
Service 0000180a-0000-1000-8000-00805f9b34fb:
  Characteristic 00002a23-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a24-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a25-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a26-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a27-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a28-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a29-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a2a-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a50-0000-1000-8000-00805f9b34fb, properties: ['read']
Service 0000180f-0000-1000-8000-00805f9b34fb:
  Characteristic 00002a19-0000-1000-8000-00805f9b34fb, properties: ['read', 'notify']
Service 99db2000-ac2d-11e3-a5e2-0800200c9a66:
  Characteristic 99db2001-ac2d-11e3-a5e2-0800200c9a66, properties: ['read', 'write']
  Characteristic 99db2002-ac2d-11e3-a5e2-0800200c9a66, properties: ['read', 'write']
  Characteristic 99db2003-ac2d-11e3-a5e2-0800200c9a66, properties: ['read', 'write']
Service 99db2100-ac2d-11e3-a5e2-0800200c9a66:
  Characteristic 99db2101-ac2d-11e3-a5e2-0800200c9a66, properties: ['notify']
  Characteristic 99db2102-ac2d-11e3-a5e2-0800200c9a66, properties: ['write']
  Characteristic 99db2103-ac2d-11e3-a5e2-0800200c9a66, properties: ['notify']
</pre>

The services used in the code we got from the developer uses the following services:
```python
# Define your service and characteristic UUIDs here
self.TIME_DATE_UUID = "99DB1001-AC2D-11E3-A5E2-0800200C9A66"
self.SETUP_UUID = "99DB1002-AC2D-11E3-A5E2-0800200C9A66"
self.COMMAND_UUID = "99DB1003-AC2D-11E3-A5E2-0800200C9A66"
self.DRIVING_BEHAVIOR_UUID = "99DB1005-AC2D-11E3-A5E2-0800200C9A66"
self.DRIVING_BEHAVIOR_SETTINGS_UUID = "99DB1006-AC2D-11E3-A5E2-0800200C9A66"
self.DATA_DOWNLOAD_UUID = "99DB1007-AC2D-11E3-A5E2-0800200C9A66"

self.FIRMWARE_UUID = "00002A26-0000-1000-8000-00805F9B34FB"
self.BATTERY_UUID = "00002A19-0000-1000-8000-00805F9B34FB"
self.SYSTEM_ID_UUID = "00002A23-0000-1000-8000-00805F9B34FB"
self.DEVICE_NAME_UUID = "00002A00-0000-1000-8000-00805F9B34FB"

self.ACC_ENABLER_UUID = "033AFFA1-6778-4112-AC5C-15265F21ED94"
self.ACC_RANGE_UUID = "033AFFA2-6778-4112-AC5C-15265F21ED94"
self.RAW_DATA_UUID = "033AFFAD-6778-4112-AC5C-15265F21ED94"
self.MEASUREMENT_PERIOD_UUID = "033AFFAE-6778-4112-AC5C-15265F21ED94"
```
These are ofcourse a lot different then what we use and are able to use at this point in time, wich means that I can conclude that we need the other software that is used by the developer to be able to read out the raw sensor data. This sensor we will get somewhere this week so that we can continue testing and make use of the raw sensor data. 

## Learning story
As a student I want to learn how I can use jupyter to create graphs and visualise data from csv datasets so that I can easily visualise the data that we get from the Hipper devices. 

### Learned
I have learned how I can use Jupyter notebook with python to generate graphs and tables of data that can visualize these datasets. I learned the basics by making use of a tuturial made by Pryke (2025). With this I installed Jupyter and did some simple tests to get familliar with it. After that I found a video by (Robot Squirrel Productions, 2021) that explains how you can create graphs by combining the python librarie pandas with csv files, wich is the format of data that we have. With this I was able to create the following end results of graphs and tables of a comparisson of data with the different sensors. ![image](../assets/ResearchRedo/LongTermResults.png) <br />
A code snippet of the merging and generation of the first graph visible in the picture:
```python
# Merge all data on Timestamp
from functools import reduce
merged = reduce(lambda left, right: pd.merge(left, right, on="Timestamp"), dfs.values())

# Plot Steps for all sensors
plt.figure(figsize=(14, 6))
for name in sensor_files:
    plt.plot(merged["Timestamp"], merged[f"Steps_{name}"], label=f"{name} Steps")
plt.title("Steps Comparison Across Sensors")
plt.xlabel("Time")
plt.ylabel("Steps")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```
With these results I now know how to visualize csv data using jupyter notebook. 

## Learning story
As a student I want to learn how I can read and write to json files using python, so that I can create log files for monitoring hipper monitors. 

Description: When creating the basestation for pulling data from hipper monitors, I need to be able to create a log file. I need this to ensure that data is only pulled once every hour or other set time, instead of every loop. For this I need to know how I can read and write to json files using python.

### Learned
To achieve this learning story, I made use of python's built in json library. I worked on a python file located at src/back-end/pam/main.py. Within this file, Before the scanning loop starts, I check if a log file already exists. If it does, I load the data using json.load():
```python
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as log_file:
        log_data = json.load(log_file)
else:
    log_data = {}
```
I found this method from GeeksforGeeks (2025). 

After succesfully pulling data from a hipper device, I write the time and date from when I did this to a log.json file. 
```python
def update_log(mac_address, activity=False, day_data=False):
    if mac_address not in log_data:
        log_data[mac_address] = {}
    if activity:
        log_data[mac_address]["last_activity_pull"] = datetime.now().isoformat()
    if day_data:
        log_data[mac_address]["last_day_data_pull"] = datetime.now().date().isoformat()
    
    with open(LOG_FILE, "w") as log_file:
        json.dump(log_data, log_file, indent=2)
```
This helps me control how often the data is pulled from the devices. The output of this log looks like this:
```
{
  "AA:BB:CC:DD:EE:FF": {
    "last_activity_pull": "2025-06-04T13:00:00",
    "last_day_data_pull": "2025-06-04"
  }
}
```
I found this method of writing data when reading a page written by Liu (2024). Here an example is shown where they also make use of the same methods. 

What I learned:
By working with JSON files, I learned how to:

    Check for the existence of a file using os.path.exists()

    Load structured data from a file using json.load()

    Update in-memory data and write it back using json.dump()

    Manage time-based conditions using Python's datetime module

This approach gives me a clean and reusable way to control device data downloads and helps ensure the system runs efficiently without overloading the devices or network.

## Learning story
As a student, I want to learn how to fetch data dynamically based on the last successful pull time, so I can ensure my system always retrieves complete and relevant data

### Learned
Initially, my data collection system fetched a fixed amount of data (e.g., the last 1 hour) whenever a device was detected. This caused issues when a device hadn’t been seen for longer periods — any activity older than that fixed window was lost.

To fix this, I created a time-aware system:

    I logged the last pull timestamp per device.

    I calculated how long it had been since the last successful pull.

    I mapped that duration to a valid range supported by the API (e.g., LAST_3_HOURS, LAST_6_HOURS).

    I dynamically adjusted the data pull request based on that.

This ensured that if a device hadn’t been seen for, say, 6 hours, I would fetch the last 6 hours of data, not just the last 1.
```python
def get_hours_since_last_activity(mac_address):
    """Calculate hours since last activity data pull."""
    last_activity_str = log_data.get(mac_address, {}).get("last_activity_pull")
    if not last_activity_str:
        return 24  # If never pulled, pull 24 hours max
    last_activity = datetime.fromisoformat(last_activity_str)
    delta_hours = (datetime.now() - last_activity).total_seconds() / 3600
    return delta_hours
```

Now, my system adapts to real-world usage and avoids data loss. I learned how to:

    Work with datetime objects in Python.

    Maintain persistent state using JSON.

    Implement robust logic for edge cases in BLE/IoT systems.

## Learning story
As a student, I want to learn how to implement reliable retry logic in my code when working with Bluetooth Low Energy (BLE) devices, so I can ensure my system gracefully handles intermittent connectivity issues without crashing or losing important data.

### Learned
When I first built my data collection script for BLE devices, I assumed the devices would always respond quickly and reliably. But in reality, BLE connections were unstable — sometimes devices were out of range, sometimes they took too long to respond, and sometimes the device shut it self off because it had not been moved(was inactive) for too long. This gave me some errors within my code that crashed the main code. For this I needed a fix. 

To make my system more robust:

    1. I added a retry mechanism with up to 3 attempts for both day data and activity data pulls.

    2. I inserted a short delay between retries using asyncio.sleep() to give the device time to recover.

    3. I caught exceptions like TimeoutError and BleakError and handled them with simple output messages.

Example code:
```python
for attempt in range(3):
    try:
        await data_downloader.run()
        break  # success
    except (BleakError, TimeoutError):
        if attempt < 2:
            await asyncio.sleep(2)  # delay before retry
        else:
            print("Giving up on this cycle.")

```

Now, my system is much more reliable when communicating with BLE devices:

    1. It doesn’t crash on failure.

    2. It gives devices a longer chance to respond.

    3. It logs which devices had persistent issues and skips them temporarily without halting the loop, ensuring the programm never stops.

This taught me how to:

    1. Write resilient code in imperfect hardware scenarios.

    2. Use try/except with retries effectively.

    3. Improve user feedback when something goes wrong.

## Learning story
As a student, I want to learn how to store logs in a relational database instead of flat files, so I can manage and query device data more efficiently and reliably.

### Learned

Initially, I was logging the last data pull times from each BLE device in a JSON file (log.json). This worked fine for a small test setup, but it quickly became hard to manage as I scaled the number of devices and the frequency of pulls. Problems included:

    File corruption risk if the program stopped while writing.

    No easy way to search or query for last pull times across multiple devices.

    Messy data structure with duplicate timestamps per device (e.g. separate for "day" and "activity" pulls).

To improve this, I decided to store this logging data in a database — in this case, SQLite for local testing. This meant designing a proper table and replacing all file I/O code with SQL queries.

Steps I took:

    Defined a schema for the logs with fields: mac_address, label_id, last_pull_time.

    Created a helper class using Python's sqlite3 module to connect, insert, update, and fetch data.

    Refactored save_log_data() and update_log() to write to the database instead of log.json.

    Unified the timestamps so each device has a single field tracking the last successful data pull.

Example of sql table and logic: 
```sql
DROP TABLE IF EXISTS `hipperdb`.`Device` ;

CREATE TABLE IF NOT EXISTS `hipperdb`.`Device` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `patient_id_device` INT NOT NULL,
  `device_label` VARCHAR(10) NOT NULL,
  `device_id` INT NOT NULL,
  `last_data_pull` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `patient_id_idx` (`patient_id_device` ASC) VISIBLE,
  CONSTRAINT `fk_patient_id_device`
    FOREIGN KEY (`patient_id_device`)
    REFERENCES `hipperdb`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
```
```python
def update_log(mac_address, label_id):
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO device_log (mac_address, label_id, last_pull_time)
        VALUES (?, ?, ?)
        ON CONFLICT(mac_address) DO UPDATE SET
            last_pull_time=excluded.last_pull_time,
            label_id=excluded.label_id;
    """, (mac_address, label_id, now))
    conn.commit()
```

Now the system:

    Stores data more reliably and doesn't risk corruption from concurrent file writes.

    Keeps a clean, consistent log where each device has a single source of truth.

    Allows querying and sorting of devices by last pull time if needed.

This taught me how to:

    Design a minimal SQL schema to replace a JSON object.

    Use sqlite3 for local development and test it without adding extra dependencies.

    Think about data structure design to simplify later queries and reporting.

## Learning story
As a student, I want to learn how to send sensor data from a Raspberry Pi to a remote server using HTTP requests, 
so I can build IoT solutions that communicate with cloud infrastructure.

### Learned
When I first started sending data from my Raspberry Pi, I assumed that sending a POST request to the backend would "just work" every time. But I quickly ran into problems: sometimes the server wasn’t reachable, sometimes the data format was wrong, and sometimes I forgot to include required fields like "activity" or "day_data". These would either throw an error or return a 400 Bad Request.

To make my system more reliable:

    I structured the JSON payload carefully and checked that all required fields were present.

    I added status code checks to make sure the data was successfully received.

    I handled network errors using try/except so that the system would retry later instead of failing.

Example code:
```python
    payload = {"activity": True, "day_data": False}
    url = f"http://server_ip:5000/log/{mac_address}"

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Log update successful")
        else:
            print(f"Server error: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Failed to send log update: {e}")
```

Now, my data upload routine is much more reliable:

    It gives me feedback when something goes wrong.

    It doesn’t crash the program if the server is offline.

    It ensures only valid, complete data gets sent to the backend.

This taught me how to:

    Build resilient client-server communication in Python.

    Debug and test web APIs effectively.

    Handle real-world errors in networked applications.

## Learning story
As a student, I want to learn how to track and update timestamps of data collection in a database, so I can monitor the freshness and reliability of the data.

### Learned
Originally, I didn’t track when data was last pulled from each device — so if something went wrong or the server restarted, I had no way to know what was up-to-date and what wasn’t. This caused confusion, especially with multiple sensors, and made debugging harder.

To fix this:

    I added a last_activity_pull and last_day_data_pull column in the database for each device.

    I created two endpoints in the Flask API: one to update timestamps and one to retrieve them.

    I made sure the timestamps were timezone-aware (Europe/Amsterdam) and stored in a consistent format (ISO 8601).

Example code:
```python
@app.route('/log/<mac_address>', methods=['POST'])
def update_log(mac_address):
    mac = mac_address.upper()
    data = request.get_json()

    activity = data.get("activity")
    day_data = data.get("day_data")

    success = db.update_log_timestamps(mac, activity, day_data)
    return {"message": "Log updated"} if success else {"error": "Failed to update"}, 200
```

Using this, my system can:

    Track exactly when each type of data was last pulled.

    Help me detect inactive devices.

    Provide a clear generalised way to have timestaped logs.

This taught me how to:

    Design and use metadata in a database schema.

    Work with timestamps and timezones reliably.

    Combine backend logic and database updates into a full data pipeline.

Using this I can now use multiple basestations in the same area, because they all have the same generalised location where they check wat time and date data was pulled for the last time from a specific sensor. 
This implementation ensures there is no double data collected from a single sensor.

## Learning story

As a student, I want to learn how to use authentication tokens when sending data from a Raspberry Pi to my backend, so that I can make sure only trusted devices can send or access data.

### Learned
Originally, my backend accepted any data coming in from any client. This was a big problem — anyone could send fake data to my system if they knew the endpoint. I realized this was insecure, especially since my devices (like the Raspberry Pi) are meant to operate over public or semi-public networks.

To fix this:

1. I generated a unique token for each authorized device and stored it in the database.

2. The Raspberry Pi includes this token in the Authorization header when making a request to the backend.

3. On the backend, I created a middleware-style function that checks if the token is valid before processing the request.

4. If the token is missing or invalid, the request is rejected with a 401 Unauthorized.

```python
from flask import request, jsonify

# Dictionary of valid tokens for example purposes (in production, use DB)
VALID_TOKENS = {
    "raspberrypi-001": "abc123xyzTOKEN",
    "raspberrypi-002": "def456TOKENzzz"
}

def validate_token():
    token = request.headers.get("Authorization")
    if not token or token not in VALID_TOKENS.values():
        return False
    return True

@app.route('/api/data', methods=['POST'])
def receive_data():
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    # Save to database...
    return jsonify({"message": "Data received securely"}), 200
```

Example code for raspberry pi:
```python
import requests

url = "https://192.168.172.141:5000/api/data"
headers = {
    "Authorization": "abc123xyzTOKEN"
}
data = {
    "day_date": NOW(),
    "time_date": NOW()
}

response = requests.post(url, json=data, headers=headers)
print(response.json())

```
Using this, my system can:

1. Ensure that only known and authorized devices can send data.

2. Prevent malicious actors from spamming or tampering with my backend.

3. Keep logs of which token/device sent what data for easier debugging.

This taught me how to:

1. Design and use token-based authentication in embedded-backend systems.

2. Secure endpoints in a stateless and lightweight way (suitable for IoT).

3. Combine basic cybersecurity principles with real-world embedded systems.

4. Store and manage per-device secrets securely (or use Key Vaults in future).

Now, I can safely deploy multiple Raspberry Pi devices in the field without worrying about spoofed or unauthorized data submissions.

## Learning story
As a student, I want to learn how to parse CSV files with different data formats so I can accurately prepare data for backend APIs, ensuring that the data I send is complete, correct, and properly formatted.

### Learned
At first, I was simply opening CSV files and trying to send raw data to the backend, but this quickly led to errors and mismatches between what my backend expected and what I actually sent. Different CSV files had different columns and formats — for example, minute-level data had timestamps with steps and PAM scores, while day-level data included zones and aggregated activity scores.

To fix this:

1. I carefully studied the CSV file structures and identified which columns were required for each data type.

2. I wrote dedicated parsing functions for each CSV format. These functions read the CSV, convert timestamps to ISO format, cast values to the correct types (int, float), and handled any missing or malformed rows gracefully.

3. I added extra fields to the parsed data as needed, such as a data_label or patient_id, to ensure the backend received all the context it needed.

4. I tested these functions thoroughly by running them on sample CSV files and verifying the output before sending it to the backend API.

```python
import csv
from datetime import datetime

def minute_csv_to_json(filepath, label_id):
    data = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                data.append({
                    "timestamp": datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S").isoformat(),
                    "steps": int(row["Steps"]),
                    "pam_score": float(row["PAM Score"]),
                    "data_label": label_id
                })
            except Exception as e:
                print(f"Skipping row due to error: {e} — row: {row}")
    return data
```

Using this, my system can:

1. Ensure data integrity by sending correctly formatted JSON to the backend.

2. Automatically handle multiple CSV formats without manual intervention.

3. Avoid backend errors caused by bad or missing data fields.

This taught me how to:

1. Work with CSV files programmatically using Python’s csv module.

2. Perform robust error handling during data parsing to avoid crashes.

3. Convert and format timestamps properly for API compatibility.

4. Prepare and structure data correctly for downstream database insertion.

Now, I can reliably convert diverse CSV data into backend-ready JSON payloads, forming a solid foundation for my data that I send to the back-end.

## Learning story
As a student, I want to learn how to handle and validate JSON data in Python so I can ensure data integrity before inserting data into a database or sending it to backend APIs.

### Learned
At first, I was simply accepting JSON data and sending it directly to the backend without any validation, which caused errors or corrupted data when the JSON was malformed or missing required fields. I need a way I can ensure the JSON data is valid to prevent this. 

<br /> <br />

# Sources
GeeksforGeeks. (2025, 2 april). Read JSON file using Python. GeeksforGeeks. https://www.geeksforgeeks.org/read-json-file-using-python/

Liu, L. (2024, 19 maart). How to read and write JSON files in Python. HackerNoon. https://hackernoon.com/how-to-read-and-write-json-files-in-python

Pryke, B. (2025, 19 mei). How to Use Jupyter Notebook: A Beginner’s Tutorial. Dataquest. https://www.dataquest.io/blog/jupyter-notebook-tutorial/

Robot Squirrel Productions. (2021, 21 december). How to Plot CSV Data in Python Using Pandas [Video]. YouTube. https://www.youtube.com/watch?v=y43_o2OnI68