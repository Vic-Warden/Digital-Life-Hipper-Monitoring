from services import *

ActivityDownload(filename="output/data_records_15M.csv",
                 filelength=get_detailed_request("LAST_15_MIN"))
