import statistics
import json

def calculate_median(steps_list):
    
    if not steps_list:
        return 0
    
    return statistics.median(steps_list)

def detect_anomalies(data, median, threshold_percent=20):
    
    anomalies = []
    threshold_value = median * (1 - threshold_percent / 100)

    for entry in data:
        if entry['steps'] < threshold_value:
            deviation_percent = round((1 - (entry['steps'] / median)) * 100, 2)
            anomalies.append({
                'date': entry['date'],
                'steps': entry['steps'],
                'deviation_percent': deviation_percent
            })
    return anomalies

def export_to_json(median, anomalies, threshold_percent):
    # Convert date object to string for JSON
    for anomaly in anomalies:
        if isinstance(anomaly['date'], (str,)):
            continue  
        anomaly['date'] = anomaly['date'].strftime('%Y-%m-%d')

    output = {
        "median_steps": median,
        "threshold_percent": threshold_percent,
        "anomalies": anomalies
    }

    with open('anomalies.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)