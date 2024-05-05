# IoT Sensor Data Processing System

This system is designed to ingest IoT sensor data, process it for anomaly detection using Robust Random Cut Forests (RRCF), and store the data in a PostgreSQL database. The architecture utilizes MQTT for communication between edge devices and the processing system, Redis for queueing incoming messages, Python workers for processing the message queue, and Grafana for reporting and visualization.

## Technologies Used:
- [MQTT](https://mqtt.org/): Lightweight messaging protocol for communication between IoT devices and the processing system.
- [Redis](https://redis.io/): In-memory data structure store used as a message broker for queueing MQTT messages.
- [Python](https://www.python.org/): Programming language used for developing the message processing workers.
- [PostgreSQL](https://www.postgresql.org/): Open source relational database used for storing IoT sensor data.
- [Robust Random Cut Forests (RRCF)](https://github.com/kLabUM/rrcf): Anomaly detection algorithm used for calculating timeseries anomaly scores.
- [Grafana](https://grafana.com/): Open source analytics and monitoring platform used for reporting and visualizations.
- [Docker](https://www.docker.com/): Containerization platform used for deploying the demo environment.
- [Docker Compose](https://docs.docker.com/compose/): Tool for defining and running multi-container Docker applications.

## System Architecture:
1. **MQTT Edge Devices**: IoT sensors push sensor data using the MQTT protocol.
2. **MQTT Consumer**: Messages from MQTT are pushed to Redis queues.
3. **Python Workers**: Workers consume messages from Redis queues, process them, and persist the IoT sensor data in a PostgreSQL database.
4. **Anomaly Detection**: RRCF algorithm is utilized to calculate timeseries anomaly scores.
5. **Reporting and Visualization**: Grafana is used for reporting and visualizations, providing insights into the processed IoT sensor data.

## Deployment:
The demo environment is deployed using Docker Compose, which simplifies the setup of the entire system. To deploy the demo:
1. Clone the repository containing the Docker Compose configuration.
2. Navigate to the directory containing the Docker Compose file.
3. Run `docker-compose up` to start the containers.
4. Access Grafana at `http://localhost:3000` to view reports and visualizations.

## Usage:
- Edge devices should push sensor data using MQTT to the designated MQTT broker.
- Python workers will automatically consume messages from the Redis queues and process them for anomaly detection.
- Anomaly scores and processed data will be stored in the PostgreSQL database.
- Users can access Grafana for reporting and visualization of the IoT sensor data.

## Synthetic Sensor Data:
For the purposes of the demo, we created synthetic audio data as our sensor data by altering the [UrbanSound8K dataset](https://urbansounddataset.weebly.com/urbansound8k.html). This dataset was modified to simulate various environmental sounds captured by IoT sensors.

## Contributing:
Contributions to the system are welcome! If you have any suggestions for improvements or would like to report issues, please open an issue or submit a pull request to the repository.

## License:
This system is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the LICENSE file for more details.
