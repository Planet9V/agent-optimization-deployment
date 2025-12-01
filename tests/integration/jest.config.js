/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>'],
  testMatch: ['**/*.test.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  collectCoverage: false, // Don't collect coverage for integration tests
  verbose: true,
  testTimeout: 30000, // 30 seconds for integration tests
  maxWorkers: 1, // Run integration tests sequentially
  transform: {
    '^.+\\.tsx?$': [
      'ts-jest',
      {
        tsconfig: {
          esModuleInterop: true,
          allowSyntheticDefaultImports: true,
          moduleResolution: 'node',
          resolveJsonModule: true,
          strict: false,
          skipLibCheck: true,
        },
      },
    ],
  },
  transformIgnorePatterns: [
    'node_modules/(?!(@xenova/transformers)/)',
  ],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/../../lib/$1',
  },
};
