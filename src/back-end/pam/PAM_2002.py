import asyncio
from bleak import BleakClient, BleakScanner
import struct

# # Replace this with your device’s BLE address (e.g., "AA:BB:CC:DD:EE:FF")
# TARGET_DEVICE_ADDRESS = "C1:08:00:01:0E:9C"
# 
# # Full 128-bit UUID for the custom “Setup (Test Data)” characteristic (2002):
# self.uuid = "99DB2002-AC2D-11E3-A5E2-0800200C9A66"

class PAM_2002():
    def __init__(self,uuid, target_address):
        self.uuid = uuid
        self.target_address = target_address
        self.adres = None

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

    def pack_setup_bytes(self,
            activation_threshold_mg: int,
            deactivation_threshold_mg: int,
            deactivation_time_s: int,
            adv_interval_byte: int,
            conn_interval_ms: float,
    ) -> bytearray:
        # Validate & convert:
        if activation_threshold_mg % 10 != 0 or not (10 <= activation_threshold_mg <= 1000):
            raise ValueError("activation_threshold_mg must be a multiple of 10 between 10 and 1000")
        if deactivation_threshold_mg % 10 != 0 or not (10 <= deactivation_threshold_mg <= 1000):
            raise ValueError("deactivation_threshold_mg must be a multiple of 10 between 10 and 1000")
        if deactivation_time_s % 10 != 0 or not (10 <= deactivation_time_s <= 2000):
            raise ValueError("deactivation_time_s must be a multiple of 10 between 10 and 2000")
        # Convert mg → 10 mg units (1…100)
        act_thr_byte = activation_threshold_mg // 10
        deact_thr_byte = deactivation_threshold_mg // 10
        # Convert seconds → 10 s units (1…200)
        deact_time_units = deactivation_time_s // 10
        # conn_interval_ms → 12.5 ms units (round to nearest)
        conn_interval_units = int(conn_interval_ms / 12.5)
        if not (1 <= conn_interval_units <= 237):
            raise ValueError("conn_interval_ms must be between 12.5 and 2962.5 ms (inclusive) in 12.5 ms steps")

        # Byte layout:
        # [
        # 0: reserved
        # 1: act threshold
        # 2: deact threshold
        # 3: deact_time
        # 4: adv_interval
        # 5: reserved
        # 6: reserved
        # 7: conn_units
        # ]
        packed = struct.pack(
            "<BBBBBBBB",
            0,  # Byte 0: Reserved
            act_thr_byte,  # Byte 1 act threshold
            deact_thr_byte,  # Byte 2 deact threshold
            deact_time_units,  # Byte 3 deact_time
            adv_interval_byte,  # Byte 4 (raw) adv_interval
            0,  # Byte 5: Reserved
            0,  # Byte 6: Reserved
            conn_interval_units,  # Byte 7
        )
        return bytearray(packed)

    # connects to PAM device, requests a file with 2102, and then downloads it with 2103
    async def connect(self):
        self.adres = None
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
            self.adres = pam_device.address
        elif self.directly_targetting_ID == True:
            self.adres = self.target_address

    async def run_read(self):
        await self.connect()

        async with BleakClient(self.adres) as client:
            if not client.is_connected:
                print(f"Failed to connect to {self.target_addresstarget_address}")
                return
            print(f"Connected to {self.target_address}")

            # 1) Read the current Setup characteristic (8 bytes)
            raw = await client.read_gatt_char(self.uuid)
            print("Raw Setup bytes:", raw.hex())
            decoded = self.decode_setup_bytes(raw)
            print("Current Setup values:")
            print(f"  • Activation threshold:   {decoded['activation_threshold_mg']} mg")
            print(f"  • Deactivation threshold: {decoded['deactivation_threshold_mg']} mg")
            print(f"  • Deactivation time:      {decoded['deactivation_time_s']} s")
            print(f"  • Adv. interval (raw):    0x{decoded['adv_interval_encoded']:02X}")
            print(f"  • Conn. interval:         {decoded['conn_interval_ms']} ms")
            # print()
            #
            # # 2) Example: change thresholds to new values
            # #    (e.g., activation → 200 mg, deactivation → 50 mg,
            # #     deactivation time → 60 s, adv interval code → 0x05, conn interval → 100 ms)
            # new_act_mg = 200
            # new_deact_mg = 50
            # new_deact_time_s = 60
            # new_adv_byte = 0x05       # encodes 5 → 546.25 ms (lower four bits = 5, multiplier=0)
            # new_conn_ms = 500.0       # will be rounded to nearest multiple of 12.5 ms (→ 8 units = 100 ms)
            #
            # to_write = self.pack_setup_bytes(
            #     activation_threshold_mg=new_act_mg,
            #     deactivation_threshold_mg=new_deact_mg,
            #     deactivation_time_s=new_deact_time_s,
            #     adv_interval_byte=new_adv_byte,
            #     conn_interval_ms=new_conn_ms,
            # )
            #
            # print("Writing new Setup bytes:", to_write.hex())
            # await client.write_gatt_char(self.uuid, to_write, response=True)
            #
            # # 3) Read back to verify
            # raw2 = await client.read_gatt_char(self.uuid)
            # print("Read back bytes:           ", raw2.hex())
            # decoded2 = self.decode_setup_bytes(raw2)
            # print("Decoded new values:")
            # print(f"  • Activation threshold:   {decoded2['activation_threshold_mg']} mg")
            # print(f"  • Deactivation threshold: {decoded2['deactivation_threshold_mg']} mg")
            # print(f"  • Deactivation time:      {decoded2['deactivation_time_s']} s")
            # print(f"  • Adv. interval (raw):    0x{decoded2['adv_interval_encoded']:02X}")
            # print(f"  • Conn. interval:         {decoded2['conn_interval_ms']} ms")
    async def run_write(self,
                        new_act_mg,
                        new_deact_mg,
                        new_deact_time_s,
                        new_adv_byte,       # encodes 5 → 546.25 ms (lower four bits = 5, multiplier=0)
                        new_conn_ms):
        await self.connect()

        async with BleakClient(self.adres) as client:
            if not client.is_connected:
                print(f"Failed to connect to {self.target_addresstarget_address}")
                return
            print(f"Connected to {self.target_address}")

            # 1) Read the current Setup characteristic (8 bytes)
            raw = await client.read_gatt_char(self.uuid)
            print("Raw Setup bytes:", raw.hex())
            decoded = self.decode_setup_bytes(raw)
            print("Current Setup values:")
            print(f"  • Activation threshold:   {decoded['activation_threshold_mg']} mg")
            print(f"  • Deactivation threshold: {decoded['deactivation_threshold_mg']} mg")
            print(f"  • Deactivation time:      {decoded['deactivation_time_s']} s")
            print(f"  • Adv. interval (raw):    0x{decoded['adv_interval_encoded']:02X}")
            print(f"  • Conn. interval:         {decoded['conn_interval_ms']} ms")
            print()

            # # 2) Change thresholds to new values
            to_write = self.pack_setup_bytes(
                activation_threshold_mg=new_act_mg,
                deactivation_threshold_mg=new_deact_mg,
                deactivation_time_s=new_deact_time_s,
                adv_interval_byte=new_adv_byte,
                conn_interval_ms=new_conn_ms,
            )

            print("Writing new Setup bytes:", to_write.hex())
            await client.write_gatt_char(self.uuid, to_write, response=True)
            import time
            time.sleep(3)

            # 3) Read back to verify
            raw2 = await client.read_gatt_char(self.uuid)
            print("Read back bytes:           ", raw2.hex())
            decoded2 = self.decode_setup_bytes(raw2)
            print("Decoded new values:")
            print(f"  • Activation threshold:   {decoded2['activation_threshold_mg']} mg")
            print(f"  • Deactivation threshold: {decoded2['deactivation_threshold_mg']} mg")
            print(f"  • Deactivation time:      {decoded2['deactivation_time_s']} s")
            print(f"  • Adv. interval (raw):    0x{decoded2['adv_interval_encoded']:02X}")
            print(f"  • Conn. interval:         {decoded2['conn_interval_ms']} ms")
