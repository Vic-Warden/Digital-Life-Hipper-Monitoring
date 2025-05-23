from services import *
import asyncio

#
# TimeDate(label_id=90248)
#
# asyncio.run(asyncio.sleep(5))
#
# SetTimestamp2101(label_id=90248)

# ActivityDownload(filename="output/body_part_experiment/chest",
#                  filelength=get_detailed_request("LAST_1_HOUR"),
#                  label_id=90245)
ActivityDownload(filename="output/testw",
                 filelength=get_detailed_request("LAST_1_HOUR"),
                 label_id=90243)
# ActivityDownload(filename="output/body_part_experiment/hip",
#                  filelength=get_detailed_request("LAST_1_HOUR"),
#                  label_id=90248)
# ActivityDownload(filename="output/body_part_experiment/foot",
#                  filelength=get_detailed_request("LAST_1_HOUR"),
#                  label_id=90242)