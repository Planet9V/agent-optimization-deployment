/**
 * Jest Configuration for GAP-006 Integration Tests
 * Simplified configuration to avoid path resolution issues
 */

module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  rootDir: '.',
  testMatch: ['**/tests/gap006/**/*.test.ts'], // Include all test folders: integration, performance, etc.
  setupFilesAfterEnv: ['<rootDir>/tests/gap006/integration/jest.setup.ts'],
  collectCoverageFrom: [
    'src/services/gap006/**/*.ts',
    '!src/services/gap006/**/*.d.ts',
    '!src/services/gap006/**/*.test.ts',
  ],
  coverageDirectory: '<rootDir>/coverage/gap006-integration',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 75,
      lines: 80,
      statements: 80,
    },
  },
  testTimeout: 30000, // 30 seconds for integration tests
  verbose: true,
  maxWorkers: 1, // Run integration tests serially to avoid conflicts
  globals: {
    'ts-jest': {
      tsconfig: {
        esModuleInterop: true,
        allowSyntheticDefaultImports: true,
        module: 'commonjs',
        target: 'ES2020',
      },
    },
  },
};
