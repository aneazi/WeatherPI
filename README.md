# WeatherPI

## On Raspberry Pi
How to build publisher container (from pi-publisher dir):
```
sudo docker build \
  -t pi-publisher:latest \
  -f pi-publisher/Dockerfile \
  .

```

How to run publisher container (from root dir):
```
sudo docker run -d \
  --name pi-publisher \
  --restart unless-stopped \
  --privileged \
  -v $(pwd)/myconfig.yaml:/app/myconfig.yaml:ro \
  -v $(pwd)/src:/app/src:ro \
  pi-publisher:latest
```
