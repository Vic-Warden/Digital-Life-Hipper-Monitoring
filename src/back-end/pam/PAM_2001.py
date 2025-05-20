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

from services import get_address_by_label

class PAM_2001:
    def __init__(self, uuid, label_id=None):
        self.uuid = uuid
        self.label_id = label_id
        self.pam_device = None
        self.directly_targetting_ID = False
        
        if label_id is not None:
            mac = get_address_by_label(label_id)
            if mac and "not found" not in mac:
                self.pam_device = type("device", (), {"address": mac, "name": f"Pam_{label_id}"})()
                self.directly_targetting_ID = True
                print(f"Targeting PAM device with MAC: {mac}")
            else:
                print(f"MAC address not found for label {label_id}")
    
    async def run(self):
        await self.set_timestamp()

    # Returns the current UTC timestamp
    async def get_current_utc_timestamp(self):
        return int(datetime.now(timezone.utc).timestamp())

    # Main function
    async def set_timestamp(self):

                # Scan BLE device if no target address was provided
        if not self.directly_targetting_ID:
            print("On standby...")

            attempts = 0
            while attempts < 5:
                devices = await BleakScanner.discover(timeout=5)

                for device in devices:
                    print(f"- {device.name} [{device.address}]")
                    if device.name and "Pam" in device.name:
                        self.pam_device = device
                        break

                if self.pam_device:
                    break
                attempts += 1

            if not self.pam_device:
                print("Pam device not connected")
                return

        print(f"Pam device found: {self.pam_device.name} [{self.pam_device.address}]")


        # Attempts to connect to the Pam device
        print(f"\n Connect to {self.pam_device.name}...")
        async with BleakClient(self.pam_device.address) as client:
            print("Connected")

            timestamp = int(datetime.now(timezone.utc).timestamp())
            print(f"Raw UTC timestamp (seconds): {timestamp}")
            data = timestamp.to_bytes(4, byteorder='little')
            print(f"Data to send (4 bytes): {data}")

            await client.write_gatt_char(self.uuid, data)
            print("Synchronized date and time")