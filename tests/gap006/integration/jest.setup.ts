/**
 * Jest Setup for GAP-006 Integration Tests
 * Global test configuration and utilities
 */

// Increase timeout for all tests
jest.setTimeout(30000);

// Suppress console output during tests (optional)
if (process.env.SUPPRESS_LOGS === 'true') {
  global.console = {
    ...console,
    log: jest.fn(),
    debug: jest.fn(),
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
  };
}

// Global test hooks
beforeAll(() => {
  console.log('🚀 Starting GAP-006 Integration Test Suite');
});

afterAll(() => {
  console.log('✅ GAP-006 Integration Test Suite Complete');
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Environment validation
const requiredEnvVars = [
  'POSTGRES_HOST',
  'POSTGRES_PORT',
  'POSTGRES_DB',
  'POSTGRES_USER',
  'REDIS_HOST',
  'REDIS_PORT',
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    console.warn(`Warning: ${envVar} not set, using default`);
  }
}

// Export test utilities
export const testUtils = {
  generateUUID: () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  },

  sleep: (ms: number) => new Promise((resolve) => setTimeout(resolve, ms)),

  retry: async (
    fn: () => Promise<any>,
    maxAttempts: number = 3,
    delayMs: number = 1000
  ) => {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error) {
        if (attempt === maxAttempts) throw error;
        await testUtils.sleep(delayMs);
      }
    }
  },
};
