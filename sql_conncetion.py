import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

__cnx = None

def get_sql_connection():
    global __cnx
    if __cnx is None:
        __cnx = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
    return __cnx