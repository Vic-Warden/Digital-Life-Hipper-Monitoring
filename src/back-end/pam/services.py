import asyncio
from PAM_2001 import PAM_2001
from PAM_2101 import PAM_2101
from PAM_2102 import PAM_2102
from PAM_2102 import get_detailed_request
from PAM_2103 import PAM_2103
import json

# Base UUID for Hipper BLE commands
base_uuid = "99DBXXXX-AC2D-11E3-A5E2-0800200C9A66"

# checks the PAM_devices.json and returns the desired mac addres if asked for
def get_address_by_label(label_id = None, filename="PAM_devices.json"):
    if label_id is None:
        return None
    label_id = "label_" + str(label_id)
    try:
        with open(filename, "r") as f:
            labels = json.load(f)
        return labels.get(label_id, "Label ID not found.")
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Error decoding JSON."

class TimeDate:
    def __init__(self, label_id=None):
        self.base_uuid = base_uuid
        # UUID for TimeDate is 2001
        # Check documentation for details
        self.uuid_extension = "2001"
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)
        self.label_id = label_id
        
        asyncio.run(self.run())
        
    async def run(self):
        pam = PAM_2001(self.uuid, label_id=self.label_id)
        await pam.run()

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

#used to download the activityfile into a csv file
class ActivityDownload:
    def __init__(self, filename, filelength, label_id = None):
        self.label_id = None
        self.label_id = label_id

        # UUID for ActivityFile is 2102
        self.base_uuid = base_uuid

        self.filelength = filelength

        self.file_uuid_extension = "2102"
        self.file_uuid = self.base_uuid.replace("XXXX", self.file_uuid_extension)

        self.download_uuid_extension = "2103"
        self.download_uuid = self.base_uuid.replace("XXXX", self.download_uuid_extension)


        # Run the PAM_2102 script to send the command and confirm transmission
        asyncio.run(self.run(filename))

    async def run(self, filename):
        pam = PAM_2103(file_uuid=self.file_uuid,
                       download_uuid=self.download_uuid,
                       filename=filename,
                       filelength=self.filelength,
                       adres=get_address_by_label(self.label_id))
        await pam.run()

class SetTimestamp2101:
    def __init__(self, label_id=None):
        self.base_uuid = base_uuid
        self.uuid_extension = "2101"
        self.uuid = self.base_uuid.replace("XXXX", self.uuid_extension)

        asyncio.run(self.run(label_id))

    async def run(self, label_id):
        pam = PAM_2101(uuid=self.uuid, label_id=label_id)
        await pam.run()
