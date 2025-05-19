import asyncio
from bleak import BleakClient, BleakScanner
import csv
from datetime import datetime, timedelta, UTC

class PAM_2103():
    def __init__(self, file_uuid, download_uuid,  filename, filelength, label_id = None):
        self.filename = filename
        #2102 for downloading the file on the PAM device
        self.ACTIVITY_FILE_UUID = file_uuid
        #2103 for downloading the file over BLE
        self.ACTIVITY_DOWNLOAD_UUID = download_uuid

        #length of activity file time
        self.REQUEST_AMOUNT_TYPE = filelength
        self.received_blocks = {}

        self.directly_targetting_ID = False

        if label_id is None:
            print("No label ID was provided. manually scanning.")
        elif label_id is not None:
            print("Label ID provided, directly targetting ID")
            self.directly_targetting_ID = True

    #callback for when a new block of bytes is received
    def notification_handler(self, sender, data):
        block_number = int.from_bytes(data[:2], byteorder='little')
        payload = data[2:]
        self.received_blocks[block_number] = payload
        print(f"Received block #{block_number} with {len(payload)} bytes")

    def parse_detailed_data_blocks(self, blocks: dict[int, bytes]) -> list[tuple[int, int, int, float]]:
        """
        Parse the received BLE blocks of a Detailed Activity Data File into a list of records.

        Args:
            blocks: A dict mapping block_number to payload bytes. Block 0 is the file header.

        Returns:
            A list of tuples:
            (day_offset, minute_offset, step_count, pam_score_float)
        """
        # 1) Extract and validate the file header (block 0)
        file_header = blocks.get(0)
        if not file_header or len(file_header) < 4:
            raise ValueError("Missing or malformed file header (block 0)")

        # bytes 0–1: file_size (lower 15 bits), MSB indicates multi-part
        raw_file_size = int.from_bytes(file_header[0:2], byteorder='little')
        file_size_bytes = raw_file_size & 0x7FFF

        # bytes 2–3: base_date (days since epoch), if you need it elsewhere:
        # base_date_days = int.from_bytes(file_header[2:4], byteorder='little')

        # Concatenate all data payloads (skip header block)
        full_data_stream = bytearray()
        for block_number in sorted(n for n in blocks if n != 0):
            full_data_stream.extend(blocks[block_number])

        # Truncate the stream to the declared file size
        full_data_stream = full_data_stream[:file_size_bytes]

        # Split into 4‑byte records and unpack
        activity_records: list[tuple[int, int, int, float]] = []
        record_size = 4
        for offset in range(0, len(full_data_stream), record_size):
            record_bytes = full_data_stream[offset: offset + record_size]
            if len(record_bytes) < record_size:
                break  # incomplete tail, ignore

            # first two bytes: combined bitfields
            bitfield = int.from_bytes(record_bytes[0:2], byteorder='little')
            day_offset = bitfield & 0x1F  # lower 5 bits: days since base date
            minute_offset = (bitfield >> 5) & 0x7FF  # next 11 bits: minutes into that day

            # third byte: steps count
            step_count = record_bytes[2]

            # fourth byte: raw PAM score, must be divided by 16 for the actual value
            raw_pam_score = record_bytes[3]
            pam_score = raw_pam_score / 16.0

            activity_records.append((day_offset, minute_offset, step_count, pam_score))

        return activity_records

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