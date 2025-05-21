# Simple code to check what services are open on a specific BLE device. 
# Change the mac adress to the correct device to see.
 
import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = "AA:BB:CC:DD:EE:FF"  # Change this to your device

async def explore_services():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print(f"Connected to {DEVICE_ADDRESS}")
        print("\nAvailable services and characteristics:\n")

        for service in client.services:
            print(f"[Service] {service.uuid} — {service.description}")
            for char in service.characteristics:
                props = ', '.join(char.properties)
                print(f"  └── [Characteristic] {char.uuid} — {char.description} (Properties: {props})")

                for descriptor in char.descriptors:
                    print(f"      └── [Descriptor] {descriptor.uuid}")

if __name__ == "__main__":
    asyncio.run(explore_services())
