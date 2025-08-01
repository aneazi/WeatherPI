import json
import sqlite3
from pathlib import Path
import paho.mqtt.client as mqtt
from datetime import datetime
from dateutil import tz
import logging
import os

UTC = tz.tzutc()
MST = tz.gettz("America/Phoenix")

def start_subscriber(config, buffer):
    # Get the directory where the script is running from
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # weather-dashboard directory
    if config.get("terminal_output", True):
        logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )
    if config.get("log_sqlite"):
        db_path = os.path.join(PROJECT_ROOT, "data", "weather.db")
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                timestamp TEXT,
                temperature REAL,
                humidity REAL,
                pressure REAL
            )
        ''')
        conn.commit()
                
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
            dt = datetime.now(datetime.timezone.utc).replace(tzinfo=UTC)
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
            logging.info(f"Received on {msg.topic} → {entry}")
        if config.get("log_sqlite"):
            conn = sqlite3.connect(os.path.join(PROJECT_ROOT, "data", "weather.db"))
            cursor = conn.cursor()
            cursor.execute('''
                INSERT or REPLACE INTO weather_data (timestamp, temperature, humidity, pressure)
                VALUES (?, ?, ?, ?)
            ''', (entry["timestamp"], entry["temperature"], entry["humidity"], entry["pressure"]))
            conn.commit()


    client = mqtt.Client()
    client.enable_logger()
    if 'username' in config and 'password' in config:
        client.username_pw_set(config['username'], config['password'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config['broker_url'], config['port'])
    client.loop_start()