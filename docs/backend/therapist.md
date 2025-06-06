# Extract Patient Activity Data

## Project Description

This project provides a Python script to extract patient activity data (steps, PAM score, and activity zone) from a MySQL database. The extracted data can be used for analysis and is exported into a CSV file for easy usage and reporting.

The script is designed for therapists who need to retrieve patient activity over a specific time period.

---

## Technologies Used

* Python 3.6+
* MySQL Database
* `mysql-connector-python` for database connection
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
   * Update the database connection parameters in `extract_patient_data.py` if needed:

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

5. **Run the script**:

   ```bash
   python extract_patient_data.py
   ```

6. **Retrieve the output**:

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