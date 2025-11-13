/**
 * Jest Configuration for AgentDB Tests
 * Optimized for TypeScript, comprehensive coverage, and performance testing
 */

module.exports = {
  displayName: 'AgentDB',
  preset: 'ts-jest',
  testEnvironment: 'node',

  // Root directories
  rootDir: '../..',
  testMatch: ['<rootDir>/tests/agentdb/**/*.test.ts'],

  // Coverage configuration
  collectCoverageFrom: [
    'lib/agentdb/**/*.ts',
    '!lib/agentdb/**/*.d.ts',
    '!lib/agentdb/index.ts',
  ],
  coverageDirectory: '<rootDir>/tests/agentdb/coverage',
  coverageReporters: ['text', 'lcov', 'html', 'json-summary'],
  coverageThresholds: {
    global: {
      statements: 90,
      branches: 85,
      functions: 90,
      lines: 90,
    },
  },

  // TypeScript configuration
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        esModuleInterop: true,
        allowSyntheticDefaultImports: true,
        resolveJsonModule: true,
        moduleResolution: 'node',
      },
    }],
  },

  // Module resolution
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/lib/$1',
    '^@xenova/transformers$': '<rootDir>/tests/agentdb/__mocks__/@xenova/transformers.js',
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],

  // Transform ESM modules
  transformIgnorePatterns: [
    'node_modules/(?!(@xenova/transformers)/)',
  ],

  // Test timeouts
  testTimeout: 30000, // 30s for performance tests
  slowTestThreshold: 5000,

  // Performance
  maxWorkers: '50%',

  // Setup and teardown
  setupFilesAfterEnv: ['<rootDir>/tests/agentdb/jest.setup.ts'],

  // Reporter configuration
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: '<rootDir>/tests/agentdb/reports',
      outputName: 'junit.xml',
      classNameTemplate: '{classname}',
      titleTemplate: '{title}',
      ancestorSeparator: ' › ',
      usePathForSuiteName: true,
    }],
    ['jest-html-reporter', {
      pageTitle: 'AgentDB Test Report',
      outputPath: '<rootDir>/tests/agentdb/reports/index.html',
      includeFailureMsg: true,
      includeConsoleLog: true,
      sort: 'status',
    }],
  ],

  // Verbose output for debugging
  verbose: true,

  // Globals
  globals: {
    'ts-jest': {
      isolatedModules: true,
    },
  },
};
