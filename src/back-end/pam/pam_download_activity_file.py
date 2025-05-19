from services import *

ActivityDownload(filename="output/data_records_1D_90245.csv",
                 filelength=get_detailed_request("LAST_1_DAY"),
                 label_id=90245)