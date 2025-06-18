# Database backend

`database.py` contains the code responsible for communicating with the `MySQL/MariaDB` database. 

Under the hood it uses the `mysql.connector` library, which provides simple but effective functions for communicating with a database.

`database.py` contains the following functions:

```python
__init__()              # Initializes connection and configuration
connect()               # Establishes the MySQL connection
do_query()              # Executes parameterized queries on the database
check_valid_table()     # Checks if a table name is allowed to be queried
check_email()           # Checks if an email is already registered
check_credentials()     # Verifies email and password combination
add_patient()           # Registers a new patient in the system
remove_patient()        # Removes a patient based on their email
create_cookie()         # Creates a new login cookie for a user
verify_cookie()         # Verifies a cookie's validity and retrieves the associated user
remove_cookie()         # Deletes a cookie from the database
change_user_email()     # Changes the users email based on session token
get_log_for_mac()       # Get the last time data was pulled from a specific sensor, by looking at the mac address
update_log_timestamps() # Update the last time data was pulled from a specific sensor, by looking at the mac address
therapist_id_from_cookie() # Retrieves the therapist's ID associated with a given session cookie.
connect_patient_to_therapist() # Creates an association between a patient and a therapist in the database.
```

### How to execute queries

Queries can be executed using the `do_query()` function. In order to make a query and execute it the user should follow the following example.

```python
db = Database(
    host="host",
    port=port,
    user="user",
    password="password",
    database="database"
)

query = "SELECT * FROM users WHERE name = %s"
params = ("some_value",)
results = db.do_query(query, params)
```

The result from this action look like this:
```python
list[tuple] | None
```

* A list of tuples containing the result set.
* None if the query fails or if there is no connection to the database.

### Data integrity and security

In order to make sure that the integrity and security of the database is enforced, multiple best practices have been applied to the code.

**Uses parameterized queries**
```python
cursor.execute(query, params)
```

* This prevents SQL injection, ensuring that values in params are properly escaped and interpreted as data, not SQL commands.
* Supports integrity by preventing malformed or malicious queries that could harm your data.

**Query execution is wrapped in a try/except/finally block**

```python
try:
    ...
except Error as e:
    ...
finally:
    cursor.close()
```

* Prevents unhandled exceptions from leaving the connection or cursor in an undefined state.
* Helps maintain transactional safety in multi-query operations.

**Connection health check**

```python
if not self._connection:
    print("No connection to the database.")
    return None
```

* Prevents trying to query a disconnected or invalid database, which avoids corruption or inconsistent reads/writes.

### Cookie Management

The class integrates a Cookie handler from a separate module to manage login sessions.

```python
self.cookie = Cookie()
```

**Cookie Functions**

`create_cookie(email: str):` Creates and stores a cookie for a given email.

`verify_cookie(cookie: str):` Validates a cookie and returns associated user info.

`remove_cookie(cookie: str):` Deletes the cookie from the database.

These functions enable session handling for users while maintaining secure authentication flows.

### Account Management

**Account Functions**

`change_user_email(token: str, new_email: str):` Changes the users email based on the session token.


### Patient Data Access

`get_patient_details(patient_id: int) -> dict | None`

Gets a full summary of a patient’s:

- PAM data records (`data` table)
- Linked devices (`device` table)
- Personal goals (`goal` table)

Returns `None` if no information is found.

`get_patients(therapeut_id: int) -> list[dict] | None`

Returns a list of patients linked to a therapist:

```python
[
  { "id": 1, "name": "John Doe", "email": "john@example.com" },
  ...
]
```

### Get last update period

`get_last_update_period(self, device_mac_addr: str)`

Gets the last time at which the data was updated.

```python
query = "SELECT last_update_period FROM Device WHERE device_mac_addr = %s;"
params = (device_mac_addr,)
result = self.do_query(query, params, fetch=True)

if result and len(result) > 0:
    return result[0][0]
return None
```

### Set last update period

`set_last_update_period(self, device_mac_addr: str) -> bool`

Sets the last dat aupdate time to the current time

