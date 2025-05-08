import asyncio
from bleak import BleakScanner, BleakClient

class PAM_2102:
    def __init__(self, uuid):
        # Initialize with UUID for the BLE device
        self.uuid = uuid
        self.devices = None
        self.pam_device = None
        self.uuid_activity = uuid

    async def bluetooth_scan(self):
        # Start scanning for BLE devices
        print("🔍 Scanning for BLE devices...")
        self.devices = await BleakScanner.discover(timeout=5)

        # Loop through found devices and check for the target device name
        for device in self.devices:
            print(f"- {device.name} [{device.address}]")
            if device.name and "Pam" in device.name:
                self.pam_device = device
                break

        # If no device was found, print an error message
        if not self.pam_device:
            print("❌ Pam sensor not found.")
            return False
        # Print success message if device is found
        print(f"✅ Found Pam device: {self.pam_device.name} [{self.pam_device.address}]")
        return True

    async def connect(self):
        # Attempt to connect to the found BLE device
        print(f"\n🔗 Connecting to {self.pam_device.name}...")
        async with BleakClient(self.pam_device.address) as client:
            print("✅ Connected!")

            # Try sending the 2102 command to the BLE device
            try:
                # Example command to request activity file (15 hours of data)
                request_command = bytearray([0x3C, 0x80])
                await client.write_gatt_char(self.uuid_activity, request_command)
                print("✅ 2102 command sent successfully.")
            except Exception as e:
                # Handle errors
                print(f"❌ Failed to send 2102 command: {e}")

    async def run(self):
        # Run the process: scan for the device and connect if found
        found = await self.bluetooth_scan()
        if found:
            await self.connect()

# Entry point for running the PAM_2102 command
if __name__ == "__main__":
    # Construct UUID for the command
    base_uuid = "99DBXXXX-AC2D-11E3-A5E2-0800200C9A66"
    uuid_extension = "2102"
    uuid = base_uuid.replace("XXXX", uuid_extension)

    # Create an instance of the PAM_2102 class and run async event loop
    pam = PAM_2102(uuid)
    asyncio.run(pam.run())
