/**
 * GAP-006 Redis Client for Job Queue Management
 *
 * Provides atomic job queue operations using Redis:
 * - BRPOPLPUSH for atomic job acquisition
 * - ZADD for priority queues
 * - SETEX for worker heartbeat
 * - HSET for job state tracking
 */

import Redis from 'ioredis';
import { EventEmitter } from 'events';

// Queue names
export const QUEUE_NAMES = {
  PENDING: 'gap006:pending-queue',
  PROCESSING: 'gap006:processing-queue',
  HIGH_PRIORITY: 'gap006:high-priority-queue',
  MEDIUM_PRIORITY: 'gap006:medium-priority-queue',
  LOW_PRIORITY: 'gap006:low-priority-queue',
  DEAD_LETTER: 'gap006:dead-letter-queue',
} as const;

// Job priority levels
export enum JobPriority {
  HIGH = 3,
  MEDIUM = 2,
  LOW = 1,
}

// Job state
export enum JobState {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  DEAD_LETTER = 'dead_letter',
}

export interface JobData {
  id: string;
  type: string;
  payload: unknown;
  priority: JobPriority;
  createdAt: number;
  attempts: number;
  maxAttempts: number;
  timeout?: number;
}

export interface WorkerHeartbeat {
  workerId: string;
  jobId: string;
  timestamp: number;
}

export class RedisJobClient extends EventEmitter {
  private redis: Redis;
  private subscriber: Redis;
  private connectionRetries = 0;
  private maxRetries = 10;
  private retryDelay = 1000;
  private connected = false;

  constructor(options?: {
    host?: string;
    port?: number;
    password?: string;
    db?: number;
    maxRetries?: number;
    retryDelay?: number;
  }) {
    super();

    const config = {
      host: options?.host || process.env.REDIS_HOST || 'localhost',
      port: options?.port || parseInt(process.env.REDIS_PORT || '6380'),
      password: options?.password || process.env.REDIS_PASSWORD || 'redis@openspg',
      db: options?.db || 0,
      retryStrategy: (times: number) => this.getRetryDelay(times),
      maxRetriesPerRequest: 3,
      enableReadyCheck: true,
      lazyConnect: true,
    };

    this.maxRetries = options?.maxRetries || 10;
    this.retryDelay = options?.retryDelay || 1000;

    // Main Redis client
    this.redis = new Redis(config);

    // Subscriber client for pub/sub
    this.subscriber = new Redis(config);

    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    this.redis.on('connect', () => {
      this.connected = true;
      this.connectionRetries = 0;
      this.emit('connected');
    });

    this.redis.on('error', (err) => {
      this.emit('error', err);
    });

    this.redis.on('close', () => {
      this.connected = false;
      this.emit('disconnected');
    });

    this.subscriber.on('message', (channel, message) => {
      this.emit('message', channel, message);
    });
  }

  private getRetryDelay(times: number): number {
    if (times > this.maxRetries) {
      this.emit('error', new Error(`Max retries (${this.maxRetries}) exceeded`));
      return -1; // Stop retrying
    }

    this.connectionRetries = times;
    // Exponential backoff with jitter
    const delay = Math.min(this.retryDelay * Math.pow(2, times - 1), 30000);
    const jitter = Math.random() * 1000;
    return delay + jitter;
  }

  /**
   * Connect to Redis
   */
  async connect(): Promise<void> {
    try {
      await Promise.all([
        this.redis.connect(),
        this.subscriber.connect(),
      ]);
    } catch (error) {
      throw new Error(`Failed to connect to Redis: ${error}`);
    }
  }

  /**
   * Disconnect from Redis
   */
  async disconnect(): Promise<void> {
    await Promise.all([
      this.redis.quit(),
      this.subscriber.quit(),
    ]);
    this.connected = false;
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.connected && this.redis.status === 'ready';
  }

  /**
   * Enqueue a job with priority
   */
  async enqueueJob(job: JobData): Promise<void> {
    const jobJson = JSON.stringify(job);
    const timestamp = Date.now();

    // Use pipeline for atomic operation
    const pipeline = this.redis.pipeline();

    // Add to priority queue (sorted set)
    const priorityQueue = this.getPriorityQueue(job.priority);
    pipeline.zadd(priorityQueue, timestamp, jobJson);

    // Add to pending queue
    pipeline.lpush(QUEUE_NAMES.PENDING, jobJson);

    // Set job state
    pipeline.hset(`gap006:job:${job.id}`, {
      state: JobState.PENDING,
      data: jobJson,
      createdAt: timestamp,
      updatedAt: timestamp,
    });

    await pipeline.exec();
  }

  /**
   * Atomically acquire next job using BRPOPLPUSH
   */
  async acquireJob(workerId: string, timeout = 5): Promise<JobData | null> {
    try {
      // BRPOPLPUSH is atomic: pop from pending, push to processing
      const result = await this.redis.brpoplpush(
        QUEUE_NAMES.PENDING,
        QUEUE_NAMES.PROCESSING,
        timeout
      );

      if (!result) {
        return null;
      }

      const job: JobData = JSON.parse(result);

      // Update job state and set worker heartbeat
      const pipeline = this.redis.pipeline();

      pipeline.hset(`gap006:job:${job.id}`, {
        state: JobState.PROCESSING,
        workerId,
        startedAt: Date.now(),
        updatedAt: Date.now(),
      });

      // Set worker heartbeat with TTL
      const heartbeatTTL = job.timeout || 300; // 5 minutes default
      pipeline.setex(
        `gap006:worker:${workerId}:heartbeat`,
        heartbeatTTL,
        JSON.stringify({
          workerId,
          jobId: job.id,
          timestamp: Date.now(),
        })
      );

      await pipeline.exec();

      return job;
    } catch (error) {
      this.emit('error', new Error(`Failed to acquire job: ${error}`));
      return null;
    }
  }

