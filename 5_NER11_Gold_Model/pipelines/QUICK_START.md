# Quick Start Guide - NER11 Bulk Document Processor

**Version**: 1.0.0 | **Status**: ✅ Production Ready

---

## 1-Minute Setup

```bash
# Start services
docker-compose up ner11-gold-api qdrant -d

# Verify services
curl http://localhost:8000/health
curl http://localhost:6333/collections
```

---

## 2-Minute Test

```bash
# Run validation tests
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 pipelines/test_bulk_processor.py

# Expected: ✅ ALL TESTS PASSED
```

---

## 3-Minute Processing

```python
from pipelines.bulk_document_processor import BulkDocumentProcessor

# Initialize
processor = BulkDocumentProcessor()

# Process all documents
report = processor.process_all_documents()

# View results
processor.print_report(report)
```

**Expected Output**:
```
Processing documents: 100%|██████████| 42/42 [02:15<00:00]
✅ Hierarchy validation PASSED
✅ Processing COMPLETE
```

---

## Common Commands

### Process Documents
```bash
python3 pipelines/bulk_document_processor.py
```

### Run Tests
```bash
python3 pipelines/test_bulk_processor.py
```

### View Logs
```bash
tail -f logs/bulk_processor.log
```

### Check Registry
```bash
wc -l logs/processed_documents.jsonl  # Count processed docs
jq . logs/processed_documents.jsonl | less  # Pretty print
```

### View Report
```bash
cat logs/bulk_processing_report.json | jq .
```

---

## Key Files

| File | Purpose |
|------|---------|
| `bulk_document_processor.py` | Main processor |
| `test_bulk_processor.py` | Validation tests |
| `logs/bulk_processor.log` | Processing log |
| `logs/processed_documents.jsonl` | Document registry |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Services not running | `docker-compose up -d` |
| Tests failing | Check service health |
| Slow processing | Check API/Qdrant logs |
| Documents skipped | Normal (idempotent) |

---

## Next Steps

1. ✅ Run validation tests
2. ✅ Process small batch (42 docs)
3. ⚠️ Expand corpus to 1,000+ docs
4. ✅ Verify validation report

---

**Full Documentation**: See `BULK_PROCESSOR_DOCUMENTATION.md`
**Implementation Report**: See `TASK_1_4_COMPLETION_REPORT.md`
