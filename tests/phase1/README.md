# Phase 1 Test Suite - McKenney-Lacan Gap Closure

Comprehensive test suite for Phase 1 implementations covering all 4 gaps plus integration tests.

## Test Coverage

### ML-004: Temporal Versioning (`test_ml004_temporal_versioning.py`)
- ✓ Create Actor with temporal properties
- ✓ Query point-in-time snapshot
- ✓ Version history accurate
- ✓ Property isolation
- ✓ Concurrent updates
- ✓ Query performance (<100ms)

### ML-005: WebSocket EWS (`test_ml005_websocket_ews.py`)
- ✓ Connect to WebSocket
- ✓ Subscribe to EWS alerts
- ✓ Receive alert when threshold breached
- ✓ <1 second latency
- ✓ Multiple subscriptions
- ✓ Metrics calculation accuracy
- ✓ Reconnection handling

### ML-010: Cascade Tracking (`test_ml010_cascade_tracking.py`)
- ✓ Create CascadeEvent
- ✓ Track genealogy (parent→child)
- ✓ Calculate velocity
- ✓ Query cascade tree
- ✓ Pattern analysis
- ✓ Cycle detection
- ✓ Branch merging

### ML-011: Batch Prediction (`test_ml011_batch_prediction.py`)
- ✓ Submit batch request
- ✓ Job queues correctly
- ✓ Job completes in <1 minute for 100 entities
- ✓ Results retrievable
- ✓ Priority queue handling
- ✓ Job cancellation
- ✓ Error handling
- ✓ Concurrent jobs
- ✓ Prediction accuracy

### Integration Tests (`test_phase1_integration.py`)
- ✓ Temporal versioning + cascade tracking work together
- ✓ EWS alerts trigger correctly
- ✓ Batch predictions use temporal data
- ✓ Complete workflow integration (all 4 gaps)

## Running Tests

### Install Dependencies
```bash
cd tests/phase1
pip install -r requirements.txt
```

### Run All Tests
```bash
# Run complete test suite with results matrix
python run_all_tests.py

# Run specific gap tests
pytest test_ml004_temporal_versioning.py -v
pytest test_ml005_websocket_ews.py -v
pytest test_ml010_cascade_tracking.py -v
pytest test_ml011_batch_prediction.py -v
pytest test_phase1_integration.py -v

# Run with coverage
pytest --cov=src --cov-report=html

# Run only integration tests
pytest -m integration
```

### Test Results

Results are saved to:
- `phase1_test_results.json` - Detailed JSON results
- `phase1_test_results.txt` - Human-readable results matrix
- `phase1_qdrant_document.json` - Qdrant-ready document

### Store Results to Qdrant

```bash
python scripts/store_to_qdrant.py \
    tests/phase1/phase1_qdrant_document.json \
    phase1-test-results
```

## Test Success Criteria

### Individual Gap Tests
- All unit tests pass (100% pass rate)
- Performance requirements met:
  - ML-004: <100ms query latency
  - ML-005: <1 second alert latency
  - ML-011: <60 seconds for 100 entities

### Integration Tests
- All components work together seamlessly
- No conflicts between implementations
- End-to-end workflow completes successfully
- Data flows correctly between components

## Expected Output

```
==================================================================================
PHASE 1 TEST RESULTS MATRIX
==================================================================================

Overall Status: PASS
Total Tests: 45
Passed: 45
Failed: 0
Pass Rate: 100.0%
Total Duration: 87.43s

----------------------------------------------------------------------------------
ML-004: Temporal Versioning
----------------------------------------------------------------------------------
Tests: 6 | Passed: 6 | Failed: 0 | Pass Rate: 100.0%

  ✓ test_create_temporal_actor (0.234s)
  ✓ test_point_in_time_snapshot (0.342s)
  ✓ test_version_history_accuracy (0.567s)
  ...

----------------------------------------------------------------------------------
ML-005: WebSocket EWS
----------------------------------------------------------------------------------
Tests: 8 | Passed: 8 | Failed: 0 | Pass Rate: 100.0%

  ✓ test_websocket_connection (0.123s)
  ✓ test_subscribe_to_ews (0.234s)
  ✓ test_ews_alert_trigger (0.456s)
  ...

[... additional gaps ...]

==================================================================================
```

## Troubleshooting

### WebSocket Tests Fail
- Ensure port 8765-8767 are available
- Check firewall settings
- Verify asyncio event loop configuration

### Batch Prediction Timeouts
- Increase timeout in `pytest.ini`
- Check system resources
- Verify queue processing is enabled

### Integration Test Failures
- Run individual gap tests first
- Check for resource conflicts
- Verify all services are running

## Next Steps

After successful Phase 1 testing:
1. Review results matrix
2. Store results to Qdrant for documentation
3. Proceed to Phase 2 implementation
4. Update main project documentation with test coverage

## Contributing

When adding new tests:
1. Follow existing naming conventions
2. Update this README with new test cases
3. Ensure tests are independent and repeatable
4. Add appropriate markers (unit, integration, slow)
5. Update expected output examples
