import os
import psycopg2
from psycopg2 import pool

# Connection pool for Neon Serverless Postgres
_postgreSQL_pool = None

def initialize_db_pool():
    global _postgreSQL_pool
    if _postgreSQL_pool is None:
        db_url = os.getenv("NEON_POSTGRES_URL")
        if not db_url:
            raise ValueError("NEON_POSTGRES_URL environment variable not set")
        _postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, db_url)
        print("Database connection pool initialized.")

def get_db_connection():
    if _postgreSQL_pool is None:
        initialize_db_pool()
    return _postgreSQL_pool.getconn()

def return_db_connection(conn):
    if _postgreSQL_pool is not None:
        _postgreSQL_pool.putconn(conn)

def close_db_pool():
    global _postgreSQL_pool
    if _postgreSQL_pool is not None:
        _postgreSQL_pool.closeall()
        _postgreSQL_pool = None
        print("Database connection pool closed.")

# Example of how to use a connection (will be called by other modules)
def execute_query(query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = False):
    conn = None
    cursor = None
    result = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Database query failed: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)
    return result


# Initialize the pool when this module is imported
# Note: In a FastAPI app, you'd typically handle this with startup/shutdown events
# initialize_db_pool() # This line should be managed by FastAPI lifecycle events
