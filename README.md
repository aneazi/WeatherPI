# WeatherPI

## On Raspberry Pi
How to build publisher container (from pi-publisher dir):
```
sudo docker build -t pi-publisher:latest -f pi-publisher/Dockerfile .

```

How to run publisher container (from root dir):
```
sudo docker run -d \
  --name pi-publisher \
  --restart unless-stopped \
  --device /dev/i2c-1:/dev/i2c-1 \
  --device /dev/spidev0.0:/dev/spidev0.0 \
  --device /dev/fb1:/dev/fb1 \
  --device /dev/input/event7:/dev/input/event7 \
  -v $(pwd)/myconfig.yaml:/app/myconfig.yaml:ro \
  -v $(pwd)/src:/app/src:ro \
  pi-publisher:latest
```
