#!/usr/bin/env node
/**
 * Standalone Environment Validation Script
 *
 * Run this to validate environment variables without starting the application.
 * Usage: npx tsx scripts/validate-env.ts
 */

import { validateEnv, logValidationResults } from '../lib/env-validation';

console.log('🔍 Validating environment variables...\n');

const result = validateEnv();
logValidationResults(result);

if (!result.success) {
  process.exit(1);
}

process.exit(0);
