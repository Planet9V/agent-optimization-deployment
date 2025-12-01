# NER11 Gold Standard API Reference

## Overview
The NER11 Gold Standard API provides a high-performance interface for Named Entity Recognition (NER) using the custom-trained NER11 model. It is built with FastAPI and designed for easy integration into data pipelines.

## Base URL
`http://localhost:8000`

## Endpoints

### 1. Extract Entities
**POST** `/ner`

Extracts named entities from the provided text.

**Request Body:**
```json
{
  "text": "The APT28 group used X-Agent malware to target the DNC server."
}
```

**Response:**
```json
{
  "entities": [
    {
      "text": "APT28",
      "label": "THREAT_ACTOR",
      "start": 4,
      "end": 9,
      "score": 1.0
    },
    {
      "text": "X-Agent",
      "label": "MALWARE",
      "start": 21,
      "end": 28,
      "score": 1.0
    },
    {
      "text": "DNC server",
      "label": "TARGET",
      "start": 51,
      "end": 61,
      "score": 1.0
    }
  ],
  "doc_length": 13
}
```

### 2. Health Check
**GET** `/health`

Checks if the API is running and the model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model": "loaded"
}
```

### 3. Model Info
**GET** `/info`

Returns metadata about the loaded model.

**Response:**
```json
{
  "model_name": "NER11 Gold Standard",
  "version": "3.0",
  "pipeline": ["transformer", "ner"],
  "labels": ["THREAT_ACTOR", "MALWARE", "VULNERABILITY", ...]
}
```

## Error Handling

- **503 Service Unavailable**: Model not loaded.
- **422 Validation Error**: Invalid request format.
