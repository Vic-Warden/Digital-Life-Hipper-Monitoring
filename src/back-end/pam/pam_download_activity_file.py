from services import *

ActivityDownload(filename="output/data_records_3H.csv",
                 filelength=get_detailed_request("LAST_3_HOURS"))