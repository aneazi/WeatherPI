# WeatherPI
This project is made for detecting weather anomalies by making use of the Raspberry Pi Sense HAT and a lightweight Isolation Forest for realtime anomaly detection. 

The Raspberry Pi communicates with the local device by using MQTT as a pub/sub service. I used scikit-learn to create my Isolation Forest with a latency of around 5 ms. I also used Chart.js for tracking current temperature, humidity, and pressure. 

## How does it work?
The Raspberry Pi publishes to a topic according to [config.yaml](config.yaml) at the rate set by the user. It collects sensor data (temperature, pressure, humidty) and publishes to a topic which the local machine subscribes to in order to perform anomaly detection. Data is stored in an SQLite database ([weather.db](weather_dashboard/data/weather.db) for reference). This is a database consisting of 4 days of data collected in my room. I trained my initial model on this data with a contamination of 0.012 which showed the best results in terms of classifying real anomalies. 

In the [model_training](model_training) folder you can train your own model based on 4 features: timestamp, temperature, humidity, and pressure. From these four features I encoded the time with a sine and cosine function so that we can relate each time with a certain temperature (4 p.m. tends to be the hottest in the house). I also extracted a rolling mean which took an average of 5 samples (5 secinds since the sampling rate was 1 Hz), as well as differences from the previous datapoint. With these 11 features, I was able to train a model which successfully classified anomalies with a low latency.

To display these anomalies I used Chart.js to flag any time the is_anomaly flag was set. The charts are displayed on localhost port 1883. 


## Configs
Set the user configs in [config.yaml](config.yaml).

## On Raspberry Pi
How to build publisher container (from project root dir):
```
docker build \
  -t pi_publisher:latest \
  -f pi_publisher/Dockerfile \
  .
```

How to run publisher container (from root dir):
```
docker run -d \
  --name pi_publisher \
  --restart unless-stopped \
  --privileged \
  -v $(pwd)/config.yaml:/app/config.yaml:ro \
  -v $(pwd)/pi_publisher/src:/app/src:ro \
  pi_publisher:latest
```

How to start publisher container:
```
docker start pi_publisher
```

## On Local Device for Anomaly Detection

### How to setup the server:
```
pip install -r requirements.txt
python weather_dashboard/src/server.py
```
### How to train your own model based on current environment:
```
python model_training/train.py
```
The output file will be saved to the [models](model_training/models/) folder.