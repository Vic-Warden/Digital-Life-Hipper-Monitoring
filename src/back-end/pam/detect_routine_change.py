import os
import mysql.connector
import pandas as pd
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Connection MySQL
load_dotenv(dotenv_path='../database/.env')

db_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "hipperdb"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}

try:
    connection = mysql.connector.connect(**db_config)
    print("Database Connected")
except mysql.connector.Error as err:
    print("Database Connection error:", err)
    exit(1)

cursor = connection.cursor(dictionary=True)



