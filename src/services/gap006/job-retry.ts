/**
 * File: job-retry.ts
 * Created: 2025-11-15
 * Modified: 2025-11-15
 * Version: v1.0.0
 * Author: AEON FORGE
 * Purpose: Retry logic with exponential backoff for GAP-006
 * Dependencies: None
 * Status: ACTIVE
 */

interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  exponentialBase: number;
  jitterEnabled: boolean;
}

interface RetryResult<T> {
  success: boolean;
  result?: T;
  error?: Error;
  attempts: number;
  totalTimeMs: number;
}

class JobRetryService {
  private defaultConfig: RetryConfig = {
    maxRetries: 5,
    baseDelayMs: 1000,
    maxDelayMs: 60000,
    exponentialBase: 2,
    jitterEnabled: true
  };

  /**
   * Execute operation with exponential backoff retry
   * @param operation Function to execute
   * @param config Retry configuration
   * @returns Retry result
   */
  async executeWithRetry<T>(
    operation: () => Promise<T>,
    config?: Partial<RetryConfig>
  ): Promise<RetryResult<T>> {
    const mergedConfig = { ...this.defaultConfig, ...config };
    const startTime = Date.now();
    let lastError: Error | undefined;

    for (let attempt = 0; attempt < mergedConfig.maxRetries; attempt++) {
      try {
        const result = await operation();
        return {
          success: true,
          result,
          attempts: attempt + 1,
          totalTimeMs: Date.now() - startTime
        };
      } catch (error) {
        lastError = error as Error;

        // Don't retry on last attempt
        if (attempt === mergedConfig.maxRetries - 1) {
          break;
        }

        // Calculate delay with exponential backoff
        const delayMs = this.calculateDelay(attempt, mergedConfig);

        // Wait before retry
        await this.sleep(delayMs);
      }
    }

    return {
      success: false,
      error: lastError,
      attempts: mergedConfig.maxRetries,
      totalTimeMs: Date.now() - startTime
    };
  }

  /**
   * Calculate delay with exponential backoff and jitter
   * @param attemptNumber Current attempt number (0-based)
   * @param config Retry configuration
   * @returns Delay in milliseconds
   */
  private calculateDelay(attemptNumber: number, config: RetryConfig): number {
    // Exponential backoff: baseDelay * (exponentialBase ^ attemptNumber)
    const exponentialDelay = config.baseDelayMs *
      Math.pow(config.exponentialBase, attemptNumber);

    // Cap at max delay
    let delay = Math.min(exponentialDelay, config.maxDelayMs);

    // Add jitter to prevent thundering herd
    if (config.jitterEnabled) {
      const jitter = Math.random() * delay * 0.3;  // ±30% jitter
      delay = delay - (delay * 0.15) + jitter;
    }

    return Math.floor(delay);
  }

  /**
   * Sleep for specified milliseconds
   * @param ms Milliseconds to sleep
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Check if error is retryable
   * @param error Error to check
   * @returns True if error should be retried
   */
  isRetryableError(error: Error): boolean {
    const retryablePatterns = [
      /ECONNREFUSED/,
      /ETIMEDOUT/,
      /ENOTFOUND/,
      /network/i,
      /timeout/i,
      /temporary/i,
      /unavailable/i
    ];

    return retryablePatterns.some(pattern =>
      pattern.test(error.message) || pattern.test(error.name)
    );
  }

  /**
   * Execute with conditional retry based on error type
   * @param operation Function to execute
   * @param config Retry configuration
   * @returns Retry result
   */
  async executeWithConditionalRetry<T>(
    operation: () => Promise<T>,
    config?: Partial<RetryConfig>
  ): Promise<RetryResult<T>> {
    const mergedConfig = { ...this.defaultConfig, ...config };
    const startTime = Date.now();
    let lastError: Error | undefined;

    for (let attempt = 0; attempt < mergedConfig.maxRetries; attempt++) {
      try {
        const result = await operation();
        return {
          success: true,
          result,
          attempts: attempt + 1,
          totalTimeMs: Date.now() - startTime
        };
      } catch (error) {
        lastError = error as Error;

        // Check if error is retryable
        if (!this.isRetryableError(lastError)) {
          // Non-retryable error, fail immediately
          return {
            success: false,
            error: lastError,
            attempts: attempt + 1,
            totalTimeMs: Date.now() - startTime
          };
        }

        // Don't retry on last attempt
        if (attempt === mergedConfig.maxRetries - 1) {
          break;
        }

        // Calculate delay and retry
        const delayMs = this.calculateDelay(attempt, mergedConfig);
        await this.sleep(delayMs);
      }
    }

    return {
      success: false,
      error: lastError,
      attempts: mergedConfig.maxRetries,
      totalTimeMs: Date.now() - startTime
    };
  }

  /**
   * Get retry schedule for given configuration
   * @param config Retry configuration
   * @returns Array of delay times in milliseconds
   */
  getRetrySchedule(config?: Partial<RetryConfig>): number[] {
    const mergedConfig = { ...this.defaultConfig, ...config };
    const schedule: number[] = [];

    for (let i = 0; i < mergedConfig.maxRetries - 1; i++) {
      schedule.push(this.calculateDelay(i, mergedConfig));
    }

    return schedule;
  }
}

export default JobRetryService;
export { RetryConfig, RetryResult };
