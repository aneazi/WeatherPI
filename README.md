# WeatherPI

How to start container (from pi-publisher dir):
sudo docker build -t pi-publisher:latest .


How to run container (from pi-publisher dir):
sudo docker run -d \
  --name pi-publisher \
  --restart unless-stopped \
  --device /dev/i2c-1:/dev/i2c-1 \
  --device /dev/spidev0.0:/dev/spidev0.0 \
  -v $(pwd)/config.yaml:/app/config.yaml:ro \
  -v $(pwd)/src:/app/src:ro \
  pi-publisher:latest