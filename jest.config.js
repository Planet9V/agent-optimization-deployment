/**
 * Default Jest Configuration
 * For general project tests
 * Use tests/jest.security.config.js for security-specific tests
 */

module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',

  testMatch: [
    '**/tests/**/*.test.ts',
    '!**/tests/security-*.test.ts' // Exclude security tests from default run
  ],

  collectCoverageFrom: [
    'app/**/*.{ts,tsx}',
    '!**/node_modules/**',
    '!**/tests/**',
    '!**/dist/**'
  ],

  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],

  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        jsx: 'react',
        esModuleInterop: true,
        allowSyntheticDefaultImports: true
      }
    }]
  },

  clearMocks: true,
  resetMocks: true,
  restoreMocks: true
};
