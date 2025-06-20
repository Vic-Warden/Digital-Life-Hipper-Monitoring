import csv
import json
import requests
from datetime import datetime

def minute_csv_to_json(filepath: str, label_id: str) -> list:
    """
    Converts a CSV file to a list of dicts formatted for the /upload-minute-data API.
    Adds zone and data_label fields.
    """
    data = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                data.append({
                    "timestamp": datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S").isoformat(),
                    "steps": int(row["Steps"]),
                    "pam_score": float(row["PAM Score"]),
                    "data_label": label_id
                })
            except Exception as e:
                print(f"Skipping row due to error: {e} — row: {row}")
    return data