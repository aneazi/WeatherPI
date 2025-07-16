import time
import json
import signal
import sys
import paho.mqtt.client as mqtt
from utils import load_config, setup_logging
from sensors import SensorReader

client = None

def signal_handler(sig, frame):
    print('\nShutting down gracefully...')
    if client:
        client.loop_stop()
        client.disconnect()
    sys.exit(0)

def main():
    global client
    
    config = load_config("config.yaml")
    setup_logging()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler) # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler) # Termination signal
    
    broker_addr = config['broker_url']
    broker_port = config['port']
    topic = config['topic']
    sample_interval = config['sample_interval']
    
    client = mqtt.Client()
    if 'username' in config and 'password' in config:
        client.username_pw_set(config['username'], config['password'])
    
    try:
        client.connect(broker_addr, broker_port)
        client.loop_start()
        print(f"Connected to MQTT broker at {broker_addr}:{broker_port}")
        print("Press Ctrl+C to stop...")
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