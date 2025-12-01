/**
 * Jest Setup for AgentDB Tests
 * Global test configuration and mocks
 */

// Make this a module for TypeScript global augmentation
export {};

// Mock @xenova/transformers to avoid ESM issues and model downloads
// The pipeline function returns a callable model function
jest.mock('@xenova/transformers', () => {
  // Create a callable model function
  const mockModelFunction = async (text: string, options?: any) => ({
    data: new Float32Array(Array.from({ length: 384 }, () => Math.random())),
  });

  // Mock pipeline that returns the model function
  const mockPipeline = jest.fn(async (task: string, model: string, options?: any) => {
    console.log('[JEST SETUP] pipeline called, returning model function');
    return mockModelFunction;
  });

  return {
    pipeline: mockPipeline,
    Pipeline: jest.fn(),
    FeatureExtractionPipeline: jest.fn(),
  };
});

// Extend Jest matchers
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () =>
          `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true,
      };
    } else {
      return {
        message: () =>
          `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false,
      };
    }
  },
});

// Global test timeout
jest.setTimeout(30000);

// Mock environment variables
process.env.QDRANT_URL = process.env.QDRANT_URL || 'http://localhost:6333';
process.env.QDRANT_API_KEY = process.env.QDRANT_API_KEY || 'test-api-key';

// Suppress console logs in tests unless debugging
const originalConsoleLog = console.log;
const originalConsoleError = console.error;

beforeAll(() => {
  if (!process.env.DEBUG_TESTS) {
    console.log = jest.fn();
    console.error = jest.fn();
  }
});

afterAll(() => {
  console.log = originalConsoleLog;
  console.error = originalConsoleError;
});

// Global test utilities - need to declare first due to circular reference
const createMockAgentConfig = (overrides = {}) => ({
  agent_type: 'test-agent',
  agent_name: 'Test Agent',
  capabilities: ['testing', 'mocking'],
  specialization: 'unit-testing',
  runtime: 'node',
  context: 'test context',
  ...overrides,
});

const createMockEmbedding = (dimension = 384) => {
  return Array.from({ length: dimension }, () => Math.random());
};

const createMockSearchResult = (overrides = {}) => ({
  id: 'test-id-' + Math.random().toString(36).substring(7),
  score: 0.95,
  payload: {
    agent_type: 'test-agent',
    agent_name: 'Test Agent',
    capabilities: ['testing'],
    config_hash: 'hash123',
    config_version: '2.0.0',
    agent_config: createMockAgentConfig(),
    avg_spawn_time_ms: 100,
    success_rate: 1.0,
    total_spawns: 1,
    created_at: Date.now(),
    last_accessed: Date.now(),
    access_count: 1,
    ttl_expires: Date.now() + 86400000,
    embedding_model: 'Xenova/all-MiniLM-L6-v2',
    embedding_version: 'v2.0',
    similarity_threshold: 0.9,
    tags: ['test'],
  },
  ...overrides,
});

const waitFor = async (
  condition: () => boolean | Promise<boolean>,
  timeoutMs = 5000,
  checkIntervalMs = 100
) => {
  const startTime = Date.now();
  while (!(await Promise.resolve(condition()))) {
    if (Date.now() - startTime > timeoutMs) {
      throw new Error('Timeout waiting for condition');
    }
    await new Promise((resolve) => setTimeout(resolve, checkIntervalMs));
  }
};

const sleep = async (ms: number) => {
  await new Promise((resolve) => setTimeout(resolve, ms));
};

const retry = async <T>(
  fn: () => Promise<T>,
  maxAttempts = 3,
  delayMs = 1000
): Promise<T> => {
  let lastError: Error | undefined;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      if (attempt < maxAttempts) {
        await sleep(delayMs * attempt);
      }
    }
  }
  throw lastError || new Error('Retry failed');
};

const measureTime = async <T>(fn: () => Promise<T>): Promise<{ result: T; time: number }> => {
  const startTime = Date.now();
  const result = await fn();
  const time = Date.now() - startTime;
  return { result, time };
};

// Global test utilities
global.testUtils = {
  createMockAgentConfig,
  createMockEmbedding,
  createMockSearchResult,
  waitFor,
  sleep,
  retry,
  measureTime,
};

// TypeScript declarations
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeWithinRange(floor: number, ceiling: number): R;
    }
  }

  var testUtils: {
    createMockAgentConfig: (overrides?: any) => any;
    createMockEmbedding: (dimension?: number) => number[];
    createMockSearchResult: (overrides?: any) => any;
    waitFor: (condition: () => boolean | Promise<boolean>, timeoutMs?: number, checkIntervalMs?: number) => Promise<void>;
    sleep: (ms: number) => Promise<void>;
    retry: <T>(fn: () => Promise<T>, maxAttempts?: number, delayMs?: number) => Promise<T>;
    measureTime: <T>(fn: () => Promise<T>) => Promise<{ result: T; time: number }>;
  };
}
