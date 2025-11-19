# NER v9 Comprehensive MITRE API

Production deployment of the NER v9 model with 18 comprehensive entity types for MITRE ATT&CK and cybersecurity framework recognition.

## Features

- **18 Entity Types**: Comprehensive coverage of MITRE ATT&CK, CVE, CWE, CAPEC, OWASP, and more
- **REST API**: FastAPI-based production API with OpenAPI documentation
- **Confidence Filtering**: Configurable confidence threshold for entity extraction
- **Batch Processing**: Efficient batch entity extraction
- **Authentication**: API key and Clerk JWT support
- **Monitoring**: Prometheus metrics integration
- **Performance**: Average processing time ~3ms per text
- **Production Ready**: Docker deployment with health checks

## Supported Entity Types

1. **ATTACK_TECHNIQUE** - MITRE ATT&CK technique identifiers
2. **CAPEC** - Common Attack Pattern Enumeration
3. **CVE** - Common Vulnerabilities and Exposures
4. **CWE** - Common Weakness Enumeration
5. **DATA_SOURCE** - Security data sources
6. **EQUIPMENT** - Security equipment
7. **HARDWARE_COMPONENT** - Hardware components
8. **INDICATOR** - Indicators of compromise
9. **MITIGATION** - Security mitigations
10. **OWASP** - OWASP classifications
11. **PROTOCOL** - Network protocols
12. **SECURITY** - Security concepts
13. **SOFTWARE** - Software applications
14. **SOFTWARE_COMPONENT** - Software components
15. **THREAT_ACTOR** - Threat actors
16. **VENDOR** - Security vendors
17. **VULNERABILITY** - Security vulnerabilities
18. **WEAKNESS** - Security weaknesses

## Quick Start

### Option 1: Direct Python Execution

```bash
# Install dependencies
cd deployment/api_v9
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the API server
python main.py
```

### Option 2: Using Start Script

```bash
cd deployment/api_v9
chmod +x start.sh
./start.sh
```

### Option 3: Docker Deployment

```bash
cd deployment/api_v9
docker-compose up -d
```

## API Endpoints

### Health Check
```bash
GET /api/v9/ner/health
```

### Model Information
```bash
GET /api/v9/ner/info
Headers: x-api-key: YOUR_API_KEY
```

### Entity Types List
```bash
GET /api/v9/ner/entity-types
Headers: x-api-key: YOUR_API_KEY
```

### Extract Entities
```bash
POST /api/v9/ner/extract
Headers: x-api-key: YOUR_API_KEY
Body: {
  "text": "APT29 exploited CVE-2021-44228 vulnerability",
  "confidence_threshold": 0.8
}
```

### Batch Extract
```bash
POST /api/v9/ner/batch
Headers: x-api-key: YOUR_API_KEY
Body: {
  "texts": ["text1", "text2", "text3"],
  "confidence_threshold": 0.8
}
```

### Prometheus Metrics
```bash
GET /api/v9/ner/metrics
```

## Configuration

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit the configuration:

```env
NER_API_KEY=your-secure-api-key
CLERK_ENABLED=false
CLERK_SECRET_KEY=your-clerk-secret-key
HOST=0.0.0.0
PORT=8001
WORKERS=4
RATE_LIMIT=100
LOG_LEVEL=INFO
```

## Testing

### Test Model Loading
```bash
cd deployment/api_v9
source venv/bin/activate
python test_model.py
```

### Test API Endpoints
```bash
# Start the API server first
python main.py

# In another terminal, run tests
python test_api.py
```

## Authentication

### API Key Authentication
```bash
curl -X POST http://localhost:8001/api/v9/ner/extract \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test text", "confidence_threshold": 0.8}'
```

### Clerk JWT Authentication
```bash
curl -X POST http://localhost:8001/api/v9/ner/extract \
  -H "x-api-key: Bearer YOUR_CLERK_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test text"}'
```

## Monitoring

### Prometheus Metrics

Access metrics at: http://localhost:8001/api/v9/ner/metrics

Metrics include:
- `ner_v9_requests_total` - Total requests by endpoint and status
- `ner_v9_request_latency_seconds` - Request latency histogram
- `ner_v9_entities_detected` - Entities detected by type

### Docker Monitoring

Prometheus is included in the Docker Compose setup:
- Prometheus UI: http://localhost:9091
- Grafana can be added for visualization

## Performance

- **Model Load Time**: ~0.2 seconds
- **Average Processing**: ~3ms per text
- **Batch Processing**: Efficient with spaCy's pipe
- **Entity Recognition**: 18 comprehensive types
- **Production Ready**: Tested and validated

## Model Details

- **Version**: v9 Comprehensive
- **Framework**: spaCy 3.7.2
- **Architecture**: Transition-Based Parser with HashEmbedCNN
- **Training**: Optimized for MITRE ATT&CK and cybersecurity entities
- **Entity Types**: 18 comprehensive categories
- **Model Path**: `/models/ner_v9_comprehensive`

## Deployment Status

✅ Model deployed and operational
✅ All 18 entity types verified
✅ API endpoints functional
✅ Authentication integrated (API key + Clerk JWT)
✅ Monitoring configured
✅ Docker deployment ready
✅ Performance validated (~3ms average)

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8001/api/v9/docs
- ReDoc: http://localhost:8001/api/v9/redoc

## Support

For issues or questions, refer to:
- Model documentation: `/models/ner_v9_comprehensive/`
- API source: `main.py`
- Test suite: `test_api.py`
- Model validation: `test_model.py`
