import os  # Import os for .env centralized settings
import pandas as pd
import mysql.connector
from mysql.connector import Error  # Error handling module
from mysql.connector import MySQLConnection  # MySQL connection type
from flask import Flask, jsonify, request  # Flask
from crypto import Cookie
from datetime import datetime
from zoneinfo import ZoneInfo


class Database:
    def __init__(self, host, port, user, password, database):
        # Initialize the database connection parameters
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self._connection = self.connect()
        self._allowed_tables = [
            "Data",
            "Device",
            "Goal",
            "User",
            "Patient_has_Therapist",
            "Therapist"
        ]
        self.cookie = Cookie()  # Initialize the Cookie class for cookie management

    def connect(self) -> MySQLConnection | None:
        # Establish a connection to the MySQL database
        try:
            connection = mysql.connector.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            # Check if the connection was successful
            # and print some server information
            if connection.is_connected():
                # Get the server information
                db_info = connection.server_info
                print("Connected to MySQL Server version", db_info)
                # Get the database name
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                # Fetch the database name
                record = cursor.fetchone()
                print("Connected to database:", record[0])

            return connection
        # Handle any errors that occur during the connection attempt
        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None

    def do_query(self, query: str, params: tuple = (), fetch=True) -> list[tuple] | None:
        """
        ### Execute a query on the database and return the result.

        ### How to use:
        ```python
        query = "SELECT * FROM users WHERE name = %s"
        params = ("some_value",)
        results = do_query(query, params)
        ```

        ### Returns:
        - A list of tuples containing the result set.
        - None if the query fails or if there is no connection to the database.
        """
        # Check if the connection is established
        if not self._connection:
            print("No connection to the database.")
            return None
        # Execute the query and fetch the results
        try:
            self._connection.autocommit = True
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                return result
            return [("Query executed successfully",)]
        # Handle any errors that occur during the query execution
        except Error as e:
            print("Error while executing query:", e)
            return None
        # At the end, close the cursor
        finally:
            cursor.close()

    def check_valid_table(self, table_name: str) -> bool:
        """
        ### Check if the table is allowed to be queried.

        Returns True if the table is in the allowed list, False otherwise.
        """
        return table_name in self._allowed_tables

    def check_email(self, email: str) -> bool:
        """
        ### Check if the email is already registered in the database.

        Returns True if the email exists, False otherwise.
        """
        query = "SELECT COUNT(*) FROM User WHERE email = %s"
        params = (email,)
        result = self.do_query(query, params)
        if result and 0 < result[0][0] < 2:
            return True
        return False

    def check_credentials(self, email: str, password: str) -> bool:
        """
        ### Check if the email and password match a registered user.

        Returns True if the credentials are valid, False otherwise.
        """
        query = "SELECT COUNT(*) FROM User WHERE email = %s AND password = %s"
        params = (email, password)
        result = self.do_query(query, params)
        if result and result[0][0] == 1:
            return True
        return False

    def add_patient(self, name: str, email: str, password: str, cookie: str) -> bool:
        """
        add a new patient linked to a therapist.

        Returns True if successful, False otherwise.
        """
        # Get therapist id
        therapist_id = self.therapist_id_from_cookie(cookie)
        if not therapist_id:
            return False
        try:
            # Insert user into db
            insert_query = """
                INSERT INTO User (name, email, password, cookies, is_therapist, fk_therapist_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """
            params = (name, email, password, '', 0,
                      therapist_id)  # '' for empty cookie, 0 for no therapist
            patient_id = self.do_query(insert_query, params)[0][0]

            # Add patient id to Patient_has_Therapist table
            self.connect_patient_to_therapist(patient_id, therapist_id)

            return True

        except Exception as e:
            print(f"Error inserting patient: {e}")
        return False

    def connect_patient_to_therapist(self, patient_id: int, therapist_id: int):
        """
        text
        """
        query = """
            INSERT INTO Patient_has_Therapist VALUES (%s, %s);
        """
        params = (patient_id, therapist_id)
        self.do_query(query, params, fetch=False)

    def remove_patient(self, email: str) -> tuple[bool, str]:
        """
        ### Remove a patient from the database by email.

        Returns:
        - A tuple (True, "") if the patient was removed successfully.
        - A tuple (False, "Patient not found.") if the patient does not exist.
        """
        query = "DELETE FROM User WHERE email = %s;"
        params = (email,)
        result = self.do_query(query, params)
        if result is not None and result[0][0] > 0:
            return (True, "")
        return (False, "Patient not found.")

    def create_cookie(self, email: str) -> tuple[bool, str]:
        """
        ### Create a cookie for the user based on their email.

        Returns a string representing the cookie.
        """
        # Create a cookie
        success, cookie = self.cookie.create_cookie(email)
        if not success:
            return (False, "Failed to create cookie.")

        # Update the database with the new cookie
        query = "UPDATE User SET `cookies` = %s WHERE `email` = %s;"
        params = (cookie, email)
        result = self.do_query(query, params, fetch=False)

        # Check if the cookie was successfully inserted into the database
        if result is not None and len(result[0][0]) > 0:
            return (True, cookie)
        return (False, "Failed to insert cookie into database.")

    def verify_cookie(self, cookie: str) -> tuple[bool, str]:
        """
        ### Verify a cookie and return the associated email if valid.

        Returns a tuple (True, email) if the cookie is valid,
        or (False, "Invalid cookie") if it is not.
        """
        success, value = self.cookie.verify_cookie(cookie)
        if not success and value == "Expired cookie":
            self.remove_cookie(cookie)

        query = "SELECT name, email FROM User WHERE cookies = %s;"
        params = (cookie,)
        result = self.do_query(query, params, fetch=True)

        if result and len(result[0][0]) > 0:
            return (True, result[0])
        return (False, "Cookie not found in database.")

    def remove_cookie(self, cookie: str) -> tuple[bool, str]:
        """
        ### Remove the cookie associated with the given email.

        Returns a tuple (True, "") if the cookie was removed successfully,
        or (False, "Failed to remove cookie") if it was not.
        """
        query = "UPDATE User SET cookies = NULL WHERE cookies = %s;"
        params = (cookie,)
        result = self.do_query(query, params, fetch=False)

        if result is not None and len(result[0][0]) > 0:
            return (True, "")
        return (False, "Failed to remove cookie.")

    def change_user_email(self, token: str, new_email: str) -> tuple[bool, str]:
        """
        ### Change the email of a user based on their token.

        Returns a tuple (True, "") if the email was changed successfully,
        or (False, "Failed to change email") if it was not.
        """
        query = "UPDATE User SET email = %s WHERE cookies = %s;"
        params = (new_email, token)
        result = self.do_query(query, params, fetch=False)

        if result is not None and len(result[0][0]) > 0:
            return (True, "")
        return (False, "Failed to change email.")

    def get_patient_details(self, patient_id: int) -> dict | None:
        """
        ### Get details of a patient by their ID.
        Returns a dictionary containing patient details or None if not found.
        """

        # --- Get patient details ---
        query_patient = """
            SELECT
                id AS patient_id,
                name,
                email
            FROM User
            WHERE id = %s;
        """
        patient_details = self.do_query(
            query_patient, (patient_id,), fetch=True)

        # --- Get all data records for this patient ---
        query_data = """
            SELECT
                Data.id AS data_id,
                Data.device_id,
                Data.timestamp,
                Data.steps,
                Data.PAM_score,
                Data.zone,
                Data.data_label
            FROM Data
            INNER JOIN Device ON Data.device_id = Device.id
            WHERE Device.patient_id_device = %s;
        """
        data = self.do_query(query_data, (patient_id,), fetch=True)

        # --- Get all devices for this patient ---
        query_device = """
            SELECT
                id,
                patient_id_device AS patient_id,
                device_label,
                device_id AS external_device_id
            FROM Device
            WHERE patient_id_device = %s;
        """
        devices = self.do_query(query_device, (patient_id,), fetch=True)

        # --- Get all goals for this patient ---
        query_goal = """
            SELECT
                id AS goal_id,
                patient_id_goal,
                patient_goal,
                type AS goal_type,
                reached
            FROM Goal
            WHERE patient_id_goal = %s;
        """
        goals = self.do_query(query_goal, (patient_id,), fetch=True)

        if not data and not devices and not goals:
            return None

        return {
            "patient_details": patient_details,
            "data": data,
            "devices": devices,
            "goals": goals
        }

    def get_patients(self, therapeut_id: int) -> list[dict] | None:
        """
        ### Get a list of patients associated with a therapist.

        Returns a list of dictionaries containing patient details.
        """
        query = """
            SELECT p.id, p.name, p.email
            FROM User AS p
            JOIN Patient_has_Therapist AS pt ON p.id = pt.patient_id
            WHERE pt.therapist_id = %s;
        """
        # TODO: Get terapist id from cookie
        params = (therapeut_id,)
        result = self.do_query(query, params, fetch=True)

        if result:
            return [{"id": row[0], "name": row[1], "email": row[2]} for row in result]
        return None

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

    def get_log_for_mac(self, mac_address):
        query = "SELECT last_activity_pull, last_day_data_pull FROM Device WHERE device_mac_addr=%s"
        params = (mac_address,)
        result = self.do_query(query, params, fetch=True)
        if result and len(result) > 0:
            row = result[0]
            return {
                "last_activity_pull": row[0].isoformat() if row[0] else None,
                "last_day_data_pull": row[1].isoformat() if row[1] else None,
            }
        return None

    def update_log_timestamps(self, mac_address, update_activity, update_day_data=False):
        now = datetime.now(ZoneInfo("Europe/Amsterdam")).replace(tzinfo=None)
        updates = []
        params = []

        if update_activity:
            updates.append("last_activity_pull = %s")
            params.append(now)

        if update_day_data:
            updates.append("last_day_data_pull = %s")
            params.append(now)

        if not updates:
            return False  # Nothing to update

        params.append(mac_address)

        query = f"""
            UPDATE Device
            SET {', '.join(updates)}
            WHERE device_mac_addr = %s
        """
        return self.do_query(query, tuple(params), fetch=False) is not None

    def get_usual_active_slots(self, patient_id: int, days: int = 7) -> list[dict]:
        """
        Retrieves the time slots (by hour) when the patient is usually active
        """

        from datetime import datetime, timedelta

        start_date = datetime(2025, 6, 1).date()
        end_date = datetime(2025, 6, 12).date()

        query = """
            SELECT HOUR(timestamp) AS hour_slot, SUM(steps) AS total_steps
            FROM Data
            INNER JOIN Device ON Data.device_id = Device.id
            WHERE Device.patient_id_device = %s
            AND timestamp BETWEEN %s AND %s
            GROUP BY hour_slot
            ORDER BY hour_slot;
        """

        result = self.do_query(query, (patient_id, start_date, end_date))

        if not result:
            print("→ patient_id:", patient_id)
            print("→ start_date:", start_date)
            print("→ end_date:", end_date)
            return []

        print("SQL Result (usual slots):", result)

        return [{"hour_slot": row[0], "total_steps": row[1]} for row in result]
    def is_super_user(self, cookie: int) -> bool:
        """
        ### Check whether the given user is a super‑user.

        Returns True if `is_super_user` = 1, False if 0 or user not found.
        """
        query = "SELECT is_superuser FROM `User` WHERE cookies = %s;"
        result = self.do_query(query, (cookie,), fetch=True)
        if not result:
            # no such user
            return False
        # result[0][0] will be 0 or 1
        return bool(result[0][0])

    def get_disruptions(self, patient_id: int, usual_slots: list[int], alert_days: int = 3) -> list[dict]:
        from datetime import datetime, timedelta
        import pandas as pd

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)

        query = """
            SELECT DATE(timestamp) AS date, HOUR(timestamp) AS hour, SUM(steps) AS total_steps
            FROM Data
            INNER JOIN Device ON Data.device_id = Device.id
            WHERE Device.patient_id_device = %s
            AND timestamp BETWEEN %s AND %s
            GROUP BY date, hour
            ORDER BY date, hour;
        """
        rows = self.do_query(query, (patient_id, start_date, end_date))

        if not rows:
            return []

        df = pd.DataFrame(rows, columns=["date", "hour", "total_steps"])
        pivot_df = df.pivot_table(
            index="date", columns="hour", values="total_steps", fill_value=0)

        alerts = []
        for slot in usual_slots:
            hour_slot = slot["hour_slot"]
            if hour_slot not in pivot_df.columns:
                continue

            is_active = pivot_df[hour_slot] > 0
            current_streak = []
            inactive_streaks = []

            for date, active in is_active.items():
                if not active:
                    current_streak.append(str(date))
                else:
                    if len(current_streak) >= alert_days:
                        inactive_streaks.append(current_streak)
                    current_streak = []

            if len(current_streak) >= alert_days:
                inactive_streaks.append(current_streak)

            for streak in inactive_streaks:
                alerts.append(
                    {"hour_slot": hour_slot, "inactive_days": streak})

        return alerts

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

    def upload_minute_data(self, mac_address: str, pam_data: list):
        """
        Upload PAM data for a patient.
        Expects pam_data to be a list of dictionaries with keys:
        - 'timestamp'
        - 'steps'
        - 'pam_score'
        - 'zone'
        - 'data_label'
        """
        patient_id, device_id = self.patient_id_and_device_id_from_mac_address(
            mac_address)

        if not pam_data:
            return False

        query = """
            INSERT INTO Data (device_id, timestamp, steps, PAM_score, zone, data_label, patient_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        params = [
            (device_id, data['timestamp'], data['steps'],
             data['pam_score'], data['zone'], data['data_label'], patient_id)
            for data in pam_data
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

    def upload_day_data(self, mac_address: str, day_data: list):
        """
        Upload daily PAM data for a patient.
        Expects day_data to be a list of dictionaries with keys:
        - 'timestamp'
        - 'steps'
        - 'pam_score'
        """
        patient_id, device_id = self.patient_id_and_device_id_from_mac_address(
            mac_address)

        if not day_data:
            return False

        query = """
            INSERT INTO Data (device_id, timestamp, steps, PAM_score, patient_id)
            VALUES (%s, %s, %s, %s, %s);
        """
        params = [
            (device_id, data['timestamp'], data['steps'],
             data['pam_score'], patient_id)
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

    def calculate_average_data(self, data):
        # Create a DataFrame taken from db `Data` structure
        df = pd.DataFrame(data, columns=[
            'id', 'device_id', 'timestamp', 'steps', 'PAM_score', 'zone', 'data_label'])

        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(
            df['timestamp']).dt.tz_localize('Europe/Amsterdam')

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

    def get_user_preferences(self, cookie: str) -> dict:
        """
        ### Get user preferences based on user ID.
        Returns a dictionary containing user preferences or None if not found.

        ### How to use:
        ```python
        preferences = get_user_preferences(cookie)
        ```
        ### Returns:
        - A dictionary containing user preferences.
        """
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

    def set_user_preferences(self, cookie: str, dark_mode: bool, large_font: bool, language: str) -> bool:
        """
        ### Set user preferences based on user ID.
        Returns True if the preferences were updated successfully, False otherwise.

        ### How to use:
        ```python
        success = set_user_preferences(
            cookie, dark_mode=True, large_font=False, language='en')
        ```
        ### Returns:
        - True if the preferences were updated successfully.
        - False if the update failed.
        """
        query = """
            UPDATE User
            SET dark_mode = %s, large_font = %s, language = %s
            WHERE cookies = %s;
        """
        params = (dark_mode, large_font, language, cookie)
        result = self.do_query(query, params, fetch=False)

        return result is not None

    def get_superusers(self):
        """
        Return a list of all users where is_superuser = 1,
        each as a dict with id, name, and email.
        """
        query = """
          SELECT id, name, email
          FROM User
          WHERE is_superuser = 1
        """
        rows = self.do_query(query)
        if rows is None:
            return None
        # transform into list of dicts for easy JSON / Jinja use
        return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]

    def set_superuser_flag(self, user_id: int, is_super: bool) -> bool:
        """
        Sets `is_superuser` = 1 if is_super True, else 0.
        Returns True on success.
        """
        val = 1 if is_super else 0
        query = "UPDATE User SET is_superuser = %s WHERE id = %s"
        try:
            self.do_query(query, (val, user_id))
            return True
        except Exception:
            return False

    def get_user_by_email(self, email):
        """
        Returns a dict of {id, name, email, is_therapist, is_superuser}, or None if not found.
        """
        query = "SELECT id, name, email, is_therapist, is_superuser FROM User WHERE LOWER(email) = %s"
        rows = self.do_query(query, (email,))
        if not rows:
            return None
        r = rows[0]
        return {"id": r[0], "name": r[1], "email": r[2], "is_therapist": bool(r[3]), "is_superuser": bool(r[4])}

    def set_superuser_flag(self, user_id: int, is_super: bool) -> bool:
        val = 1 if is_super else 0
        query = "UPDATE User SET is_superuser = %s WHERE id = %s"
        try:
            self.do_query(query, (val, user_id))
            return True
        except:
            return False

    def patient_id_and_device_id_from_mac_address(self, mac_address: str) -> tuple[int, int] | None:
        """
        Get the patient ID and device ID associated with a MAC address.
        Returns a tuple (patient_id, device_id) or None if not found.
        """
        query = """
            SELECT patient_id_device, device_id
            FROM Device
            WHERE device_mac_addr = %s;
        """
        params = (mac_address,)
        result = self.do_query(query, params, fetch=True)

        if result and len(result) > 0:
            return result[0][0], result[0][1]
        return None
