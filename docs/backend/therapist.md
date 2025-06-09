# Extract Patient Activity Data

## Project Description

This project provides a Python script to extract patient activity data (steps, PAM score, and activity zone) from a MySQL database. The extracted data can be used for analysis and is exported into a CSV file for easy usage and reporting.

The script is designed for therapists who need to retrieve patient activity over a specific time period.

---

## Technologies Used

* Python 3.6+
* MySQL Database
* mysql-connector-python for database connection
* CSV file export

---

## How to use it 

1 **Clone the repository**

2. **Install the required Python packages**

   ```bash
   pip install mysql-connector-python
   ```

3. **Set up the MySQL Database**

   * Ensure a MySQL database is running.
   * Update the database connection parameters in extract_patient_data.py if needed:

     ```python
     host = "localhost"
     user = "root"
     password = "superstronkrootpw"
     database = "hipperdb"
     ```
---

4. **Configure the extraction parameters**:

   * `patient_id`
   * `start_date`
   * `end_date`

   Example inside the script:

   ```python
   patient_id = 1
   start_date = "2025-06-01"
   end_date = "2025-06-10"
   ```

5. **Run the script**

   ```bash
   python extract_patient_data.py
   ```

6. **Retrieve the output**

   * The extracted data will be available in the generated `results.csv` file.

---

## Features

* Extracts patient activity data: date, steps, PAM score, and zone.
* Allows selection of the time window for data extraction.
* Automatically exports the extracted data to a CSV file.
* Handles UTF-8 characters correctly for international data.

---

## Constraints

* If no time window is specified, the extraction should default to the last 7 days.
* The exported data must be structured and exportable in a machine-readable format

---

## Anomaly Detection Feature

This project also provides an anomaly detection feature to identify significant deviations in patient activity. Therapists can detect sudden drops in activity that may require intervention.

* The system calculates the median of daily steps over a specified time window.
* It flags any day where the activity is more than 20% below the median.
* Results are available via API and a simple web form.

---

## How to Use the API

1. **Start the Flask API**

   ```bash
   python -m flask run --port=6001
   ```

2. **Send a POST request to the endpoint**

   **URL**: `http://localhost:6001/api/detect-anomalies`

   **Request Body** (JSON):

   ```json
   {
     "patient_id": 1,
     "start_date": "2025-06-01",
     "end_date": "2025-06-10",
     "threshold_percent": 20
   }
   ```

3. **Response**

   ```json
   {
     "median_steps": 3150.0,
     "threshold_percent": 20,
     "anomalies": [
       {
         "date": "2025-06-02",
         "steps": 145,
         "deviation_percent": 95.4
       }
     ]
   }
   ```

---

## How to Use the Web Form

1. **Access the form**

   ```
   http://localhost:6001/anomaly-form
   ```

2. **Fill the form fields**

   * Patient ID
   * Start Date
   * End Date
   * Threshold Percent

3. **Submit the form to detect anomalies.** 

   Results will be displayed directly on the page.

---

## Requirements

To install the necessary Python packages, run:

```bash
pip install -r requirements.txt
```

**Content of `requirements.txt`:**

```
Flask>=2.0.0
mysql-connector-python>=8.0.0
python-dotenv>=0.21.0
```

---

## Future Improvements

Support for detecting extended inactivity periods.

Pattern change detection (e.g., activity shifts from morning to evening).

Configurable thresholds per patient.

Detection of consecutive days with low activity (e.g., steps < 100).

Identification of daily habit pattern shifts based on active hours.

Calculation of 7-day moving average trends.

Computation of a trend score based on activity fluctuations.

Measurement of daily activity variability using standard deviation.

Detection of prolonged low-activity streaks (2+ consecutive days).

Calculation of daily inactivity duration (requires hourly data).

Computation of the percentage of goal achievement days.

Prediction of activity drops using simple machine learning models (e.g., linear regression).

Clustering of patients based on behavior similarity (e.g., k-means clustering).

# **Real-time Activity Monitoring**

This project provides a real-time monitoring feature that automatically detects significant deviations in patient activity as soon as new data is available.

### How It Works

* The system continuously monitors the database for new activity entries every 5 seconds.
* It calculates the rolling median of daily steps for each patient.
* If the new activity is more than 30% below the median, it triggers an anomaly alert.
* Alerts are displayed directly in the system console.

### Features

* Real-time anomaly detection (within 5 seconds of new data).
* Median calculation for deviation detection.
* Configurable global threshold (default: 30%).
* Scalable monitoring for multiple patients simultaneously.

### How to Run the Real-time Monitoring

1. **Ensure your database is running and populated with activity data**

2. **Launch the monitoring script**

   ```bash
   python realtime_alert.py
   ```

3. **Monitor the console for alerts**

   Example of a detected anomaly:

   ```
   [ALERT] Patient 1: 2025-06-08 | Baseline: 2800, Steps: 1000 (Deviation: -64.29%)
   ```

### Requirements

```bash
pip install -r requirements.txt
```

Additional requirements for real-time monitoring:

```
python-dotenv>=0.21.0
```

---

# **Limitations & Future Work**

## Limitations

* Currently, the system uses a global threshold for anomaly detection (e.g., 30% for all patients).
* Notifications are delivered via system console only (no email or dashboard yet).

## Future Work

* **Per-patient threshold configuration**: Allow therapists to define custom thresholds for each patient.
* **Email Notifications**: Send automatic email alerts to therapists for detected anomalies.
* **Web Dashboard**: Display alerts in a real-time dashboard for a better clinical overview.
* **Advanced anomaly types**: Detect prolonged inactivity, pattern shifts, and activity variability.
* **Machine Learning**: Predict potential drops in activity based on historical trends.
