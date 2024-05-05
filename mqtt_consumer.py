import paho.mqtt.client as mqtt
import redis


class MQTTToRedisService:
    def __init__(self, mqtt_broker='localhost', mqtt_port=1883, mqtt_topic='timeseries/data',
                 redis_host='localhost', redis_port=6379, redis_queue='timeseries/data'):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_queue = redis_queue

        # Initialize Redis
        self.redis_client = redis.Redis(host=self.redis_host, port=self.redis_port)

        # Initialize MQTT Client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
            client.subscribe(self.mqtt_topic)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
            self.redis_client.rpush(self.redis_queue, msg.payload)  # Push to Redis list
        except Exception as e:
            print(f"Failed to handle message: {e}")

    def start(self):
        # Connect to MQTT Broker
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
        # Start the loop
        self.mqtt_client.loop_forever()


if __name__ == "__main__":
    service = MQTTToRedisService()
    service.start()
