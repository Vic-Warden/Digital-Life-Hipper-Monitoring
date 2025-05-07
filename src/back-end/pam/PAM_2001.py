# Imports asyncio module
import asyncio

# Imports the BleakScanner class from the bleak module
from bleak import BleakScanner

# Main function
async def main():

    # Scann BLE device search for 5 seconds
    print("On standby...")
    devices = await BleakScanner.discover(timeout=5)

    # Displays the name and MAC address of each device
    for device in devices:
        print(f"- {device.name} [{device.address}]")

# Executes the program
if __name__ == "__main__":
    asyncio.run(main())