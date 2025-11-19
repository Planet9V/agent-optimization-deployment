/**
 * Application Initialization
 *
 * Run environment validation and initialization checks at startup.
 * Import this file at the top of your main application entry point.
 */

import { validateEnvOrThrow, logValidationResults, ValidatedEnv } from './env-validation';

/**
 * Initialize application with environment validation
 * Call this at the very start of your application (e.g., in next.config.js or app startup)
 */
export function initializeApp(): ValidatedEnv {
  console.log('🚀 Initializing AEON Digital Twin Dashboard...\n');

  try {
    // Validate environment variables
    const env = validateEnvOrThrow();

    console.log('\n✅ Initialization complete\n');
    return env;
  } catch (error) {
    console.error('\n❌ Initialization failed:', error);
    process.exit(1);
  }
}

/**
 * Initialize for Next.js
 * Use this in instrumentation.ts for Next.js 13+
 */
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    initializeApp();
  }
}

// Auto-initialize if running directly
if (require.main === module) {
  initializeApp();
}

export default initializeApp;
