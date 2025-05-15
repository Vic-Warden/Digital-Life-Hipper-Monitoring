import asyncio
from bleak import BleakClient, BleakScanner
import csv
from datetime import datetime, timedelta, UTC

class PAM_2103():
    def __init__(self, file_uuid, download_uuid,  filename, filelength):
        self.filename = filename
        #2102 for downloading the file on the PAM device
        self.ACTIVITY_FILE_UUID = file_uuid
        #2103 for downloading the file over BLE
        self.ACTIVITY_DOWNLOAD_UUID = download_uuid

        #length of activity file time
        self.REQUEST_AMOUNT_TYPE = filelength
        self.received_blocks = {}

    #callback for when a new block of bytes is received
    def notification_handler(self, sender, data):
        block_number = int.from_bytes(data[:2], byteorder='little')
        payload = data[2:]
        self.received_blocks[block_number] = payload
        print(f"Received block #{block_number} with {len(payload)} bytes")

    def parse_detailed_data_blocks(self, blocks):
        """
        blocks: dict of {block_number: payload_bytes}, where block 0 is the 4‑byte header
        containing [fileSize (2 bytes), baseDate (2 bytes)].
        Returns a list of tuples (di, ti, steps, score).
        """
        # 1) Extract header
        header = blocks.get(0)
        if header is None or len(header) < 4:
            raise ValueError("Missing or malformed file header (block 0)")
        # fileSize: lower 15 bits of bytes[0:2]
        raw_size = int.from_bytes(header[0:2], byteorder='little')
        file_size = raw_size & 0x7FFF
        # baseDate if you want to double-check here:
        # base_date = int.from_bytes(header[2:4], byteorder='little')

        # 2) Concatenate all payloads in order (skipping block 0)
        data_bytes = bytearray()
        for blk_num in sorted(k for k in blocks.keys() if k != 0):
            data_bytes += blocks[blk_num]

        # 3) Truncate to file_size
        data_bytes = data_bytes[:file_size]

        # 4) Parse into 4‑byte records
        records = []
        for offset in range(0, len(data_bytes), 4):
            chunk = data_bytes[offset:offset + 4]
            if len(chunk) < 4:
                break
            # unpack the 16‑bit bitfield
            raw = int.from_bytes(chunk[0:2], byteorder='little')
            di = raw & 0x1F  # lower 5 bits
            ti = (raw >> 5) & 0x7FF  # next 11 bits
            steps = chunk[2]
            score = chunk[3] / 16.0  # per spec: divide by 16 for float
            records.append((di, ti, steps, score))

        return records

    #displays the records here
    def display_records(self, records, base_date):

        print(records)
        # times 86400 to account for the amount of seconds for each day
        start_date = datetime.fromtimestamp(base_date * 86400)

        # Assuming `records` is already defined
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Writing the header
            writer.writerow(['Timestamp', 'Steps', 'PAM Score'])

            # Writing each record
            for di, ti, steps, score in records:
                timestamp = start_date + timedelta(days=di, minutes=ti)
                writer.writerow([timestamp, steps, score])


    #connects to PAM device, requests a file with 2102, and then downloads it with 2103
    async def run(self):
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
        async with BleakClient(pam_device.address) as client:
            print(" Connected to PAM device!")

            await client.start_notify(self.ACTIVITY_DOWNLOAD_UUID, self.notification_handler)
            await asyncio.sleep(1)

            await client.write_gatt_char(self.ACTIVITY_FILE_UUID, self.REQUEST_AMOUNT_TYPE)
            print("Requested activity file...")

            import time
            print("waiting")
            time.sleep(30)

            await client.stop_notify(self.ACTIVITY_DOWNLOAD_UUID)
            print("Download complete. Processing data...")

            if 0 not in self.received_blocks:
                print("Download failed; Missing file header.")
                return

            header = self.received_blocks[0]
            base_date = int.from_bytes(header[4:6], byteorder='little')
            print("Base date is: ", base_date)
            print(self.received_blocks)

            records = self.parse_detailed_data_blocks(self.received_blocks)
            self.display_records(records, base_date)