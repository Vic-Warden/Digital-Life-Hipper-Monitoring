import asyncio
import json
import os
from datetime import datetime, timedelta
from bleak import BleakScanner
from bleak.exc import BleakError
from services import ActivityDownload, DayDataDownload, get_detailed_request

LOG_FILE = "log.json"
PAM_DEVICES_FILE = "PAM_devices.json"
TIME_LIMIT = timedelta(hours=1)
SCAN_INTERVAL = 10  # seconds
DEVICE_LABEL_START = 9240 # Starting point for PAM device labels

# Load or initialize the log file
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        log = json.load(f)
else:
    log = {}

# Load pam devices list    
if os.path.exists(PAM_DEVICES_FILE):
    with open(PAM_DEVICES_FILE, "r") as f:
        pam_devices = json.load(f)
else:
    pam_devices = {}

# Invert the dictionary to map MAC -> label_id (int)
mac_to_label = {v.upper(): int(k.replace("label_", "")) for k, v in pam_devices.items()}

def save_log():
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def save_pam_devices():
    with open(PAM_DEVICES_FILE, "w") as f:
        json.dump(pam_devices, f, indent=2)

def should_pull_day_data(mac):
    today = datetime.now().date().isoformat()
    last_date = log.get(mac, {}).get("last_day_data_pull")
    return last_date != today  # Pull if never pulled or date is outdated

def should_pull_activity(mac):
    last_pull_ts = log.get(mac, {}).get("last_activity_pull")
    if not last_pull_ts:
        return True
    last_pull_dt = datetime.fromisoformat(last_pull_ts)
    return datetime.now() - last_pull_dt > TIME_LIMIT

def update_log(mac, activity=False, day_data=False):
    log.setdefault(mac, {})
    if activity:
        log[mac]["last_activity_pull"] = datetime.now().isoformat()
    if day_data:
        log[mac]["last_day_data_pull"] = datetime.now().date().isoformat()
    save_log()

def generate_new_label():
    existing_labels = [
        int(label.split('_')[1])
        for label in pam_devices.keys()
        if label.startswith("label_") and label.split('_')[1].isdigit()
    ]
    next_number = max(existing_labels) + 1 if existing_labels else DEVICE_LABEL_START
    return f"label_{next_number}"

async def main_loop():
    while True:
        print("\n🔍 Scanning for devices...")
        devices = await BleakScanner.discover(timeout=5)

        for device in devices:
            if device.name and "Pam" in device.name:
                mac = device.address.upper()
                print(f"✅ Found PAM device: {device.name} [{mac}]")

                label_id = mac_to_label.get(mac)
                if not label_id:
                    # New device found, assign new label and update maps and file
                    new_label = generate_new_label()
                    print(f"🆕 New PAM device detected! Assigning new label {new_label} for MAC {mac}")
                    pam_devices[new_label] = mac
                    mac_to_label[mac] = int(new_label.replace("label_", ""))
                    save_pam_devices()
                    label_id = mac_to_label[mac]

                pulled_something = False

                # Pull day data if needed
                if should_pull_day_data(mac):
                    print(f"📅 Pulling day data for {mac} (label {label_id})...")

                    for attempt in range(3):
                        try:
                            day_data = DayDataDownload(
                                filename=f"output/dayData_{mac.replace(':', '')}",
                                days=10,
                                label_id=label_id
                            )
                            await day_data.run()
                            update_log(mac, day_data=True)
                            pulled_something = True
                            break
                        except (asyncio.TimeoutError, BleakError, Exception) as e:
                            print(f"⚠️ Error pulling day data for {mac} on attempt {attempt+1}: {e}")
                            if attempt < 2:
                                print("⏳ Retrying...")
                                await asyncio.sleep(2)
                            else:
                                print("❌ Giving up on day data for this cycle.")

                # Pull activity data if needed
                if should_pull_activity(mac):
                    print(f"📥 Pulling activity data for {mac} (label {label_id})...")

                    for attempt in range(3):
                        try:
                            activity = ActivityDownload(
                                filename=f"output/activity_{mac.replace(':', '')}",
                                filelength=get_detailed_request("LAST_1_HOUR"),
                                label_id=label_id
                            )
                            await activity.run()
                            update_log(mac, activity=True)
                            pulled_something = True
                            break
                        except (asyncio.TimeoutError, BleakError, Exception) as e:
                            print(f"⚠️ Error pulling activity data for {mac} on attempt {attempt+1}: {e}")
                            if attempt < 2:
                                print("⏳ Retrying...")
                                await asyncio.sleep(2)
                            else:
                                print("❌ Giving up on activity data for this cycle.")

                if not pulled_something:
                    print(f"⏱️ Skipping {mac} — already pulled recently.")

        await asyncio.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main_loop())