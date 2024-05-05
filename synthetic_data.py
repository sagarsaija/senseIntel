import json
import os
import random
from datetime import datetime, timedelta

import librosa
import paho.mqtt.client as mqtt
import pandas as pd

# Configuration
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "timeseries/data"


# MQTT Publisher Function
def publish_mqtt(messages):
    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
            for msg in messages:
                client.publish(mqtt_topic, json.dumps(msg))
                print(f"Message sent: {msg}")
            client.disconnect()  # Disconnect after sending all messages
        else:
            print(f"Failed to connect, return code {rc}")

    client.on_connect = on_connect

    try:
        client.connect(mqtt_broker, mqtt_port, 60)
        client.loop_forever()  # Handle network traffic and dispatch callbacks
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.loop_stop()


# Path to your metadata CSV and root directory of audio files
metadata_path = 'our_data/UrbanSound8K/metadata/UrbanSound8K.csv'
audio_root = 'our_data/UrbanSound8K/audio'


def random_offset():
    return random.uniform(-0.3, 0.3)


def read_and_process_audio(metadata_path, audio_root, max_files=20):
    df = pd.read_csv(metadata_path)
    sensor_id = 1

    locations = [
        {'name': 'Prypyat Area', 'lat': 51.405, 'lon': 30.056},
        {'name': 'Carpathian Mountains', 'lat': 48.155, 'lon': 24.830},
        {'name': 'Bukovina Border Area', 'lat': 48.300, 'lon': 26.500},
        {'name': 'Chernihiv Area', 'lat': 51.500, 'lon': 31.300},
        {'name': 'Donetsk', 'lat': 48.015, 'lon': 37.802},
        {'name': 'Mariupol', 'lat': 47.097, 'lon': 37.543},
        {'name': 'Luhansk', 'lat': 48.574, 'lon': 39.307},
        {'name': 'Kharkiv', 'lat': 49.993, 'lon': 36.230},
        {'name': 'Zaporizhzhia', 'lat': 47.838, 'lon': 35.139},
        {'name': 'Mykolaiv', 'lat': 46.965, 'lon': 32.000}
    ]

    base_datetime = datetime.now() - timedelta(days=1)  # Base time for simulations

    for index, row in df.iterrows():
        if index >= max_files:
            break

        file_path = os.path.join(audio_root, f"fold{row['fold']}", row['slice_file_name'])
        audio, sr = librosa.load(file_path, sr=None)
        audio_length = len(audio[0:1000])
        mqtt_messages = []

        current_datetime = base_datetime  # Reset the base time for each new audio file

        for i in range(audio_length):
            sample_time = current_datetime + timedelta(seconds=i)  # Increment by one second per sample
            location = locations[index % len(locations)]
            sensor_metadata = {
                'sensor_id': sensor_id,
                'sensor_name': row['slice_file_name'],
                'sensor_type': 'Audio',
                'location': location['name'],
                'latitude': location['lat'] + random_offset(),
                'longitude': location['lon'] + random_offset(),
                'installation_date': current_datetime.strftime('%Y-%m-%d'),
            }
            mqtt_message = {
                'metadata': sensor_metadata,
                'timestamp': sample_time.strftime('%Y-%m-%d %H:%M:%S'),
                'value': float(audio[i] if i < audio_length else 0)  # Ensure audio index does not go out of range
            }
            mqtt_messages.append(mqtt_message)

        # Publish messages for the current file
        publish_mqtt(mqtt_messages)
        print(f"Completed processing and publishing for file: {row['slice_file_name']}")
        sensor_id += 1


# Call the function
read_and_process_audio(metadata_path, audio_root)
