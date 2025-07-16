# Use an ARM‑compatible Python base
FROM arm32v7/python:3.8-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy config and source code
COPY config.yaml ./
COPY src/ ./src

# Run the publisher script
CMD ["python", "src/publisher.py"]