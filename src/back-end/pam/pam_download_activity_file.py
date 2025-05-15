from services import *

# ActivityDownload(filename="output/data_records_30M.csv",
#                  filelength=get_detailed_request("LAST_30_MIN"))

ActivityDownload(filename="output/data_records_1H.csv",
                 filelength=get_detailed_request("LAST_1_HOUR"))

ActivityDownload(filename="output/data_records_6H.csv",
                 filelength=get_detailed_request("LAST_6_HOURS"))

ActivityDownload(filename="output/data_records_1D.csv",
                 filelength=get_detailed_request("LAST_1_DAY"))

ActivityDownload(filename="output/data_records_3D.csv",
                 filelength=get_detailed_request("LAST_3_DAYS"))

ActivityDownload(filename="output/data_records_MAX.csv",
                 filelength=get_detailed_request("MAX"))