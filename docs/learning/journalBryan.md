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


# Sources
GeeksforGeeks. (2025, 2 april). Read JSON file using Python. GeeksforGeeks. https://www.geeksforgeeks.org/read-json-file-using-python/

Liu, L. (2024, 19 maart). How to read and write JSON files in Python. HackerNoon. https://hackernoon.com/how-to-read-and-write-json-files-in-python

Pryke, B. (2025, 19 mei). How to Use Jupyter Notebook: A Beginner’s Tutorial. Dataquest. https://www.dataquest.io/blog/jupyter-notebook-tutorial/

Robot Squirrel Productions. (2021, 21 december). How to Plot CSV Data in Python Using Pandas [Video]. YouTube. https://www.youtube.com/watch?v=y43_o2OnI68