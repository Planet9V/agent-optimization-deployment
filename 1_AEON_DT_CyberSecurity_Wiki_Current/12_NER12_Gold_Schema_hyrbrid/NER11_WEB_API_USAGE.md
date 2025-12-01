# NER11 Gold Web API Usage Guide

## Overview
This document details how to use the NER11 Gold Standard FastAPI service for entity extraction and integration with the AEON Digital Twin.

## 1. API Access
- **Base URL**: `http://localhost:8000` (or `http://ner11-api:8000` within Docker network)
- **Authentication**: Currently open (Internal Network Only). Future versions will require API Keys via `X-API-Key` header.

## 2. Endpoints

### Extract Entities
- **URL**: `/ner`
- **Method**: `POST`
- **Payload**:
  ```json
  { "text": "The APT28 group targeted the SCADA system." }
  ```
- **Response**:
  ```json
  {
    "entities": [
      { "text": "APT28", "label": "THREAT_ACTOR", "start": 4, "end": 9 },
      { "text": "SCADA system", "label": "ICS_ASSET", "start": 29, "end": 41 }
    ],
    "doc_length": 9
  }
  ```

## 3. Python Integration Example
```python
import requests

def extract_entities(text):
    url = "http://localhost:8000/ner"
    response = requests.post(url, json={"text": text})
    return response.json()['entities']
```

## 4. Security Best Practices
- **Network Isolation**: Ensure the container is only accessible from trusted services (Neo4j, Backend).
- **TLS**: Use a reverse proxy (Nginx) for SSL/TLS termination if exposing outside the cluster.
- **Rate Limiting**: Implement rate limiting at the proxy level to prevent DoS.
