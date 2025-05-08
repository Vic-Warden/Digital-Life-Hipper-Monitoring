# Imports asyncio module
import asyncio

# read CSV files 
import csv 

# interact with the operating system
import os 

# Imports the BleakScanner class from the bleak module
from bleak import BleakScanner, BleakClient

# Imports datetime and timezone for timestamp
from datetime import datetime, timezone

# UUID of the BLE characteristic
TIME_DATE_UUID = "99DB2001-AC2D-11E3-A5E2-0800200C9A66"

# Log file
LOG_FILE = "log.csv"

# Returns the current UTC timestamp
def get_current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

# Main function
async def main():

    # Scann BLE device for 5 seconds
    print("On standby...")
    devices = await BleakScanner.discover(timeout=5)

    # Variable 
    pam_device = None

    # Displays the name and MAC address of each device
    for device in devices:
        print(f"- {device.name} [{device.address}]")

        # Checks if the device name contains 'Pam'
        if device.name and "Pam" in device.name:
            pam_device = device
            break

    # If no Pam device is found, print a message and stop
    if not pam_device:
        print("Pam device not connected")
        return

    # Attempts to connect to the Pam device
    print(f"\n Connect to {pam_device.name}...")
    async with BleakClient(pam_device.address) as client:
        print("Connected")

         # Gets and displays the current UTC timestamp
        timestamp = get_current_utc_timestamp()
        print(f"Current UTC timestamp: {timestamp}")
        
        # Converts the timestamp to a 4 bytes
        data = timestamp.to_bytes(4, byteorder='little')
        print(f"Data to send (little-endian): {data}")

        await client.write_gatt_char(TIME_DATE_UUID, data)
        print("Synchronized date and time")
        
# Executes the program
if __name__ == "__main__":
    asyncio.run(main())