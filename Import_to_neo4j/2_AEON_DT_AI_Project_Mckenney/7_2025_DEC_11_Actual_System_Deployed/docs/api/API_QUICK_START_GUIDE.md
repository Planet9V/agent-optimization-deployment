# API Quick Start Guide

## Getting Started

This guide will help you get started with the NER11 Gold Standard API quickly.

### Base URL

```
http://localhost:8000
```

### Authentication

All API requests require authentication headers:

```bash
curl -X GET "http://localhost:8000/api/v2/endpoint" \
  -H "x-customer-id: <your_customer_id>" \
  -H "x-namespace: <your_namespace>" \
  -H "x-user-id: <your_user_id>" \
  -H "x-access-level: <read|write|admin>"
```

**Required Headers:**
- `x-customer-id`: Your customer identifier (required for all requests)
- `x-namespace`: Customer namespace (optional, but recommended)
- `x-user-id`: User identifier (optional)
- `x-access-level`: Access level (`read`, `write`, or `admin`, defaults to `read`)

### Access Levels

| Level | Permissions |
|-------|-------------|
| `read` | View data, run queries |
| `write` | Create, update resources |
| `admin` | Full access including deletion |

## Common Request Patterns

### 1. List Resources

```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms?skip=0&limit=10" \
  -H "x-customer-id: customer-123" \
  -H "x-namespace: production"
```

### 2. Get Single Resource

```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}" \
  -H "x-customer-id: customer-123"
```

### 3. Create Resource

```bash
curl -X POST "http://localhost:8000/api/v2/sbom/sboms" \
  -H "x-customer-id: customer-123" \
  -H "x-access-level: write" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My SBOM",
    "version": "1.0.0",
    "components": []
  }'
```

### 4. Update Resource

```bash
curl -X PUT "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}" \
  -H "x-customer-id: customer-123" \
  -H "x-access-level: write" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated SBOM",
    "version": "1.1.0"
  }'
```

### 5. Delete Resource

```bash
curl -X DELETE "http://localhost:8000/api/v2/sbom/sboms/{sbom_id}" \
  -H "x-customer-id: customer-123" \
  -H "x-access-level: admin"
```

## Error Handling

### Common Error Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| `400` | Bad Request | Invalid request body or parameters |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Insufficient permissions (access level too low) |
| `404` | Not Found | Resource doesn't exist |
| `422` | Unprocessable Entity | Missing required parameters or validation failed |
| `500` | Internal Server Error | Server-side error (report to developers) |

### Error Response Format

```json
{
  "detail": "Error description",
  "status_code": 422,
  "error_type": "validation_error"
}
```

### Handling 422 Errors

422 errors typically indicate missing or invalid parameters:

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Solution:** Check the `detail` array to see which fields are missing or invalid.

## Rate Limiting

- No rate limiting currently implemented
- Best practice: Batch requests when possible
- Use pagination for large datasets

## Pagination

List endpoints support pagination:

```bash
curl -X GET "http://localhost:8000/api/v2/sbom/sboms?skip=0&limit=50" \
  -H "x-customer-id: customer-123"
```

**Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 10, max: 100)

## Filtering and Search

Many endpoints support filtering:

```bash
# Search SBOMs by name
curl -X GET "http://localhost:8000/api/v2/sbom/sboms?name=myapp" \
  -H "x-customer-id: customer-123"

# Filter by date range
curl -X GET "http://localhost:8000/api/v2/sbom/sboms?created_after=2025-01-01" \
  -H "x-customer-id: customer-123"
```

## Example Workflows

### Workflow 1: Create and Analyze SBOM

```bash
# Step 1: Create SBOM
SBOM_ID=$(curl -X POST "http://localhost:8000/api/v2/sbom/sboms" \
  -H "x-customer-id: customer-123" \
  -H "x-access-level: write" \
  -H "Content-Type: application/json" \
  -d '{"name":"myapp","version":"1.0.0"}' | jq -r '.id')

# Step 2: Get vulnerability analysis
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/$SBOM_ID/vulnerabilities" \
  -H "x-customer-id: customer-123"

# Step 3: Get risk assessment
curl -X GET "http://localhost:8000/api/v2/sbom/sboms/$SBOM_ID/risks" \
  -H "x-customer-id: customer-123"
```

### Workflow 2: Compliance Check

```bash
# Step 1: List compliance frameworks
curl -X GET "http://localhost:8000/api/v2/compliance/frameworks" \
  -H "x-customer-id: customer-123"

# Step 2: Run compliance assessment
curl -X POST "http://localhost:8000/api/v2/compliance/assessments" \
  -H "x-customer-id: customer-123" \
  -H "x-access-level: write" \
  -H "Content-Type: application/json" \
  -d '{"framework_id":"nist-csf","asset_id":"asset-123"}'

# Step 3: Get compliance report
curl -X GET "http://localhost:8000/api/v2/compliance/reports/{report_id}" \
  -H "x-customer-id: customer-123"
```

## API Phases

The API is organized into phases:

### Phase B2: SBOM Analysis (36 endpoints)
Software Bill of Materials management, component analysis, dependency tracking

### Phase B3: Threat & Risk (81 endpoints)
Vulnerability management, threat intelligence, risk assessment, remediation tracking

### Phase B4: Compliance (28 endpoints)
Compliance frameworks, audit trails, control assessments

### Phase B5: Alerts & Demographics (82 endpoints)
Alert management, demographic analysis, economic indicators

### Psychometric APIs (8 endpoints)
Psychological assessments, user profiling

### Vendor & Equipment (23 endpoints)
Vendor management, equipment tracking, asset inventory

## Best Practices

1. **Always include customer-id header** - Required for all requests
2. **Use appropriate access levels** - Only request the permissions you need
3. **Handle errors gracefully** - Check status codes and parse error details
4. **Use pagination** - Don't fetch all records at once
5. **Cache responses** - Reduce unnecessary API calls
6. **Test in development** - Use test customer IDs before production
7. **Monitor rate limits** - Track your usage patterns
8. **Keep credentials secure** - Never commit API keys to version control

## Support

- **API Documentation**: See phase-specific docs for detailed endpoint information
- **OpenAPI Spec**: Available at `http://localhost:8000/openapi.json`
- **Interactive Docs**: Available at `http://localhost:8000/docs`

## Next Steps

1. Review phase-specific documentation for detailed endpoint information
2. Set up authentication with your customer ID
3. Try the example workflows above
4. Explore the interactive API docs at `/docs`

