from services import *

TimeDate()

SetTimestamp2101(label_id=90248)

ActivityDownload(filename="output/data_records_1D_90248.csv",
                 filelength=get_detailed_request("LAST_1_DAY"),
                 label_id=90248)