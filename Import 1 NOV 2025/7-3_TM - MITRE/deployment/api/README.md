# NER v8 MITRE API

Production-ready FastAPI backend for Named Entity Recognition using the NER v8 MITRE model.

## Model Performance

- **F1 Score**: 97.01%
- **Precision**: 94.20%
- **Recall**: 100.00%
- **Version**: v8

## Features

- ✅ RESTful API with FastAPI
- ✅ Single and batch text processing
- ✅ API key authentication
- ✅ Rate limiting (100 req/min)
- ✅ CORS configuration
- ✅ Prometheus metrics
- ✅ Health check endpoint
- ✅ Request/response validation
- ✅ Comprehensive error handling
- ✅ Production logging

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. **Create virtual environment**:
```bash
cd "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/deployment/api"
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and set your API key:
# NER_API_KEY=your-secure-api-key-here
```

4. **Verify model path**:
Ensure the model exists at:
```
/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/models/ner_v8_mitre
```

## Running the API

### Development Mode

```bash
python main.py
```

The API will be available at: `http://localhost:8000`

### Production Mode

Using Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Using Gunicorn (recommended for production):
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### 1. Health Check (Public)

**GET** `/api/v1/ner/v8/health`

Check if the API and model are operational.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "/path/to/model",
  "model_version": "v8",
  "loaded_at": "2025-11-08T20:00:00",
  "uptime_seconds": 3600.5
}
```

### 2. Model Information (Requires Auth)

**GET** `/api/v1/ner/v8/info`

**Headers**:
- `X-API-Key`: Your API key

**Response**:
```json
{
  "model_version": "v8",
  "model_path": "/path/to/model",
  "performance_metrics": {
    "f1_score": 97.01,
    "precision": 94.20,
    "recall": 100.00
  },
  "entity_labels": ["TECHNIQUE", "TACTIC", "SOFTWARE", ...],
  "pipeline_components": ["tok2vec", "ner"],
  "loaded_at": "2025-11-08T20:00:00"
}
```

### 3. Single Text Prediction (Requires Auth)

**POST** `/api/v1/ner/v8/predict`

**Headers**:
- `X-API-Key`: Your API key
- `Content-Type`: application/json

**Request Body**:
```json
{
  "text": "APT28 used credential dumping techniques to access systems."
}
```

**Response**:
```json
{
  "text": "APT28 used credential dumping techniques to access systems.",
  "entities": [
    {
      "text": "APT28",
      "label": "SOFTWARE",
      "start": 0,
      "end": 5,
      "confidence": 1.0
    },
    {
      "text": "credential dumping",
      "label": "TECHNIQUE",
      "start": 11,
      "end": 29,
      "confidence": 1.0
    }
  ],
  "processing_time_ms": 45.2,
  "model_version": "v8"
}
```

### 4. Batch Prediction (Requires Auth)

**POST** `/api/v1/ner/v8/batch`

**Headers**:
- `X-API-Key`: Your API key
- `Content-Type`: application/json

**Request Body**:
```json
{
  "texts": [
    "APT28 used credential dumping.",
    "The attack involved lateral movement.",
    "Ransomware encrypted the files."
  ]
}
```

**Response**:
```json
{
  "results": [
    {
      "text": "APT28 used credential dumping.",
      "entities": [...],
      "processing_time_ms": 0,
      "model_version": "v8"
    },
    ...
  ],
  "total_processing_time_ms": 120.5,
  "model_version": "v8"
}
```

### 5. Prometheus Metrics (Public)

**GET** `/api/v1/ner/v8/metrics`

Returns Prometheus-formatted metrics for monitoring.

## Usage Examples

### cURL Examples

**Health Check**:
```bash
curl http://localhost:8000/api/v1/ner/v8/health
```

**Single Prediction**:
```bash
curl -X POST http://localhost:8000/api/v1/ner/v8/predict \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"text": "APT28 used credential dumping techniques."}'
```

**Batch Prediction**:
```bash
curl -X POST http://localhost:8000/api/v1/ner/v8/batch \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Text 1", "Text 2", "Text 3"]}'
```

### Python Client Example

```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "your-api-key"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Single prediction
response = requests.post(
    f"{API_URL}/api/v1/ner/v8/predict",
    headers=headers,
    json={"text": "APT28 used credential dumping techniques."}
)
result = response.json()
print(f"Found {len(result['entities'])} entities")

# Batch prediction
response = requests.post(
    f"{API_URL}/api/v1/ner/v8/batch",
    headers=headers,
    json={"texts": ["Text 1", "Text 2", "Text 3"]}
)
results = response.json()
print(f"Processed {len(results['results'])} texts")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const API_URL = 'http://localhost:8000';
const API_KEY = 'your-api-key';

async function predictEntities(text) {
  try {
    const response = await axios.post(
      `${API_URL}/api/v1/ner/v8/predict`,
      { text },
      { headers: { 'X-API-Key': API_KEY } }
    );
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

// Usage
predictEntities('APT28 used credential dumping techniques.')
  .then(result => console.log(result));
```

## Configuration

### Environment Variables

Create a `.env` file with:

```bash
NER_API_KEY=your-secure-api-key-here
MODEL_PATH=/path/to/model
RATE_LIMIT_PER_MINUTE=100
LOG_LEVEL=info
```

### config.yaml

Edit `config.yaml` to customize:
- Server settings (host, port, workers)
- CORS origins
- Rate limiting
- Batch processing limits
- Monitoring options

## Security

1. **Change the default API key** in production
2. Configure CORS origins appropriately
3. Use HTTPS in production (configure SSL certificates)
4. Implement additional authentication if needed (JWT, OAuth)
5. Set up firewall rules to restrict access

## Monitoring

### Prometheus Metrics

Available at `/api/v1/ner/v8/metrics`:

- `ner_requests_total{endpoint, status}` - Total requests
- `ner_request_latency_seconds{endpoint}` - Request latency histogram
- `ner_entities_detected{entity_type}` - Total entities by type

### Logging

Logs include:
- Request/response details
- Processing times
- Error traces
- Model loading status

## Performance

- **Model Load Time**: ~2-3 seconds (one-time, cached)
- **Single Prediction**: ~40-80ms per text
- **Batch Processing**: ~100-200ms for 10 texts (using spaCy pipe)
- **Throughput**: ~100 requests/minute (configurable)

## Troubleshooting

### Model Not Loading

Check:
1. Model path is correct in config
2. Model files exist and are readable
3. spaCy is installed correctly
4. Sufficient memory available

### Rate Limit Errors

- Increase `RATE_LIMIT_PER_MINUTE` in `.env`
- Implement distributed rate limiting for multiple instances

### Performance Issues

- Increase worker count
- Use batch endpoint for multiple texts
- Enable caching for repeated requests
- Consider GPU acceleration if available

## Development

### Running Tests

```bash
pytest tests/
```

### API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## License

[Your License Here]

## Support

For issues or questions, contact [Your Contact Info]
