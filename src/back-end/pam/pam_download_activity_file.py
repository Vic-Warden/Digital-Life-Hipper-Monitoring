from services import *

ActivityDownload(filename="output/data_records_MAX.csv",
                 filelength=get_detailed_request("MAX"))
