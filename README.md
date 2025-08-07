# WeatherPI



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
