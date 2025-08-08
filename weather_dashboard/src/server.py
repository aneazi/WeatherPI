from threading import Thread
from collections import deque
from flask import Flask, render_template, request, jsonify, g
from subscriber import start_subscriber
from utils import load_config
import os
import sqlite3

# Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # weather-dashboard directory
config = load_config("myconfig.yaml")

data_dir = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(data_dir, config.get("db_name"))

# Ensure data directory exists
if config.get("log_sqlite"):
    os.makedirs(data_dir, exist_ok=True)

# Flask app
app = Flask(
    __name__, 
    template_folder=os.path.join(PROJECT_ROOT, "templates"), 
    static_folder=os.path.join(PROJECT_ROOT, "static")
)
buffer = deque(maxlen=config.get("buffer_size", 100))

# Database helper
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DB_PATH, check_same_thread=False)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

@app.teardown_appcontext
def close_db(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/data')
def data():
    if config.get("log_sqlite"):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
              FROM weather_data
             ORDER BY timestamp DESC
             LIMIT ?
            """,
            (config["buffer_size"],)
        )
        rows = [dict(r) for r in cursor.fetchall()]
        # reverse so oldest→newest
        return jsonify(list(reversed(rows)))
    return jsonify(list(buffer))

@app.route('/')
def index():
    return render_template('index.html', port=config.get("port", 5000))

def main():
    # Start MQTT subscriber in background
    t = Thread(target=start_subscriber, args=(config, buffer), daemon=True)
    t.start()
    # Run Flask
    app.run(host="0.0.0.0", port=config.get("port", 5000))

if __name__ == "__main__":
    main()