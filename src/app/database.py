import os  # Import os for .env centralized settings
import mysql.connector
from mysql.connector import Error  # Error handling module
from mysql.connector import MySQLConnection  # MySQL connection type
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
                db_info = connection.get_server_info()
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

    def add_patient(self, name: str, email: str, password: str) -> tuple[bool, str]:
        """
        ### Add a new patient to the database.

        Returns:
        - A tuple (True, "") if the patient was added successfully.
        - A tuple (False, "Email already registered.") if the email is already in use.
        """
        if self.check_email(email):
            return (False, "Email already registered.")
        query = "INSERT INTO User (name, email, password, is_therapist) VALUES (%s, %s, %s, %s);"
        params = (name, email, password, 0)  # is_therapist = 0 for patients
        result = self.do_query(query, params)
        return (result is not None, "")

    def assign_patient_to_therapist(self, patient_id: int, therapist_id: int) -> bool:
        print("HAS YET TO BE IMPLEMENTED")
        return False

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

    # def get_last_update_period(self, device_mac_addr: str):
    #     """
    #     ### Get the last update period for a device based on its MAC address.

    #     Returns the last update period as a string.
    #     """
    #     query = "SELECT last_update_period FROM Device WHERE device_mac_addr = %s;"
    #     params = (device_mac_addr,)
    #     result = self.do_query(query, params, fetch=True)

    #     if result and len(result) > 0:
    #         return result[0][0]
    #     return None

    # def set_last_update_period(self, device_mac_addr: str) -> bool:
    #     """
    #     ### Set the last update period for a device based on its MAC address.

    #     Returns True if the update was successful, False otherwise.
    #     """
    #     # Get current time
    #     now = datetime.now()

    #     # Format as MySQL-compatible DATETIME string
    #     current_time = now.strftime('%Y-%m-%d %H:%M:%S')

    #     # Update the last_data_pull for the device
    #     query = "UPDATE Device SET last_data_pull = %s WHERE device_mac_addr = %s;"
    #     params = (current_time, device_mac_addr)
    #     result = self.do_query(query, params, fetch=False)
    #     return result is not None

    def get_log_for_mac(self, mac_address):
        query = "SELECT last_activity_pull, last_day_data_pull FROM Device WHERE device_mac_addr=%s"
        params = (mac_address,)
        result = self.do_query(query, params, fetch=True)

        if result and len(result) > 0:
            return result[0][0]
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
