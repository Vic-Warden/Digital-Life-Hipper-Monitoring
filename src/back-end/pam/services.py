import asyncio
from PAM_2101 import PAM_2101
base_uuid = "99DBXXXX-AC2D-11E3-A5E2-0800200C9A66"


class TimeDate:
    def __init__(self):
        self.base_uuid = base_uuid
        # UUID for TimeDate is 2001
        # Check documentation for details
        self.uuid_extension = "2001"
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)

class ActivityData:
    def __init__(self):
        self.base_uuid = base_uuid
        self.uuid_extension = "2101"  # for ActivityData
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)

        asyncio.run(self.run())

    async def run(self):
        pam = PAM_2101(self.uuid)
        await pam.run()


class ActivityFile:
    def __init__(self):
        self.base_uuid = base_uuid
        # UUID for ActivityFile is 2003
        # Check documentation for details
        self.uuid_extension = "2102"
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)


class ActivityDownload:
    def __init__(self):
        self.base_uuid = base_uuid
        # UUID for ActivityDownload is 2004
        # Check documentation for details
        self.uuid_extension = "2103"
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)
