/**
 * Environment Variable Validation
 *
 * Validates all required environment variables at application startup.
 * Provides clear error messages for missing or invalid configuration.
 */

import { z } from 'zod';

// ============================================
// Validation Schemas
// ============================================

/**
 * Neo4j connection string validation
 * Supports bolt://, neo4j://, bolt+s://, neo4j+s:// protocols
 */
const neo4jUriSchema = z.string()
  .regex(
    /^(bolt|neo4j)(\+s)?:\/\/[\w.-]+(:\d+)?$/,
    'Must be a valid Neo4j URI (e.g., bolt://localhost:7687)'
  );

/**
 * HTTP/HTTPS URL validation
 */
const urlSchema = z.string()
  .url('Must be a valid URL')
  .regex(/^https?:\/\//, 'Must start with http:// or https://');

/**
 * PostgreSQL connection string validation (for Neon)
 */
const postgresUrlSchema = z.string()
  .regex(
    /^postgresql:\/\/.+/,
    'Must be a valid PostgreSQL connection string'
  );

/**
 * Complete environment schema with all required and optional variables
 */
const envSchema = z.object({
  // Node Environment
  NODE_ENV: z.enum(['development', 'production', 'test']).default('production'),

  // Neo4j (Graph Database) - REQUIRED
  NEO4J_URI: neo4jUriSchema,
  NEO4J_USER: z.string().min(1, 'Neo4j user is required'),
  NEO4J_PASSWORD: z.string().min(1, 'Neo4j password is required'),
  NEO4J_DATABASE: z.string().default('neo4j'),

  // MySQL (Relational Database) - REQUIRED
  MYSQL_HOST: z.string().min(1, 'MySQL host is required'),
  MYSQL_PORT: z.string().regex(/^\d+$/, 'Must be a number').default('3306'),
  MYSQL_DATABASE: z.string().min(1, 'MySQL database name is required'),
  MYSQL_USER: z.string().min(1, 'MySQL user is required'),
  MYSQL_PASSWORD: z.string().min(1, 'MySQL password is required'),

  // Qdrant (Vector Database) - REQUIRED
  QDRANT_URL: urlSchema,
  QDRANT_API_KEY: z.string().optional(),

  // MinIO (Object Storage) - REQUIRED
  MINIO_ENDPOINT: z.string().min(1, 'MinIO endpoint is required'),
  MINIO_ACCESS_KEY: z.string().min(1, 'MinIO access key is required'),
  MINIO_SECRET_KEY: z.string().min(1, 'MinIO secret key is required'),
  MINIO_USE_SSL: z.enum(['true', 'false']).default('false'),

  // PostgreSQL (Neon Database) - OPTIONAL
  DATABASE_URL: postgresUrlSchema.optional(),

  // OpenSPG Server - OPTIONAL
  OPENSPG_SERVER_URL: urlSchema.optional(),

  // NextAuth - OPTIONAL (but recommended for production)
  NEXTAUTH_URL: urlSchema.optional(),
  NEXTAUTH_SECRET: z.string().optional(),

  // Clerk Authentication - OPTIONAL
  CLERK_SECRET_KEY: z.string().optional(),
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: z.string().optional(),

  // Redis - OPTIONAL (for BullMQ queues)
  REDIS_HOST: z.string().optional(),
  REDIS_PORT: z.string().regex(/^\d+$/, 'Must be a number').optional(),
  REDIS_PASSWORD: z.string().optional(),

  // Application Configuration
  PORT: z.string().regex(/^\d+$/, 'Must be a number').default('3000'),
  TZ: z.string().default('UTC'),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  DEBUG: z.enum(['true', 'false']).default('false'),
});

// ============================================
// Type Exports
// ============================================

export type ValidatedEnv = z.infer<typeof envSchema>;

// ============================================
// Validation Results
// ============================================

interface ValidationResult {
  success: boolean;
  errors: string[];
  warnings: string[];
  env?: ValidatedEnv;
}

// ============================================
// Validation Functions
// ============================================

/**
 * Validates all environment variables
 * @returns Validation result with errors and warnings
 */
export function validateEnv(): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  try {
    // Parse and validate environment variables
    const parsed = envSchema.parse(process.env);

    // Check for recommended optional variables in production
    if (parsed.NODE_ENV === 'production') {
      checkProductionWarnings(parsed, warnings);
    }

    // Check database connectivity (validation only, not actual connection)
    validateDatabaseConfig(parsed, warnings);

    return {
      success: true,
      errors,
      warnings,
      env: parsed,
    };
  } catch (error) {
    if (error instanceof z.ZodError) {
      // Extract validation errors
      errors.push(...error.issues.map(err => {
        const path = err.path.join('.');
        return `${path}: ${err.message}`;
      }));
    } else {
      errors.push(`Unexpected validation error: ${error}`);
    }

    return {
      success: false,
      errors,
      warnings,
    };
  }
}

