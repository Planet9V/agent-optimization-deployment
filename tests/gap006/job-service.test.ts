/**
 * File: job-service.test.ts
 * Created: 2025-11-15
 * Modified: 2025-11-15
 * Version: v1.0.0
 * Author: AEON FORGE
 * Purpose: Unit tests for job lifecycle service
 * Dependencies: jest, @types/jest
 * Status: ACTIVE
 */

import JobService from '../../src/services/gap006/job-service';
import JobRetryService from '../../src/services/gap006/job-retry';
import { Pool } from 'pg';
import Redis from 'ioredis';

// Mock dependencies
jest.mock('pg');
jest.mock('ioredis');

describe('JobService', () => {
  let jobService: JobService;
  let mockPool: jest.Mocked<Pool>;
  let mockRedis: jest.Mocked<Redis>;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Create mock instances
    mockPool = {
      query: jest.fn(),
      end: jest.fn()
    } as any;

    mockRedis = {
      zadd: jest.fn(),
      brpoplpush: jest.fn(),
      lrem: jest.fn(),
      hset: jest.fn(),
      hgetall: jest.fn(),
      expire: jest.fn(),
      quit: jest.fn()
    } as any;

    // Mock constructors
    (Pool as jest.MockedClass<typeof Pool>).mockImplementation(() => mockPool);
    (Redis as jest.MockedClass<typeof Redis>).mockImplementation(() => mockRedis);

    jobService = new JobService();
  });

  afterEach(async () => {
    await jobService.close();
  });

  describe('createJob', () => {
    it('should create job with correct priority queue', async () => {
      const mockJobId = 'job-123';
      mockPool.query.mockResolvedValueOnce({
        rows: [{ job_id: mockJobId }]
      } as any);

      const jobId = await jobService.createJob({
        jobType: 'email-notification',
        payload: { userId: 'user-1', message: 'Test' },
        priority: 4
      });

      expect(jobId).toBe(mockJobId);
      expect(mockPool.query).toHaveBeenCalledWith(
        expect.stringContaining('INSERT INTO jobs'),
        expect.arrayContaining(['email-notification', 'PENDING', 4])
      );
      expect(mockRedis.zadd).toHaveBeenCalledWith(
        'gap006:high-priority-queue',
        expect.any(Number),
        mockJobId
      );
    });

    it('should use default priority if not specified', async () => {
      const mockJobId = 'job-456';
      mockPool.query.mockResolvedValueOnce({
        rows: [{ job_id: mockJobId }]
      } as any);

      await jobService.createJob({
        jobType: 'report-generation',
        payload: { reportId: 'report-1' }
      });

      expect(mockRedis.zadd).toHaveBeenCalledWith(
        'gap006:low-priority-queue',
        expect.any(Number),
        mockJobId
      );
    });
  });

  describe('acquireJob', () => {
    it('should acquire job atomically from high priority queue first', async () => {
      const mockJobId = 'job-789';
      mockRedis.brpoplpush.mockResolvedValueOnce(mockJobId);

      const jobId = await jobService.acquireJob('worker-1');

      expect(jobId).toBe(mockJobId);
      expect(mockRedis.brpoplpush).toHaveBeenCalledWith(
        'gap006:high-priority-queue',
        'gap006:processing-queue',
        5
      );
      expect(mockPool.query).toHaveBeenCalledWith(
        expect.stringContaining('UPDATE jobs'),
        expect.arrayContaining([mockJobId, 'worker-1'])
      );
    });

    it('should try medium priority queue if high priority is empty', async () => {
      mockRedis.brpoplpush
        .mockResolvedValueOnce(null)  // High priority empty
        .mockResolvedValueOnce('job-medium');  // Medium priority has job

      const jobId = await jobService.acquireJob('worker-2');

      expect(jobId).toBe('job-medium');
      expect(mockRedis.brpoplpush).toHaveBeenCalledTimes(2);
    });

    it('should return null if no jobs available in any queue', async () => {
      mockRedis.brpoplpush.mockResolvedValue(null);

      const jobId = await jobService.acquireJob('worker-3');

      expect(jobId).toBeNull();
      expect(mockRedis.brpoplpush).toHaveBeenCalledTimes(3);  // All 3 queues
    });
  });

  describe('completeJob', () => {
    it('should mark job as completed and update worker stats', async () => {
      await jobService.completeJob('job-complete', { status: 'success' });

      expect(mockPool.query).toHaveBeenCalledWith(
        expect.stringContaining('UPDATE jobs'),
        expect.arrayContaining(['job-complete'])
      );
      expect(mockRedis.lrem).toHaveBeenCalledWith(
        'gap006:processing-queue',
        1,
        'job-complete'
      );
      expect(mockRedis.hset).toHaveBeenCalledWith(
        'gap006:job:job-complete',
        expect.objectContaining({ status: 'COMPLETED' })
      );
    });
  });

  describe('failJob', () => {
    it('should retry job if under max retries', async () => {
      mockPool.query.mockResolvedValueOnce({
        rows: [{ retry_count: 2, max_retries: 5 }]
      } as any);

      await jobService.failJob('job-fail', 'Connection timeout');

      expect(mockPool.query).toHaveBeenCalledWith(
        expect.stringContaining('UPDATE jobs'),
        expect.arrayContaining(['job-fail', 'Connection timeout'])
      );
      expect(mockRedis.zadd).toHaveBeenCalledWith(
        'gap006:medium-priority-queue',
        expect.any(Number),
        'job-fail'
      );
    });

    it('should move to dead letter queue if max retries exceeded', async () => {
      mockPool.query.mockResolvedValueOnce({
        rows: [{ retry_count: 5, max_retries: 5 }]
      } as any);

      await jobService.failJob('job-dead', 'Fatal error');

      expect(mockPool.query).toHaveBeenCalledWith(
        expect.stringContaining('INSERT INTO dead_letter_queue'),
        expect.arrayContaining(['job-dead', 'Fatal error'])
      );
      expect(mockRedis.zadd).toHaveBeenCalledWith(
        'gap006:dead-letter-queue',
        expect.any(Number),
        'job-dead'
      );
    });
  });

  describe('getJobStatus', () => {
    it('should return job status with metadata', async () => {
      mockPool.query.mockResolvedValueOnce({
        rows: [{ status: 'COMPLETED', error_message: null }]
      } as any);
      mockRedis.hgetall.mockResolvedValueOnce({
        result: JSON.stringify({ data: 'test' }),
        completedAt: '2025-11-15T10:00:00Z'
      });

      const status = await jobService.getJobStatus('job-status');

      expect(status).toEqual({
        jobId: 'job-status',
        status: 'COMPLETED',
        result: { data: 'test' },
        error: null
      });
    });

    it('should throw error if job not found', async () => {
      mockPool.query.mockResolvedValueOnce({ rows: [] } as any);

      await expect(jobService.getJobStatus('nonexistent')).rejects.toThrow(
        'Job not found: nonexistent'
      );
    });
  });
});

