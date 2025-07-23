from threading import Thread
from collections import deque
from flask import Flask, render_template, request, jsonify
from subscriber import start_subscriber
from utils import load_config
import csv
import os
from pathlib import Path

# Get the directory where the script is running from
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # weather-dashboard directory

config = load_config("myconfig.yaml")

app = Flask(__name__, 
           template_folder=os.path.join(PROJECT_ROOT, "templates"), 
           static_folder=os.path.join(PROJECT_ROOT, "static"))
buffer = deque(maxlen=config.get("buffer_size", 100))

@app.route('/data')
def data():
    # If CSV‐logging is on, read the last N rows from the file instead of in‑memory buffer
    if config.get("log_csv", False):
        csv_path = os.path.join(PROJECT_ROOT, "data", "weather_data.csv")
        if os.path.exists(csv_path):
            rows = []
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                all_rows = list(reader)
                
            # only keep the last buffer_size rows
            for row in all_rows[-config["buffer_size"]:]:
                # convert strings back to appropriate types
                rows.append({
                    "timestamp": row["timestamp"],
                    "temperature": float(row["temperature"]),
                    "humidity": float(row["humidity"]),
                    "pressure": float(row["pressure"])
                })
            return jsonify(rows)
        # fall back if file is missing
    return jsonify(list(buffer))
        
        

@app.route('/')
def index():
    return render_template('index.html', port=config.get("port", 5000))

def main():
    t = Thread(target=start_subscriber, args=(config, buffer), daemon=True)
    t.start()
    
    app.run(host="0.0.0.0", port=config.get("port", 5000))
    
if __name__ == "__main__":
    main()
    
