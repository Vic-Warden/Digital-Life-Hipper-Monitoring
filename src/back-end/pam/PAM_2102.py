import asyncio
from bleak import BleakScanner, BleakClient

class PAM_2102:
    def __init__(self, uuid):
        self.uuid = uuid
        self.devices = None
        self.pam_device = None
        self.uuid_activity = uuid

    async def bluetooth_scan(self):
        print("🔍 Scanning for BLE devices...")
        self.devices = await BleakScanner.discover(timeout=5)

        for device in self.devices:
            print(f"- {device.name} [{device.address}]")
            if device.name and "Pam" in device.name:
                self.pam_device = device
                break

        if not self.pam_device:
            print("❌ Pam sensor not found.")
            return False
        print(f"✅ Found Pam device: {self.pam_device.name} [{self.pam_device.address}]")
        return True

    async def connect(self):
        print(f"\n🔗 Connecting to {self.pam_device.name}...")
        async with BleakClient(self.pam_device.address) as client:
            print("✅ Connected!")

            # Sending the 2102 command to request the activity file
            try:
                request_command = bytearray([0x3C, 0x80])  # Example command (15 hours of data)
                await client.write_gatt_char(self.uuid_activity, request_command)
                print("✅ 2102 command sent successfully.")
            except Exception as e:
                print(f"❌ Failed to send 2102 command: {e}")

    async def run(self):
        found = await self.bluetooth_scan()
        if found:
            await self.connect()

# Entry point for running the PAM_2102 command
if __name__ == "__main__":
    base_uuid = "99DBXXXX-AC2D-11E3-A5E2-0800200C9A66"
    uuid_extension = "2102"
    uuid = base_uuid.replace("XXXX", uuid_extension)

    pam = PAM_2102(uuid)
    asyncio.run(pam.run())
