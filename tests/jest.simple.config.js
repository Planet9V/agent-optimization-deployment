/**
 * Simplified Jest Configuration for Security Tests
 * Minimal configuration to run tests quickly
 */

module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  rootDir: '..',

  // Only run security tests
  testMatch: [
    '**/tests/security-*.test.ts'
  ],

  // Coverage
  collectCoverage: true,
  collectCoverageFrom: [
    'app/api/upload/route.ts'
  ],

  coverageDirectory: 'tests/reports/coverage',

  // Verbose output
  verbose: true,

  // Timeout
  testTimeout: 30000,

  // Clear mocks
  clearMocks: true,
  resetMocks: true,
  restoreMocks: true,

  // Transform
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        jsx: 'react',
        esModuleInterop: true,
        allowSyntheticDefaultImports: true
      }
    }]
  },

  // Setup
  setupFilesAfterEnv: ['<rootDir>/tests/security-test-setup.ts'],

  // Test environment variables
  testEnvironmentOptions: {
    env: {
      MINIO_ACCESS_KEY: 'test_access_key',
      MINIO_SECRET_KEY: 'test_secret_key',
      MINIO_ENDPOINT: 'http://localhost:9000',
      MINIO_BUCKET: 'test-bucket',
      MINIO_REGION: 'us-east-1',
      NODE_ENV: 'test'
    }
  },

  // Sequential execution for security tests
  maxWorkers: 1
};
