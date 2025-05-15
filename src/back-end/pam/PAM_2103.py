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

    #decodes the bytes of the incomming message based on the documentation from Pam_BLE_Spec_V1_8
    # def parse_detailed_data_blocks(self, blocks):
    #     all_data = b''.join(payload for block, payload in sorted(blocks.items()) if block != 0)
    #     records = []
    #
    #     for i in range(0, len(all_data), 4):
    #         if i + 4 > len(all_data):
    #             break
    #         byte0 = all_data[i]
    #         date_index = byte0 & 0x1F
    #         ts_index = int.from_bytes(all_data[i+1:i+2] + bytes([byte0 >> 5]), byteorder="little") & 0x7FF
    #         steps = all_data[i + 2]
    #         score_raw = all_data[i + 3]
    #         score = round(score_raw / 16.0, 2)
    #
    #         records.append((date_index, ts_index, steps, score))
    #
    #     return records
    # def parse_detailed_data_blocks(self, blocks):
    #     all_data = b''.join(
    #         payload for block, payload in sorted(blocks.items()) if block != 0
    #     )
    #     records = []
    #
    #     for i in range(0, len(all_data), 4):
    #         if i + 4 > len(all_data):
    #             break
    #
    #         byte0 = all_data[i]
    #         byte1 = all_data[i + 1]
    #         steps = all_data[i + 2]
    #         score_raw = all_data[i + 3]
    #
    #         # lower 5 bits of byte0 = date_index
    #         date_index = byte0 & 0x1F
    #         # upper 3 bits of byte0 as MSBs, byte1 as LSBs → 11‑bit ts_index
    #         ts_index = ((byte0 >> 5) << 8) | byte1
    #         # convert raw score to float
    #         score = round(score_raw / 16.0, 2)
    #
    #         records.append((date_index, ts_index, steps, score))
    #
    #     return records
    def parse_detailed_data_blocks(self, blocks):
        all_data = b''.join(
            payload for block, payload in sorted(blocks.items()) if block != 0
        )
        records = []

        for i in range(0, len(all_data), 4):
            if i + 4 > len(all_data):
                break

            byte0 = all_data[i]
            byte1 = all_data[i + 1]
            steps = all_data[i + 2]
            score_raw = all_data[i + 3]

            date_index = byte0 & 0x1F
            ts_index   = ((byte0 >> 5) << 8) | byte1
            score      = round(score_raw / 16.0, 2)

            records.append((date_index, ts_index, steps, score))

        return records

    #
    # def display_records(self, records, base_date):
    #     # 1) sort to guarantee chronological order
    #     # records = sorted(records, key=lambda x: (x[0], x[1]))
    #
    #     # 2) get the midnight UTC base date
    #     # start_date = datetime.utcfromtimestamp(base_date * 86400)
    #     from datetime import datetime, timedelta, timezone
    #     start_date = datetime.fromtimestamp(base_date * 86400, tz=timezone.utc).astimezone(your_local_tz)
    #
    #     with open(self.filename, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(['Timestamp', 'Steps', 'PAM Score'])
    #
    #         for di, ti, steps, score in records:
    #             # ti is minutes since midnight:
    #             ts = start_date + timedelta(days=di, minutes=ti)
    #             writer.writerow([ts, steps, score])
    def display_records(self, records, base_date):
        from datetime import datetime, timedelta, timezone
        import csv
        import pytz
        # 1) sort the raw records by (day, minute)
        records = sorted(records, key=lambda x: (x[0], x[1]))

        # 2) build a map from absolute UTC-minute to (steps, score)
        #    absolute minutes since 1970‐01‐01 00:00 UTC:
        abs_map = {}
        for di, ti, steps, score in records:
            abs_min = base_date * 1440 + di * 1440 + ti
            abs_map[abs_min] = (steps, score)

        # 3) define continuous range from first to last minute
        first_min = min(abs_map)
        last_min = max(abs_map)

        # 4) set up your timezone converter
        utc = timezone.utc
        local_tz = pytz.timezone('Europe/Amsterdam')

        # 5) write every minute in that span to CSV
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Steps', 'PAM Score'])

            current = first_min
            while current <= last_min:
                # lookup or default
                steps, score = abs_map.get(current, (0, 0.0))

                # convert back to a datetime in UTC, then to local
                dt_utc = datetime(1970, 1, 1, tzinfo=utc) + timedelta(minutes=current)
                dt_local = dt_utc.astimezone(local_tz)

                writer.writerow([dt_local.strftime('%Y-%m-%d %H:%M:%S'),
                                 steps,
                                 f'{score:.2f}'])
                current += 1




    # #displays the records here
    # def display_records(self, records, base_date):
    #
    #     print(records)
    #     # times 86400 to account for the amount of seconds for each day
    #     start_date = datetime.fromtimestamp(base_date * 86400)
    #
    #     # Assuming `records` is already defined
    #     with open(self.filename, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         # Writing the header
    #         writer.writerow(['Timestamp', 'Steps', 'PAM Score'])
    #
    #         # Writing each record
    #         for di, ti, steps, score in records:
    #             timestamp = start_date + timedelta(days=di, minutes=ti)
    #             writer.writerow([timestamp, steps, score])


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

            import time
            print("waiting")
            time.sleep(30)

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