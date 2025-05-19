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

class PAM_2001:
    def __init__(self, uuid):
        self.uuid = uuid
    
    async def run(self):
        await self.set_timestamp()

    # Returns the current UTC timestamp
    async def get_current_utc_timestamp(self):
        return int(datetime.now(timezone.utc).timestamp())

    # Main function
    async def set_timestamp(self):

        # Scann BLE device for 5 seconds
        print("On standby...")

        # Variable 
        pam_device = None
        attempts = 0
        
        while attempts < 5:
            devices = await BleakScanner.discover(timeout=5)

            # Displays the name and MAC address of each device
            for device in devices:
                print(f"- {device.name} [{device.address}]")

                # Checks if the device name contains 'Pam'
                if device.name and "Pam" in device.name:
                    pam_device = device
                    break
                
            if pam_device:
                break
            
            attempts += 1

        # If no Pam device is found, print a message and stop
        if not pam_device:
                print("Pam device not connected")
                return
        
        print(f"Pam device found: {pam_device.name} [{pam_device.address}]")

        # Attempts to connect to the Pam device
        print(f"\n Connect to {pam_device.name}...")
        async with BleakClient(pam_device.address) as client:
            print("Connected")

            timestamp = int(datetime.now(timezone.utc).timestamp())
            print(f"Raw UTC timestamp (seconds): {timestamp}")
            data = timestamp.to_bytes(4, byteorder='little')
            print(f"Data to send (4 bytes): {data}")

            await client.write_gatt_char(self.uuid, data)
            print("Synchronized date and time")