/**
 * Jest Configuration for Security Tests
 * Specialized configuration for running security test suite
 */

module.exports = {
  // Use default Jest config as base
  preset: 'ts-jest',
  testEnvironment: 'node',

  // Only run security tests
  testMatch: [
    '**/tests/security-*.test.ts'
  ],

  // Coverage configuration
  collectCoverage: true,
  collectCoverageFrom: [
    'app/api/upload/route.ts',
    '!**/node_modules/**',
    '!**/tests/**',
    '!**/dist/**'
  ],

  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },

  coverageReporters: [
    'text',
    'text-summary',
    'html',
    'json',
    'lcov'
  ],

  // Coverage directory
  coverageDirectory: 'tests/reports/coverage',

  // Verbose output for security tests
  verbose: true,

  // Display individual test results
  testResultsProcessor: undefined,

  // Timeout for security tests (some may take longer)
  testTimeout: 30000,

  // Clear mocks between tests
  clearMocks: true,

  // Reset mocks between tests
  resetMocks: true,

  // Restore mocks between tests
  restoreMocks: true,

  // Module paths
  modulePaths: ['<rootDir>'],

  // Module file extensions
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],

  // Transform files
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        jsx: 'react',
        esModuleInterop: true,
        allowSyntheticDefaultImports: true
      }
    }]
  },

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/tests/security-test-setup.ts'],

  // Global variables available in tests
  globals: {
    'ts-jest': {
      isolatedModules: true
    }
  },

  // Reporters
  reporters: [
    'default',
    [
      'jest-html-reporter',
      {
        pageTitle: 'QW-001 Security Test Report',
        outputPath: 'tests/reports/security-test-report.html',
        includeFailureMsg: true,
        includeConsoleLog: true,
        theme: 'darkTheme',
        sort: 'status'
      }
    ],
    [
      'jest-junit',
      {
        outputDirectory: 'tests/reports',
        outputName: 'security-junit.xml',
        classNameTemplate: '{classname}',
        titleTemplate: '{title}',
        ancestorSeparator: ' › ',
        usePathForSuiteName: true
      }
    ]
  ],

  // Error on deprecated APIs
  errorOnDeprecated: true,

  // Notify on completion
  notify: true,
  notifyMode: 'failure-change',

  // Detect open handles
  detectOpenHandles: true,

  // Force exit after tests
  forceExit: true,

  // Max workers for parallel execution
  maxWorkers: 1, // Sequential for security tests to avoid race conditions

  // Test categories using test name patterns
  testNamePattern: undefined // Can be overridden via CLI

  // Example CLI usage:
  // npm test -- --config=tests/jest.security.config.js
  // npm test -- --config=tests/jest.security.config.js --testNamePattern="Path Traversal"
};
