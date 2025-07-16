import time
import json
import paho.mqtt.client as mqtt
from utils import load_config, setup_logging
from sensors import SensorReader


def main():
    config = load_config("config.yaml")
    setup_logging()
    broker_addr = config['broker_url']
    topic = config['topic']
    sample_interval = config['sample_interval']
    
    client = mqtt.Client()
    try:
        client.connect(broker_addr)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return
    
    sensor_reader = SensorReader()
    while True:
        try:
            data = sensor_reader.get_all_data()
            payload = json.dumps(data)
            client.publish(topic, payload)
            print(f"Published data: {payload}")
        except Exception as e:
            print(f"Error reading sensor data: {e}")
        
        time.sleep(sample_interval)

if __name__ == "__main__":
    main()