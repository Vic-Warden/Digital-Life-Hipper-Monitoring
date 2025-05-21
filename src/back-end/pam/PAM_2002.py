import asyncio
from bleak import BleakClient, BleakScanner
import struct

# Replace this with your device’s BLE address (e.g., "AA:BB:CC:DD:EE:FF")
TARGET_DEVICE_ADDRESS = "C1:08:00:01:0E:9C"

# Full 128-bit UUID for the custom “Setup (Test Data)” characteristic (2002):
SETUP_CHAR_UUID = "99DB2002-AC2D-11E3-A5E2-0800200C9A66"

class PAM_2002():
    def __init__(self,uuid, target_address):
        self.uuid = uuid
        self.target_address = target_address

        self.directly_targetting_ID = False
        if self.target_address != None:
            self.directly_targetting_ID = True

    def decode_setup_bytes(self,data: bytearray) -> dict:
        """
        Given an 8-byte array from the Setup characteristic, decode into human-readable fields.
        Returns a dict with keys:
          - activation_threshold (in mg)
          - deactivation_threshold (in mg)
          - deactivation_time (in seconds)
          - adv_interval_encoded (raw byte)
          - conn_interval_ms (in ms)
        """
        if len(data) != 8:
            raise ValueError("Expected exactly 8 bytes for Setup characteristic")
        # Byte 0 is reserved (ignore)
        _, act_thr, deact_thr, deact_time_units, adv_interval_byte, _, _, conn_interval_units = struct.unpack(
            "<BBBBBBBB", data)

        return {
            "activation_threshold_mg": act_thr * 10,
            "deactivation_threshold_mg": deact_thr * 10,
            "deactivation_time_s": deact_time_units * 10,
            "adv_interval_encoded": adv_interval_byte,
            "conn_interval_ms": conn_interval_units * 12.5,
        }

    # connects to PAM device, requests a file with 2102, and then downloads it with 2103
    async def run(self):
        adres = None
        if self.directly_targetting_ID == False:
            print("Scanning for BLE devices...")
            devices = await BleakScanner.discover(timeout=5)

            pam_device = None
            for device in devices:
                print(f"- {device.name} [{device.address}]")
                if device.name and "Pam" in device.name:
                    pam_device = device
                    break

            if not pam_device:
                print("Pam sensor not found.")
                return

            print(f"\nConnecting to {pam_device.name}...")
            adres = pam_device.address
        elif self.directly_targetting_ID == True:
            adres = self.target_address

        async with BleakClient(adres) as client:
            if not client.is_connected:
                print(f"Failed to connect to {self.target_addresstarget_address}")
                return
            print(f"Connected to {self.target_address}")

            # 1) Read the current Setup characteristic (8 bytes)
            raw = await client.read_gatt_char(SETUP_CHAR_UUID)
            print("Raw Setup bytes:", raw.hex())
            decoded = self.decode_setup_bytes(raw)
            print("Current Setup values:")
            print(f"  • Activation threshold:   {decoded['activation_threshold_mg']} mg")
            print(f"  • Deactivation threshold: {decoded['deactivation_threshold_mg']} mg")
            print(f"  • Deactivation time:      {decoded['deactivation_time_s']} s")
            print(f"  • Adv. interval (raw):    0x{decoded['adv_interval_encoded']:02X}")
            print(f"  • Conn. interval:         {decoded['conn_interval_ms']} ms")
            print()
