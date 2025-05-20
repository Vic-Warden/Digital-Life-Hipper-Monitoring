import asyncio
from bleak import BleakScanner, BleakClient
from services import get_address_by_label


class PAM_2101:
    def __init__(self, uuid, label_id = None):
        # UUID of the Activity Data characteristic (2101)
        self.uuid = uuid
        self.devices = None
        self.pam_device = None
        self.uuidACTIVITY_CHAR_UUID = uuid
        self.label_id = label_id
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
        # Start scanning and connect if a suitable device is found
        found = await self.bluetooth_scan()
        if found:
            await self.connect()

    async def bluetooth_scan(self):
        # Scan for nearby BLE devices for 5 seconds
        print("Scanning for BLE devices...")
        self.devices = await BleakScanner.discover(timeout=5)

        for device in self.devices:
            print(f"- {device.name} [{device.address}]")
            # Identify the Pam device by name
            if device.name and "Pam" in device.name:
                self.pam_device = device
                break

        if not self.pam_device:
            print("Pam sensor not found.")
            return False
        return True

    async def connect(self):
        # Attempt to connect to the Pam device via BLE
        print(f"\nConnecting to {self.pam_device.name}...")
        async with BleakClient(self.pam_device.address) as client:
            print("Connected!")

            # Subscribe to notifications from the Activity Data characteristic
            print(f"Subscribing to Activity Data ({self.uuidACTIVITY_CHAR_UUID})...")
            await client.start_notify(self.uuidACTIVITY_CHAR_UUID, self.notification_handler)

            print("Receiving notifications... (Press Ctrl+C to stop)")
            try:
                while True:
                    # Keep the connection alive to receive notifications
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("Stopping...")
                # Stop notifications when interrupted
                await client.stop_notify(self.uuidACTIVITY_CHAR_UUID)

    def notification_handler(self, sender, data):
        # Callback for handling incoming notifications
        parsed = self.parse_activity_notification(data)
        print(f"\nNotification from {sender}")
        print(f"Parsed Data: {parsed}")

    def parse_activity_notification(self, data: bytearray):
        """
        Parses an 8-byte notification payload from the Pam Activity Data (UUID 2101).
        Structure based on PAM device BLE Interface Specification provided by Michel Oey:

        Byte 0-1: Steps (uint16, little endian)
        Byte 2-3: Activity Score (uint16, little endian)
        Byte 4  : Lower 8 bits of Zone 3 (Sport)
        Byte 5  : Bit 0 = MSB of Zone 3
                  Bits 1-7 = Lower 7 bits of Zone 2 (Health)
        Byte 6  : Bits 0-3 = MSB of Zone 2
                  Bits 4-7 = Lower 4 bits of Zone 1 (Living)
        Byte 7  : MSB of Zone 1
        """

        # Byte 0 and 1: step count (little endian)
        steps = int.from_bytes(data[0:2], 'little')

        # Byte 2 and 3: activity score (little endian)
        score = int.from_bytes(data[2:4], 'little')

        # Zone 3 (sport) time in minutes (9-bit value):
        # Byte 4 = lower 8 bits, Byte 5 (bit 0) = upper 1 bit
        zone3 = data[4] + ((data[5] & 0x01) << 8)

        # Zone 2 (health) time in minutes (11-bit value):
        # Byte 5 (bits 1-7) = lower 7 bits, Byte 6 (bits 0-3) = upper 4 bits
        zone2 = ((data[5] >> 1) & 0x7F) + ((data[6] & 0x0F) << 7)

        # Zone 1 (living) time in minutes (12-bit value):
        # Byte 6 (bits 4-7) = lower 4 bits, Byte 7 = upper 8 bits
        zone1 = ((data[6] >> 4) & 0x0F)

        # Return the parsed values in a dictionary for further use
        return {
            "steps": steps,
            "activity_score": score,
            "zone1_minutes": zone1,
            "zone2_minutes": zone2,
            "zone3_minutes": zone3
        }