import asyncio
from bleak import BleakScanner, BleakClient

class PAM_2101:
    def __init__(self, uuid):
        self.uuid = uuid
        self.devices = None
        self.pam_device = None
        self.uuidACTIVITY_CHAR_UUID = uuid  # make sure this is correct!

    async def run(self):
        found = await self.BluetoothScan()
        if found:
            await self.connect()

    async def BluetoothScan(self):
        print("Scanning for BLE devices...")
        self.devices = await BleakScanner.discover(timeout=5)

        for device in self.devices:
            print(f"- {device.name} [{device.address}]")
            if device.name and "Pam" in device.name:
                self.pam_device = device
                break

        if not self.pam_device:
            print("Pam sensor not found.")
            return False
        return True

    async def connect(self):
        print(f"\nConnecting to {self.pam_device.name}...")
        async with BleakClient(self.pam_device.address) as client:
            print("Connected!")

            print(f"Subscribing to Activity Data ({self.uuidACTIVITY_CHAR_UUID})...")
            await client.start_notify(self.uuidACTIVITY_CHAR_UUID, self.notification_handler)

            print("Receiving notifications... (Press Ctrl+C to stop)")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("Stopping...")
                await client.stop_notify(self.uuidACTIVITY_CHAR_UUID)

    def notification_handler(self, sender, data):
        parsed = self.parse_activity_notification(data)
        print(f"\nNotification from {sender}")
        print(f"Parsed Data: {parsed}")

    def parse_activity_notification(self, data: bytearray):
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
