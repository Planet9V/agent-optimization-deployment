/**
 * Jest Setup for AgentDB Tests
 * Global test configuration and mocks
 */

// Mock @xenova/transformers to avoid ESM issues and model downloads
jest.mock('@xenova/transformers', () => ({
  pipeline: jest.fn().mockResolvedValue(async (text: string) => ({
    data: Array.from({ length: 384 }, () => Math.random()),
  })),
  Pipeline: jest.fn(),
  FeatureExtractionPipeline: jest.fn(),
}));

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

// Global test utilities
global.testUtils = {
  /**
   * Create mock agent config
   */
  createMockAgentConfig: (overrides = {}) => ({
    agent_type: 'test-agent',
    agent_name: 'Test Agent',
    capabilities: ['testing', 'mocking'],
    specialization: 'unit-testing',
    runtime: 'node',
    context: 'test context',
    ...overrides,
  }),

  /**
   * Create mock embedding
   */
  createMockEmbedding: (dimension = 384) => {
    return Array.from({ length: dimension }, () => Math.random());
  },

  /**
   * Create mock search result
   */
  createMockSearchResult: (overrides = {}) => ({
    id: 'test-id-' + Math.random().toString(36).substring(7),
    score: 0.95,
    payload: {
      agent_type: 'test-agent',
      agent_name: 'Test Agent',
      capabilities: ['testing'],
      config_hash: 'hash123',
      config_version: '2.0.0',
      agent_config: global.testUtils.createMockAgentConfig(),
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
  }),

  /**
   * Wait for condition with timeout
   */
  waitFor: async (
    condition: () => boolean,
    timeout = 5000,
    interval = 100
  ) => {
    const startTime = Date.now();
    while (!condition()) {
      if (Date.now() - startTime > timeout) {
        throw new Error('Timeout waiting for condition');
      }
      await new Promise((resolve) => setTimeout(resolve, interval));
    }
  },

  /**
   * Measure execution time
   */
  measureTime: async <T>(fn: () => Promise<T>): Promise<{ result: T; time: number }> => {
    const startTime = Date.now();
    const result = await fn();
    const time = Date.now() - startTime;
    return { result, time };
  },
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
    waitFor: (condition: () => boolean, timeout?: number, interval?: number) => Promise<void>;
    measureTime: <T>(fn: () => Promise<T>) => Promise<{ result: T; time: number }>;
  };
}
