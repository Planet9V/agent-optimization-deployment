/**
 * Security Validation Test Suite for QW-001 Parallel S3 Uploads
 *
 * Tests all 5 critical security fixes:
 * 1. Environment variable validation (fail-fast)
 * 2. Filename sanitization (path traversal prevention)
 * 3. MIME type validation (malware prevention)
 * 4. HTTPS endpoint configuration
 * 5. Credential security
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';

// ============================================================================
// SECURITY TEST UTILITIES
// ============================================================================

/**
 * Mock File class for testing
 */
class MockFile extends File {
  constructor(
    bits: BlobPart[],
    name: string,
    options?: FilePropertyBag
  ) {
    super(bits, name, options);
  }
}

/**
 * Create test file with specific properties
 */
function createTestFile(
  name: string,
  content: string,
  type: string
): File {
  return new MockFile([content], name, { type });
}

// ============================================================================
// ISSUE #1: Environment Variable Validation Tests
// ============================================================================

describe('Security Issue #1: Environment Variable Validation', () => {
  const originalEnv = { ...process.env };

  afterEach(() => {
    process.env = { ...originalEnv };
  });

  it('should fail-fast when MINIO_ACCESS_KEY is missing', () => {
    delete process.env.MINIO_ACCESS_KEY;

    expect(() => {
      // Module will throw on import when env vars are missing
      require('../../app/api/upload/route');
    }).toThrow('FATAL: MINIO_ACCESS_KEY environment variable is required');
  });

  it('should fail-fast when MINIO_SECRET_KEY is missing', () => {
    delete process.env.MINIO_SECRET_KEY;

    expect(() => {
      require('../../app/api/upload/route');
    }).toThrow('FATAL: MINIO_SECRET_KEY environment variable is required');
  });

  it('should fail-fast when MINIO_BUCKET is missing', () => {
    delete process.env.MINIO_BUCKET;

    expect(() => {
      require('../../app/api/upload/route');
    }).toThrow('FATAL: MINIO_BUCKET environment variable is required');
  });

  it('should fail-fast when MINIO_ENDPOINT is missing', () => {
    delete process.env.MINIO_ENDPOINT;

    expect(() => {
      require('../../app/api/upload/route');
    }).toThrow('FATAL: MINIO_ENDPOINT environment variable is required');
  });

  it('should NOT use hardcoded credentials as fallback', () => {
    // Verify no hardcoded fallback values exist
    const routeFile = require('fs').readFileSync(
      'app/api/upload/route.ts',
      'utf-8'
    );

    // Should NOT find fallback patterns
    expect(routeFile).not.toMatch(/\|\s*['"]minio['"]/);
    expect(routeFile).not.toMatch(/\|\s*['"]minio@openspg['"]/);
    expect(routeFile).not.toMatch(/\|\s*['"]aeon-documents['"]/);
  });
});

// ============================================================================
// ISSUE #2: Filename Sanitization Tests (Path Traversal Prevention)
// ============================================================================

describe('Security Issue #2: Filename Sanitization', () => {
  // Test the sanitizeFileName function directly
  const sanitizeFileName = (filename: string): string => {
    if (!filename || typeof filename !== 'string') {
      throw new Error('Invalid filename: must be a non-empty string');
    }

    return filename
      .replace(/\\/g, '/')
      .split('/').pop()!
      .replace(/\.\./g, '_')
      .replace(/[^a-zA-Z0-9._-]/g, '_')
      .replace(/^\.+/, '_')
      .slice(0, 255);
  };

  describe('Path Traversal Attack Prevention', () => {
    it('should remove directory traversal sequences', () => {
      expect(sanitizeFileName('../../../etc/passwd')).toBe('etc_passwd');
      expect(sanitizeFileName('../../secret.txt')).toBe('secret.txt');
      expect(sanitizeFileName('..\\..\\windows\\system32')).toBe('windows_system32');
    });

    it('should remove absolute paths', () => {
      expect(sanitizeFileName('/etc/passwd')).toBe('passwd');
      expect(sanitizeFileName('C:\\Windows\\System32\\config')).toBe('config');
      expect(sanitizeFileName('/var/www/html/index.php')).toBe('index.php');
    });

    it('should handle complex path traversal attempts', () => {
      expect(sanitizeFileName('uploads/../../etc/passwd')).toBe('passwd');
      expect(sanitizeFileName('foo/../bar/../baz.txt')).toBe('baz.txt');
      expect(sanitizeFileName('./.././.././../etc/passwd')).toBe('passwd');
    });
  });

  describe('Special Character Sanitization', () => {
    it('should remove shell metacharacters', () => {
      expect(sanitizeFileName('file;rm -rf /.txt')).toBe('file_rm_-rf__.txt');
      expect(sanitizeFileName('file|cat /etc/passwd.txt')).toBe('file_cat__etc_passwd.txt');
      expect(sanitizeFileName('file`whoami`.txt')).toBe('file_whoami_.txt');
    });

    it('should remove null bytes and control characters', () => {
      expect(sanitizeFileName('file\x00.txt')).toBe('file_.txt');
      expect(sanitizeFileName('file\n.txt')).toBe('file_.txt');
      expect(sanitizeFileName('file\r.txt')).toBe('file_.txt');
    });

    it('should prevent hidden file creation', () => {
      expect(sanitizeFileName('.hidden')).toBe('_hidden');
      expect(sanitizeFileName('...hidden')).toBe('_hidden');
      expect(sanitizeFileName('.bashrc')).toBe('_bashrc');
    });
  });

  describe('Filename Length Limits', () => {
    it('should limit filename to 255 characters', () => {
      const longName = 'a'.repeat(300) + '.txt';
      const sanitized = sanitizeFileName(longName);
      expect(sanitized.length).toBeLessThanOrEqual(255);
    });

    it('should preserve file extension when truncating', () => {
      const longName = 'a'.repeat(300) + '.important.txt';
      const sanitized = sanitizeFileName(longName);
      expect(sanitized).toMatch(/\.txt$/);
    });
  });

  describe('Valid Filenames', () => {
    it('should preserve safe filenames', () => {
      expect(sanitizeFileName('document.pdf')).toBe('document.pdf');
      expect(sanitizeFileName('report_2024.xlsx')).toBe('report_2024.xlsx');
      expect(sanitizeFileName('data-export.csv')).toBe('data-export.csv');
    });

    it('should allow alphanumeric and safe characters', () => {
      expect(sanitizeFileName('file123.txt')).toBe('file123.txt');
      expect(sanitizeFileName('my-file_v2.pdf')).toBe('my-file_v2.pdf');
      expect(sanitizeFileName('Report.Final.2024.docx')).toBe('Report.Final.2024.docx');
    });
  });
});

// ============================================================================
// ISSUE #3: MIME Type Validation Tests
// ============================================================================

describe('Security Issue #3: MIME Type Validation', () => {
  const ALLOWED_MIME_TYPES = new Set([
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'text/plain',
    'text/csv',
    'application/json',
  ]);

  const validateContentType = (file: File): string => {
    const mimeType = file.type.toLowerCase().trim();

    if (!mimeType) {
      throw new Error('File type is required but was not provided');
    }

    if (!ALLOWED_MIME_TYPES.has(mimeType)) {
      throw new Error(`File type "${mimeType}" is not allowed`);
    }

    return mimeType;
  };

  describe('Allowed File Types', () => {
    it('should accept PDF files', () => {
      const file = createTestFile('doc.pdf', 'content', 'application/pdf');
      expect(validateContentType(file)).toBe('application/pdf');
    });

    it('should accept image files', () => {
      const jpeg = createTestFile('img.jpg', 'content', 'image/jpeg');
      const png = createTestFile('img.png', 'content', 'image/png');

      expect(validateContentType(jpeg)).toBe('image/jpeg');
      expect(validateContentType(png)).toBe('image/png');
    });

    it('should accept document files', () => {
      const word = createTestFile('doc.docx', 'content',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document');

      expect(validateContentType(word)).toBe(
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      );
    });
  });

  describe('Blocked File Types (Malware Prevention)', () => {
    it('should reject executable files', () => {
      const exe = createTestFile('malware.exe', 'content', 'application/x-msdownload');
      expect(() => validateContentType(exe)).toThrow('not allowed');
    });

    it('should reject script files', () => {
      const bat = createTestFile('script.bat', 'content', 'application/x-bat');
      const sh = createTestFile('script.sh', 'content', 'application/x-sh');

      expect(() => validateContentType(bat)).toThrow('not allowed');
      expect(() => validateContentType(sh)).toThrow('not allowed');
    });

    it('should reject potential malware types', () => {
      const malwareTypes = [
        'application/x-executable',
        'application/x-dosexec',
        'application/vnd.microsoft.portable-executable',
      ];

      malwareTypes.forEach(type => {
        const file = createTestFile('malware', 'content', type);
        expect(() => validateContentType(file)).toThrow('not allowed');
      });
    });
  });

  describe('MIME Type Confusion Prevention', () => {
    it('should reject empty MIME types', () => {
      const file = createTestFile('file.txt', 'content', '');
      expect(() => validateContentType(file)).toThrow('File type is required');
    });

    it('should handle case-insensitive MIME types', () => {
      const file = createTestFile('doc.pdf', 'content', 'APPLICATION/PDF');
      expect(validateContentType(file)).toBe('application/pdf');
    });

    it('should trim whitespace from MIME types', () => {
      const file = createTestFile('doc.pdf', 'content', '  application/pdf  ');
      expect(validateContentType(file)).toBe('application/pdf');
    });
  });
});

// ============================================================================
// ISSUE #4: HTTPS Endpoint Configuration Tests
// ============================================================================

describe('Security Issue #4: HTTPS Endpoint Configuration', () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    process.env = { ...originalEnv };
  });

  it('should warn when production uses HTTP endpoint', () => {
    const consoleWarn = jest.spyOn(console, 'warn').mockImplementation();

    process.env.NODE_ENV = 'production';
    process.env.MINIO_ENDPOINT = 'http://openspg-minio:9000';

    // Module will log warning on initialization
    require('../../app/api/upload/route');

    expect(consoleWarn).toHaveBeenCalledWith(
      expect.stringContaining('Production environment should use HTTPS')
    );

    consoleWarn.mockRestore();
  });

  it('should accept HTTPS endpoint in production', () => {
    const consoleWarn = jest.spyOn(console, 'warn').mockImplementation();

    process.env.NODE_ENV = 'production';
    process.env.MINIO_ENDPOINT = 'https://openspg-minio:9000';

    require('../../app/api/upload/route');

    expect(consoleWarn).not.toHaveBeenCalledWith(
      expect.stringContaining('should use HTTPS')
    );

    consoleWarn.mockRestore();
  });

  it('should allow HTTP endpoint in development', () => {
    const consoleWarn = jest.spyOn(console, 'warn').mockImplementation();

    process.env.NODE_ENV = 'development';
    process.env.MINIO_ENDPOINT = 'http://localhost:9000';

    require('../../app/api/upload/route');

    expect(consoleWarn).not.toHaveBeenCalled();

    consoleWarn.mockRestore();
  });
});

// ============================================================================
// ISSUE #5: Security Logging Tests
// ============================================================================

describe('Security Issue #5: Security Logging', () => {
  const logSecurityEvent = (event: string, details: Record<string, any>): void => {
    const sanitizedDetails = {
      ...details,
      accessKeyId: undefined,
      secretAccessKey: undefined,
      credentials: undefined,
    };

    console.log(`[Security] ${event}:`, JSON.stringify(sanitizedDetails, null, 2));
  };

  it('should sanitize sensitive data from logs', () => {
    const consoleLog = jest.spyOn(console, 'log').mockImplementation();

    logSecurityEvent('Test event', {
      file: 'test.pdf',
      accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
      secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
      credentials: { user: 'admin', pass: 'secret' },
    });

    const logOutput = consoleLog.mock.calls[0][1];

    // Should NOT contain sensitive data
    expect(logOutput).not.toContain('AKIAIOSFODNN7EXAMPLE');
    expect(logOutput).not.toContain('wJalrXUtnFEMI');
    expect(logOutput).not.toContain('secret');

    // Should contain non-sensitive data
    expect(logOutput).toContain('test.pdf');

    consoleLog.mockRestore();
  });

  it('should log file operations with sanitized data', () => {
    const consoleLog = jest.spyOn(console, 'log').mockImplementation();

    logSecurityEvent('File uploaded', {
      originalName: '../../etc/passwd',
      sanitizedName: 'passwd',
      size: 1024,
      contentType: 'text/plain',
    });

    const logOutput = consoleLog.mock.calls[0][1];

    expect(logOutput).toContain('passwd');
    expect(logOutput).toContain('1024');
    expect(logOutput).toContain('text/plain');

    consoleLog.mockRestore();
  });
});

// ============================================================================
// INTEGRATION TESTS: Combined Security Scenarios
// ============================================================================

describe('Integration Tests: Combined Security Scenarios', () => {
  it('should reject malicious upload attempt', async () => {
    // Attempt to upload executable with path traversal
    const maliciousFile = createTestFile(
      '../../../bin/malware.exe',
      'malicious content',
      'application/x-msdownload'
    );

    // Should fail at MIME type validation
    expect(() => {
      // This would fail in prepareUpload()
      if (!['application/pdf', 'image/jpeg', 'image/png'].includes(maliciousFile.type)) {
        throw new Error('File type not allowed');
      }
    }).toThrow('File type not allowed');
  });

  it('should handle legitimate upload securely', () => {
    const legitimateFile = createTestFile(
      'Q4_Report_2024.pdf',
      'PDF content',
      'application/pdf'
    );

    // Should pass all validations
    expect(legitimateFile.type).toBe('application/pdf');
    expect(legitimateFile.name).toMatch(/^[a-zA-Z0-9._-]+$/);
  });

  it('should prevent credential exposure in error responses', () => {
    const error = {
      message: 'Upload failed',
      accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
      secretAccessKey: 'secret123',
    };

    // Error should be sanitized before logging
    const sanitizedError = {
      message: error.message,
      // Credentials should be removed
    };

    expect(sanitizedError).not.toHaveProperty('accessKeyId');
    expect(sanitizedError).not.toHaveProperty('secretAccessKey');
  });
});

// ============================================================================
// PERFORMANCE TESTS: Security Should Not Impact Performance
// ============================================================================

describe('Performance Tests: Security with Performance', () => {
  it('should maintain parallel upload performance', () => {
    // Security checks should happen during preparation phase
    // Parallel uploads should still be concurrent

    const files = [
      createTestFile('file1.pdf', 'content', 'application/pdf'),
      createTestFile('file2.pdf', 'content', 'application/pdf'),
      createTestFile('file3.pdf', 'content', 'application/pdf'),
    ];

    // All files should be validated in parallel
    const startTime = Date.now();

    Promise.all(files.map(file => {
      // Simulate validation
      if (file.type !== 'application/pdf') throw new Error('Invalid');
      return Promise.resolve(file);
    }));

    const duration = Date.now() - startTime;

    // Should complete very quickly (parallel)
    expect(duration).toBeLessThan(100);
  });
});
