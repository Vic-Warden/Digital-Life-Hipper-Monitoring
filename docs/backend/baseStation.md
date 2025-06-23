# Base Station

For this project, a "base station" is needed. This base station will be used to make a connection to the Hipper monitors, and then pull data from these monitors. It should then get this data online so that it can be used and visualized in the application for users and therapists. This base station will consist of a Raspberry Pi. This could be any Pi that has Wi-Fi and Bluetooth compatibility. In this case, a Raspberry Pi 4 Model B is used.

## Startup of basestation
To start the base station, you first need to ensure you have a raspberry pi flashed. For this you should use a legacy OS (NOT A LITE LEGACY OS). Make sure that when you flash the pi, the user name and name of the pi are both set to 'hippy'. Then turn on the pi and connect to it using a computer. In a terminal, ensure git is installed by doing:
```cmd
sudo apt update
sudo apt install git -y
```
Then, in the user directory, pull the gitlab repository using: 
```cmd 
git clone https://gitlab.fdmci.hva.nl/IoT/2024-2025-semester-2/group-project/duuseedeewuu36.git
```
And navigate in to the folder:
```cmd
cd duuseedeewuu36
```
After you cloned the git repository and are in the folder, you can run the setup file for the raspberry pi. You can do this by running the following commands:
```cmd
chmod +x pi_setup.sh
./pi_setup.sh
```

This will start up the service to run the code of the base station. All of the base station code is found under `src/back-end/pam` and the main file is in that folder. This file is called `main.py`. Make sure that when running this code, the `BACKEND_URL` is set to the correct link to where the back-end is running, otherwise this code will not function correctly. 

## Main Code

The main code used for this base station makes use of the already existing [BLE commands](bleCommands.md) to pull the data of a full day, and of intervals of 1 hour. 

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

## Database Integration

In the new version of the main code for the base station, data is no longer only written to local files. Instead, once the data is pulled from the Hipper monitors, The time and date is directly gotten and updated from the database. 

Once the data has been pulled (either daily or activity data), the data is processed, After that the code makes a request to the back-end to update the last time it has pulled data from the current monitor. This is done by looking at the MAC adress.
For any information about the backend and how this connection is handled, go to [backend](database.py.md) for the implementation code and to [website](website.md) for the routing.


### Data Sent

The contents of the file that used to be saved locally are now also as JSON in the body of the API request. This ensures that both the local log and the backend database stay in sync. This is done by converting the csv formatted files to json in src/back-end/pam/day_csv_to_json.py and src/back-end/pam/minute_csv_to_json.py. After converting it the data is sent to the backend to the endpoints: `/api/upload-day-data` and `/api/upload-minute-data`. The backend takes care of everything else like putting the data in the Data or MinuteData table. 

The API takes care of:

    Receiving the data,

    Validating it,

    Storing it in the appropriate tables,

    And making it available for visualization.

If the backend is unreachable or if there's an error during the upload, the base station logs the error and proceeds as usual. The upload can be retried on the next run.

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