/**
 * Check for production warnings
 */
function checkProductionWarnings(env: ValidatedEnv, warnings: string[]): void {
  // Authentication warnings
  if (!env.NEXTAUTH_SECRET) {
    warnings.push('NEXTAUTH_SECRET not set - authentication may not work correctly');
  } else if (env.NEXTAUTH_SECRET === 'change-me-in-production') {
    warnings.push('NEXTAUTH_SECRET is using default value - SECURITY RISK!');
  }

  if (!env.CLERK_SECRET_KEY && !env.NEXTAUTH_SECRET) {
    warnings.push('No authentication configured (neither Clerk nor NextAuth)');
  }

  // Database warnings
  if (!env.DATABASE_URL) {
    warnings.push('DATABASE_URL not set - Neon database features will be unavailable');
  }

  if (!env.QDRANT_API_KEY) {
    warnings.push('QDRANT_API_KEY not set - Qdrant may not be secured');
  }

  // Redis warnings
  if (!env.REDIS_HOST) {
    warnings.push('REDIS_HOST not set - Queue features will be unavailable');
  }
}

/**
 * Validate database configuration
 */
function validateDatabaseConfig(env: ValidatedEnv, warnings: string[]): void {
  // Check Neo4j URI format
  if (env.NEO4J_URI.includes('localhost') && env.NODE_ENV === 'production') {
    warnings.push('Neo4j URI uses localhost in production - verify configuration');
  }

  // Check MySQL host
  if (env.MYSQL_HOST === 'localhost' && env.NODE_ENV === 'production') {
    warnings.push('MySQL host uses localhost in production - verify configuration');
  }

  // Check Qdrant URL
  if (env.QDRANT_URL.includes('localhost') && env.NODE_ENV === 'production') {
    warnings.push('Qdrant URL uses localhost in production - verify configuration');
  }

  // Check MinIO endpoint
  if (env.MINIO_ENDPOINT.includes('localhost') && env.NODE_ENV === 'production') {
    warnings.push('MinIO endpoint uses localhost in production - verify configuration');
  }
}

/**
 * Format and log validation results
 */
export function logValidationResults(result: ValidationResult): void {
  if (result.success) {
    console.log('✅ Environment validation successful');

    if (result.warnings.length > 0) {
      console.warn('\n⚠️  Warnings:');
      result.warnings.forEach(warning => {
        console.warn(`   - ${warning}`);
      });
    }

    if (result.env) {
      console.log('\n📋 Configuration summary:');
      console.log(`   - Environment: ${result.env.NODE_ENV}`);
      console.log(`   - Neo4j: ${result.env.NEO4J_URI}`);
      console.log(`   - MySQL: ${result.env.MYSQL_HOST}:${result.env.MYSQL_PORT}`);
      console.log(`   - Qdrant: ${result.env.QDRANT_URL}`);
      console.log(`   - MinIO: ${result.env.MINIO_ENDPOINT}`);
      console.log(`   - Port: ${result.env.PORT}`);
    }
  } else {
    console.error('❌ Environment validation failed\n');
    console.error('Missing or invalid environment variables:');
    result.errors.forEach(error => {
      console.error(`   - ${error}`);
    });

    console.error('\n📖 Please check .env.example for required variables');
    console.error('   Copy .env.example to .env.local and configure all required values\n');
  }
}

/**
 * Validate environment and throw on error
 * Use this in application initialization
 */
export function validateEnvOrThrow(): ValidatedEnv {
  const result = validateEnv();
  logValidationResults(result);

  if (!result.success) {
    throw new Error(
      `Environment validation failed with ${result.errors.length} error(s). ` +
      'Please fix the environment variables and restart the application.'
    );
  }

  return result.env!;
}

/**
 * Get validated environment variables
 * Safe to use after validateEnvOrThrow() has been called
 */
export function getEnv(): ValidatedEnv {
  // This assumes validation has already been done at startup
  // If not, this will throw
  return envSchema.parse(process.env);
}

// ============================================
// Helper Functions
// ============================================

/**
 * Check if running in development mode
 */
export function isDevelopment(): boolean {
  return process.env.NODE_ENV === 'development';
}

/**
 * Check if running in production mode
 */
export function isProduction(): boolean {
  return process.env.NODE_ENV === 'production';
}

/**
 * Check if running in test mode
 */
export function isTest(): boolean {
  return process.env.NODE_ENV === 'test';
}

/**
 * Check if debug mode is enabled
 */
export function isDebugEnabled(): boolean {
  return process.env.DEBUG === 'true';
}

// ============================================
// Exports
// ============================================

export default {
  validateEnv,
  validateEnvOrThrow,
  logValidationResults,
  getEnv,
  isDevelopment,
  isProduction,
  isTest,
  isDebugEnabled,
};
