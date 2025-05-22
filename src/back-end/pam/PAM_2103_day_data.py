import asyncio
from bleak import BleakClient, BleakScanner
import csv
from datetime import datetime, timedelta, UTC
import time
#
# import time
# class PAM_2103_Day_Data():
#     def __init__(self, file_uuid, download_uuid,  filename, filelength, adres = None):
#         self.filename = filename
#         #2102 for downloading the file on the PAM device
#         self.ACTIVITY_FILE_UUID = file_uuid
#         #2103 for downloading the file over BLE
#         self.ACTIVITY_DOWNLOAD_UUID = download_uuid
#
#         #length of activity file time
#         self.REQUEST_AMOUNT_TYPE = filelength
#         self.received_blocks = {}
#
#         self.directly_targetting_ID = False
#
#         if adres is None:
#             print("No label ID was provided. manually scanning.")
#         elif adres is not None:
#             self.adres = adres
#             print(f"Label ID provided, directly targetting ID {self.adres}")
#             self.directly_targetting_ID = True
#
#     #callback for when a new block of bytes is received
#     def notification_handler(self, sender, data):
#         block_number = int.from_bytes(data[:2], byteorder='little')
#         payload = data[2:]
#         self.received_blocks[block_number] = payload
#         print(f"Received block #{block_number} with {len(payload)} bytes")
#
#     def parse_detailed_data_blocks(self, received_blocks):
#         """
#         Parse a dict of received_blocks (key -> bytearray) into a list of 8‐byte records.
#         Each record is unpacked into:
#           - "Steps"
#           - "Activity Score"
#           - "Zone 3 (Sport, min)"
#           - "Zone 2 (Health, min)"
#           - "Zone 1 (Living, min)"
#
#         :param received_blocks: dict[int, bytearray]
#         :return: List[dict[str, int]]
#         """
#         # 1) Concatenate all blocks in ascending key order
#         all_bytes = b''.join(received_blocks[k] for k in sorted(received_blocks.keys()))
#
#         # 2) Split the concatenated bytes into 8‐byte chunks
#         records = []
#         for i in range(0, len(all_bytes), 8):
#             chunk = all_bytes[i: i + 8]
#             if len(chunk) < 8:
#                 # ignore any trailing partial chunk
#                 break
#
#             # 3) Parse each 8‐byte chunk
#             # Bytes 0–1: steps (little‐endian)
#             steps = chunk[0] | (chunk[1] << 8)
#
#             # Bytes 2–3: activity score (little‐endian)
#             activity_score = chunk[2] | (chunk[3] << 8)
#
#             # Bytes 4–5: time in zone 3 (sport)
#             #   - Byte 4: lower 8 bits
#             #   - Byte 5, bit 7: upper 1 bit (shifted into bit 8)
#             zone3_low = chunk[4]
#             zone3_high = (chunk[5] & 0x80) >> 7  # extract bit 7 of byte 5
#             zone3 = (zone3_high << 8) | zone3_low
#
#             # Bytes 5–6: time in zone 2 (health)
#             #   - Byte 5, bits 0–6: lower 7 bits
#             #   - Byte 6, bits 4–7: upper 4 bits (shifted into bits 7–10)
#             zone2_low = chunk[5] & 0x7F  # bits 0–6 of byte 5
#             zone2_high = (chunk[6] & 0xF0) >> 4  # bits 4–7 of byte 6, shift down to 0–3
#             zone2 = (zone2_high << 7) | zone2_low
#
#             # Bytes 6–7: time in zone 1 (living)
#             #   - Byte 6, bits 0–3: lower 4 bits
#             #   - Byte 7: upper 8 bits (shifted into bits 4–11)
#             zone1_low = chunk[6] & 0x0F  # bits 0–3 of byte 6
#             zone1_high = chunk[7]  # all 8 bits of byte 7
#             zone1 = (zone1_high << 4) | zone1_low
#
#             # 4) Append parsed record as a dict
#             records.append({
#                 "Steps": steps,
#                 "Activity Score": activity_score,
#                 "Zone 3 (Sport, min)": zone3,
#                 "Zone 2 (Health, min)": zone2,
#                 "Zone 1 (Living, min)": zone1
#             })
#
#         return records
#
#     #displays the records here
#     def display_records(self, records, base_date):
#         """
#         Print each parsed record with its corresponding date, and save all records to a CSV file.
#
#         :param records: List[dict[str, int]] as returned by parse_detailed_data_blocks
#         :param base_date: datetime.date or datetime.datetime indicating the first record's date
#         """
#         # 1) Normalize base_date to a date object (if a datetime was passed)
#         if isinstance(base_date, datetime):
#             base_date = base_date.date()
#
#         # 2) Prepare CSV filename using the base_date
#         filename = f"activity_{base_date.isoformat()}.csv"
#
#         # 3) Open the CSV file for writing
#         with open(filename, mode='w', newline='') as csvfile:
#             fieldnames = [
#                 "Date",
#                 "Steps",
#                 "Activity Score",
#                 "Zone 3 (Sport, min)",
#                 "Zone 2 (Health, min)",
#                 "Zone 1 (Living, min)"
#             ]
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#
#             # 4) Iterate through records, print to console, and write to CSV
#             for idx, rec in enumerate(records):
#                 # Compute this record's date as base_date + idx days
#                 record_date = base_date + timedelta(days=idx)
#
#                 # Build a row dictionary for CSV
#                 row = {
#                     "Date": record_date.isoformat(),
#                     "Steps": rec["Steps"],
#                     "Activity Score": rec["Activity Score"],
#                     "Zone 3 (Sport, min)": rec["Zone 3 (Sport, min)"],
#                     "Zone 2 (Health, min)": rec["Zone 2 (Health, min)"],
#                     "Zone 1 (Living, min)": rec["Zone 1 (Living, min)"],
#                 }
#
#                 # Print to console in a readable format
#                 print(f"Record {idx + 1} — Date: {record_date.isoformat()}")
#                 print(f"    Steps: {rec['Steps']}")
#                 print(f"    Activity Score: {rec['Activity Score']}")
#                 print(f"    Zone 3 (Sport)  : {rec['Zone 3 (Sport, min)']} min")
#                 print(f"    Zone 2 (Health) : {rec['Zone 2 (Health, min)']} min")
#                 print(f"    Zone 1 (Living) : {rec['Zone 1 (Living, min)']} min\n")
#
#                 # Write this row into the CSV
#                 writer.writerow(row)
#
#         print(f"All records have been written to {filename}")
#
#
#     #connects to PAM device, requests a file with 2102, and then downloads it with 2103
#     async def run(self):
#         adres = None
#         if self.directly_targetting_ID == False:
#             print("Scanning for BLE devices...")
#             devices = await BleakScanner.discover(timeout=5)
#
#             pam_device = None
#             for device in devices:
#                 print(f"- {device.name} [{device.address}]")
#                 if device.name and "Pam" in device.name:
#                     pam_device = device
#                     break
#
#             if not pam_device:
#                 print("Pam sensor not found.")
#                 return
#
#             print(f"\nConnecting to {pam_device.name}...")
#             adres = pam_device.address
#         elif self.directly_targetting_ID == True:
#             adres = self.adres
#
#         async with BleakClient(adres) as client:
#             print(" Connected to PAM device!")
#
#             await client.start_notify(self.ACTIVITY_DOWNLOAD_UUID, self.notification_handler)
#             await asyncio.sleep(1)
#             time.sleep(5)
#
#             await client.write_gatt_char(self.ACTIVITY_FILE_UUID, self.REQUEST_AMOUNT_TYPE)
#             print("Requested activity file...")
#
#             print("waiting")
#             time.sleep(5)
#
#             await client.stop_notify(self.ACTIVITY_DOWNLOAD_UUID)
#             print("Download complete. Processing data...")
#
#             if 0 not in self.received_blocks:
#                 print("Download failed; Missing file header.")
#                 return
#
#             header = self.received_blocks[0]
#             base_date = int.from_bytes(header[2:4], byteorder='little')
#             print("Base date is: ", base_date)
#             print(self.received_blocks)
#
#             records = self.parse_detailed_data_blocks(self.received_blocks)
#             self.display_records(records, base_date)


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
        print(f"Received block #{block_number} with {len(payload)} bytes")

    def parse_detailed_data_blocks(self, received_blocks):
        all_bytes = b''.join(received_blocks[k] for k in sorted(received_blocks.keys()))
        records = []
        for i in range(0, len(all_bytes), 8):
            chunk = all_bytes[i : i + 8]
            if len(chunk) < 8:
                break

            steps = chunk[0] | (chunk[1] << 8)
            activity_score = chunk[2] | (chunk[3] << 8)

            zone3_low = chunk[4]
            zone3_high = (chunk[5] & 0x80) >> 7
            zone3 = (zone3_high << 8) | zone3_low

            zone2_low = chunk[5] & 0x7F
            zone2_high = (chunk[6] & 0xF0) >> 4
            zone2 = (zone2_high << 7) | zone2_low

            zone1_low = chunk[6] & 0x0F
            zone1_high = chunk[7]
            zone1 = (zone1_high << 4) | zone1_low

            records.append({
                "Steps": steps,
                "Activity Score": activity_score,
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
                record_date = base_date + timedelta(days=idx)
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
