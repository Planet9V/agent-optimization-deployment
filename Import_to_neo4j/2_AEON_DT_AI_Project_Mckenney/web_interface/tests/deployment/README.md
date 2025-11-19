# Deployment Validation Test Suite

Comprehensive test suite for validating deployment health and service connectivity.

## Overview

This test suite validates:
- ✅ All 4 service connections (Neo4j, MySQL, Qdrant, MinIO)
- ✅ Health endpoint response format and accuracy
- ✅ Environment variable presence and security
- ✅ Network connectivity and response times
- ✅ Service operation functionality

## Test Files

### 1. health-check.test.ts
Validates the `/api/health` endpoint:
- Response format validation
- Service status reporting
- Response time benchmarks (<5 seconds)
- System status logic (healthy/degraded/unhealthy)
- Error handling

### 2. service-connectivity.test.ts
Validates actual connectivity to all 4 services:
- **Neo4j**: Connection, query execution, concurrent operations
- **MySQL**: Connection, SQL queries, transactions
- **Qdrant**: Connection, collection operations, vector search
- **MinIO**: Connection, bucket/object operations
- **Cross-Service**: All services available simultaneously

### 3. environment-validation.test.ts
Validates environment configuration:
- Required environment variables present
- Valid format for URLs, ports, credentials
- Security checks (no default passwords in production)
- Network hostname resolution
- Configuration completeness

## Running Tests

### Quick Validation
```bash
# Run all deployment tests
npm run test:deployment

# Run complete validation sequence
npm run validate:deployment
```

### Individual Test Suites
```bash
# Health check only
npm run test:health

# Service connectivity only
npm run test:connectivity

# Environment validation only
npm run test:env
```

### Advanced Options
```bash
# Watch mode for development
npm run test:watch tests/deployment

# With coverage report
npm run test:coverage -- tests/deployment

# Verbose output
npm run test:deployment -- --verbose

# Run specific test
jest tests/deployment/health-check.test.ts -t "should respond within 5 seconds"
```

## Environment Setup

### Required Environment Variables

Create a `.env` file with:

```bash
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=aeon_db

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key  # Optional for local

# MinIO
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_USE_SSL=false

# Application
NODE_ENV=development
PORT=3000
API_BASE_URL=http://localhost:3000
```

### Production Environment

For production deployments, ensure:
- ✅ Strong passwords (12+ chars, mixed case, numbers, symbols)
- ✅ No default credentials (neo4j, root, minioadmin)
- ✅ HTTPS/SSL enabled for all services
- ✅ No localhost references in URLs
- ✅ API keys for Qdrant configured

## Test Expectations

### Response Time Benchmarks
- Health endpoint: <5 seconds
- Individual services: <2 seconds
- 5 consecutive health checks: <10 seconds

### Service Connectivity
All services must:
- ✅ Establish connection successfully
- ✅ Execute basic operations
- ✅ Handle concurrent requests
- ✅ Support service-specific operations

### Security Requirements
Production must have:
- ✅ Passwords ≥12 characters
- ✅ Password complexity (3+ character types)
- ✅ No default credentials
- ✅ SSL/TLS enabled
- ✅ No localhost/127.0.0.1 in URLs

## Troubleshooting

### Test Failures

#### "Connection refused"
- Ensure service is running
- Check host/port configuration
- Verify network connectivity
- Check firewall rules

#### "Authentication failed"
- Verify credentials in `.env`
- Check service user permissions
- Confirm database/schema exists

#### "Timeout"
- Increase timeout in test file (TIMEOUT constant)
- Check service performance
- Verify network latency

#### "Environment variable not defined"
- Create `.env` file
- Copy from `.env.example`
- Source environment variables

### Service-Specific Issues

#### Neo4j
```bash
# Test connection manually
cypher-shell -a bolt://localhost:7687 -u neo4j -p password
```

#### MySQL
```bash
# Test connection manually
mysql -h localhost -u root -p
```

#### Qdrant
```bash
# Test connection manually
curl http://localhost:6333/collections
```

#### MinIO
```bash
# Test connection manually
mc alias set local http://localhost:9000 minioadmin minioadmin
mc ls local
```

## CI/CD Integration

### Docker Compose
```yaml
version: '3.8'
services:
  test-runner:
    build: .
    environment:
      - NODE_ENV=test
    depends_on:
      - neo4j
      - mysql
      - qdrant
      - minio
    command: npm run validate:deployment
```

### GitHub Actions
```yaml
- name: Run deployment tests
  run: npm run validate:deployment
  env:
    NEO4J_URI: ${{ secrets.NEO4J_URI }}
    MYSQL_PASSWORD: ${{ secrets.MYSQL_PASSWORD }}
    # ... other secrets
```

### Pre-deployment Validation
```bash
#!/bin/bash
# pre-deploy.sh

echo "Validating deployment environment..."
npm run test:env || exit 1

echo "Testing service connectivity..."
npm run test:connectivity || exit 1

echo "Validating health endpoint..."
npm run test:health || exit 1

echo "✅ Deployment validation passed!"
```

## Test Development

### Adding New Tests

1. Create test file in `tests/deployment/`
2. Import test utilities from `../setup.ts`
3. Use global `testUtils` for retry logic
4. Follow existing patterns for consistency

### Test Utilities

Available in all tests:
```typescript
// Sleep
await global.testUtils.sleep(1000);

// Retry with backoff
const result = await global.testUtils.retry(
  () => fetch('/api/health'),
  3,  // max attempts
  1000 // delay ms
);

// Wait for condition
await global.testUtils.waitFor(
  () => service.isReady(),
  5000,  // timeout ms
  100    // check interval ms
);
```

## Performance Monitoring

### Benchmark Results
Track test execution times:
```bash
# Run with timing
npm run test:deployment -- --verbose 2>&1 | grep "Time:"
```

Expected times:
- Health checks: 2-3 seconds
- Service connectivity: 5-10 seconds
- Environment validation: <1 second
- Full suite: 10-15 seconds

## Support

For issues or questions:
1. Check service logs
2. Verify environment configuration
3. Review test output for specific failures
4. Check network connectivity
5. Consult service-specific documentation

## License

Part of AEON Digital Twin Cybersecurity Dashboard
