import mysql.connector
from mysql.connector import Error  # Error handling module


class Database:
    def __init__(self, host, user, password, database):
        # Initialize the database connection parameters
        self.host = host
        self.user = user
        self.password = password
        self.database = database
