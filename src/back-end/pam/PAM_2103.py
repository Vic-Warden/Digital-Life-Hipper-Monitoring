# import asyncio
# from bleak import BleakClient
#
# class PAM_2103:
#     def __init__(self, uuid_download, uuid_request, request_command, request_timeout=30):
#         self.uuid_download = uuid_download
#         self.uuid_request = uuid_request
#         self.request_command = request_command
#         self.received_blocks = {}
#         self.client = None
#         self.request_timeout = request_timeout  # max time to wait for header
#
#     def notification_handler(self, sender, data):
#         # Extract block number and payload
#         block_number = int.from_bytes(data[:2], byteorder='little')
#         payload = data[2:]
#         self.received_blocks[block_number] = payload
#         print(f"📦 Received block #{block_number} with {len(payload)} bytes")
#
#     async def start_download(self, client):
#         """
#         Subscribe to notifications, send file request, and collect all data blocks.
#         """
#         self.client = client
#         # Start notifications first to avoid missing the header
#         await self.client.start_notify(self.uuid_download, self.notification_handler)
#         print("📡 Started notification handler on 2103")
#
#         # Give some time to register notifications
#         await asyncio.sleep(0.5)
#
#         # Send the file request command
#         await self.client.write_gatt_char(self.uuid_request, self.request_command)
#         print("📥 Sent file request command via 2102")
#
#         # Wait for header block (block 0)
#         waited = 0.0
#         interval = 0.5
#         while waited < self.request_timeout:
#             if 0 in self.received_blocks:
#                 print("✅ Header block received")
#                 break
#             await asyncio.sleep(interval)
#             waited += interval
#         else:
#             # Header not received within timeout
#             print("❌ Header block (block 0) missing after timeout.")
#             await self.client.stop_notify(self.uuid_download)
#             return False
#
#         # Wait additional time for remaining blocks
#         remaining = self.request_timeout - waited
#         if remaining > 0:
#             await asyncio.sleep(remaining)
#
#         # Stop notifications
#         await self.client.stop_notify(self.uuid_download)
#         print("✅ 2103 download complete")
#         return True
#
#     def get_received_blocks(self):
#         """
#         Return the dictionary of received blocks (block_number -> payload).
#         """
#         return self.received_blocks

import asyncio
from bleak import BleakClient

class PAM_2103:
    def __init__(self, uuid_download, uuid_request, request_command, request_timeout=30):
        self.uuid_download = uuid_download
        self.uuid_request = uuid_request
        self.request_command = request_command
        self.received_blocks = {}
        self.client = None
        self.request_timeout = request_timeout  # max time to wait for header

    def notification_handler(self, sender, data):
        # Extract block number and payload
        block_number = int.from_bytes(data[:2], byteorder='little')
        payload = data[2:]
        self.received_blocks[block_number] = payload
        print(f"📦 Received block #{block_number} with {len(payload)} bytes")

    async def start_download(self, client):
        """
        Subscribe to notifications, send file request, and collect all data blocks.
        """
        self.client = client
        # Start notifications first to avoid missing the header
        await self.client.start_notify(self.uuid_download, self.notification_handler)
        print("📡 Started notification handler on 2103")

        # Give some time to register notifications
        await asyncio.sleep(0.5)

        # Send the file request command
        await self.client.write_gatt_char(self.uuid_request, self.request_command)
        print("📥 Sent file request command via 2102")

        # Wait for header block (block 0)
        waited = 0.0
        interval = 0.5
        while waited < self.request_timeout:
            if 0 in self.received_blocks:
                print("✅ Header block received")
                break
            await asyncio.sleep(interval)
            waited += interval
        else:
            # Header not received within timeout
            print("❌ Header block (block 0) missing after timeout.")
            await self.client.stop_notify(self.uuid_download)
            return False

        # Wait additional time for remaining blocks
        remaining = self.request_timeout - waited
        if remaining > 0:
            await asyncio.sleep(remaining)

        # Stop notifications
        await self.client.stop_notify(self.uuid_download)
        print("✅ 2103 download complete")
        return True

    def get_received_blocks(self):
        """
        Return the dictionary of received blocks (block_number -> payload).
        """
        return self.received_blocks
