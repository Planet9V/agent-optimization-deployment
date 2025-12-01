# Environment Validation - Quick Start Guide

## Setup (30 seconds)

### 1. Copy Environment Template
```bash
cp .env.example .env.local
```

### 2. Edit Required Variables
```bash
nano .env.local
```

Minimum required configuration:
```bash
# Neo4j
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg

# MySQL
MYSQL_HOST=openspg-mysql
MYSQL_DATABASE=openspg
MYSQL_USER=root
MYSQL_PASSWORD=openspg

# Qdrant
QDRANT_URL=http://openspg-qdrant:6333

# MinIO
MINIO_ENDPOINT=http://openspg-minio:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
```

### 3. Validate Configuration
```bash
npx tsx scripts/validate-env.ts
```

### 4. Start Application
```bash
npm run dev
```

## Expected Output

### ✅ Success
```
🚀 Initializing AEON Digital Twin Dashboard...

✅ Environment validation successful

📋 Configuration summary:
   - Environment: production
   - Neo4j: bolt://openspg-neo4j:7687
   - MySQL: openspg-mysql:3306
   - Qdrant: http://openspg-qdrant:6333
   - MinIO: http://openspg-minio:9000
   - Port: 3000
```

### ❌ Failure
```
❌ Environment validation failed

Missing or invalid environment variables:
   - NEO4J_URI: Required
   - MYSQL_HOST: MySQL host is required

📖 Please check .env.example for required variables
```

## Common Issues

### Issue: "NEO4J_URI: Must be a valid Neo4j URI"
**Solution**: Ensure URI starts with `bolt://` or `neo4j://`
```bash
# ✅ Correct
NEO4J_URI=bolt://localhost:7687

# ❌ Wrong
NEO4J_URI=localhost:7687
```

### Issue: "Port must be between 1 and 65535"
**Solution**: Use valid port numbers
```bash
# ✅ Correct
MYSQL_PORT=3306

# ❌ Wrong
MYSQL_PORT=99999
```

### Issue: "QDRANT_URL: Must be a valid URL"
**Solution**: Include protocol
```bash
# ✅ Correct
QDRANT_URL=http://localhost:6333

# ❌ Wrong
QDRANT_URL=localhost:6333
```

## Production Checklist

Before deploying to production:

- [ ] Copy `.env.example` to `.env.local`
- [ ] Set all required variables
- [ ] Change `NEXTAUTH_SECRET` from default
- [ ] Set `QDRANT_API_KEY` for security
- [ ] Configure `DATABASE_URL` if using Neon
- [ ] Set up authentication (Clerk or NextAuth)
- [ ] Run validation: `npx tsx scripts/validate-env.ts`
- [ ] Check for warnings
- [ ] Test build: `npm run build`

## Helper Functions

```typescript
import {
  isDevelopment,
  isProduction,
  isDebugEnabled,
  getEnv
} from '@/lib/env-validation';

if (isDevelopment()) {
  console.log('Dev mode');
}

const env = getEnv();
console.log(env.NEO4J_URI);  // Type-safe
```

## Documentation

- **Full Guide**: `/docs/environment-validation.md`
- **Implementation Summary**: `/docs/ENV_VALIDATION_IMPLEMENTATION.md`
- **This Quick Start**: `/docs/ENV_VALIDATION_QUICK_START.md`

## Support

If validation fails:
1. Check error messages for specific issues
2. Verify `.env.local` exists
3. Compare with `.env.example`
4. Ensure no typos in variable names
5. Check variable values match expected formats
6. Review documentation for validation rules

## Status

✅ **READY FOR USE**
- Automatic validation on startup
- Comprehensive error messages
- Production warnings
- Type-safe environment access
