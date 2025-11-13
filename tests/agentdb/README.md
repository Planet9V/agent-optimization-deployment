# AgentDB Test Suite

Comprehensive test suite for GAP-002 AgentDB implementation with 100+ tests.

## Test Files

1. **agent-db.test.ts** - Core AgentDB functionality (40+ tests)
   - Initialization and configuration
   - L1 cache operations
   - L2 Qdrant integration
   - Multi-level caching
   - TTL management
   - Cache statistics
   - Error handling

2. **qdrant-client.test.ts** - Qdrant integration (35+ tests)
   - Collection management
   - Point storage and retrieval
   - Similarity search
   - Batch operations
   - Filters and queries
   - Error handling

3. **embedding-service.test.ts** - Embedding generation (30+ tests)
   - Model initialization
   - Embedding generation
   - Caching
   - Batch processing
   - Performance validation

4. **performance.test.ts** - Performance benchmarks (25+ tests)
   - L1 cache latency (< 1ms target)
   - L2 cache latency (< 10ms target)
   - Embedding generation (< 5ms target)
   - Cache hit rate measurement
   - Speedup calculations (150-12,500x)
   - Throughput benchmarks

5. **integration.test.ts** - End-to-end integration (20+ tests)
   - Full workflow testing
   - Multiple agent types
   - Real Qdrant integration (optional)
   - Fallback scenarios
   - Resource management

## Running Tests

### Run All Tests
```bash
npm test -- tests/agentdb
```

### Run Specific Test File
```bash
npm test -- tests/agentdb/agent-db.test.ts
npm test -- tests/agentdb/performance.test.ts
```

### Run with Coverage
```bash
npm test -- tests/agentdb --coverage
```

### Watch Mode
```bash
npm test -- tests/agentdb --watch
```

### Integration Tests (with real Qdrant)
```bash
QDRANT_URL=http://localhost:6333 TEST_INTEGRATION=true npm test -- tests/agentdb/integration.test.ts
```

## Test Configuration

### jest.config.js
- Coverage thresholds: >90% for statements, branches, functions, lines
- Test timeout: 30s for performance tests
- TypeScript support via ts-jest
- HTML and JUnit reports

### jest.setup.ts
- Global test utilities
- Mock setup
- Custom matchers

## Coverage Targets

- **Statements**: >90%
- **Branches**: >85%
- **Functions**: >90%
- **Lines**: >90%

## Performance Targets

- **L1 Cache Latency**: < 1ms
- **L2 Cache Latency**: < 10ms
- **Embedding Generation**: < 5ms
- **Cache Hit Rate**: >80% (production workload)
- **Speedup**: 150-12,500x (vs no caching)

## Test Reports

Test reports are generated in:
- `tests/agentdb/reports/` - JUnit XML and HTML reports
- `tests/agentdb/coverage/` - Coverage reports

## Environment Variables

- `QDRANT_URL` - Qdrant server URL (default: http://localhost:6333)
- `QDRANT_API_KEY` - Qdrant API key
- `TEST_INTEGRATION` - Enable integration tests with real Qdrant
- `DEBUG_TESTS` - Enable debug logging during tests

## Mocking Strategy

- **Embedding Service**: Mocked @xenova/transformers pipeline
- **Qdrant Client**: Mocked @qdrant/js-client-rest
- **Integration Tests**: Can use real Qdrant or mocks

## Common Issues

### Tests fail with "EISDIR: illegal operation on a directory"
- Make sure you're using `Read(file_path)` not `Read(directory_path)`
- Use `Bash("ls directory")` or `Glob("directory/*")` to explore directories

### Integration tests timeout
- Ensure Qdrant server is running if `TEST_INTEGRATION=true`
- Check `QDRANT_URL` environment variable

### Coverage below threshold
- Run with `--coverage` to see uncovered lines
- Check if all error paths are tested

## Test Utilities

Global test utilities available via `global.testUtils`:

- `createMockAgentConfig()` - Create mock agent configuration
- `createMockEmbedding()` - Create mock embedding vector
- `createMockSearchResult()` - Create mock search result
- `waitFor()` - Wait for condition with timeout
- `measureTime()` - Measure async function execution time

## CI/CD Integration

Tests are designed to run in CI/CD without real Qdrant:
- All tests pass with mocked dependencies
- Integration tests auto-skip if Qdrant unavailable
- Coverage reports generated for quality gates
