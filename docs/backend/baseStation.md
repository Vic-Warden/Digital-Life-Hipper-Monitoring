# Base Station

For this project, a "base station" is needed. This base station will be used to make a connection to the Hipper monitors, and then pull data from these monitors. It should then get this data online so that it can be used and visualized in the application for users and therapists. This base station will consist of a Raspberry Pi. This could be any Pi that has Wi-Fi and Bluetooth compatibility. In this case, a Raspberry Pi 4 Model B is used.

## Main Code

The main code used for this base station makes use of the already existing [BLE commands](bleCommands.md) to pull the data of a full day, and of intervals of 1 hour. In an automatically generated and updated `log.json` file, there will be timestamps of when the data was last pulled from a device with a specific MAC address. This will look like this:

```json
{
  "C1:08:00:01:12:33": {
    "last_day_data_pull": "2025-06-02",
    "last_activity_pull": "2025-06-02T11:57:12.181395"
  },
  "C1:08:00:01:0E:9C": {
    "last_day_data_pull": "2025-06-02",
    "last_activity_pull": "2025-06-02T11:58:44.017814"
  }
}
```

This is generated from:

```python
# Load or initialize the log data
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as log_file:
        log_data = json.load(log_file)
else:
    log_data = {}
```

And can be updated using this function:

```python
def save_log_data():
    """Save the log data to the log file."""
    with open(LOG_FILE, "w") as log_file:
        json.dump(log_data, log_file, indent=2)
```

Used with:

```python
update_log(mac_address, activity=True)
```

Or for day data:

```python
update_log(mac_address, day_data=True)
```

The main code can be run using Python. It scans for any devices in the region at an interval of 10 seconds using low-powered Bluetooth, that correspond with a Hipper monitor. If it finds one that it does not recognize, it adds the MAC address with a generated label to `PAM_devices.json`:

```json
{
  "label_90243": "C1:08:00:01:12:33",
  "label_90248": "C1:08:00:01:36:3A",
  "label_90245": "C1:08:00:01:0E:9C",
  "label_90242": "C1:08:00:01:23:B0"
}
```

After doing this, or if the device is already known, the code checks the log file to determine whether it needs to pull any data. If it has not pulled any data in the last hour, or has not pulled the day data file for that day, it uses the services from [BLE Commands](bleCommands.md) to pull the data. This then saves the data under the `output` folder as either `activity_macAddress` or `day_data_macAddress`. If the data has already been pulled, it skips this device.

## Dynamic times
The device pulls the data form the hipper monitors by comparing the time now and the last time it was pulled. In the code used there are some set options for time, for example 30mins, 1 hour, 3 hours, 6 hours, etc. This is a limit for the base station as of right now. To compare the times and see how much data it has to pull, 2 functions are used. 
```python
def get_days_since_last_day_pull(mac_address):
    """Calculate days since last day data pull. Return min 1, max 31."""
    last_day_str = log_data.get(mac_address, {}).get("last_day_data_pull")
    if not last_day_str:
        return 31  # If never pulled, pull max days
    last_day = datetime.fromisoformat(last_day_str).date()
    delta_days = (datetime.now().date() - last_day).days
    return min(max(delta_days, 1), 31)

def get_hours_since_last_activity(mac_address):
    """Calculate hours since last activity data pull."""
    last_activity_str = log_data.get(mac_address, {}).get("last_activity_pull")
    if not last_activity_str:
        return 24  # If never pulled, pull 24 hours max
    last_activity = datetime.fromisoformat(last_activity_str)
    delta_hours = (datetime.now() - last_activity).total_seconds() / 3600
    return delta_hours
```

These calculate the time that needs to be pulled. For the amount of hours this time is compared to the list of possibility's that can be used in the functions to get the activitydata. 

In the main loop, this is then used to get the correct amount of data. 
```python
if hours_since >= 1:
  # Cap max hours to max supported request (12 hours)
  capped_hours = min(int(hours_since), MAX_PULL_HOURS)
  request_name = select_request_name(capped_hours)
  print(f"📥 Pulling activity data for {mac_address} (label {label_id}) for {request_name}...")
  for attempt in range(3):
      try:
          activity_downloader = ActivityDownload(
              filename=os.path.join(OUTPUT_DIR, f"activity_{mac_address.replace(':', '')}"),
              filelength=get_detailed_request(request_name),
              label_id=label_id,
          )
          await activity_downloader.run()
          update_log(mac_address, activity=True)
          pulled_data = True
          break
```

### Error Handling

If any errors occur while trying to pull data (most commonly the device shutting down while trying to connect), it will print that there was an error and attempt to pull the data 2 more times (3 times in total). If this does not work, it skips that device for that scan and will retry once it finds the device again in the next scan.
```python
except (asyncio.TimeoutError, BleakError, Exception) as error:
    print(f"⚠️ Error pulling day data for {mac_address} on attempt {attempt + 1}: {error}")
    if attempt < 2:
        print("⏳ Retrying...")
        await asyncio.sleep(2)
    else:
        print("❌ Giving up on day data for this cycle.")
```
