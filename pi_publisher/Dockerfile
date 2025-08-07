# Use an ARM‑compatible Python base
FROM arm32v7/python:3.8-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1) Install system packages & build tools (incl. Git for RTIMULib source)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      python3-dev \
      python3-smbus \
      i2c-tools \
      python3-yaml \
      python3-pip \
      git \
      libjpeg-dev \
      zlib1g-dev \
      libtiff5-dev \
      libfreetype6-dev \
      libwebp-dev \
      libopenjp2-7-dev \
      libatlas-base-dev \
      gfortran \
    && rm -rf /var/lib/apt/lists/*

# 2) Install Python packages via pip
RUN pip3 install --no-cache-dir \
      sense-hat \
      paho-mqtt \
      PyYAML \
      pillow

# 3) Install RTIMULib (C library + Python bindings) from upstream source
RUN git clone https://github.com/RPi-Distro/RTIMULib.git /tmp/RTIMULib && \
    cd /tmp/RTIMULib/Linux/python && \
    pip3 install --no-cache-dir . && \
    rm -rf /tmp/RTIMULib

# 4) Set working directory
WORKDIR /app

# 5) Copy in your default config (optional, overridden by bind‑mount)
COPY myconfig.yaml ./myconfig.yaml

# 6) Copy in your source code (overridden by bind‑mount if you choose)
COPY src/ ./src/

# 7) Run your publisher (referencing the path inside /app)
CMD ["python3", "-u", "src/publisher.py"]
