import asyncio
from PAM_2101 import PAM_2101
from PAM_2102 import PAM_2102
from PAM_2103 import PAM_2103

# Base UUID for Hipper BLE commands
base_uuid = "99DBXXXX-AC2D-11E3-A5E2-0800200C9A66"

class TimeDate:
    def __init__(self):
        self.base_uuid = base_uuid
        # UUID for TimeDate is 2001
        # Check documentation for details
        self.uuid_extension = "2001"
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)

class ActivityData:
    # This mode is used for making a client that receives data every few seconds from the PAM device
    def __init__(self):
        # UUID for ActivityData is 2101
        # Check documentation for details
        self.base_uuid = base_uuid
        self.uuid_extension = "2101"  # for ActivityData
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)

        asyncio.run(self.run())

    async def run(self):
        pam = PAM_2101(self.uuid)
        await pam.run()

class ActivityFile:
    def __init__(self):
        # UUID for ActivityFile is 2102
        self.base_uuid = base_uuid
        self.uuid_extension = "2102"
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)

        # Run the PAM_2102 script to send the command and confirm transmission
        asyncio.run(self.run())

    async def run(self):
        pam = PAM_2102(self.uuid)
        await pam.run()

class ActivityDownload:
    def __init__(self):
        # UUID for ActivityFile is 2102
        self.base_uuid = base_uuid
        self.uuid_extension = "2103"
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)

        # Run the PAM_2102 script to send the command and confirm transmission
        asyncio.run(self.run())

    async def run(self):
        pam = PAM_2103(self.uuid)
        await pam.run()