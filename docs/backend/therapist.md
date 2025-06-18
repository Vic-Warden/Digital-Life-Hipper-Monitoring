# Extract Patient Activity Data

## Description

This first part of the documentation provides a Python script to extract patient activity data from a MySQL database. The extracted data can be used for analysis and is exported to a file for ease of use and reporting.

The script is designed for therapists who need to extract patient activity over a specific period of time.

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

   * Ensure MySQL database is running
   * Update the database connection parameters in extract_patient_data.py if needed :

     ```python
     host = "localhost"
     user = "root"
     password = "superstronkrootpw"
     database = "hipperdb"
     ```
---

4. **Configure the extraction parameters :**

   * `patient_id`
   * `start_date`
   * `end_date`

   Example inside the script :

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

   * The extracted data will be available in the generated `results.csv` file

---

## Features

* Extracts patient activity data : date, steps, PAM score, and zone
* Allows selection of the time window for data extraction
* Automatically exports the extracted data to a CSV file

---

# Anomaly Detection Feature

The second part of this documentation provides an anomaly detection feature to identify deviations in patient activity. Therapists can detect sudden drops in activity that may require intervention

* The system calculates the median of daily steps over a specified time window
* It flags any day where the activity is below than 20% the median
* Results are available via API and a simple web form

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

- If a patient doesn't move at all during an extended inactivity periods

- Maybe we can try to use some pattern change detection, maybe split the day like morning / evening and try to make it configurable about that

- Two patients can and are very different, we could be able to configure thresholds per patient

- We should implement a consecutive days, for exemple if a patient travel by plane he'll just stay sit down during a long period and it will not be necessary to send a notification for that so implement a detection of prolonged low-activity streaks like more 2 days in a row it can be usefull

- We should try to implement a machine learning who can learn from the patient about his habit

- For the different calculations we should see from a 7 periods of day & on activity fluctuations

- We could implement a pourcentage of goal achivements days it can be a motivation's source for the patient

---

# **Real-time Activity Monitoring**

The third part of the documentation provides a real-time monitoring feature that automatically detects significant deviations in patient activity

### How It Works

* The system continuously monitors the database for new activity entries every 5 seconds
* It calculates the rolling median of daily steps for each patient
* If the new activity is below than 20% the median, it triggers an anomaly alert
* Alerts are displayed directly in the system console for now

### Features

* Real-time anomaly detection (within 5 seconds of new data)
* Median calculation for deviation detection
* Configurable global threshold (default: 20%)
* Scalable monitoring for multiple patients simultaneously

## How to Run the Real-time Monitoring

1. **Ensure your database is running**

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

* Currently, the system uses a global threshold for anomaly detection (20% for all patients)
* Notifications are delivered via system console only (no email or dashboard yet)

## Future Work

* **Per-patient threshold configuration**: Allow therapists to define custom thresholds for each patient
* **Email Notifications**: Send automatic email alerts to therapists for detected anomalies
* **Web Dashboard**: Display alerts in a real-time dashboard for a better clinical overview
* **Advanced anomaly types**: Detect prolonged inactivity, pattern shifts, and activity variability
* **Machine Learning**: Predict potential drops in activity based on historical trends

# **Machine Learning**

Prediction of short-term decline in activity

**Objective :** predict whether a patient's activity will decline in the next 3 days

**Utility :** proactive prevention, alerts to therapists

**Model :** binary classification

**Data :** step history, WFP, activity zones

**Deployment :** in the API or via weekly batch

---

Behavioural profiling of patients (clustering)

**Objective :** segment patients according to their level and regularity of activity.

**Benefits :** personalisation of care plans, population analysis.

**Model :** K-Means, DBSCAN

**Data :** average daily steps, zone ratios, average MAP

**Visualisation :** ‘patient mapping’ type dashboard

---

Detection of Changes in Routine

**Objective :** detect lasting changes in activity patterns (switching from morning to evening)

**Utility :** longitudinal monitoring, identification of critical periods

**Method :** changepoint detection, HMM, time series

**Display :** chronology of changes

---

Activity Pattern Recognition by Deep Learning

**Objective :** automatically identify patterns (walking, resting, brief efforts)

**Utility :** advanced typology of days

**Model :** CNN or LSTM on fine time series

**Data :** raw acceleration vectors or series of steps/zone per hour

**Complexity :** high level (need for volume and labels)

---

## Routine Change Detection

This feature identifies when a patient breaks their usual daily rhythm 

- Detects most active hours during the past 7 days
- Flags inactivity at usual active hours over 3+ consecutive days
- Provides both an API and a simple web interface

### Web Form

- URL: `/routine-form`
- Input: Patient ID
- Output:
  - Patient details
  - Usual activity slots
  - Period of analysis
  - List of detected disruptions

### Flask Endpoints

- `POST /routine-form`: returns usual activity hours + detected disruptions
- `GET /routine-form`: shows a web form


- `get_usual_active_slots`: aggregates steps per hour over the past 7 days to find activity routine
- `get_disruptions`: checks inactivity during usual active hours over last 3 days
