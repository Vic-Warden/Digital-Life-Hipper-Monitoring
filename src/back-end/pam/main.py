import asyncio
import json
import os
import aiohttp
import requests
from minute_csv_to_json import minute_csv_to_json
from day_csv_to_json import day_csv_to_json
from datetime import datetime, timedelta
from bleak import BleakScanner
from bleak.exc import BleakError
from services import ActivityDownload, DayDataDownload, get_detailed_request

BACKEND_URL = "http://145.109.185.134:5000"

LOG_FILE = "log.json"
PAM_DEVICES_FILE = "PAM_devices.json"
OUTPUT_DIR = "output"
SCAN_INTERVAL_SECONDS = 10
DEVICE_LABEL_START = 9240  # Starting number for PAM device labels
MAX_PULL_HOURS = 12  # Maximum hours to pull for activity data (max request option is LAST_12_HOURS)

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load or initialize the log data
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as log_file:
        log_data = json.load(log_file)
else:
    log_data = {}

# Load or initialize PAM devices data
if os.path.exists(PAM_DEVICES_FILE):
    with open(PAM_DEVICES_FILE, "r") as devices_file:
        pam_devices_data = json.load(devices_file)
else:
    pam_devices_data = {}

async def fetch_log(mac_address):
    # print(f"[fetch_log] Fetching log for MAC: {mac_address}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/log/{mac_address}") as resp:
                # print(f"[fetch_log] HTTP GET {BACKEND_URL}/log/{mac_address} -> Status: {resp.status}")
                if resp.status == 200:
                    data = await resp.json()
                    # print(f"[fetch_log] Log data found for {mac_address}: {data}")
                    return data
                else:
                    # print(f"[fetch_log] No log entry found for {mac_address}, returning empty dict.")
                    return {}  # If no log exists
    except Exception as e:
        print(f"[fetch_log] Error fetching log for {mac_address}: {e}")
        return {}

async def update_log(mac_address, activity=False, day_data=False):
    payload = {
        "activity": activity,
        "day_data": day_data
    }
    # print(f"[update_log] Updating log for {mac_address} with payload: {payload}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BACKEND_URL}/log/{mac_address}", json=payload) as resp:
                # print(f"[update_log] HTTP POST {BACKEND_URL}/log/{mac_address} -> Status: {resp.status}")
                if resp.status != 200:
                    print(f"[update_log] Failed to update log for {mac_address}: HTTP {resp.status}")
    except Exception as e:
        print(f"[update_log] Error updating log for {mac_address}: {e}")

async def get_days_since_last_day_pull(mac_address):
    # print(f"[get_days_since_last_day_pull] Checking days since last day_data pull for {mac_address}")
    log_entry = await fetch_log(mac_address)
    last_day_str = log_entry.get("last_day_data_pull")
    if not last_day_str:
        print(f"[get_days_since_last_day_pull] No previous day_data pull found. Returning 31 days.")
        return 31
    last_day = datetime.fromisoformat(last_day_str).date()
    today = datetime.now().date()
    delta_days = (today - last_day).days

    if delta_days == 0:
        # Last pull was today, so no need to pull again
        # print(f"[get_days_since_last_day_pull] Last pull was today, returning 0 days.")
        return 0
    else:
        # Return number of days, capped between 1 and 31
        # print(f"[get_days_since_last_day_pull] Last pull was {delta_days} days ago.")
        return min(max(delta_days, 1), 31)


async def get_hours_since_last_activity(mac_address):
    # print(f"[get_hours_since_last_activity] Checking hours since last activity pull for {mac_address}")
    log_entry = await fetch_log(mac_address)
    last_activity_str = log_entry.get("last_activity_pull")
    if not last_activity_str:
        print(f"[get_hours_since_last_activity] No previous activity pull found. Returning 24 hours.")
        return 24
    last_activity = datetime.fromisoformat(last_activity_str)
    delta_hours = (datetime.now() - last_activity).total_seconds() / 3600
    # print(f"[get_hours_since_last_activity] Last activity pull was {delta_hours:.2f} hours ago.")
    return delta_hours

