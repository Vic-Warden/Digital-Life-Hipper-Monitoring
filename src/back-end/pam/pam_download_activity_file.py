from services import *
import asyncio

#
# TimeDate(label_id=90248)
#
# asyncio.run(asyncio.sleep(5))
#
# SetTimestamp2101(label_id=90248)

ActivityDownload(filename="output/dump/device_5",
                 filelength=get_detailed_request("MAX"),
                 label_id=90245)
ActivityDownload(filename="output/dump/device_3",
                 filelength=get_detailed_request("MAX"),
                 label_id=90243)
ActivityDownload(filename="output/dump/device_8",
                 filelength=get_detailed_request("MAX"),
                 label_id=90248)
ActivityDownload(filename="output/dump/device_2",
                 filelength=get_detailed_request("MAX"),
                 label_id=90242)