import asyncio
from bleak import BleakScanner, BleakClient

ACTIVITY_CHAR_UUID = "99DB2101-AC2D-11E3-A5E2-0800200C9A66"

# Parse Activity Notification
def parse_activity_notification(data: bytearray):
    steps = int.from_bytes(data[0:2], 'little')
    score = int.from_bytes(data[2:4], 'little')
    zone3 = data[4] + ((data[5] & 0x01) << 8)
    zone2 = ((data[5] >> 1) & 0x7F) + ((data[6] & 0x0F) << 7)
    zone1 = ((data[6] >> 4) & 0x0F) + (data[7] << 4)

    return {
        "steps": steps,
        "activity_score": score,
        "zone1_minutes": zone1,
        "zone2_minutes": zone2,
        "zone3_minutes": zone3
    }

# Notification handler
def notification_handler(sender, data):
    parsed = parse_activity_notification(data)
    print(f"\nNotification from {sender}")
    print(f"Parsed Data: {parsed}")

async def main():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=5)

    pam_device = None
    for device in devices:
        print(f"- {device.name} [{device.address}]")
        if device.name and "Pam" in device.name:  # Adjust this based on actual device name
            pam_device = device
            break

    if not pam_device:
        print("Pam sensor not found.")
        return

    print(f"\nConnecting to {pam_device.name}...")
    async with BleakClient(pam_device.address) as client:
        print("Connected!")

        # Enable notifications
        print(f"Subscribing to Activity Data ({ACTIVITY_CHAR_UUID})...")
        await client.start_notify(ACTIVITY_CHAR_UUID, notification_handler)

        print("Receiving notifications... (Press Ctrl+C to stop)")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Stopping...")
            await client.stop_notify(ACTIVITY_CHAR_UUID)

# Run the BLE loop
if __name__ == "__main__":
    asyncio.run(main())

