from threading import Thread
from collections import deque
from flask import Flask, render_template, request, jsonify
from subscriber import start_subscriber
from utils import load_config

config = load_config("myconfig.yaml")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
buffer = deque(maxlen=config.get("buffer_size", 100))

@app.route('/data')
def data():
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
    
