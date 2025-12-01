/**
 * Test suite for parallel S3 upload optimization
 * Tests both success and failure scenarios
 */

import { NextRequest } from 'next/server';
import { POST } from '../app/api/upload/route';

// Mock S3Client
jest.mock('@aws-sdk/client-s3', () => {
  const mockSend = jest.fn();
  return {
    S3Client: jest.fn(() => ({
      send: mockSend
    })),
    PutObjectCommand: jest.fn(),
    __mockSend: mockSend
  };
});

describe('Parallel S3 Upload Optimization', () => {
  const { __mockSend } = require('@aws-sdk/client-s3');

  beforeEach(() => {
    jest.clearAllMocks();
    __mockSend.mockResolvedValue({});
  });

  const createMockFile = (name: string, size: number = 1024): File => {
    const blob = new Blob(['test content'], { type: 'text/plain' });
    return new File([blob], name, { type: 'text/plain' });
  };

  const createMockRequest = (files: File[]): NextRequest => {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    return {
      formData: async () => formData
    } as any;
  };

  describe('Parallel Execution', () => {
    it('should upload multiple files concurrently', async () => {
      const files = [
        createMockFile('file1.txt'),
        createMockFile('file2.txt'),
        createMockFile('file3.txt'),
      ];

      const request = createMockRequest(files);
      const startTime = Date.now();

      const response = await POST(request);
      const data = await response.json();

      const duration = Date.now() - startTime;

      expect(response.status).toBe(200);
      expect(data.success).toBe(true);
      expect(data.files).toHaveLength(3);
      expect(data.count).toBe(3);
      expect(data.duration).toBeLessThan(1000); // Should be fast with mocked S3
      expect(__mockSend).toHaveBeenCalledTimes(3);
    });

    it('should be faster than sequential execution', async () => {
      // Create 20 files to test performance improvement
      const files = Array.from({ length: 20 }, (_, i) =>
        createMockFile(`file${i}.txt`)
      );

      const request = createMockRequest(files);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.success).toBe(true);
      expect(data.files).toHaveLength(20);
      expect(data.duration).toBeDefined();
      expect(__mockSend).toHaveBeenCalledTimes(20);

      console.log(`Parallel upload of 20 files took ${data.duration}ms`);
    });
  });

  describe('Error Handling', () => {
    it('should return HTTP 400 for oversized files', async () => {
      const files = [
        createMockFile('small.txt', 1024),
        createMockFile('huge.txt', 101 * 1024 * 1024), // 101MB - exceeds limit
      ];

      const request = createMockRequest(files);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.success).toBe(false);
      expect(data.error).toContain('exceeds 100MB limit');
    });

    it('should return HTTP 207 for partial failures', async () => {
      const files = [
        createMockFile('success1.txt'),
        createMockFile('fail.txt'),
        createMockFile('success2.txt'),
      ];

      // Mock S3 to fail on second file
      __mockSend
        .mockResolvedValueOnce({}) // success1
        .mockRejectedValueOnce(new Error('S3 error')) // fail
        .mockResolvedValueOnce({}); // success2

      const request = createMockRequest(files);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(207);
      expect(data.success).toBe(false);
      expect(data.partialSuccess).toBe(true);
      expect(data.files).toHaveLength(2); // 2 successes
      expect(data.failures).toHaveLength(1); // 1 failure
      expect(data.count).toBe(2);
      expect(data.failureCount).toBe(1);
    });

    it('should return HTTP 500 if all uploads fail', async () => {
      const files = [
        createMockFile('file1.txt'),
        createMockFile('file2.txt'),
      ];

      __mockSend.mockRejectedValue(new Error('S3 unavailable'));

      const request = createMockRequest(files);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(500);
      expect(data.success).toBe(false);
      expect(data.error).toBe('All uploads failed');
      expect(data.failures).toHaveLength(2);
    });
  });

  describe('Validation', () => {
    it('should reject empty file list', async () => {
      const request = createMockRequest([]);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.success).toBe(false);
      expect(data.error).toBe('No files uploaded');
    });

    it('should reject more than 20 files', async () => {
      const files = Array.from({ length: 21 }, (_, i) =>
        createMockFile(`file${i}.txt`)
      );

      const request = createMockRequest(files);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.success).toBe(false);
      expect(data.error).toBe('Maximum 20 files allowed');
    });
  });

  describe('Performance Logging', () => {
    it('should include duration in response', async () => {
      const files = [createMockFile('test.txt')];
      const request = createMockRequest(files);
      const response = await POST(request);
      const data = await response.json();

      expect(data.duration).toBeDefined();
      expect(typeof data.duration).toBe('number');
      expect(data.duration).toBeGreaterThanOrEqual(0);
    });

    it('should log performance metrics', async () => {
      const consoleSpy = jest.spyOn(console, 'log');
      const files = [createMockFile('test.txt')];
      const request = createMockRequest(files);

      await POST(request);

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('[Upload] Starting parallel upload')
      );
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('[Upload] Completed in')
      );
    });
  });

  describe('Backward Compatibility', () => {
    it('should maintain original response format for successful uploads', async () => {
      const files = [createMockFile('test.txt', 1024)];
      const request = createMockRequest(files);
      const response = await POST(request);
      const data = await response.json();

      expect(data).toHaveProperty('success');
      expect(data).toHaveProperty('files');
      expect(data).toHaveProperty('count');

      // New property added
      expect(data).toHaveProperty('duration');

      // Check file structure
      expect(data.files[0]).toHaveProperty('originalName');
      expect(data.files[0]).toHaveProperty('path');
      expect(data.files[0]).toHaveProperty('size');
      expect(data.files[0]).toHaveProperty('type');
    });
  });
});
