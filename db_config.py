import psycopg2
from psycopg2 import sql

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",      # Update as needed
        database="MILF",  # Replace with your database name
        user="postgres",      # Replace with your PostgreSQL username
        password="0000"  # Replace with your PostgreSQL password
    )
    return conn
