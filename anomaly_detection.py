import os
from multiprocessing import Pool

import numpy as np
import psycopg2
import rrcf

# Database connection parameters
host = os.environ.get('DB_HOST')
dbname = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')


def process_sensor_data(sensor_id):
    print(f"Processing sensor: {sensor_id}")
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    cursor = conn.cursor()

    # Set all anomaly scores to NULL at the start
    cursor.execute("UPDATE sensor_timeseries_data SET anomaly_score = NULL WHERE sensor_id = %s;", (sensor_id,))

    # Fetch data for a specific sensor
    fetch_query = """
    SELECT entry_id, value FROM sensor_timeseries_data WHERE sensor_id = %s ORDER BY timestamp;
    """
    cursor.execute(fetch_query, (sensor_id,))
    data = cursor.fetchall()

    if data:
        # Prepare data for RRCF
        points = np.array([item[1] for item in data])
        ids = [item[0] for item in data]

        # Set tree parameters
        num_trees = 100
        tree_size = 256
        forest = []

        # Create forest
        for _ in range(num_trees):
            tree = rrcf.RCTree()
            forest.append(tree)

        # Insert points into RRCF and calculate anomaly scores
        anomaly_scores = {}
        for point, entry_id in zip(points, ids):
            for tree in forest:
                if len(tree.leaves) > tree_size:
                    tree.forget_point(min(tree.leaves))
                tree.insert_point(point, index=entry_id)
            # Average anomaly score across all trees
            score = np.mean([tree.codisp(entry_id) for tree in forest])
            anomaly_scores[entry_id] = score

        # Normalize anomaly scores
        max_score = max(anomaly_scores.values())
        for entry_id in anomaly_scores:
            anomaly_scores[entry_id] /= max_score

        # Update normalized anomaly scores in the database
        update_query = """
        UPDATE sensor_timeseries_data SET anomaly_score = %s WHERE entry_id = %s;
        """
        for entry_id, score in anomaly_scores.items():
            cursor.execute(update_query, (score, entry_id))

        # Commit the updates to the database
        conn.commit()

    # Close database connection
    cursor.close()
    conn.close()


def main():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    cursor = conn.cursor()

    # Fetch all sensor IDs
    cursor.execute("SELECT sensor_id FROM sensor_metadata;")
    sensor_ids = cursor.fetchall()

    # Close initial database connection
    cursor.close()
    conn.close()

    # Process each sensor's data in parallel
    with Pool() as pool:
        pool.map(process_sensor_data, [sensor_id[0] for sensor_id in sensor_ids])


if __name__ == '__main__':
    main()
    print("Anomaly scores updated successfully for all sensors.")
