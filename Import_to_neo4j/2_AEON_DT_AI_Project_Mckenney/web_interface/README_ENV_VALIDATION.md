# Environment Validation System

## Quick Start

```bash
# 1. Setup environment
cp .env.example .env.local

# 2. Validate configuration
npx tsx scripts/validate-env.ts

# 3. Start application (auto-validates)
npm run dev
```

## Features

✅ Automatic startup validation via Next.js instrumentation  
✅ Validates all database connections (Neo4j, MySQL, Qdrant, MinIO)  
✅ Type-safe environment access with TypeScript  
✅ Production security warnings  
✅ Clear error messages with actionable feedback  
✅ Comprehensive test suite  

## Files

- `/lib/env-validation.ts` - Main validation logic
- `/lib/init.ts` - Application initialization
- `/instrumentation.ts` - Next.js startup hook
- `/tests/env-validation.test.ts` - Test suite
- `/scripts/validate-env.ts` - Standalone validation
- `/docs/environment-validation.md` - Full documentation
- `/docs/ENV_VALIDATION_QUICK_START.md` - Quick start guide

## Required Variables

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

## Usage

### Automatic (Default)
Validation runs automatically on startup. No code needed.

### Manual in Code
```typescript
import { validateEnvOrThrow, getEnv } from '@/lib/env-validation';

const env = validateEnvOrThrow();
console.log(env.NEO4J_URI);  // Type-safe
```

### Run Tests
```bash
npm test tests/env-validation.test.ts
```

## Documentation

See `/docs/environment-validation.md` for complete documentation.

## Status: PRODUCTION READY ✅