# Create reverse mapping from MAC address to label ID (int)
mac_to_label_id = {
    mac.upper(): int(label.replace("label_", ""))
    for label, mac in pam_devices_data.items()
}

def save_log_data():
    """Save the log data to the log file."""
    with open(LOG_FILE, "w") as log_file:
        json.dump(log_data, log_file, indent=2)

def save_pam_devices_data():
    """Save the PAM devices data to the devices file."""
    with open(PAM_DEVICES_FILE, "w") as devices_file:
        json.dump(pam_devices_data, devices_file, indent=2)

def select_request_name(hours):
    """Select the closest valid request name for activity data based on hours."""
    if hours <= 1:
        return "LAST_1_HOUR"
    elif hours <= 3:
        return "LAST_3_HOURS"
    elif hours <= 6:
        return "LAST_6_HOURS"
    elif hours <= 12:
        return "LAST_12_HOURS"
    elif hours <= 15:
        return "LAST_15_HOURS"
    elif hours <= 24:
        return "LAST_1_DAY"
    else:
        return "LAST_1_DAY"  # fallback to max daily

def send_minute_data_to_backend(api_url, auth_token, mac_address, pam_data):
    """
    Sends minute PAM data to the Flask backend.
    """
    payload = {
        "auth_token": auth_token,
        "mac_address": mac_address,
        "pam_data": json.dumps(pam_data)  # Needs to be a JSON string
    }

    try:
        response = requests.post(api_url, data=payload)
        print(f"Status Code: {response.status_code}")
        print("Response:", response.json())
        return response.status_code == 200
    except Exception as e:
        print("Error sending data to backend:", e)
        return False

def send_day_data_to_backend(api_url, auth_token, mac_address, pam_data):
    """
    Sends PAM day data to the Flask backend.
    """
    payload = {
        "auth_token": auth_token,
        "mac_address": mac_address,
        "pam_data": json.dumps(pam_data)
    }

    try:
        response = requests.post(api_url, data=payload)
        print(f"📤 Status Code: {response.status_code}")
        print("🧾 Response:", response.json())
        return response.status_code == 200
    except Exception as e:
        print("❌ Error sending day-level data to backend:", e)
        return False
    
def get_device_label_from_backend(api_url, auth_token, mac_address):
    """
    Sends a POST request to backend to get the label of a device by MAC address.
    Returns the device label if successful, or None otherwise.
    """
    payload = {
        "auth_token": auth_token,
        "mac_address": mac_address
    }

    try:
        response = requests.get(api_url, data=payload)
        print(f"📤 Status Code: {response.status_code}")
        resp_json = response.json()
        print("🧾 Response:", resp_json)

        if response.status_code == 200 and "device_label" in resp_json:
            return resp_json["device_label"]
        else:
            print("⚠️ Unexpected response content or status code")
            return None
    except Exception as e:
        print("❌ Error getting device label from backend:", e)
        return None


