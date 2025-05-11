from services import *

ActivityDownload(filename="output/data_records.csv",
                 filelength=get_detailed_request("LAST_1_HOUR"))
