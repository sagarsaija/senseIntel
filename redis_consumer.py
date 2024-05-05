import json
import os
from datetime import datetime

import psycopg2
import redis

# Database connection parameters
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# Redis connection parameters
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_QUEUE = os.environ.get('REDIS_QUEUE')

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Connect to PostgreSQL
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
conn.autocommit = False
cursor = conn.cursor()


def ensure_sensor_exists(metadata):
    sensor_id = metadata['sensor_id']
    sensor_name = metadata['sensor_name']

    # Check if sensor metadata already exists
    cursor.execute('SELECT sensor_id FROM sensor_metadata WHERE sensor_id = %s OR sensor_name = %s',
                   (sensor_id, sensor_name))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return existing sensor_id
    else:
        # Insert new sensor metadata
        cursor.execute(
            """
            INSERT INTO sensor_metadata (sensor_id, sensor_name, sensor_type, location, latitude, longitude, installation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING sensor_id
            """,
            (sensor_id, sensor_name, metadata['sensor_type'], metadata['location'],
             metadata['latitude'], metadata['longitude'], metadata['installation_date'])
        )
        conn.commit()
        return cursor.fetchone()[0]


def insert_timeseries_data(sensor_id, timestamp, value):
    cursor.execute(
        """
        INSERT INTO sensor_timeseries_data (sensor_id, timestamp, value)
        VALUES (%s, %s, %s)
        """,
        (sensor_id, timestamp, value)
    )
    conn.commit()


def main():
    while True:
        # Blocking pop from Redis queue
        _, message = r.blpop(REDIS_QUEUE)
        data = json.loads(message)

        # Extract metadata and timeseries data
        metadata = data['metadata']
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        value = data['value']

        try:
            # Ensure sensor is registered
            sensor_id = ensure_sensor_exists(metadata)
            # Insert timeseries data
            insert_timeseries_data(sensor_id, timestamp, value)
        except Exception as e:
            print("Failed to process message:", e)
            conn.rollback()
        else:
            print("Data inserted successfully for sensor_id:", sensor_id)


if __name__ == '__main__':
    main()
