import pyodbc
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Database connection settings from environment variables
server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
driver = os.getenv("DB_DRIVER")
TrustServerCertificate = os.getenv("TrustServerCertificate")

# Establish the connection
def get_db_connection():
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate={TrustServerCertificate}"
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        return None

# Query execution function
def execute_query(query, params=None, fetch_all=True):
    conn = get_db_connection()
    if not conn:
        print("Database connection failed.")  # Debug log
        return None
    try:
        cursor = conn.cursor()
        if params:
            print(f"Executing query with params: {params}")  # Debug log
            cursor.execute(query, params)
        else:
            print("Executing query without params.")  # Debug log
            cursor.execute(query)
        
        if fetch_all:
            results = cursor.fetchall()
            print(f"Fetched results: {results}")  # Debug log
            conn.close()
            return results
        
        conn.commit()
        print("Query committed successfully.")  # Debug log
        conn.close()
        return True  # Indicate success for non-fetch queries
    except pyodbc.Error as e:
        print(f"Query execution failed: {e}")  # Debug log
        return None
