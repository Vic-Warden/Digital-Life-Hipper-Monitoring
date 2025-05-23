import time
import asyncio
from bleak import BleakClient, BleakScanner
import csv
from datetime import datetime, timedelta

class PAM_2103_Day_Data():
    def __init__(self, file_uuid, download_uuid, filename, filelength, adres=None):
        self.filename = filename
        self.ACTIVITY_FILE_UUID = file_uuid
        self.ACTIVITY_DOWNLOAD_UUID = download_uuid
        self.REQUEST_AMOUNT_TYPE = filelength
        self.received_blocks = {}
        self.directly_targetting_ID = False

        if adres is None:
            print("No label ID was provided. Manually scanning.")
        else:
            self.adres = adres
            print(f"Label ID provided, directly targetting ID {self.adres}")
            self.directly_targetting_ID = True

    def notification_handler(self, sender, data):
        block_number = int.from_bytes(data[:2], byteorder='little')
        payload = data[2:]
        self.received_blocks[block_number] = payload
        print(f"Received block #{block_number} with {len(payload)} bytes \n {payload}")


    def parse_detailed_data_blocks(self, received_blocks):
        # Exclude header block (block number 0)
        data_blocks = {
            k: v for k, v in received_blocks.items() if k != 0
        }

        # Concatenate in ascending block-number order
        all_bytes = b''.join(data_blocks[k] for k in sorted(data_blocks.keys()))

        records = []
        for i in range(0, len(all_bytes), 8):
            chunk = all_bytes[i: i + 8]

            # --- First 2 bytes: [ date_index (5 bits) | living_zone (11 bits) ] ---
            first_word = chunk[0] | (chunk[1] << 8)
            zone1_time = (first_word >> 5) & 0x7FF  # Living Zone (11 bits)

            # --- Next 4 bytes: [ health_zone (10 bits) | sport_zone (9 bits) | pam_score (13 bits) ] ---
            second_dword = (
                    chunk[2]
                    | (chunk[3] << 8)
                    | (chunk[4] << 16)
                    | (chunk[5] << 24)
            )
            zone2_time = second_dword & 0x3FF  # Health Zone (10 bits)
            zone3_time = (second_dword >> 10) & 0x1FF  # Sport Zone (9 bits)
            activity_score = (second_dword >> 19) & 0x1FFF  # PAM Score  (13 bits)

            # --- Last 2 bytes: steps (uint16 little-endian) ---
            steps = chunk[6] | (chunk[7] << 8)

            records.append({
                "Steps": steps,
                "Activity Score": activity_score,
                "Zone 3 (Sport)": zone3_time,
                "Zone 2 (Health)": zone2_time,
                "Zone 1 (Living)": zone1_time
            })

        return records


    def display_records(self, records, base_date):
        # Ensure base_date is a date (in case someone passes datetime)
        if isinstance(base_date, datetime):
            base_date = base_date.date()

        filename = f"{self.filename}.csv"
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = [
                "Date",
                "Steps",
                "Activity Score",
                "Zone 3 (Sport)",
                "Zone 2 (Health)",
                "Zone 1 (Living)"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for idx, rec in enumerate(records):
                record_date = (base_date - timedelta(days=len(records))) + timedelta(days=idx + 1)
                row = {
                    "Date": record_date.isoformat(),
                    "Steps": rec["Steps"],
                    "Activity Score": rec["Activity Score"],
                    "Zone 3 (Sport)": rec["Zone 3 (Sport)"],
                    "Zone 2 (Health)": rec["Zone 2 (Health)"],
                    "Zone 1 (Living)": rec["Zone 1 (Living)"],
                }

                writer.writerow(row)

        print(f"All records have been written to {filename}")

    async def run(self):
        if not self.directly_targetting_ID:
            print("Scanning for BLE devices…")
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
            print(f"\nConnecting to {pam_device.name}…")
            adres = pam_device.address
        else:
            adres = self.adres

        async with BleakClient(adres) as client:
            print("Connected to PAM device!")

            await client.start_notify(self.ACTIVITY_DOWNLOAD_UUID, self.notification_handler)
            await asyncio.sleep(1)
            time.sleep(5)

            await client.write_gatt_char(self.ACTIVITY_FILE_UUID, self.REQUEST_AMOUNT_TYPE)
            print("Requested activity file…")

            print("waiting")
            time.sleep(5)

            await client.stop_notify(self.ACTIVITY_DOWNLOAD_UUID)
            print("Download complete. Processing data…")

            if 0 not in self.received_blocks:
                print("Download failed; Missing file header.")
                return

            header = self.received_blocks[0]
            raw_days = int.from_bytes(header[2:4], byteorder='little')
            # Convert raw integer into a real date
            base_date = datetime(1970, 1, 1).date() + timedelta(days=raw_days)
            print("Base date is:", base_date.isoformat())
            print(self.received_blocks)

            records = self.parse_detailed_data_blocks(self.received_blocks)
            self.display_records(records, base_date)
