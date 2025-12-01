# Environment Validation

Comprehensive environment variable validation system for the AEON Digital Twin Dashboard.

## Overview

The environment validation system ensures all required configuration is present and valid before the application starts. This prevents runtime errors and provides clear feedback about missing or misconfigured variables.

## Features

- ✅ **Comprehensive Validation**: Validates all required and optional environment variables
- ✅ **Schema Validation**: Uses Zod for type-safe validation with detailed error messages
- ✅ **Connection String Validation**: Validates database URLs, Neo4j URIs, and API endpoints
- ✅ **Production Warnings**: Warns about security issues and missing recommended variables
- ✅ **Clear Error Messages**: Provides actionable feedback for configuration issues
- ✅ **Type Safety**: Exports TypeScript types for validated environment
- ✅ **Automatic Startup**: Integrates with Next.js instrumentation for automatic validation

## Required Variables

### Neo4j (Graph Database)
```bash
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg
NEO4J_DATABASE=neo4j
```

### MySQL (Relational Database)
```bash
MYSQL_HOST=openspg-mysql
MYSQL_PORT=3306
MYSQL_DATABASE=openspg
MYSQL_USER=root
MYSQL_PASSWORD=openspg
```

### Qdrant (Vector Database)
```bash
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY=your-api-key  # Optional but recommended
```

### MinIO (Object Storage)
```bash
MINIO_ENDPOINT=http://openspg-minio:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false
```

## Optional Variables

### PostgreSQL (Neon Database)
```bash
DATABASE_URL=postgresql://user:pass@host:5432/database
```

### Authentication (NextAuth)
```bash
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
```

### Authentication (Clerk)
```bash
CLERK_SECRET_KEY=your-clerk-secret
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-public-key
```

### Redis (Queue System)
```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
```

### Application Configuration
```bash
NODE_ENV=production
PORT=3000
TZ=UTC
LOG_LEVEL=info
DEBUG=false
```

## Usage

### Automatic Validation (Recommended)

The validation runs automatically on Next.js startup via the `instrumentation.ts` file:

```typescript
// instrumentation.ts (already created)
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const { initializeApp } = await import('./lib/init');
    initializeApp();
  }
}
```

No additional code needed - validation happens automatically when you run:
```bash
npm run dev
npm run build
npm start
```

### Manual Validation

If you need to validate manually in your code:

```typescript
import { validateEnvOrThrow, getEnv } from '@/lib/env-validation';

// Validate and throw on error
const env = validateEnvOrThrow();

// Use validated environment
console.log(env.NEO4J_URI);
console.log(env.MYSQL_HOST);
```

### Validation Without Throwing

For custom error handling:

```typescript
import { validateEnv, logValidationResults } from '@/lib/env-validation';

const result = validateEnv();
logValidationResults(result);

if (!result.success) {
  // Handle errors your way
  console.error('Configuration errors:', result.errors);
  // Don't exit, continue with fallback config, etc.
}
```

### Get Validated Environment

After validation has run at startup, safely access environment:

```typescript
import { getEnv } from '@/lib/env-validation';

// Safe to use - throws if validation hasn't run
const env = getEnv();
```

## Helper Functions

```typescript
import {
  isDevelopment,
  isProduction,
  isTest,
  isDebugEnabled
} from '@/lib/env-validation';

if (isDevelopment()) {
  console.log('Running in development mode');
}

if (isProduction()) {
  console.log('Running in production mode');
}

if (isDebugEnabled()) {
  console.log('Debug mode enabled');
}
```

## Validation Rules

### Neo4j URI Formats
Accepts the following formats:
- `bolt://hostname:port`
- `neo4j://hostname:port`
- `bolt+s://hostname:port` (secure)
- `neo4j+s://hostname:port` (secure)

### Port Numbers
- Must be between 1 and 65535
- Validated as numbers (not strings)

### URLs
- Must be valid HTTP or HTTPS URLs
- Protocol is required

