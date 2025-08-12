# WeatherSense
This project is made for detecting weather anomalies by making use of the Raspberry Pi Sense HAT and a lightweight Isolation Forest for realtime anomaly detection. 

The Raspberry Pi communicates with the local device by using MQTT as a pub/sub service. I used scikit-learn to create my Isolation Forest with a latency of around 5 ms. I also used Chart.js for tracking current temperature, humidity, and pressure. 

## How does it work?
The Raspberry Pi publishes to a topic according to [`config.yaml`](config.yaml) at the rate set by the user. It collects sensor data (temperature, pressure, humidity) and publishes to a topic which the local machine subscribes to in order to perform anomaly detection. Data is stored in an SQLite database ([`weather.db`](weather_dashboard/data/weather.db) for reference). This is a database consisting of 4 days of data collected in my room. I trained my initial model on this data with a contamination of 0.012 which showed the best results in terms of classifying real anomalies. 

In the [`model_training`](model_training) folder you can train your own model based on 4 features: timestamp, temperature, humidity, and pressure. From these four features I encoded the time with a sine and cosine function so that we can relate each time with a certain temperature (4 p.m. tends to be the hottest in the house). I also extracted a rolling mean which took an average of 5 samples (5 seconds since the sampling rate was 1 Hz), as well as differences from the previous datapoint. With these 11 features, I was able to train a model which successfully classified anomalies with a low latency.

To display these anomalies I used Chart.js to flag any time the is_anomaly flag was set. Additionally, there is a chart for scoring how close each event is to an anomaly. The charts are displayed on [http://localhost:8000](http://localhost:8000). 


## Configurations

Edit [`config.yaml`](config.yaml) to set:
- MQTT broker address and port
- Publish interval
- Topic names
- Model path

## Raspberry Pi - Publisher
**Build image**:
```bash
docker build \
  -t pi_publisher:latest \
  -f pi_publisher/dockerfile \
  .
```

**Run container**:
```bash
docker run -d \
  --name pi_publisher \
  --restart unless-stopped \
  --privileged \
  -v $(pwd)/config.yaml:/app/config.yaml:ro \
  -v $(pwd)/pi_publisher/src:/app/src:ro \
  pi_publisher:latest
```

**Start:**
```bash
docker start pi_publisher
```

**Stop:**
```bash
docker stop pi_publisher
```

## Local Device - Anomaly Detection Dashboard

**Build Image:**
```bash
docker build -f weather_dashboard/dockerfile -t weathersense-dashboard .
```

**Run container:**
```bash
docker run -d --name weathersense \
  -p 8000:8000 weathersense-dashboard
```

**Start:**
```bash
docker start weathersense
```

**Stop:**
```bash
docker stop weathersense
```
**View dashboard:**  
Visit [http://localhost:8000](http://localhost:8000)


## Training your own model:
To train a model using your current environment data:
```bash
python model_training/train.py
```
  - Output is saved to [`models`](model_training/models/) folder by default but the pasth can be set in the [`config.yaml`](config.yaml).
  - **Note:** If you replace the model inside the container, you may need to rebuild the image for changes to take effect.