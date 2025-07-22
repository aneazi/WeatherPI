# WeatherPI

## On Raspberry Pi
How to build publisher container (from pi-publisher dir):
```
docker build \
  -t pi-publisher:latest \
  -f pi-publisher/Dockerfile \
  .

```

How to run publisher container (from root dir):
```
docker run -d \
  --name pi-publisher \
  --restart unless-stopped \
  --privileged \
  -v $(pwd)/myconfig.yaml:/app/config.yaml:ro \
  -v $(pwd)/pi-publisher/src:/app/src:ro \
  pi-publisher:latest
```