async def main_loop():
    while True:
        print("\n🔍 Scanning for devices...")
        devices = await BleakScanner.discover(timeout=5)

        for device in devices:
            if device.name and "Pam" in device.name:
                mac_address = device.address.upper()
                print(f"✅ Found PAM device: {device.name} [{mac_address}]")

                # Step 1: Check backend if device exists and get label
                backend_label = get_device_label_from_backend(
                    api_url=BACKEND_URL + "/log/device_label/" + mac_address,
                    auth_token=1234567890,
                    mac_address=mac_address)
                if backend_label is None:
                    print(f"⏩ Skipping device {mac_address} as it does not exist in backend.")
                    continue  # skip this device entirely

                # Step 2: Check if local label matches backend label
                local_label = None
                # Find local label for this MAC (reverse mapping)
                for label, mac in pam_devices_data.items():
                    if mac.upper() == mac_address:
                        local_label = label
                        break

                if local_label != backend_label:
                    # Update local file to match backend label
                    print(f"🔄 Updating local PAM_devices.json for MAC {mac_address} to label {backend_label}")
                    # Remove old label if it exists
                    if local_label:
                        pam_devices_data.pop(local_label)
                    # Add new label mapping
                    pam_devices_data[backend_label] = mac_address
                    save_pam_devices_data()

                label_id = int(backend_label.replace("label_", ""))

                pulled_data = False
                # ... Continue with your day data and activity data pulling logic as before ...

                # Pull day data dynamically
                days_to_pull = await get_days_since_last_day_pull(mac_address)
                if days_to_pull > 0:
                    print(f"📅 Pulling day data for {mac_address} (label {label_id}) for last {days_to_pull} days...")
                    for attempt in range(3):
                        try:
                            day_data_downloader = DayDataDownload(
                                filename=os.path.join(OUTPUT_DIR, f"day_data_{mac_address.replace(':', '')}"),
                                days=days_to_pull,
                                label_id=label_id,
                            )
                            await day_data_downloader.run()
                            await update_log(mac_address, day_data=True)

                            filepath = os.path.join(OUTPUT_DIR, f"day_data_{mac_address.replace(':', '')}.csv")
                            pam_data = day_csv_to_json(filepath, label_id)
                            if pam_data:
                                success = send_day_data_to_backend(
                                    api_url=BACKEND_URL + "/api/upload-day-data",
                                    auth_token="1234567890",
                                    mac_address=mac_address,
                                    pam_data=pam_data
                                )
                                if success:
                                    print("✅ Day Data successfully uploaded to backend.")
                                else:
                                    print("❌ Failed to upload Day data.")
                            else:
                                print("⚠️ No Day data to send.")

                            pulled_data = True
                            break
                        except (asyncio.TimeoutError, BleakError, Exception) as error:
                            print(f"⚠️ Error pulling day data for {mac_address} on attempt {attempt + 1}: {error}")
                            if attempt < 2:
                                print("⏳ Retrying...")
                                await asyncio.sleep(2)
                            else:
                                print("❌ Giving up on day data for this cycle.")

                # Pull activity data dynamically based on hours since last pull
                hours_since = await get_hours_since_last_activity(mac_address)
                if hours_since >= 1:
                    capped_hours = min(int(hours_since), MAX_PULL_HOURS)
                    request_name = select_request_name(capped_hours)
                    print(f"📥 Pulling activity data for {mac_address} (label {label_id}) for {request_name}...")
                    for attempt in range(3):
                        try:
                            activity_downloader = ActivityDownload(
                                filename=os.path.join(OUTPUT_DIR, f"activity_{mac_address.replace(':', '')}.csv"),
                                filelength=get_detailed_request(request_name),
                                label_id=label_id,
                            )
                            await activity_downloader.run()
                            await update_log(mac_address, activity=True)

                            filepath = os.path.join(OUTPUT_DIR, f"activity_{mac_address.replace(':', '')}.csv")
                            pam_data = minute_csv_to_json(filepath, label_id)
                            if pam_data:
                                success = send_minute_data_to_backend(
                                    api_url=BACKEND_URL + "/api/upload-minute-data",
                                    auth_token="1234567890",
                                    mac_address=mac_address,
                                    pam_data=pam_data
                                )
                                if success:
                                    print("✅ Minute Data successfully uploaded to backend.")
                                else:
                                    print("❌ Failed to upload Minute data.")
                            else:
                                print("⚠️ No Minute data to send.")

                            pulled_data = True
                            break
                        except (asyncio.TimeoutError, BleakError, Exception) as error:
                            print(f"⚠️ Error pulling activity data for {mac_address} on attempt {attempt + 1}: {error}")
                            if attempt < 2:
                                print("⏳ Retrying...")
                                await asyncio.sleep(2)
                            else:
                                print("❌ Giving up on activity data for this cycle.")

                if not pulled_data:
                    print(f"⏱️ Skipping {mac_address} — data was pulled recently.")

        await asyncio.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main_loop())
