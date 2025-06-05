import asyncio
import json
import os
from datetime import datetime, timedelta
from bleak import BleakScanner
from bleak.exc import BleakError
from services import ActivityDownload, DayDataDownload, get_detailed_request

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

def update_log(mac_address, activity=False, day_data=False):
    """Update the log data timestamps for the given MAC address."""
    if mac_address not in log_data:
        log_data[mac_address] = {}
    if activity:
        log_data[mac_address]["last_activity_pull"] = datetime.now().isoformat()
    if day_data:
        log_data[mac_address]["last_day_data_pull"] = datetime.now().date().isoformat()
    save_log_data()

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

                # Pull day data dynamically
                days_to_pull = get_days_since_last_day_pull(mac_address)
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

                # Pull activity data dynamically based on hours since last pull
                hours_since = get_hours_since_last_activity(mac_address)
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