describe('JobRetryService', () => {
  let retryService: JobRetryService;

  beforeEach(() => {
    retryService = new JobRetryService();
  });

  describe('executeWithRetry', () => {
    it('should succeed on first attempt', async () => {
      const operation = jest.fn().mockResolvedValue('success');

      const result = await retryService.executeWithRetry(operation);

      expect(result.success).toBe(true);
      expect(result.result).toBe('success');
      expect(result.attempts).toBe(1);
      expect(operation).toHaveBeenCalledTimes(1);
    });

    it('should retry on failure and eventually succeed', async () => {
      const operation = jest.fn()
        .mockRejectedValueOnce(new Error('Temporary failure'))
        .mockRejectedValueOnce(new Error('Temporary failure'))
        .mockResolvedValueOnce('success');

      const result = await retryService.executeWithRetry(operation, {
        maxRetries: 5,
        baseDelayMs: 10
      });

      expect(result.success).toBe(true);
      expect(result.attempts).toBe(3);
      expect(operation).toHaveBeenCalledTimes(3);
    });

    it('should fail after max retries', async () => {
      const operation = jest.fn().mockRejectedValue(new Error('Permanent failure'));

      const result = await retryService.executeWithRetry(operation, {
        maxRetries: 3,
        baseDelayMs: 10
      });

      expect(result.success).toBe(false);
      expect(result.error?.message).toBe('Permanent failure');
      expect(result.attempts).toBe(3);
      expect(operation).toHaveBeenCalledTimes(3);
    });
  });

  describe('isRetryableError', () => {
    it('should identify retryable errors', () => {
      expect(retryService.isRetryableError(new Error('ECONNREFUSED'))).toBe(true);
      expect(retryService.isRetryableError(new Error('Network timeout'))).toBe(true);
      expect(retryService.isRetryableError(new Error('Service unavailable'))).toBe(true);
    });

    it('should identify non-retryable errors', () => {
      expect(retryService.isRetryableError(new Error('Invalid input'))).toBe(false);
      expect(retryService.isRetryableError(new Error('Authentication failed'))).toBe(false);
    });
  });

  describe('getRetrySchedule', () => {
    it('should calculate exponential backoff schedule', () => {
      const schedule = retryService.getRetrySchedule({
        maxRetries: 5,
        baseDelayMs: 1000,
        exponentialBase: 2,
        jitterEnabled: false
      });

      expect(schedule).toHaveLength(4);
      expect(schedule[0]).toBe(1000);   // 1000 * 2^0
      expect(schedule[1]).toBe(2000);   // 1000 * 2^1
      expect(schedule[2]).toBe(4000);   // 1000 * 2^2
      expect(schedule[3]).toBe(8000);   // 1000 * 2^3
    });

    it('should cap delays at maxDelayMs', () => {
      const schedule = retryService.getRetrySchedule({
        maxRetries: 5,
        baseDelayMs: 1000,
        maxDelayMs: 5000,
        exponentialBase: 2,
        jitterEnabled: false
      });

      expect(schedule.every(delay => delay <= 5000)).toBe(true);
    });
  });
});
