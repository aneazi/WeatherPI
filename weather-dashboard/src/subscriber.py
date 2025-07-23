import json
import csv
from pathlib import Path
import paho.mqtt.client as mqtt
from datetime import datetime
from dateutil import tz
import logging

UTC = tz.tzutc()
MST = tz.gettz("America/Phoenix")

def start_subscriber(config, buffer):
    if config.get("terminal_output", True):
        logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )
    if config.get("log_csv"):
        data_dir = Path("weather-dashboard/data")
        csv_path=data_dir / "weather_data.csv"
        if not csv_path.exists():
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "temperature", "humidity", "pressure"])
                
    def on_connect(client, userdata, flags, rc):
        client.subscribe(config['raw_topic'])
    
    def on_message(client, userdata, msg):
        payload = json.loads(msg.payload.decode('utf-8'))
        ts_utc_str = payload.get("timestamp")
        if ts_utc_str:
            dt = datetime.fromisoformat(ts_utc_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)
        else:
            dt = datetime.utcnow().replace(tzinfo=UTC)
        dt_mst = dt.astimezone(MST)
        ts_mst = dt_mst.strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": ts_mst,
            "temperature": payload.get("temperature"),
            "humidity": payload.get("humidity"),
            "pressure": payload.get("pressure")
        }
        buffer.append(entry)
        if config.get("terminal_output", True):
            logging.info(f"Received on `{msg.topic}` → {entry}")
        if config.get("log_csv"):
            with open(csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([entry["timestamp"], entry["temperature"], entry["humidity"], entry["pressure"]])


    client = mqtt.Client()
    client.enable_logger()
    if 'username' in config and 'password' in config:
        client.username_pw_set(config['username'], config['password'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config['broker_url'], config['port'])
    client.loop_start()