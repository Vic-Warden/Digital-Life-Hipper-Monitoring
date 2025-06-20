import csv
import json
import requests
from datetime import datetime

def day_csv_to_json(filepath: str, label_id: str) -> list:
    """
    Converts a CSV file to a list of dicts formatted for the /upload-day-data API.
    Fields:
      - timestamp (from Date)
      - steps
      - pam_score (from Activity Score)
      - zone_1 (from Zone 1 (Living))
      - zone_2 (from Zone 2 (Health))
      - zone_3 (from Zone 3 (Sport))
      - data_label
    """
    data = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                data.append({
                    "timestamp": datetime.strptime(row["Date"], "%Y-%m-%d").isoformat(),
                    "steps": int(row["Steps"]),
                    "pam_score": float(row["Activity Score"]),
                    "zone_1": int(row["Zone 1 (Living)"]),
                    "zone_2": int(row["Zone 2 (Health)"]),
                    "zone_3": int(row["Zone 3 (Sport)"]),
                    "data_label": label_id
                })
            except Exception as e:
                print(f"⚠️ Skipping row due to error: {e} — row: {row}")
    return data
