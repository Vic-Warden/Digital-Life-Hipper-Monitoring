import os
import mysql.connector
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv(dotenv_path='../database/.env')

# Retrieve MySQL connection parameters
db_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "hipperdb"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}

# Connection to the data base
try:
    connection = mysql.connector.connect(**db_config)
    print("Success")
except mysql.connector.Error as err:
    print("error", err)
    exit(1)

connection.close()