  /**
   * Complete a job successfully
   */
  async completeJob(jobId: string, result?: unknown): Promise<void> {
    const pipeline = this.redis.pipeline();

    // Remove from processing queue
    pipeline.lrem(QUEUE_NAMES.PROCESSING, 1, jobId);

    // Update job state
    pipeline.hset(`gap006:job:${jobId}`, {
      state: JobState.COMPLETED,
      result: result ? JSON.stringify(result) : '',
      completedAt: Date.now(),
      updatedAt: Date.now(),
    });

    await pipeline.exec();
  }

  /**
   * Fail a job and optionally retry or send to DLQ
   */
  async failJob(jobId: string, error: Error, retry = true): Promise<void> {
    const jobData = await this.getJobData(jobId);
    if (!jobData) {
      throw new Error(`Job ${jobId} not found`);
    }

    const job: JobData = JSON.parse(jobData);
    job.attempts += 1;

    const pipeline = this.redis.pipeline();

    // Remove from processing queue
    pipeline.lrem(QUEUE_NAMES.PROCESSING, 1, JSON.stringify(job));

    if (retry && job.attempts < job.maxAttempts) {
      // Re-queue for retry
      const timestamp = Date.now();
      pipeline.lpush(QUEUE_NAMES.PENDING, JSON.stringify(job));
      pipeline.hset(`gap006:job:${jobId}`, {
        state: JobState.PENDING,
        attempts: job.attempts,
        lastError: error.message,
        updatedAt: timestamp,
      });
    } else {
      // Send to dead letter queue
      pipeline.lpush(QUEUE_NAMES.DEAD_LETTER, JSON.stringify(job));
      pipeline.hset(`gap006:job:${jobId}`, {
        state: JobState.DEAD_LETTER,
        attempts: job.attempts,
        lastError: error.message,
        failedAt: Date.now(),
        updatedAt: Date.now(),
      });
    }

    await pipeline.exec();
  }

  /**
   * Update worker heartbeat
   */
  async updateHeartbeat(workerId: string, jobId: string, ttl = 300): Promise<void> {
    const heartbeat: WorkerHeartbeat = {
      workerId,
      jobId,
      timestamp: Date.now(),
    };

    await this.redis.setex(
      `gap006:worker:${workerId}:heartbeat`,
      ttl,
      JSON.stringify(heartbeat)
    );
  }

  /**
   * Get job data
   */
  async getJobData(jobId: string): Promise<string | null> {
    return await this.redis.hget(`gap006:job:${jobId}`, 'data');
  }

  /**
   * Get job state
   */
  async getJobState(jobId: string): Promise<Record<string, string> | null> {
    const state = await this.redis.hgetall(`gap006:job:${jobId}`);
    return Object.keys(state).length > 0 ? state : null;
  }

  /**
   * Get queue length
   */
  async getQueueLength(queueName: string): Promise<number> {
    return await this.redis.llen(queueName);
  }

  /**
   * Get all queue lengths
   */
  async getAllQueueLengths(): Promise<Record<string, number>> {
    const pipeline = this.redis.pipeline();

    Object.values(QUEUE_NAMES).forEach((queue) => {
      pipeline.llen(queue);
    });

    const results = await pipeline.exec();

    if (!results) {
      return {};
    }

    const lengths: Record<string, number> = {};
    Object.keys(QUEUE_NAMES).forEach((key, index) => {
      const queueName = QUEUE_NAMES[key as keyof typeof QUEUE_NAMES];
      lengths[queueName] = (results[index]?.[1] as number) || 0;
    });

    return lengths;
  }

  /**
   * Get priority queue name based on priority level
   */
  private getPriorityQueue(priority: JobPriority): string {
    switch (priority) {
      case JobPriority.HIGH:
        return QUEUE_NAMES.HIGH_PRIORITY;
      case JobPriority.MEDIUM:
        return QUEUE_NAMES.MEDIUM_PRIORITY;
      case JobPriority.LOW:
        return QUEUE_NAMES.LOW_PRIORITY;
      default:
        return QUEUE_NAMES.MEDIUM_PRIORITY;
    }
  }

  /**
   * Subscribe to job events
   */
  async subscribe(channel: string, handler: (message: string) => void): Promise<void> {
    await this.subscriber.subscribe(channel);
    this.subscriber.on('message', (ch, msg) => {
      if (ch === channel) {
        handler(msg);
      }
    });
  }

  /**
   * Publish job event
   */
  async publish(channel: string, message: unknown): Promise<void> {
    await this.redis.publish(channel, JSON.stringify(message));
  }

  /**
   * Get Redis client for advanced operations
   */
  getClient(): Redis {
    return this.redis;
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<boolean> {
    try {
      const result = await this.redis.ping();
      return result === 'PONG';
    } catch {
      return false;
    }
  }
}

// Singleton instance
let redisClient: RedisJobClient | null = null;

export function getRedisClient(options?: Parameters<typeof RedisJobClient.prototype.constructor>[0]): RedisJobClient {
  if (!redisClient) {
    redisClient = new RedisJobClient(options);
  }
  return redisClient;
}

export async function closeRedisClient(): Promise<void> {
  if (redisClient) {
    await redisClient.disconnect();
    redisClient = null;
  }
}
