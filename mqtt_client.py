import json

import paho.mqtt.client as mqtt

# Configuration
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "timeseries/data"


# MQTT Publisher Function
def publish_mqtt(data):
    client = mqtt.Client()

    # Handle connection callback
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
            client.publish(mqtt_topic, json.dumps(data))
        else:
            print(f"Failed to connect, return code {rc}")

    # Set the connection callback
    client.on_connect = on_connect

    try:
        client.connect(mqtt_broker, mqtt_port, 60)
        client.loop_forever()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.disconnect()
