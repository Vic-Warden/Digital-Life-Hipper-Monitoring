import asyncio
from bleak import BleakClient, BleakScanner
import csv
from datetime import datetime, timedelta, UTC

class PAM_2103():
    def __init__(self, uuid,  filename):
        self.filename = filename
        #2102 for downloading the file on the PAM device
        self.ACTIVITY_FILE_UUID = "99DB2102-AC2D-11E3-A5E2-0800200C9A66"
        #2103 for downloading the file over BLE
        self.ACTIVITY_DOWNLOAD_UUID = "99DB2103-AC2D-11E3-A5E2-0800200C9A66"

        #length of activity file time
        self.REQUEST_DETAILED_LAST_15_HOURS = bytearray([0x3C, 0x80])  # 15 hours

        self.REQUEST_AMOUNT_TYPE = self.REQUEST_DETAILED_LAST_15_HOURS
        self.received_blocks = {}

    #callback for when a new block of bytes is received
    def notification_handler(self, sender, data):
        block_number = int.from_bytes(data[:2], byteorder='little')
        payload = data[2:]
        self.received_blocks[block_number] = payload
        print(f"Received block #{block_number} with {len(payload)} bytes")

    #decodes the bytes of the incomming message based on the documentation from Pam_BLE_Spec_V1_8
    def parse_detailed_data_blocks(self, blocks):
        all_data = b''.join(payload for block, payload in sorted(blocks.items()) if block != 0)
        records = []

        for i in range(0, len(all_data), 4):
            if i + 4 > len(all_data):
                break
            byte0 = all_data[i]
            date_index = byte0 & 0x1F
            ts_index = int.from_bytes(all_data[i+1:i+2] + bytes([byte0 >> 5]), byteorder="little") & 0x7FF
            steps = all_data[i + 2]
            score_raw = all_data[i + 3]
            score = round(score_raw / 16.0, 2)

            records.append((date_index, ts_index, steps, score))

        return records

    #displays the records here
    def display_records(self, records, base_date):

        print(records)

        start_date = datetime.fromtimestamp(base_date * 86400, UTC)

        # Assuming `records` is already defined
        with open('records_output.csv', mode='w', newline='') as file:
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

            await client.stop_notify(self.ACTIVITY_DOWNLOAD_UUID)
            print("Download complete. Processing data...")

            if 0 not in self.received_blocks:
                print("Download failed; Missing file header.")
                return

            header = self.received_blocks[0]
            base_date = int.from_bytes(header[4:6], byteorder='little')
            print("Base date is: ", base_date)

            records = self.parse_detailed_data_blocks(self.received_blocks)
            self.display_records(records, base_date)