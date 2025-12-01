# Phase 1 Tests - Quick Start Guide

## 🚀 One-Command Execution

```bash
cd /home/jim/2_OXOT_Projects_Dev/tests/phase1
python run_all_tests.py
```

## 📊 What Gets Tested

| Gap | Feature | Key Tests | Performance |
|-----|---------|-----------|-------------|
| ML-004 | Temporal Versioning | 6 tests | <100ms queries |
| ML-005 | WebSocket EWS | 8 tests | <1s alerts |
| ML-010 | Cascade Tracking | 8 tests | <200ms genealogy |
| ML-011 | Batch Prediction | 10 tests | <60s for 100 entities |
| Integration | All gaps together | 4 tests | Complete workflow |

**Total**: 45+ tests, ~90 seconds

## ✅ Success Indicators

```
Overall Status: PASS
Total Tests: 45
Passed: 45
Failed: 0
Pass Rate: 100.0%
```

## 📁 Output Files

- `phase1_test_results.txt` - Results matrix
- `phase1_test_results.json` - Detailed JSON
- `phase1_qdrant_document.json` - For Qdrant storage

## 🔧 Individual Tests

```bash
# Temporal versioning
pytest test_ml004_temporal_versioning.py -v

# WebSocket EWS
pytest test_ml005_websocket_ews.py -v

# Cascade tracking
pytest test_ml010_cascade_tracking.py -v

# Batch prediction
pytest test_ml011_batch_prediction.py -v

# Integration
pytest test_phase1_integration.py -v
```

## 🐛 Quick Fixes

```bash
# Port conflicts
lsof -ti:8765 | xargs kill -9

# Install deps
pip install -r requirements.txt

# Clean test cache
pytest --cache-clear
```

## 📚 Full Documentation

See `PHASE1_TEST_EXECUTION_GUIDE.md` for comprehensive details.
