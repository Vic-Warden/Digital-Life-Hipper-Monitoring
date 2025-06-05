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



