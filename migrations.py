import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration
# DATABASE = 'timeseries'
# USER = 'doadmin'
# PASSWORD = 'AVNS_bjip2lSzYvfoW0edZXj'
# HOST = 'db-postgresql-sfo3-65542-do-user-16558773-0.c.db.ondigitalocean.com'
# PORT = '25060'

DATABASE = 'timeseries'
USER = 'postgres'
PASSWORD = 'mysecretpassword'
HOST = 'localhost'
PORT = '5432'

# SQL statements for creating tables
CREATE_METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS sensor_metadata (
    sensor_id SERIAL PRIMARY KEY,
    sensor_name VARCHAR(255) NOT NULL,
    sensor_type VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    installation_date DATE,
    additional_info JSONB
);
"""

CREATE_TIMESERIES_TABLE = """
CREATE TABLE IF NOT EXISTS sensor_timeseries_data (
    entry_id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    value NUMERIC NOT NULL,
    anomaly_score NUMERIC,
    FOREIGN KEY (sensor_id) REFERENCES sensor_metadata (sensor_id)
);
"""


def drop_tables(conn):
    """Drop existing tables in the database to ensure we can recreate them fresh."""
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS sensor_timeseries_data cascade;")
        cur.execute("DROP TABLE IF EXISTS sensor_metadata cascade;")
        conn.commit()
        print("Existing tables dropped successfully.")


def create_database(conn):
    # Create a connection to the default database (usually 'postgres')
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='mysecretpassword',
        host='localhost',
        port='5432'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Set the isolation level

    with conn.cursor() as cur:
        cur.execute("DROP DATABASE IF EXISTS timeseries;")  # Optionally drop existing database
        cur.execute("CREATE DATABASE timeseries;")  # Create new database

    conn.close()  # Close the connection


def create_tables(conn):
    """Create tables in the PostgreSQL database."""
    with conn.cursor() as cur:
        cur.execute(CREATE_METADATA_TABLE)
        cur.execute(CREATE_TIMESERIES_TABLE)
        conn.commit()
        print("Tables created successfully.")


def main():
    conn = psycopg2.connect(
        dbname='postgres',
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    create_database(conn)
    conn = psycopg2.connect(
        dbname='timeseries',
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    try:
        drop_tables(conn)
        create_tables(conn)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
