import asyncio
from datetime import datetime, timedelta, UTC
import csv

from bleak import BleakClient
from PAM_2102 import PAM_2102
from PAM_2103 import PAM_2103

UUID_2102 = "99DB2102-AC2D-11E3-A5E2-0800200C9A66"
UUID_2103 = "99DB2103-AC2D-11E3-A5E2-0800200C9A66"
REQUEST_DETAILED_LAST_15_HOURS = bytearray([0x3C, 0x80])

def parse_detailed_data_blocks(blocks):
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

def display_records(records, base_date):
    start_date = datetime.fromtimestamp(base_date * 86400, UTC)

    with open('records_output.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Steps', 'PAM Score'])

        for di, ti, steps, score in records:
            timestamp = start_date + timedelta(days=di, minutes=ti)
            writer.writerow([timestamp.isoformat(), steps, score])

async def main():
    # Step 1: Use 2102 to send the request
    pam_2102 = PAM_2102(UUID_2102)
    if not await pam_2102.bluetooth_scan():
        return

    # Step 2: Connect and send request using 2102
    print("\n➡️ Sending request via 2102...")
    async with BleakClient(pam_2102.pam_device.address) as client:
        await client.write_gatt_char(UUID_2102, REQUEST_DETAILED_LAST_15_HOURS)
        print("✅ Request sent.")

        # Step 3: Use 2103 to receive and store the data
        print("\n⬇️ Starting download via 2103...")
        pam_2103 = PAM_2103(UUID_2103)
        await pam_2103.start_download(client)

        # Step 4: Process and save results
        received_blocks = pam_2103.get_received_blocks()
        if 0 not in received_blocks:
            print("❌ Header block (block 0) missing.")
            return

        header = received_blocks[0]
        base_date = int.from_bytes(header[4:6], byteorder='little')

        records = parse_detailed_data_blocks(received_blocks)
        display_records(records, base_date)
        print("📁 Data saved to records_output.csv")

if __name__ == "__main__":
    asyncio.run(main())
