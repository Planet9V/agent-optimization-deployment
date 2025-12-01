# Deployment Tests - Quick Start Guide

## Prerequisites

Ensure all 4 services are running:
- ✅ Neo4j (bolt://localhost:7687)
- ✅ MySQL (localhost:3306)
- ✅ Qdrant (http://localhost:6333)
- ✅ MinIO (http://localhost:9000)

## 5-Minute Setup

### 1. Install Dependencies (First Time Only)
```bash
npm install
```

### 2. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your actual credentials
nano .env
```

### 3. Run Tests
```bash
# Quick validation (recommended)
npm run validate:deployment

# Or run all tests
npm run test:deployment
```

## What Gets Tested

### ✅ Environment Validation (~1 second)
- All required environment variables present
- Valid URL/port formats
- Security checks (no default passwords in production)
- Network hostname resolution

### ✅ Service Connectivity (~5-10 seconds)
- **Neo4j**: Connection + query execution + concurrent operations
- **MySQL**: Connection + SQL queries + transactions
- **Qdrant**: Connection + collection operations + vector search
- **MinIO**: Connection + bucket operations + object storage

### ✅ Health Endpoint (~2-3 seconds)
- Response format validation
- All service statuses reported correctly
- Response time < 5 seconds
- System status logic (healthy/degraded/unhealthy)

## Expected Output

### ✅ All Tests Passing
```
PASS  tests/deployment/environment-validation.test.ts
PASS  tests/deployment/service-connectivity.test.ts
PASS  tests/deployment/health-check.test.ts

Test Suites: 3 passed, 3 total
Tests:       87 passed, 87 total
Time:        12.456 s
```

### ❌ If Services Are Down
```
FAIL  tests/deployment/service-connectivity.test.ts
  ● Neo4j Connectivity › should connect to Neo4j
    Connection refused: bolt://localhost:7687
```

**Fix**: Start the missing service and re-run tests.

## Individual Test Commands

```bash
# Test environment only
npm run test:env

# Test service connectivity only
npm run test:connectivity

# Test health endpoint only
npm run test:health
```

## Troubleshooting

### "Connection refused"
1. Check service is running: `docker ps` or `systemctl status <service>`
2. Verify port is correct in .env
3. Check firewall: `sudo ufw status`

### "Authentication failed"
1. Verify credentials in .env match service configuration
2. For Neo4j: Check if default password changed
3. For MySQL: Verify user has correct permissions

### "Timeout"
1. Services may be slow to start
2. Increase timeout in test files (TIMEOUT constant)
3. Check system resources (CPU/memory)

### "Environment variable not defined"
1. Ensure .env file exists: `ls -la .env`
2. Check variable names match .env.example
3. Restart terminal to reload environment

## Pre-Deployment Checklist

Before deploying to production:

```bash
# 1. Run full validation
npm run validate:deployment

# 2. Check for security issues
npm run test:env | grep -i "production"

# 3. Verify health endpoint works
curl http://localhost:3000/api/health | jq

# 4. Test under load (optional)
for i in {1..10}; do curl http://localhost:3000/api/health & done
```

All tests should pass ✅ before deployment!

## Next Steps

After tests pass:
1. ✅ Tests validate deployment → Ready for production
2. 🚀 Deploy application
3. 📊 Monitor health endpoint
4. 🔄 Run tests post-deployment to verify

## Support

For detailed documentation, see:
- [README.md](./README.md) - Complete test suite documentation
- [Environment Setup](../../.env.example) - Configuration reference
- [Health API](../../src/app/api/health/route.ts) - Health endpoint implementation
