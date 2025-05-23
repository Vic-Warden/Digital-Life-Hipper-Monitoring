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
        print(f"Received block #{block_number} with {len(payload)} bytes \n {data}")

    def parse_detailed_data_blocks(self, received_blocks):
        all_bytes = b''.join(received_blocks[k] for k in sorted(received_blocks.keys()))
        records = []

        for i in range(0, len(all_bytes), 8):
            chunk = all_bytes[i : i + 8]

            if len(chunk) < 8:
                break

            steps = chunk[0] | (chunk[1] << 8)
            score = chunk[2] | (chunk[3] << 8)

            zone3_low = chunk[4]
            zone3_high = (chunk[5] & 0x80) >> 7
            zone3 = (zone3_high << 8) | zone3_low

            zone2_low = chunk[5] & 0x7F
            zone2_high = (chunk[6] & 0xF0) >> 4
            zone2 = (zone2_high << 7) | zone2_low

            zone1_low = chunk[6] & 0x0F
            zone1_high = chunk[7]
            zone1 = (zone1_high << 4) | zone1_low

            # # Byte 0 and 1: step count (little endian)
            # steps = int.from_bytes(chunk[0:2], 'little')
            #
            # # Byte 2 and 3: activity score (little endian)
            # score = int.from_bytes(chunk[2:4], 'little')
            #
            # # Zone 3 (sport) time in minutes (9-bit value):
            # # Byte 4 = lower 8 bits, Byte 5 (bit 0) = upper 1 bit
            # zone3 = chunk[4] + ((chunk[5] & 0x01) << 8)
            #
            # # Zone 2 (health) time in minutes (11-bit value):
            # # Byte 5 (bits 1-7) = lower 7 bits, Byte 6 (bits 0-3) = upper 4 bits
            # zone2 = ((chunk[5] >> 1) & 0x7F) + ((chunk[6] & 0x0F) << 7)
            #
            # # Zone 1 (living) time in minutes (12-bit value):
            # # Byte 6 (bits 4-7) = lower 4 bits, Byte 7 = upper 8 bits
            # zone1 = ((chunk[6] >> 4) & 0x0F)

            records.append({
                "Steps": steps,
                "Activity Score": score,
                "Zone 3 (Sport, min)": zone3,
                "Zone 2 (Health, min)": zone2,
                "Zone 1 (Living, min)": zone1
            })

        return records

    def display_records(self, records, base_date):
        # Ensure base_date is a date (in case someone passes datetime)
        if isinstance(base_date, datetime):
            base_date = base_date.date()

        filename = f"activity_{base_date.isoformat()}.csv"
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = [
                "Date",
                "Steps",
                "Activity Score",
                "Zone 3 (Sport, min)",
                "Zone 2 (Health, min)",
                "Zone 1 (Living, min)"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for idx, rec in enumerate(records):
                record_date = (base_date - timedelta(days=len(records))) + timedelta(days=idx)
                row = {
                    "Date": record_date.isoformat(),
                    "Steps": rec["Steps"],
                    "Activity Score": rec["Activity Score"],
                    "Zone 3 (Sport, min)": rec["Zone 3 (Sport, min)"],
                    "Zone 2 (Health, min)": rec["Zone 2 (Health, min)"],
                    "Zone 1 (Living, min)": rec["Zone 1 (Living, min)"],
                }

                print(f"Record {idx+1} — Date: {record_date.isoformat()}")
                print(f"    Steps: {rec['Steps']}")
                print(f"    Activity Score: {rec['Activity Score']}")
                print(f"    Zone 3 (Sport)  : {rec['Zone 3 (Sport, min)']} min")
                print(f"    Zone 2 (Health) : {rec['Zone 2 (Health, min)']} min")
                print(f"    Zone 1 (Living) : {rec['Zone 1 (Living, min)']} min\n")

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