```python
# Get current time
now = datetime.now()

# Format as MySQL-compatible DATETIME string
current_time = now.strftime('%Y-%m-%d %H:%M:%S')

# Update the last_update_period for the device
query = "UPDATE Device SET last_update_period = %s WHERE device_mac_addr = %s;"
params = (current_time, device_mac_addr)
result = self.do_query(query, params, fetch=False)

return result is not None and len(result[0][0]) > 0
```

### API Token Authentication

Verifies the authentication token and return the associated email if valid.

`verify_auth_token(self, token: str) -> tuple[bool, str]`

```python
def verify_auth_token(self, token: str) -> tuple[bool, str]:
    """
    ### Verify the authentication token and return the associated email if valid.

    Returns a tuple (True, email) if the token is valid,
    or (False, "Invalid token") if it is not.
    """
    query = "SELECT patient_id_device FROM Device WHERE auth_token = %s;"
    params = (token,)
    result = self.do_query(query, params, fetch=True)

    if result and len(result[0]) > 0:
        return (True, result[0][0])
    return (False, "Invalid token")
```

### Getting and setting time for sensor data
2 functions are used to interact with the backend database for reading and updating log timestamps for each device, based on its MAC address.

#### get_log_for_mac(mac_address)
This function retrieves the last time activity and day data were pulled for a specific device from the database.
Parameters
    mac_address (str): The MAC address of the device.

Returns
    A dictionary with the following keys:

        "last_activity_pull": The last time activity data was pulled, in ISO 8601 format.

        "last_day_data_pull": The last time day data was pulled, in ISO 8601 format.

    If the device is not found in the database, it returns None.

Example Output
```json
{
  "last_activity_pull": "2025-06-12T09:45:00",
  "last_day_data_pull": "2025-06-11"
}
```

#### update_log_timestamps(mac_address, update_activity, update_day_data=False)

This function updates the database with the current timestamp for a given device, showing the most recent time that data was pulled.
Parameters
    mac_address (str): The MAC address of the device to update.

    update_activity (bool): Whether to update the activity data timestamp.

    update_day_data (bool) (optional): Whether to update the day data timestamp. Default is False.

Behavior
    If either flag (update_activity or update_day_data) is set to True, it will update the corresponding timestamp in the database using the current time in the Europe/Amsterdam time zone.

    If no flags are set, the function returns False and does nothing.

Returns
    True if the update was successful.

    False if no update was performed.

### Get device id from patient id

This function is provided to get the device_id (base station device id) associated with a patient.

```python
def device_id_from_patient_id(self, patient_id: int) -> int:
    """
    Get the device ID associated with a patient ID.
    Returns the device ID or None if not found.
    """
    query = "SELECT device_id FROM Device WHERE patient_id_device = %s;"
    params = (patient_id,)
    result = self.do_query(query, params, fetch=True)

    if result and len(result) > 0:
        return result[0][0]
    return None
```

### Upload minute data

Uploads minute data to the database using the patient_id.

```python
def upload_minute_data(self, patient_id: int, minute_data: list):
    """
    Upload PAM data for a patient.
    Expects pam_data to be a list of dictionaries with keys:
    - 'timestamp'
    - 'steps'
    - 'pam_score'
    - 'zone'
    - 'data_label'
    """
    device_id = self.device_id_from_patient_id(patient_id)

    if not pam_data:
        return False

    query = """
        INSERT INTO Data (device_id, timestamp, steps, PAM_score, zone, data_label)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    params = [
        (device_id, data['timestamp'], data['steps'],
        data['pam_score'], data['zone'], data['data_label'])
        for data in minute_data
    ]

    try:
        cursor = self._connection.cursor()
        cursor.executemany(query, params)
        self._connection.commit()
        return True
    except Error as e:
        print("Error while uploading PAM data:", e)
        return False
    finally:
        cursor.close()
```

### Upload day data

Uploads day data to the database using patient_id.

