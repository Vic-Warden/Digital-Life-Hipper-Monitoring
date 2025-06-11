from services import *
import asyncio
#
# TimeDate(label_id=90248)
#
# asyncio.run(asyncio.sleep(5))
#
# SetTimestamp2101(label_id=8)
#
# asyncio.run(asyncio.sleep(5))

# TimeDate(label_id=90242)
#
# asyncio.run(asyncio.sleep(5))
#
# SetTimestamp2101(label_id=2)
#
# downloader = ActivityDownload(filename="../AI/training_data/06_06_2025_device_8.csv",
#                               filelength=get_detailed_request("MAX"),
#                               label_id=90248)
# asyncio.run(downloader.run())
#
# downloader = ActivityDownload(filename="../AI/training_data/06_06_2025_device_5.csv",
#                               filelength=get_detailed_request("MAX"),
#                               label_id=90245)
# asyncio.run(downloader.run())
#
# downloader = ActivityDownload(filename="../AI/training_data/06_06_2025_device_3.csv",
#                               filelength=get_detailed_request("MAX"),
#                               label_id=90243)
# asyncio.run(downloader.run())

downloader = ActivityDownload(filename="../AI/training_data/11_06_2025_device_2.csv",
                              filelength=get_detailed_request("MAX"),
                              label_id=90242)
asyncio.run(downloader.run())

downloader = ActivityDownload(filename="../AI/training_data/11_06_2025_device_3.csv",
                              filelength=get_detailed_request("MAX"),
                              label_id=90243)
asyncio.run(downloader.run())