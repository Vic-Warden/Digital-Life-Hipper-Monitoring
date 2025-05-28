import asyncio
import json
import os
import time
from datetime import datetime, timedelta
from bleak import BleakScanner
# import services.py  # your BLE handler class

LOG_FILE = "log.json"
TIME_LIMIT = timedelta(hours=1)
SCAN_INTERVAL = 10  # seconds

# Load or initialize the log file
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        log = json.load(f)
else:
    log = {}

def update_log(mac_address):
    log[mac_address] = time.time()
    with open(LOG_FILE, "w") as f:
        json.dump(log, f)

def should_pull(mac_address):
    last_seen = log.get(mac_address)
    if not last_seen:
        return True
    last_dt = datetime.fromtimestamp(last_seen)
    return datetime.now() - last_dt > TIME_LIMIT

async def main_loop():
    while True:
        print("\n🔍 Scanning for devices...")
        devices = await BleakScanner.discover(timeout=5)

        for device in devices:
            if device.name and "Pam" in device.name:
                mac = device.address
                print(f"✅ Found PAM device: {device.name} [{mac}]")

                if should_pull(mac):
                    print(f"📥 Pulling data from {mac}...")
                    # handler = PamHandler(mac)
                    # await handler.run()
                    update_log(mac)
                else:
                    print(f"⏱️ Skipping {mac} — already pulled in last hour.")

        await asyncio.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main_loop())