```python
def upload_day_data(self, patient_id: int, day_data: list):
    """
    Upload daily PAM data for a patient.
    Expects day_data to be a list of dictionaries with keys:
    - 'timestamp'
    - 'steps'
    - 'pam_score' 
    """
    device_id = self.device_id_from_patient_id(patient_id)

    if not day_data:
        return False

    query = """
        INSERT INTO Data (device_id, timestamp, steps, PAM_score)
        VALUES (%s, %s, %s, %s);
    """
    params = [
        (device_id, data['timestamp'], data['steps'],
            data['pam_score'])
        for data in day_data
    ]

    try:
        cursor = self._connection.cursor()
        cursor.executemany(query, params)
        self._connection.commit()
        return True
    except Error as e:
        print("Error while uploading daily PAM data:", e)
        return False
    finally:
        cursor.close()
```

### therapist_id_from_cookie

This function retrieves the therapist's ID associated with a given session cookie.

```python
    def therapist_id_from_cookie(self, cookie: str) -> int | bool:
        """
        
        """
        try:
            insert_query = """
            SELECT fk_therapist_id FROM User WHERE cookies = %s;
            """
            params = (cookie,)
            result = self.do_query(insert_query, params)
            return result[0][0]

        except Exception as e:
            print(f"Error inserting patient: {e}")
        return False
```

### connect_patient_to_therapist

This function creates an association between a patient and a therapist in the database.

```python
    def connect_patient_to_therapist(self, patient_id: int, therapist_id: int):
        """
        text
        """
        query = """
            INSERT INTO Patient_has_Therapist VALUES (%s, %s);
        """
        params = (patient_id, therapist_id)
        self.do_query(query, params, fetch=False)
```

### Data averages for historical graph

```python
    def calculate_average_data(self, data):
        # Create a DataFrame taken from db `Data` structure
        df = pd.DataFrame(data, columns=['id', 'device_id', 'timestamp', 'steps', 'PAM_score', 'zone', 'data_label'])

        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('Europe/Amsterdam')

        # Set timestamp as index
        df.set_index('timestamp', inplace=True)

        # Resample and calculate means
        hourly_avg = df.resample('h')[['steps', 'PAM_score']].mean()
        daily_avg = df.resample('D')[['steps', 'PAM_score']].mean()
        weekly_avg = df.resample('W')[['steps', 'PAM_score']].mean()
        monthly_avg = df.resample('ME')[['steps', 'PAM_score']].mean()

        return {
            'hourly': hourly_avg.reset_index().to_dict(orient='records'),
            'daily': daily_avg.reset_index().to_dict(orient='records'),
            'weekly': weekly_avg.reset_index().to_dict(orient='records'),
            'monthly': monthly_avg.reset_index().to_dict(orient='records')
        } 
```

The function seen above processes activity data and calculates average steps and PAM_score over different time intervals: hourly, daily, weekly, and monthly.

Parameters:
* data: list of records containing id, device_id, timestamp, steps, PAM_score, zone, and data_label.

Returns:
* A dictionary with keys: 'hourly', 'daily', 'weekly', 'monthly'.
Each contains a list of records with average steps and PAM_score for the corresponding time period.

Key Steps:
> Converts data to a DataFrame.

> Parses timestamps and sets as index.

> Resamples data by time intervals.

> Computes mean values and formats results as dictionaries.

### Get user preferences

Returns the user preferences such as dark_mode, large_font, and language, by using the cookie (active session) of the player.

```python
    def get_user_preferences(self, cookie: str) -> dict:
        query = "SELECT dark_mode, large_font, language FROM User WHERE cookies = %s;"
        params = (cookie,)
        result = self.do_query(query, params, fetch=True)

        if result and len(result) > 0:
            return_dict = {
                "dark_mode": result[0][0],
                "large_font": result[0][1],
                "language": result[0][2]
            }
            return return_dict
        return {}
```

### Set user preferences

Sets the user preferences using the cookie (active session) of the player.

```python
def set_user_preferences(self, cookie: str, dark_mode: bool, large_font: bool, language: str) -> bool:
    query = """
        UPDATE User
        SET dark_mode = %s, large_font = %s, language = %s
        WHERE cookies = %s;
    """
    params = (dark_mode, large_font, language, cookie)
    result = self.do_query(query, params, fetch=False)

    return result is not None
```