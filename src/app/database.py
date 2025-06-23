import os  # Import os for .env centralized settings
import pandas as pd
import mysql.connector
from mysql.connector import Error  # Error handling module
from mysql.connector import MySQLConnection  # MySQL connection type
from flask import Flask, jsonify, request  # Flask
from crypto import Cookie
from datetime import datetime, timedelta
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

        cursor = None
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
            if cursor:
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

        Returns False if the email exists, True otherwise.
        """
        query = "SELECT COUNT(*) FROM User WHERE email = %s"
        params = (email,)
        result = self.do_query(query, params)
        if result[0][0] > 0:
            return False
        return True

    def check_credentials(self, email: str, password: str) -> bool:
        """
        ### Check if the email and password match a registered user.

        Returns True if the credentials are valid, False otherwise.
        """
        # query = "SELECT password FROM User WHERE email = %s"
        # result = self.do_query(query, (email,))
        # if not result:
        #     return False
        # stored_hash = result[0][0]
        # return check_password_hash(stored_hash, password)
        query = "SELECT COUNT(*) FROM User WHERE email = %s AND password = %s"
        params = (email, password)
        result = self.do_query(query, params)
        if result and result[0][0] == 1:
            return True
        return False


    def add_patient(self, name: str, email: str, password: str, cookie: str) -> bool:
        """
        add a new patient linked to a therapist,
        and initialize their daily/weekly/monthly goals to 0.

        Returns True if successful, False otherwise.
        """
        # 1) find the current therapist from their cookie
        therapist_id = self.therapist_id_from_cookie(cookie)
        if not therapist_id:
            return False

        try:
            # 2) Insert new patient record
            insert_user_sql = """
                INSERT INTO `User` 
                    (name, email, password, cookies, is_therapist, fk_therapist_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """
            params = (name, email, password, None, 0, therapist_id)
            patient_id = self.do_query(insert_user_sql, params)[0][0]

            # 3) Link patient ↔ therapist
            self.connect_patient_to_therapist(patient_id, therapist_id)

            # 4) Seed the patient's goals to zero
            insert_goal_sql = """
                INSERT INTO `Goal`
                    (patient_id_goal, patient_goal, type, reached)
                VALUES (%s, %s, %s, %s);
            """
            for period in ('daily', 'weekly', 'monthly'):
                self.do_query(insert_goal_sql, (patient_id, 0, period, 0))

            # 5) Seed other tables here, e.g. Data or MinuteData:
            insert_data_sql = """
                INSERT INTO `Data`
                    (device_id, timestamp, steps, PAM_score, zone_1, zone_2, zone_3, patient_id)
                VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s);
            """
            self.do_query(insert_data_sql, (0, 0, 0.0, 0, 0, 0, patient_id))

            return True

        except Exception as e:
            print(f"Error inserting patient and initializing data: {e}")
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
                Data.zone_1, 
                Data.zone_2, 
                Data.zone_3,
                Data.patient_id
            FROM Data
            INNER JOIN Device ON Data.device_id = Device.device_id
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
    
    def get_all_patients(self) -> list[dict] | None:
        """
        Get a list of all users who are patients (not therapists).
        """
        query = """
            SELECT id, name, email
            FROM User
            WHERE is_therapist = 0;
        """
        result = self.do_query(query, fetch=True)

        if result:
            return [{"id": row[0], "name": row[1], "email": row[2]} for row in result]
        return None  # Now correctly outside the if-block


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

    def is_super_user(self, cookie: str) -> bool:
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
        - 'data_label'
        """
        patient_id, device_id = self.patient_id_and_device_id_from_mac_address(
            mac_address)

        if not pam_data:
            return False

        query = """
            INSERT INTO MinuteData (device_id, timestamp, steps, PAM_score, data_label, patient_id)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = [
            (device_id, data['timestamp'], data['steps'],
             data['pam_score'], data['data_label'], patient_id)
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
            INSERT INTO Data (device_id, timestamp, steps, PAM_score, zone_1, zone_2, zone_3, patient_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = [
            (
                device_id,
                data['timestamp'],
                data['steps'],
                data['pam_score'],
                data['zone_1'],
                data['zone_2'],
                data['zone_3'],
                patient_id
            ) for data in day_data]

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

    def calculate_patient_data(self, dataset: dict):

        if not isinstance(dataset, dict) or dataset.get('patient_details') is None or not dataset.get('data'):
            return {
                'hourly': [],
                'daily': [],
                'weekly': [],
                'monthly': [],
                'last_data_pull_ago': "No data available",
                'total_steps_today': 0,
                'combined_goal_completion_percent': None,
                'goal_completion_details': []
            }
                
        patient = dataset['patient_details']
        data = dataset['data']
        goals = dataset['goals']

        df = pd.DataFrame(data, columns=[
            'id', 'device_id', 'timestamp', 'steps', 'PAM_score',
            'zone_1', 'zone_2', 'zone_3', 'patient_id'
        ])
        
        patient_id = df['patient_id'].iloc[0]

        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('Europe/Amsterdam')
        df.set_index('timestamp', inplace=True)

        hourly_avg = df.resample('h')[['steps', 'PAM_score']].mean()
        daily_avg = df.resample('D')[['steps', 'PAM_score']].mean()
        weekly_avg = df.resample('W')[['steps', 'PAM_score']].mean()
        monthly_avg = df.resample('ME')[['steps', 'PAM_score']].mean()

        now = datetime.now(ZoneInfo('Europe/Amsterdam'))
        today = now.date()

        today_steps = df[df.index.date == today]['steps'].sum()
        last_data_pull = df.index.max()

        if pd.isna(last_data_pull):
            last_data_pull_ago = "No data available"
        else:
            delta = now - last_data_pull
            hours, remainder = divmod(delta.total_seconds(), 3600)
            minutes = remainder // 60
            last_data_pull_ago = f"{int(hours)}h, {int(minutes)}min ago"

        combined_completion = None
        goal_completion_details = []

        patient_goals = [g for g in goals if g[1] == patient_id]

        if patient_goals:
            total_percent = 0
            count = 0

            for goal in patient_goals:
                goal_id, patient_id_goal, target, goal_type, _ = goal
                if not target:
                    continue

                if goal_type == 'daily':
                    steps = df[df.index.date == today]['steps'].sum()
                elif goal_type == 'weekly':
                    start_of_week = now - pd.to_timedelta(now.weekday(), unit='d')
                    steps = df[df.index.date >= start_of_week.date()]['steps'].sum()
                elif goal_type == 'monthly':
                    start_of_month = now.replace(day=1)
                    steps = df[df.index.date >= start_of_month.date()]['steps'].sum()
                else:
                    continue

                percent = min((steps / target) * 100, 100)
                total_percent += percent
                count += 1

                # 🔁 Update goal reached
                if percent >= 100:
                    self.update_goal_reached(1, patient_id_goal, goal_id, goal_type)
                else:
                    self.update_goal_reached(0, patient_id_goal, goal_id, goal_type)

                # 🔍 Fetch current `reached` value
                queryGet = """
                    SELECT reached FROM Goal
                    WHERE patient_id_goal = %s AND id = %s;
                """
                result = self.do_query(queryGet, (patient_id_goal, goal_id), fetch=True)
                reached_count = result[0][0] if result else None

                goal_completion_details.append({
                    'goal_type': goal_type,
                    'target': target,
                    'steps': int(steps),
                    'percent_completed': round(percent, 2),
                    'reached': reached_count
                })

            combined_completion = round(total_percent / count, 1) if count > 0 else None

            hourly = hourly_avg.reset_index().to_dict(orient='records')
            daily = daily_avg.reset_index().to_dict(orient='records')
            weekly = weekly_avg.reset_index().to_dict(orient='records')
            monthly = monthly_avg.reset_index().to_dict(orient='records')

            weekly_therapist = sorted(daily, key=lambda x: x['timestamp'])
            daily_therapist = sorted(hourly, key=lambda x: x['timestamp'])

            for entry in weekly_therapist:
                entry['date_str'] = entry['timestamp'].strftime('%Y-%m-%d')

            for entry in daily_therapist:
                entry['hour_str'] = entry['timestamp'].strftime('%-H:00')

        return {
            'name': patient[0][1],
            'email': patient[0][2],
            'hourly': hourly[-24:],
            'daily': daily[-7:],
            'daily_therapist_sorted': daily_therapist[-16:],
            'weekly': weekly[-6:],
            'weekly_therapist_sorted': weekly_therapist[-7:],
            'monthly': monthly[-6:],
            'last_data_pull_ago': last_data_pull_ago,
            'total_steps_today': int(today_steps),
            'combined_goal_completion_percent': combined_completion,
            'goal_completion_details': goal_completion_details
        }
    
    def update_goal_reached(self, reached, patient_id_goal, id, goal_type):
        """
        Updates the 'reached' count based on whether the goal was met for the period.
        Prevents multiple updates within the same day/week/month depending on goal type.
        """
        now = datetime.now(ZoneInfo('Europe/Amsterdam'))

        # Determine current period identifier
        if goal_type == 'daily':
            current_period = now.date()
        elif goal_type == 'weekly':
            current_period = (now - timedelta(days=now.weekday())).date()
        elif goal_type == 'monthly':
            current_period = now.date().replace(day=1)
        else:
            return False  # Unknown goal type

        # Fetch existing goal
        queryGet = """
            SELECT reached, last_updated FROM Goal
            WHERE patient_id_goal = %s AND id = %s;
        """
        getParams = (patient_id_goal, id)
        getResult = self.do_query(queryGet, getParams, fetch=True)

        if not getResult:
            return False

        currentReached, last_updated = getResult[0]

        if last_updated is not None:
            last_updated = last_updated.astimezone(ZoneInfo('Europe/Amsterdam'))

            if goal_type == 'daily':
                last_period = last_updated.date()
            elif goal_type == 'weekly':
                last_period = (last_updated - timedelta(days=last_updated.weekday())).date()
            elif goal_type == 'monthly':
                last_period = last_updated.date().replace(day=1)
            else:
                return False

            # Skip if already updated for this period
            if last_period == current_period:
                return False

        # Update reached count
        newReached = currentReached + 1 if reached == 1 else 0

        # Update the goal record
        queryUpdate = """
            UPDATE Goal
            SET reached = %s, last_updated = %s
            WHERE patient_id_goal = %s AND id = %s;
        """
        setParams = (newReached, now, patient_id_goal, id)
        setResult = self.do_query(queryUpdate, setParams, fetch=True)

        return setResult is not None


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
    
    def user_id_from_cookie(self, cookie: str) -> int | bool:
        """

        """
        try:
            insert_query = """
            SELECT id FROM User WHERE cookies = %s;
            """
            params = (cookie,)
            result = self.do_query(insert_query, params)
            return result

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

    def is_therapist(self, cookie: str) -> bool:
        """
        Check if the user is a therapist based on their cookie.

        Returns True if the user is a therapist, False otherwise.
        """
        query = "SELECT is_therapist FROM User WHERE cookies = %s;"
        params = (cookie,)
        result = self.do_query(query, params, fetch=True)

        if result and len(result) > 0:
            return result[0][0] == 1
        return False

    def get_devices(self) -> list[dict] | None:
        """
        Get a list of all devices in the database.
        Returns a list of dictionaries containing device details or None if not found.
        """
        query = """
            SELECT patient_id_device, device_label, device_id
            FROM Device;
        """
        result = self.do_query(query, fetch=True)

        if result:
            return [{"patient_id": row[0], "device_label": row[1], "device_id": row[2]} for row in result]
        return None

    def bind_device_to_patient(self, device_id: int, patient_id: int) -> bool:
        """
        Bind a device to a patient by updating the patient_id_device field.
        Returns True if successful, False otherwise.
        """
        query = "UPDATE Device SET patient_id_device = %s WHERE device_id = %s;"
        params = (patient_id, device_id)
        result = self.do_query(query, params, fetch=False)

        return result is not None

    def unbind_device_from_patient(self, device_id: int) -> bool:
        """
        Unbind a device from its current patient by setting patient_id_device to NULL.
        Returns True if successful, False otherwise.
        """
        query = "UPDATE Device SET patient_id_device = NULL WHERE device_id = %s;"
        params = (device_id,)
        result = self.do_query(query, params, fetch=False)

        return result is not None

    def get_therapists(self) -> list[dict]:
        """Return all therapists (is_therapist=1)."""
        rows = self.do_query(
            "SELECT id,name,email FROM User WHERE is_therapist = 1;", fetch=True)
        return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows] if rows else []


    def add_therapist(self, name: str, email: str, password: str) -> bool:
        """
        Create a new therapist:
         1. Insert into Therapist(name) → get therapist_id
         2. Insert into User with is_therapist=1, fk_therapist_id, is_superuser
        """
        try:
            cursor = self._connection.cursor()

            # 1️⃣ Insert into Therapist
            cursor.execute(
                "INSERT INTO Therapist (name) VALUES (%s);",
                (name,)
            )
            therapist_id = cursor.lastrowid

            # 2️⃣ Insert into User (only the 7 specified columns)

            cursor.execute("""
                INSERT INTO `User`
                  (`name`, `email`, `password`, `cookies`,
                   `is_therapist`, `fk_therapist_id`, `is_superuser`)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
                name,
                email,
                password,
                None,
                1,
                therapist_id,
                0  # or 0 if you don't want them super immediately
            ))

            self._connection.commit()
            cursor.close()
            return True

        except Exception as e:
            print("add_therapist error:", e)
            return False

    def remove_therapist_by_id(self, therapist_id: int) -> bool:
        """Delete a therapist (and cascade relationships)."""
        result = self.do_query(
            "DELETE FROM User WHERE id = %s AND is_therapist = 1;", (therapist_id,), fetch=False)
        # fetch=False returns [("Query executed successfully",)] on success
        return result is not None

    def reset_therapist_password(self, email: str, new_password: str) -> bool:
        """
        Update the password for a therapist identified by email.
        Returns True if exactly one row was updated.
        """
        # 1) Lookup the user and confirm they're a therapist
        user = self.get_user_by_email(email)
        if not user or not user.get('is_therapist'):
            return False

        # 2) Run the UPDATE against the PK, then commit and check rowcount
        query = "UPDATE `User` SET password = %s WHERE id = %s"
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, (new_password, user['id']))
            self._connection.commit()
            affected = cursor.rowcount
            cursor.close()
            # Return True only if exactly one row was updated
            return affected == 1
        except Error as e:
            print("reset_therapist_password error:", e)
            return False

