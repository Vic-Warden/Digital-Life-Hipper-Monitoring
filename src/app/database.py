import mysql.connector
from mysql.connector import Error  # Error handling module


class Database:
    def __init__(self, host, port, user, password, database):
        # Initialize the database connection parameters
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database

    def connect(self):
        # Establish a connection to the MySQL database
        try:
            connection = mysql.connector.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database
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
        # At the end, close the connection if it was established
        finally:
            print("Attempting to close the connection...", end=" ")
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("OK!")
            else:
                print("FAIL!, reason: no connection to close.")


db = Database(
    host="localhost",
    port=3306,
    user="root",
    password="superstronkrootpassword",
    database="hipperdb"
)

db.connect()
