/**
 * Security Test Setup
 * Global configuration and utilities for security testing
 */

// Extend Jest matchers for security testing
expect.extend({
  toBeSecureFilename(received: string) {
    const securityChecks = {
      noPathTraversal: !received.includes('..'),
      noAbsolutePaths: !received.match(/^\/|^[A-Z]:\\/),
      noShellMetachars: !received.match(/[;`$|&]/),
      noNullBytes: !received.includes('\x00'),
      reasonableLength: received.length <= 300,
      startsWithUploads: received.startsWith('uploads/')
    };

    const failedChecks = Object.entries(securityChecks)
      .filter(([_, passed]) => !passed)
      .map(([check]) => check);

    const pass = failedChecks.length === 0;

    return {
      pass,
      message: () => pass
        ? `Expected ${received} not to be a secure filename`
        : `Expected ${received} to be a secure filename. Failed checks: ${failedChecks.join(', ')}`
    };
  },

  toBeAllowedMimeType(received: string) {
    const allowedTypes = new Set([
      'application/pdf',
      'image/jpeg',
      'image/png',
      'image/gif',
      'image/webp',
      'text/plain',
      'text/csv',
      'application/json',
      'application/xml',
      'text/xml'
    ]);

    const normalized = received.toLowerCase().split(';')[0].trim();
    const pass = allowedTypes.has(normalized);

    return {
      pass,
      message: () => pass
        ? `Expected ${received} not to be an allowed MIME type`
        : `Expected ${received} to be an allowed MIME type. Allowed types: ${Array.from(allowedTypes).join(', ')}`
    };
  },

  toNotContainSensitiveInfo(received: string) {
    const sensitivePatterns = [
      /minio@openspg/i,
      /password/i,
      /secret/i,
      /access[_-]?key/i,
      /api[_-]?key/i,
      /bearer\s+[a-zA-Z0-9]/i,
      /[a-f0-9]{32,}/i // Potential tokens
    ];

    const foundPatterns = sensitivePatterns
      .map((pattern, index) => ({ pattern, index }))
      .filter(({ pattern }) => pattern.test(received))
      .map(({ index }) => `Pattern ${index}`);

    const pass = foundPatterns.length === 0;

    return {
      pass,
      message: () => pass
        ? `Expected ${received} to contain sensitive information`
        : `Expected ${received} not to contain sensitive information. Found: ${foundPatterns.join(', ')}`
    };
  },

  toBeWithinPerformanceBudget(received: number, budget: number) {
    const pass = received <= budget;
    const percentage = ((received / budget) * 100).toFixed(1);

    return {
      pass,
      message: () => pass
        ? `Expected ${received}ms not to be within budget of ${budget}ms`
        : `Expected ${received}ms to be within budget of ${budget}ms (currently at ${percentage}% of budget)`
    };
  }
});

// Declare custom matchers for TypeScript
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeSecureFilename(): R;
      toBeAllowedMimeType(): R;
      toNotContainSensitiveInfo(): R;
      toBeWithinPerformanceBudget(budget: number): R;
    }
  }
}

// Global test utilities
global.securityTestUtils = {
  // Create malicious file for testing
  createMaliciousFile(name: string, size = 1024, type = 'text/plain'): File {
    const content = 'a'.repeat(size);
    const blob = new Blob([content], { type });
    return new File([blob], name, { type });
  },

  // Verify filename was sanitized
  verifySanitizedFilename(original: string, sanitized: string) {
    expect(sanitized).not.toContain('..');
    expect(sanitized).not.toMatch(/^\/|^[A-Z]:\\/);
    expect(sanitized).not.toMatch(/[;`$|&]/);
    expect(sanitized).not.toContain('\x00');
    expect(sanitized.length).toBeLessThanOrEqual(300);
  },

  // Verify MIME type is safe
  verifySafeMimeType(mimeType: string) {
    const dangerous = [
      'application/x-executable',
      'application/x-dosexec',
      'application/x-msdownload',
      'application/javascript',
      'text/javascript'
    ];

    expect(dangerous).not.toContain(mimeType.toLowerCase());
  },

  // Extract S3 command parameters from mock
  getS3CommandParams(mockSend: jest.Mock, callIndex = 0) {
    return mockSend.mock.calls[callIndex]?.[0] || null;
  },

  // Verify no sensitive data in logs
  verifyNoSensitiveLogging(consoleSpy: jest.SpyInstance) {
    const allLogs = [
      ...consoleSpy.mock.calls.map(call => call.join(' '))
    ];

    allLogs.forEach(log => {
      expect(log).not.toContain('minio@openspg');
      expect(log).not.toMatch(/secret[_-]?key/i);
      expect(log).not.toMatch(/access[_-]?key/i);
    });
  }
};

// Declare global utilities type
declare global {
  var securityTestUtils: {
    createMaliciousFile(name: string, size?: number, type?: string): File;
    verifySanitizedFilename(original: string, sanitized: string): void;
    verifySafeMimeType(mimeType: string): void;
    getS3CommandParams(mockSend: jest.Mock, callIndex?: number): any;
    verifyNoSensitiveLogging(consoleSpy: jest.SpyInstance): void;
  };
}

// Security test environment setup
beforeAll(() => {
  console.log('🔒 Security Test Suite Starting');
  console.log('Testing against QW-001 security vulnerabilities');
});

afterAll(() => {
  console.log('🔒 Security Test Suite Completed');
});

// Backup environment before each test
let originalEnv: NodeJS.ProcessEnv;

beforeEach(() => {
  originalEnv = { ...process.env };
});

afterEach(() => {
  process.env = originalEnv;
});

export {};
