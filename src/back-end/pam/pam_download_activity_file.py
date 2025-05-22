from services import *
import asyncio

#
# TimeDate(label_id=90248)
#
# asyncio.run(asyncio.sleep(5))
#
# SetTimestamp2101(label_id=90248)

ActivityDownload(filename="output/data_records_LAST_14_DAYS_90248.csv",
                 filelength=get_detailed_request("LAST_14_DAYS"),
                 label_id=90248)