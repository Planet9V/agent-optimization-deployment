# Container Operations Guide

## Overview
This guide covers the lifecycle management of the NER11 Gold Standard API container, including building, running, stopping, and debugging.

## 1. Building the Container

Navigate to the `docker` directory and run:

```bash
cd docker
./build_and_run.sh
```

Or manually:

```bash
docker build -t ner11-gold-api .
```

## 2. Running the Container

Start the container in detached mode (background):

```bash
docker run -d \
  --name ner11-api \
  -p 8000:8000 \
  --gpus all \
  ner11-gold-api
```

*Note: Remove `--gpus all` if running on a CPU-only machine.*

## 3. Stopping the Container

```bash
docker stop ner11-api
docker rm ner11-api
```

## 4. Maintenance & Diagnostics

### View Logs
Check the application logs for errors or access records:

```bash
docker logs -f ner11-api
```

### Access Shell
Enter the running container for debugging:

```bash
docker exec -it ner11-api bash
```

### Check Resource Usage
Monitor CPU and Memory usage:

```bash
docker stats ner11-api
```

## 5. Health Check

Verify the service is up:

```bash
curl http://localhost:8000/health
```

Expected output: `{"status":"healthy","model":"loaded"}`
