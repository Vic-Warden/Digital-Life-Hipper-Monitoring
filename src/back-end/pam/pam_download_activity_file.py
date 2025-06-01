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
ActivityDownload(filename="../../research/data/device__8__3.csv",
                 filelength=get_detailed_request("MAX"),
                 label_id=90248)
ActivityDownload(filename="../../research/data/device__2__3.csv",
                 filelength=get_detailed_request("MAX"),
                 label_id=90242)
