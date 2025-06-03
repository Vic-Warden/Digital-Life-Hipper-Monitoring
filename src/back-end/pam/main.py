import asyncio
import json
import os
from datetime import datetime, timedelta
from bleak import BleakScanner
from bleak.exc import BleakError
from services import ActivityDownload, DayDataDownload, get_detailed_request

LOG_FILE = "log.json"
PAM_DEVICES_FILE = "pam_devices.json"
TIME_LIMIT = timedelta(hours=1)
SCAN_INTERVAL_SECONDS = 10
DEVICE_LABEL_START = 9240  # Starting number for PAM device labels

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

def should_pull_day_data(mac_address):
    """Return True if day data should be pulled for the device MAC."""
    today_str = datetime.now().date().isoformat()
    last_pull_date = log_data.get(mac_address, {}).get("last_day_data_pull")
    return last_pull_date != today_str

def should_pull_activity_data(mac_address):
    """Return True if activity data should be pulled for the device MAC."""
    last_pull_timestamp = log_data.get(mac_address, {}).get("last_activity_pull")
    if not last_pull_timestamp:
        return True
    last_pull_dt = datetime.fromisoformat(last_pull_timestamp)
    return datetime.now() - last_pull_dt > TIME_LIMIT

def update_log(mac_address, activity=False, day_data=False):
    """Update the log data timestamps for the given MAC address."""
    if mac_address not in log_data:
        log_data[mac_address] = {}
    if activity:
        log_data[mac_address]["last_activity_pull"] = datetime.now().isoformat()
    if day_data:
        log_data[mac_address]["last_day_data_pull"] = datetime.now().date().isoformat()
    save_log_data()

def generate_new_label():
    """Generate a new label string for a PAM device."""
    existing_label_numbers = [
        int(label.split('_')[1])
        for label in pam_devices_data.keys()
        if label.startswith("label_") and label.split('_')[1].isdigit()
    ]
    next_label_number = max(existing_label_numbers) + 1 if existing_label_numbers else DEVICE_LABEL_START
    return f"label_{next_label_number}"

async def main_loop():
    """Main async loop to scan and process PAM devices."""
    while True:
        print("\n🔍 Scanning for devices...")
        devices = await BleakScanner.discover(timeout=5)

        for device in devices:
            if device.name and "Pam" in device.name:
                mac_address = device.address.upper()
                print(f"✅ Found PAM device: {device.name} [{mac_address}]")

                label_id = mac_to_label_id.get(mac_address)
                if label_id is None:
                    # New device detected: assign new label and update mappings
                    new_label = generate_new_label()
                    print(f"🆕 New PAM device detected! Assigning new label {new_label} for MAC {mac_address}")
                    pam_devices_data[new_label] = mac_address
                    mac_to_label_id[mac_address] = int(new_label.replace("label_", ""))
                    save_pam_devices_data()
                    label_id = mac_to_label_id[mac_address]

                pulled_data = False

                # Pull day data if needed
                if should_pull_day_data(mac_address):
                    print(f"📅 Pulling day data for {mac_address} (label {label_id})...")

                    for attempt in range(3):
                        try:
                            day_data_downloader = DayDataDownload(
                                filename=f"output/day_data_{mac_address.replace(':', '')}",
                                days=10,
                                label_id=label_id,
                            )
                            await day_data_downloader.run()
                            update_log(mac_address, day_data=True)
                            pulled_data = True
                            break
                        except (asyncio.TimeoutError, BleakError, Exception) as error:
                            print(f"⚠️ Error pulling day data for {mac_address} on attempt {attempt + 1}: {error}")
                            if attempt < 2:
                                print("⏳ Retrying...")
                                await asyncio.sleep(2)
                            else:
                                print("❌ Giving up on day data for this cycle.")

                # Pull activity data if needed
                if should_pull_activity_data(mac_address):
                    print(f"📥 Pulling activity data for {mac_address} (label {label_id})...")

                    for attempt in range(3):
                        try:
                            activity_downloader = ActivityDownload(
                                filename=f"output/activity_{mac_address.replace(':', '')}",
                                filelength=get_detailed_request("LAST_1_HOUR"),
                                label_id=label_id,
                            )
                            await activity_downloader.run()
                            update_log(mac_address, activity=True)
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
