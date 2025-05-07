# Imports asyncio module
import asyncio

# Imports the BleakScanner class from the bleak module
from bleak import BleakScanner, BleakClient

# Main function
async def main():

    # Scann BLE device search for 5 seconds
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

# Executes the program
if __name__ == "__main__":
    asyncio.run(main())