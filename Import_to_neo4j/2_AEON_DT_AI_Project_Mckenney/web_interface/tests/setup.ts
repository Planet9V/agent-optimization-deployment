/**
 * Jest Test Setup
 * Global configuration and utilities for test suite
 */

import * as dotenv from 'dotenv';
import * as path from 'path';

// Load environment variables from .env file
const envPath = path.resolve(__dirname, '../.env');
dotenv.config({ path: envPath });

// Set test environment
process.env.NODE_ENV = process.env.NODE_ENV || 'test';

// Extend Jest matchers if needed
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () => `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true,
      };
    } else {
      return {
        message: () => `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false,
      };
    }
  },
});

// Global test utilities
global.testUtils = {
  sleep: (ms: number) => new Promise(resolve => setTimeout(resolve, ms)),

  retry: async <T>(
    fn: () => Promise<T>,
    maxAttempts: number = 3,
    delayMs: number = 1000
  ): Promise<T> => {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error) {
        if (attempt === maxAttempts) throw error;
        await global.testUtils.sleep(delayMs);
      }
    }
    throw new Error('Retry failed');
  },

  waitFor: async (
    condition: () => boolean | Promise<boolean>,
    timeoutMs: number = 5000,
    checkIntervalMs: number = 100
  ): Promise<void> => {
    const startTime = Date.now();
    while (Date.now() - startTime < timeoutMs) {
      if (await condition()) return;
      await global.testUtils.sleep(checkIntervalMs);
    }
    throw new Error(`Condition not met within ${timeoutMs}ms`);
  }
};

// Declare global types
declare global {
  var testUtils: {
    sleep: (ms: number) => Promise<void>;
    retry: <T>(fn: () => Promise<T>, maxAttempts?: number, delayMs?: number) => Promise<T>;
    waitFor: (condition: () => boolean | Promise<boolean>, timeoutMs?: number, checkIntervalMs?: number) => Promise<void>;
  };

  namespace jest {
    interface Matchers<R> {
      toBeWithinRange(floor: number, ceiling: number): R;
    }
  }
}

// Suppress console output during tests unless VERBOSE is set
if (!process.env.VERBOSE) {
  global.console.log = jest.fn();
  global.console.info = jest.fn();
  global.console.debug = jest.fn();
}

// Keep errors and warnings visible
const originalError = console.error;
const originalWarn = console.warn;

beforeEach(() => {
  console.error = originalError;
  console.warn = originalWarn;
});

// Cleanup after all tests
afterAll(async () => {
  // Give async operations time to complete
  await global.testUtils.sleep(1000);
});
