import statistics
import json

def calculate_median(steps_list):
    """Calculates the median of a list of step counts.

    Args:
        steps_list : A list of integers or floats representing step counts.

    Returns:
        float: The median value of the list. Returns 0 if the list is empty.
    """
    
    if not steps_list:
        return 0
    
    return statistics.median(steps_list)

def detect_anomalies(data, median, threshold_percent=20):
    """Detects anomalies in step data based on a threshold percentage below the median.

    An anomaly is defined as a step count lower than (1 - threshold_percent / 100) * median.

    Args:
        data (list): containes 'date' and 'steps'.
        median (float): The median number of steps.
        threshold_percent (float, optional): The threshold percentage to detect anomalies. Defaults to 20.

    Returns:
        list: A list of anomaly dictionaries with 'date', 'steps', and 'deviation_percent'.
    """
    
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
    """Exports the median and anomalies to a JSON file.

    Dates are converted to string format (YYYY-MM-DD) before writing.

    Args:
        median (float): The calculated median steps value.
        anomalies (list): List of anomalies detected.
        threshold_percent (float): The threshold percentage used for anomaly detection.

    Outputs:
        File anomalies.json containing the median, threshold, and list of anomalies.
    """
    
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