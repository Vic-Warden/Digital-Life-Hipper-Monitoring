import asyncio
import json
import os
from datetime import datetime, timedelta
from bleak import BleakScanner
from bleak.exc import BleakError
from services import ActivityDownload, DayDataDownload, get_detailed_request

LOG_FILE = "log.json"
PAM_DEVICES_FILE = "pam_devices.json"
OUTPUT_DIR = "output"
SCAN_INTERVAL_SECONDS = 10
DEVICE_LABEL_START = 9240
MAX_PULL_HOURS = 30  # Max 30 hours to pull at once

os.makedirs(OUTPUT_DIR, exist_ok=True)

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        log_data = json.load(f)
else:
    log_data = {}

if os.path.exists(PAM_DEVICES_FILE):
    with open(PAM_DEVICES_FILE, "r") as f:
        pam_devices_data = json.load(f)
else:
    pam_devices_data = {}

mac_to_label_id = {
    mac.upper(): int(label.replace("label_", ""))
    for label, mac in pam_devices_data.items()
}

def save_log_data():
    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)

def save_pam_devices_data():
    with open(PAM_DEVICES_FILE, "w") as f:
        json.dump(pam_devices_data, f, indent=2)

def should_pull_day_data(mac):
    today = datetime.now().date().isoformat()
    last_day = log_data.get(mac, {}).get("last_day_data_pull")
    return last_day != today

def get_hours_since_last_activity(mac):
    last_pull = log_data.get(mac, {}).get("last_activity_pull")
    if not last_pull:
        return float('inf')
    dt = datetime.fromisoformat(last_pull)
    return (datetime.now() - dt).total_seconds() / 3600

def update_log(mac, activity=False, day_data=False):
    if mac not in log_data:
        log_data[mac] = {}
    if activity:
        log_data[mac]["last_activity_pull"] = datetime.now().isoformat()
    if day_data:
        log_data[mac]["last_day_data_pull"] = datetime.now().date().isoformat()
    save_log_data()

def generate_new_label():
    existing = [
        int(label.split('_')[1])
        for label in pam_devices_data.keys()
        if label.startswith("label_") and label.split('_')[1].isdigit()
    ]
    next_num = max(existing) + 1 if existing else DEVICE_LABEL_START
    return f"label_{next_num}"

def select_request_name(hours):
    # Valid options from your error message and docs:
    valid_periods = {
        0.25: "LAST_15_MIN",
        0.5: "LAST_30_MIN",
        1: "LAST_1_HOUR",
        3: "LAST_3_HOURS",
        6: "LAST_6_HOURS",
        12: "LAST_12_HOURS",
        15: "LAST_15_HOURS",
        24: "LAST_1_DAY",
        72: "LAST_3_DAYS",
        168: "LAST_7_DAYS",
        336: "LAST_14_DAYS",
        720: "LAST_30_DAYS",
    }
    # Find smallest valid_period >= hours, else max
    sorted_hours = sorted(valid_periods.keys())
    for h in sorted_hours:
        if hours <= h:
            return valid_periods[h]
    return "MAX"  # fallback

async def main_loop():
    while True:
        print("\n🔍 Scanning for devices...")
        devices = await BleakScanner.discover(timeout=5)
        for device in devices:
            if device.name and "Pam" in device.name:
                mac = device.address.upper()
                print(f"✅ Found PAM device: {device.name} [{mac}]")

                label_id = mac_to_label_id.get(mac)
                if label_id is None:
                    new_label = generate_new_label()
                    print(f"🆕 New PAM device detected! Assigning label {new_label} for MAC {mac}")
                    pam_devices_data[new_label] = mac
                    mac_to_label_id[mac] = int(new_label.replace("label_", ""))
                    save_pam_devices_data()
                    label_id = mac_to_label_id[mac]

                pulled = False

                if should_pull_day_data(mac):
                    print(f"📅 Pulling day data for {mac} (label {label_id})...")
                    for attempt in range(3):
                        try:
                            downloader = DayDataDownload(
                                filename=os.path.join(OUTPUT_DIR, f"day_data_{mac.replace(':', '')}"),
                                days=10,
                                label_id=label_id,
                            )
                            await downloader.run()
                            update_log(mac, day_data=True)
                            pulled = True
                            break
                        except (asyncio.TimeoutError, BleakError, Exception) as e:
                            print(f"⚠️ Error pulling day data for {mac} attempt {attempt+1}: {e}")
                            if attempt < 2:
                                print("⏳ Retrying...")
                                await asyncio.sleep(2)
                            else:
                                print("❌ Giving up on day data.")

                hours_since = get_hours_since_last_activity(mac)
                if hours_since >= 1:
                    # Cap max pull to 30 hours
                    hours_to_pull = min(int(hours_since), MAX_PULL_HOURS)
                    request_name = select_request_name(hours_to_pull)
                    print(f"📥 Pulling activity data for {mac} (label {label_id}) for {request_name}...")
                    for attempt in range(3):
                        try:
                            downloader = ActivityDownload(
                                filename=os.path.join(OUTPUT_DIR, f"activity_{mac.replace(':', '')}"),
                                filelength=get_detailed_request(request_name),
                                label_id=label_id,
                            )
                            await downloader.run()
                            update_log(mac, activity=True)
                            pulled = True
                            break
                        except (asyncio.TimeoutError, BleakError, Exception) as e:
                            print(f"⚠️ Error pulling activity data for {mac} attempt {attempt+1}: {e}")
                            if attempt < 2:
                                print("⏳ Retrying...")
                                await asyncio.sleep(2)
                            else:
                                print("❌ Giving up on activity data.")

                if not pulled:
                    print(f"⏱️ Skipping {mac} — data was pulled recently.")
        await asyncio.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main_loop())
