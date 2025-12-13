# Qdrant Integration

## Credentials

- Username: jim
- Password: jim

## Endpoint

- Proxy: http://localhost:8000/qdrant/{path:path}
- Direct: http://localhost:6333 (internal: qdrant:6333)

## Curl Examples

### Health Check

```bash
curl -u jim:jim http://localhost:8000/qdrant/healthz
```

### Create Collection

```bash
curl -u jim:jim -X PUT http://localhost:8000/qdrant/collections/test_coll \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 384,
      "distance":