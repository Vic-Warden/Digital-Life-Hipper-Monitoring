from services import *

# ActivityDownload(filename="output/data_records_1H.csv",
#                  filelength=get_detailed_request("LAST_1_HOUR"))

ActivityDownload(filename="output/data_records_1D.csv",
                 filelength=get_detailed_request("LAST_1_DAY"))