### PostgreSQL Connection Strings
- Must start with `postgresql://`
- Full connection string format required

## Error Messages

### Missing Required Variable
```
❌ Environment validation failed

Missing or invalid environment variables:
   - NEO4J_URI: Required
   - MYSQL_PASSWORD: MySQL password is required

📖 Please check .env.example for required variables
   Copy .env.example to .env.local and configure all required values
```

### Invalid Format
```
❌ Environment validation failed

Missing or invalid environment variables:
   - NEO4J_URI: Must be a valid Neo4j URI (e.g., bolt://localhost:7687)
   - MYSQL_PORT: Port must be between 1 and 65535
```

### Production Warnings
```
✅ Environment validation successful

⚠️  Warnings:
   - NEXTAUTH_SECRET is using default value - SECURITY RISK!
   - QDRANT_API_KEY not set - Qdrant may not be secured
   - Neo4j URI uses localhost in production - verify configuration
```

## Configuration Summary

On successful validation, you'll see:
```
✅ Environment validation successful

📋 Configuration summary:
   - Environment: production
   - Neo4j: bolt://openspg-neo4j:7687
   - MySQL: openspg-mysql:3306
   - Qdrant: http://openspg-qdrant:6333
   - MinIO: http://openspg-minio:9000
   - Port: 3000
```

## Testing

Run tests for the validation system:

```bash
npm test tests/env-validation.test.ts
```

Tests cover:
- ✅ Valid configuration acceptance
- ✅ Missing required variables
- ✅ Invalid URI/URL formats
- ✅ Port number validation
- ✅ Production warnings
- ✅ Optional variable handling

## TypeScript Types

The validation system exports TypeScript types:

```typescript
import { ValidatedEnv } from '@/lib/env-validation';

function useDatabase(env: ValidatedEnv) {
  // env.NEO4J_URI is typed and validated
  // env.MYSQL_HOST is typed and validated
  // Optional vars are typed as string | undefined
}
```

## Best Practices

1. **Always use `.env.local`** for local development
2. **Never commit** `.env.local` to version control
3. **Copy from `.env.example`** when setting up
4. **Use strong secrets** in production (not default values)
5. **Enable validation** in all environments
6. **Review warnings** before deploying to production
7. **Keep `.env.example`** updated with new variables

## Troubleshooting

### "Environment validation failed" on startup

1. Check you have a `.env.local` file (copy from `.env.example`)
2. Verify all required variables are set
3. Check variable formats match the requirements
4. Review error messages for specific issues

### Variables not loading

1. Ensure `.env.local` is in the project root
2. Restart the development server
3. Check for typos in variable names
4. Verify no trailing spaces in values

### TypeScript errors

1. Run `npm run typecheck` to see detailed errors
2. Ensure you imported from `@/lib/env-validation`
3. Check that validation has run before using `getEnv()`

## Integration with Next.js

The validation integrates seamlessly with Next.js:

- Runs before any application code via `instrumentation.ts`
- Works with both App Router and Pages Router
- Compatible with Next.js 13+ instrumentation
- No performance impact on startup

## Security Considerations

1. **Never log sensitive values** (passwords, API keys)
2. **Use different secrets** for each environment
3. **Rotate secrets** regularly in production
4. **Enable SSL/TLS** for database connections in production
5. **Review warnings** about missing authentication
6. **Secure API keys** for Qdrant and other services

## Files Created

```
lib/
  ├── env-validation.ts     # Main validation logic
  └── init.ts               # Application initialization

instrumentation.ts          # Next.js startup hook

tests/
  └── env-validation.test.ts # Comprehensive tests

docs/
  └── environment-validation.md # This documentation
```

## Next Steps

1. ✅ Copy `.env.example` to `.env.local`
2. ✅ Configure all required variables
3. ✅ Run `npm run dev` to test validation
4. ✅ Fix any errors or warnings
5. ✅ Run `npm test` to verify tests pass
6. ✅ Review production configuration before deployment
