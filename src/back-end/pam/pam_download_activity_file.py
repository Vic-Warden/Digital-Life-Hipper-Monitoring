from services import *

ActivityDownload(filename="output/data_records_1H.csv",
                 filelength=get_detailed_request("LAST_30_MIN"))
