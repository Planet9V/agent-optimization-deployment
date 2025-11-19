/**
 * Redis Health Check Tests
 * Tests for Redis connection validation and retry logic
 * NOTE: Skipped - using in-memory queue instead of Redis
 */

// import { validateRedisConnection, waitForRedis, redis } from '@/config/redis.config';

describe.skip('Redis Health Check', () => {
  // Tests skipped - using in-memory queue instead of Redis
  it('should skip Redis tests', () => {
    expect(true).toBe(true);
  });
});
