# Redis Health Check Implementation

## Overview
Redis connection validation with automatic retry logic to ensure the document processing queue can connect reliably to Redis before starting workers.

## Implementation Details

### Files Modified
1. `config/redis.config.ts` - Added health check functions
2. `lib/queue/documentQueue.ts` - Integrated health checks into worker initialization

### Functions Added

#### `validateRedisConnection(redisClient: Redis): Promise<boolean>`
Validates Redis connection using PING command.

**Parameters:**
- `redisClient`: Redis client instance to validate

**Returns:**
- `true` if connection is valid (receives PONG response)
- `false` if connection fails

**Behavior:**
- Sends PING command to Redis
- Logs success (✅) or failure (❌) to console
- Catches and logs connection errors

#### `waitForRedis(redisClient: Redis, maxRetries: number = 5): Promise<void>`
Waits for Redis connection with retry logic.

**Parameters:**
- `redisClient`: Redis client instance
- `maxRetries`: Maximum number of retry attempts (default: 5)

**Returns:**
- Resolves when connection is successful
- Rejects with error after maxRetries attempts

**Behavior:**
- Initiates connection if not already connected
- Retries up to `maxRetries` times
- 2-second delay between retry attempts
- Logs retry attempts to console
- Throws descriptive error on final failure

### Integration into Document Queue

#### Changes to `getDocumentWorker()`
```typescript
export async function getDocumentWorker(): Promise<Worker<DocumentJobData>> {
  if (!workerInstance) {
    // Validate Redis connection before creating worker
    try {
      await waitForRedis(redis);
    } catch (err) {
      console.error('Redis connection failed:', errorMessage);
      throw new Error(`Cannot create worker without Redis connection: ${errorMessage}`);
    }

    // ... rest of worker initialization
  }
  return workerInstance;
}
```

**Key Changes:**
1. Function now returns `Promise<Worker>` instead of synchronous return
2. Calls `waitForRedis()` before worker creation
3. Fails fast with descriptive error if Redis unavailable
4. Prevents worker creation with invalid Redis connection

## Usage

### Basic Usage
```typescript
import { redis, waitForRedis } from '@/config/redis.config';

// Wait for Redis before using it
await waitForRedis(redis);

// Now safe to use Redis-dependent operations
const worker = await getDocumentWorker();
```

### Custom Retry Configuration
```typescript
// Use fewer retries for faster failure detection
await waitForRedis(redis, 3);

// Use more retries for slower/unreliable networks
await waitForRedis(redis, 10);
```

## Error Handling

### Connection Failure
```
❌ Redis connection failed: Connection refused
Retrying Redis connection (1/5)...
❌ Redis connection failed: Connection refused
Retrying Redis connection (2/5)...
...
Error: Could not connect to Redis after 5 retries
```

### Worker Creation Failure
```
Redis connection failed: Could not connect to Redis after 5 retries
Error: Cannot create worker without Redis connection: Could not connect to Redis after 5 retries
```

## Testing

### Unit Tests
Located in `tests/redis-health-check.test.ts`:

1. **validateRedisConnection** tests:
   - ✓ Returns true for valid connections
   - ✓ Returns false for failed connections

2. **waitForRedis** tests:
   - ✓ Succeeds when Redis is available
   - ✓ Retries on connection failure
   - ✓ Respects maxRetries parameter
   - ✓ Correct retry timing (2s delay per retry)

### Running Tests
```bash
npm test tests/redis-health-check.test.ts
```

## Performance Impact

### Startup Time
- **Success Case**: ~10-50ms (single PING roundtrip)
- **Retry Case**: ~2 seconds per retry attempt
- **Max Failure Time**: ~10 seconds (5 retries × 2s delay)

### Benefits
1. **Fail Fast**: Detect Redis issues immediately at startup
2. **Reliability**: Automatic retry handles temporary connection issues
3. **Clear Feedback**: Console logging provides visibility into connection status
4. **Safety**: Prevents worker creation with invalid Redis connection

## Configuration

### Environment Variables
```bash
# Redis connection settings (from .env)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=optional_password
REDIS_DB=0
```

### Retry Configuration
Default: 5 retries with 2-second delays

To customize:
```typescript
// In application code
await waitForRedis(redis, 3); // 3 retries
```

## Monitoring

### Log Messages
```
✅ Redis connection validated          # Success
❌ Redis connection failed: [error]    # Failure
Retrying Redis connection (N/M)...     # Retry attempt
```

### Metrics to Track
- Connection success rate
- Average retry count
- Time to successful connection
- Failure rate after max retries

## Troubleshooting

### Common Issues

1. **"Could not connect to Redis after N retries"**
   - Check Redis is running: `redis-cli ping`
   - Verify REDIS_HOST and REDIS_PORT environment variables
   - Check network connectivity
   - Review Redis logs

2. **"Invalid PING response"**
   - Redis is running but not responding correctly
   - Check Redis configuration
   - Verify authentication (REDIS_PASSWORD)

3. **Slow connection attempts**
   - Network latency issues
   - Redis overloaded
   - Consider increasing retry delay or reducing maxRetries

## Future Enhancements

Potential improvements:
1. Exponential backoff for retry delays
2. Health check endpoint for monitoring
3. Automatic reconnection on connection loss
4. Circuit breaker pattern for repeated failures
5. Metrics collection for observability
