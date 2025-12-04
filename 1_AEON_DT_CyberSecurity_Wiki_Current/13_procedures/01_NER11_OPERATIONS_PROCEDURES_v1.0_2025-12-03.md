# NER11 Gold Standard - Operations Procedures Manual

**File**: 01_NER11_OPERATIONS_PROCEDURES_v1.0_2025-12-03.md
**Created**: 2025-12-03 00:00:00 UTC
**Modified**: 2025-12-03 00:00:00 UTC
**Version**: v1.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete operational procedures for NER11 Gold Standard Model
**Status**: ACTIVE

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              NER11 GOLD STANDARD - OPERATIONS PROCEDURES                     ║
║                                                                              ║
║   ┌────────────────────────────────────────────────────────────────────┐    ║
║   │  PRODUCTION MODEL: ner11_v3                                        │    ║
║   │  MODEL PATH: models/ner11_v3/model-best                            │    ║
║   │  API VERSION: 3.3.0                                                │    ║
║   │  STATUS: ACTIVE                                                    │    ║
║   └────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Table of Contents

1. [Quick Reference Card](#1-quick-reference-card)
2. [Startup Procedures](#2-startup-procedures)
3. [Shutdown Procedures](#3-shutdown-procedures)
4. [Health Monitoring](#4-health-monitoring)
5. [Model Validation](#5-model-validation)
6. [Document Ingestion](#6-document-ingestion)
7. [Troubleshooting Procedures](#7-troubleshooting-procedures)
8. [Backup and Recovery](#8-backup-and-recovery)
9. [Maintenance Procedures](#9-maintenance-procedures)
10. [Emergency Procedures](#10-emergency-procedures)

---

## 1. Quick Reference Card

### 1.1 Essential Commands

```bash
# Start Services
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
source venv/bin/activate
uvicorn serve_model:app --host 0.0.0.0 --port 8000

# Check Service Health
curl http://localhost:8000/health

# Validate Model
python utils/model_validator.py --model ner11_v3

# Test Entity Extraction
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text": "APT29 exploited CVE-2024-12345"}'

# Check Qdrant
curl http://localhost:6333/collections/ner11_entities_hierarchical

# Check Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "MATCH (n) RETURN count(n)"
```

### 1.2 Service Ports

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| NER11 API | 8000 | HTTP | Entity extraction, search |
| Neo4j Bolt | 7687 | Bolt | Graph database |
| Neo4j HTTP | 7474 | HTTP | Neo4j Browser |
| Qdrant | 6333 | HTTP | Vector database |
| Qdrant gRPC | 6334 | gRPC | Vector database (gRPC) |

### 1.3 Critical Paths

| Resource | Path |
|----------|------|
| Production Model | `models/ner11_v3/model-best` |
| API Server | `serve_model.py` |
| Model Validator | `utils/model_validator.py` |
| Context Augmentation | `utils/context_augmentation.py` |
| Embedding Service | `pipelines/entity_embedding_service_hierarchical.py` |
| Ingestion Scripts | `scripts/` |
| Logs | `logs/` |

---

## 2. Startup Procedures

### 2.1 Full System Startup (Recommended Order)

#### Step 1: Start Infrastructure Services

```bash
# 1.1 Start Neo4j (if not already running)
docker start openspg-neo4j

# 1.2 Verify Neo4j is ready (wait for "Started")
docker logs -f openspg-neo4j | grep -m1 "Started"

# 1.3 Start Qdrant (if not already running)
docker start qdrant

# 1.4 Verify Qdrant is ready
curl http://localhost:6333/collections
```

#### Step 2: Start NER11 API Service

```bash
# 2.1 Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# 2.2 Activate virtual environment
source venv/bin/activate

# 2.3 Set environment variables (if needed)
export MODEL_PATH="models/ner11_v3/model-best"
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="neo4j@openspg"
export QDRANT_HOST="localhost"
export QDRANT_PORT="6333"

# 2.4 Start API server
uvicorn serve_model:app --host 0.0.0.0 --port 8000

# Or with auto-reload for development:
# uvicorn serve_model:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 3: Verify All Services

```bash
# 3.1 Check NER11 API health
curl http://localhost:8000/health

# Expected output:
# {
#   "status": "healthy",
#   "ner_model_custom": "loaded",
#   "ner_model_fallback": "loaded",
#   "model_checksum": "verified",
#   "pattern_extraction": "enabled",
#   "semantic_search": "available",
#   "neo4j_graph": "connected",
#   "version": "3.3.0"
# }

# 3.2 Test entity extraction
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text": "APT29 used T1566.001"}'

# 3.3 Check Qdrant collection
curl http://localhost:6333/collections/ner11_entities_hierarchical

# 3.4 Check Neo4j connection
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1"
```

### 2.2 Startup Checklist

- [ ] Neo4j container is running and accepting connections
- [ ] Qdrant container is running and collection exists
- [ ] Python virtual environment activated
- [ ] Environment variables set correctly
- [ ] NER11 API server started without errors
- [ ] Health check returns "healthy" status
- [ ] Model checksum verified
- [ ] Test entity extraction working
- [ ] Semantic search returning results
- [ ] Neo4j graph queries working

---

## 3. Shutdown Procedures

### 3.1 Graceful Shutdown

```bash
# 3.1.1 Stop NER11 API (Ctrl+C if running in foreground)
# Or if running as background process:
pkill -f "uvicorn serve_model:app"

# 3.1.2 Stop Qdrant (optional - usually left running)
docker stop qdrant

# 3.1.3 Stop Neo4j (optional - usually left running)
docker stop openspg-neo4j

# 3.1.4 Deactivate virtual environment
deactivate
```

### 3.2 Emergency Shutdown

```bash
# Kill all related processes immediately
pkill -9 -f "uvicorn serve_model"
docker stop --time 10 openspg-neo4j qdrant
```

### 3.3 Shutdown Checklist

- [ ] Verify no active API requests in progress
- [ ] Stop NER11 API server gracefully
- [ ] Verify no background ingestion processes running
- [ ] Stop Qdrant (if needed)
- [ ] Stop Neo4j (if needed)
- [ ] Log shutdown time and reason

---

## 4. Health Monitoring

### 4.1 Health Check API

```bash
# Full health check
curl http://localhost:8000/health | python3 -m json.tool

# Quick status check
curl -s http://localhost:8000/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'])"
```

### 4.2 Health Status Interpretation

| Field | Healthy Value | Degraded | Action |
|-------|---------------|----------|--------|
| `status` | `healthy` | `unhealthy` | Investigate immediately |
| `ner_model_custom` | `loaded` | `not_loaded` | Check model path |
| `ner_model_fallback` | `loaded` | `not_loaded` | Check spaCy installation |
| `model_checksum` | `verified` | `not_verified` | Run validation, check for corruption |
| `pattern_extraction` | `enabled` | `disabled` | Check context_augmentation.py |
| `semantic_search` | `available` | `not_available` | Check Qdrant connection |
| `neo4j_graph` | `connected` | `not_connected` | Check Neo4j container |

### 4.3 Continuous Monitoring Script

```bash
#!/bin/bash
# health_monitor.sh - Run every 5 minutes via cron

LOG_FILE="/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/health_$(date +%Y%m%d).log"

# Check API health
HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
STATUS=$(echo $HEALTH | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null)

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

if [ "$STATUS" = "healthy" ]; then
    echo "$TIMESTAMP - OK - API healthy" >> $LOG_FILE
else
    echo "$TIMESTAMP - ALERT - API status: $STATUS" >> $LOG_FILE
    echo "$TIMESTAMP - Full response: $HEALTH" >> $LOG_FILE
    # Send alert (customize as needed)
    # mail -s "NER11 API Alert" admin@example.com < $LOG_FILE
fi

# Check Qdrant
QDRANT=$(curl -s http://localhost:6333/collections/ner11_entities_hierarchical 2>/dev/null)
if [ -z "$QDRANT" ]; then
    echo "$TIMESTAMP - ALERT - Qdrant not responding" >> $LOG_FILE
fi

# Check Neo4j
NEO4J=$(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1" 2>/dev/null)
if [ -z "$NEO4J" ]; then
    echo "$TIMESTAMP - ALERT - Neo4j not responding" >> $LOG_FILE
fi
```

### 4.4 Metrics Collection

```bash
# Get Qdrant collection stats
curl -s http://localhost:6333/collections/ner11_entities_hierarchical | python3 -c "
import sys, json
d = json.load(sys.stdin)
r = d.get('result', {})
print(f\"Qdrant Entities: {r.get('points_count', 0):,}\")
print(f\"Indexed Vectors: {r.get('indexed_vectors_count', 0):,}\")
"

# Get Neo4j stats
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "
MATCH (n) RETURN labels(n)[0] as label, count(n) as count
ORDER BY count DESC LIMIT 10
"
```

---

## 5. Model Validation

### 5.1 Full Validation Procedure

```bash
# Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# Activate environment
source venv/bin/activate

# Run full validation (requires API running)
python utils/model_validator.py --model ner11_v3 --api-url http://localhost:8000

# Store result in Qdrant registry
python utils/model_validator.py --model ner11_v3 --api-url http://localhost:8000 --store-result
```

### 5.2 Checksum-Only Validation

```bash
# Quick checksum check (no API required)
python utils/model_validator.py --model ner11_v3 --checksum-only

# Expected output:
# Checksum verification: PASSED
```

### 5.3 Entity Tests Only

```bash
# Run entity extraction tests (requires API)
python utils/model_validator.py --model ner11_v3 --tests-only --api-url http://localhost:8000

# Expected output:
# Entity tests: 8/8 passed
```

### 5.4 Manual Checksum Verification

```bash
# Calculate current checksums
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/models/ner11_v3/model-best

# Verify meta.json
md5sum meta.json
# Expected: 0710e14d78a87d54866208cc6a5c8de3

# Verify ner/model
md5sum ner/model
# Expected: f326672a81a00c54be06422aae07ecf1
```

### 5.5 Validation Test Cases

| Test ID | Input | Expected Label | Min Confidence |
|---------|-------|----------------|----------------|
| T001 | APT29 | APT_GROUP | 0.90 |
| T002 | CVE-2024-12345 | CVE | 1.00 |
| T003 | T1566.001 | TECHNIQUE | 1.00 |
| T004 | CWE-79 | CWE | 1.00 |
| T005 | Cobalt Strike | MALWARE | 0.90 |
| T006 | TA0001 | TACTIC | 1.00 |
| T007 | IEC 62443-3-3 | IEC_62443 | 0.85 |
| T008 | TID-001 | MITRE_EM3D | 1.00 |

---

## 6. Document Ingestion

### 6.1 Single Document Ingestion

```bash
# Navigate to project
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# Ingest single document
python scripts/ingest_wiki_documents.py \
  --wiki-root "/path/to/documents" \
  --file "specific_document.md"
```

### 6.2 Batch Document Ingestion

```bash
# Ingest all documents in directory
python scripts/ingest_wiki_documents.py \
  --wiki-root "/path/to/documents" \
  --all

# Rate-limited ingestion (recommended for large batches)
python scripts/rate_limited_ingest.py \
  --wiki-root "/path/to/documents" \
  --delay 5 \
  --timeout 120
```

### 6.3 Chunked Ingestion for Large Documents

```bash
# For documents larger than 50KB
python scripts/chunked_ingest.py \
  --wiki-root "/path/to/documents" \
  --chunk-size 50000 \
  --all
```

### 6.4 Monitor Ingestion Progress

```bash
# Check Qdrant entity count during ingestion
while true; do
  COUNT=$(curl -s http://localhost:6333/collections/ner11_entities_hierarchical | \
    python3 -c "import sys,json; print(json.load(sys.stdin)['result']['points_count'])")
  echo "$(date '+%H:%M:%S') - Entities: $COUNT"
  sleep 30
done
```

### 6.5 Ingestion Best Practices

1. **Always check API health before starting**
2. **Use rate-limited ingestion for large batches** (>100 documents)
3. **Monitor entity count during ingestion**
4. **Chunk documents larger than 50KB**
5. **Log all ingestion sessions** with timestamps and document counts
6. **Verify ingestion completion** with sample queries

---

## 7. Troubleshooting Procedures

### 7.1 API Not Starting

**Symptom**: `uvicorn` fails to start or crashes immediately

```bash
# Check for port conflicts
lsof -i :8000

# Kill conflicting process
kill -9 $(lsof -t -i:8000)

# Check model path exists
ls -la models/ner11_v3/model-best/

# Verify spaCy installation
python -c "import spacy; print(spacy.__version__)"

# Check Python dependencies
pip list | grep -E "spacy|fastapi|uvicorn"

# Start with verbose logging
uvicorn serve_model:app --host 0.0.0.0 --port 8000 --log-level debug
```

### 7.2 Model Not Loading

**Symptom**: Health check shows `ner_model_custom: not_loaded`

```bash
# Verify model files exist
ls -la models/ner11_v3/model-best/
ls -la models/ner11_v3/model-best/ner/

# Check model can be loaded manually
python -c "
import spacy
nlp = spacy.load('models/ner11_v3/model-best')
print('Model loaded successfully')
print('Labels:', nlp.get_pipe('ner').labels)
"

# Check for missing dependencies
python -c "
try:
    import spacy_transformers
    print('spacy-transformers OK')
except ImportError:
    print('MISSING: pip install spacy-transformers')
"
```

### 7.3 Checksum Verification Failing

**Symptom**: `model_checksum: not_verified`

```bash
# Calculate actual checksums
cd models/ner11_v3/model-best
md5sum meta.json
md5sum ner/model

# Compare with expected (from model_validator.py):
# meta.json: 0710e14d78a87d54866208cc6a5c8de3
# ner/model: f326672a81a00c54be06422aae07ecf1

# If mismatch, model may be corrupted - restore from backup
```

### 7.4 Neo4j Connection Issues

**Symptom**: `neo4j_graph: not_connected`

```bash
# Check container status
docker ps | grep neo4j

# Start if not running
docker start openspg-neo4j

# Check logs for errors
docker logs --tail 50 openspg-neo4j

# Test connection
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1"

# Check network connectivity
nc -zv localhost 7687
```

### 7.5 Qdrant Connection Issues

**Symptom**: `semantic_search: not_available`

```bash
# Check container status
docker ps | grep qdrant

# Start if not running
docker start qdrant

# Check health
curl http://localhost:6333/health

# Check collection exists
curl http://localhost:6333/collections/ner11_entities_hierarchical

# If collection missing, recreate
# (See section 8.4 for collection recreation)
```

### 7.6 Slow Entity Extraction

**Symptom**: API latency >500ms for simple queries

```bash
# Check system resources
top -b -n 1 | head -20

# Check if GPU is being used (if available)
nvidia-smi

# Check for memory pressure
free -h

# Restart API to clear any accumulated state
pkill -f "uvicorn serve_model:app"
uvicorn serve_model:app --host 0.0.0.0 --port 8000
```

### 7.7 Entity Extraction Not Finding Entities

**Symptom**: Known patterns (e.g., "APT29") not being extracted

```bash
# Test pattern extraction directly
python -c "
from utils.context_augmentation import extract_pattern_entities
entities = extract_pattern_entities('APT29 used CVE-2024-12345')
for e in entities:
    print(f'{e.text}: {e.label} ({e.confidence})')
"

# Test fallback model
python -c "
import spacy
nlp = spacy.load('en_core_web_trf')
doc = nlp('Microsoft announced a vulnerability')
for ent in doc.ents:
    print(f'{ent.text}: {ent.label_}')
"

# Check context augmentation module is loaded
curl http://localhost:8000/health | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('Pattern extraction:', d.get('pattern_extraction'))
"
```

---

## 8. Backup and Recovery

### 8.1 Model Backup Procedure

```bash
# Create timestamped backup
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/mnt/d/1_Apps_to_Build/AEON_Cyber_Digital_Twin_backups/ner11_v3_${BACKUP_DATE}"

mkdir -p "$BACKUP_DIR"
cp -r models/ner11_v3 "$BACKUP_DIR/"

# Verify backup
ls -la "$BACKUP_DIR/ner11_v3/model-best/"
md5sum "$BACKUP_DIR/ner11_v3/model-best/meta.json"
md5sum "$BACKUP_DIR/ner11_v3/model-best/ner/model"
```

### 8.2 Qdrant Collection Backup

```bash
# Create Qdrant snapshot
curl -X POST "http://localhost:6333/collections/ner11_entities_hierarchical/snapshots"

# List snapshots
curl http://localhost:6333/collections/ner11_entities_hierarchical/snapshots

# Download snapshot
SNAPSHOT_NAME="ner11_entities_hierarchical-TIMESTAMP.snapshot"
curl -o "qdrant_backup_$(date +%Y%m%d).snapshot" \
  "http://localhost:6333/collections/ner11_entities_hierarchical/snapshots/$SNAPSHOT_NAME"
```

### 8.3 Neo4j Database Backup

```bash
# Stop Neo4j first for consistent backup
docker stop openspg-neo4j

# Backup data directory
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
tar -czvf "/mnt/d/1_Apps_to_Build/AEON_Cyber_Digital_Twin_backups/neo4j_${BACKUP_DATE}.tar.gz" \
  /path/to/neo4j/data

# Restart Neo4j
docker start openspg-neo4j
```

### 8.4 Model Recovery Procedure

```bash
# 1. Stop API
pkill -f "uvicorn serve_model:app"

# 2. Restore model from backup
BACKUP_PATH="/mnt/d/1_Apps_to_Build/AEON_Cyber_Digital_Twin_backups/ner11_v3_YYYYMMDD"
rm -rf models/ner11_v3
cp -r "$BACKUP_PATH/ner11_v3" models/

# 3. Verify checksums
python utils/model_validator.py --model ner11_v3 --checksum-only

# 4. Restart API
uvicorn serve_model:app --host 0.0.0.0 --port 8000

# 5. Verify health
curl http://localhost:8000/health
```

### 8.5 Qdrant Collection Recovery

```bash
# Restore from snapshot
SNAPSHOT_PATH="/path/to/qdrant_backup.snapshot"

# Delete existing collection (if corrupted)
curl -X DELETE http://localhost:6333/collections/ner11_entities_hierarchical

# Restore from snapshot
curl -X POST "http://localhost:6333/collections/ner11_entities_hierarchical/snapshots/recover" \
  -H "Content-Type: application/json" \
  -d "{\"location\": \"$SNAPSHOT_PATH\"}"

# Verify restoration
curl http://localhost:6333/collections/ner11_entities_hierarchical
```

---

## 9. Maintenance Procedures

### 9.1 Weekly Maintenance

```bash
#!/bin/bash
# weekly_maintenance.sh

echo "=== NER11 Weekly Maintenance $(date) ==="

# 1. Verify model integrity
echo "1. Checking model checksums..."
python utils/model_validator.py --model ner11_v3 --checksum-only

# 2. Check disk space
echo "2. Checking disk space..."
df -h /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# 3. Check Qdrant collection health
echo "3. Checking Qdrant collection..."
curl -s http://localhost:6333/collections/ner11_entities_hierarchical | python3 -c "
import sys, json
d = json.load(sys.stdin)
r = d.get('result', {})
print(f\"   Entities: {r.get('points_count', 0):,}\")
print(f\"   Indexed: {r.get('indexed_vectors_count', 0):,}\")
print(f\"   Status: {d.get('status')}\")
"

# 4. Check Neo4j statistics
echo "4. Checking Neo4j statistics..."
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "
MATCH (n) RETURN count(n) as total_nodes
"

# 5. Rotate logs
echo "5. Rotating logs..."
find logs/ -name "*.log" -mtime +30 -exec gzip {} \;
find logs/ -name "*.log.gz" -mtime +90 -delete

echo "=== Maintenance Complete ==="
```

### 9.2 Monthly Maintenance

```bash
#!/bin/bash
# monthly_maintenance.sh

echo "=== NER11 Monthly Maintenance $(date) ==="

# 1. Full validation test
echo "1. Running full validation..."
python utils/model_validator.py --model ner11_v3 --api-url http://localhost:8000 --store-result

# 2. Create full backup
echo "2. Creating backups..."
./backup_all.sh

# 3. Check for outdated dependencies
echo "3. Checking dependencies..."
pip list --outdated | grep -E "spacy|fastapi|uvicorn|qdrant"

# 4. Optimize Qdrant collection
echo "4. Optimizing Qdrant collection..."
curl -X POST "http://localhost:6333/collections/ner11_entities_hierarchical/index"

echo "=== Monthly Maintenance Complete ==="
```

### 9.3 Log Rotation

```bash
# Add to crontab:
# 0 0 * * 0 /path/to/rotate_logs.sh

#!/bin/bash
# rotate_logs.sh

LOG_DIR="/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs"

# Compress logs older than 7 days
find $LOG_DIR -name "*.log" -mtime +7 -exec gzip {} \;

# Delete compressed logs older than 90 days
find $LOG_DIR -name "*.log.gz" -mtime +90 -delete

# Archive health check logs
mkdir -p $LOG_DIR/archive/$(date +%Y%m)
mv $LOG_DIR/health_*.log.gz $LOG_DIR/archive/$(date +%Y%m)/ 2>/dev/null
```

---

## 10. Emergency Procedures

### 10.1 API Unresponsive - Immediate Recovery

```bash
# 1. Force kill API process
pkill -9 -f "uvicorn serve_model:app"

# 2. Check for zombie processes
ps aux | grep -E "python|uvicorn" | grep -v grep

# 3. Clear any locks
rm -f /tmp/ner11_*.lock 2>/dev/null

# 4. Restart API
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
source venv/bin/activate
uvicorn serve_model:app --host 0.0.0.0 --port 8000 &

# 5. Verify recovery
sleep 10
curl http://localhost:8000/health
```

### 10.2 Model Corruption Detected

```bash
# 1. Stop API immediately
pkill -f "uvicorn serve_model:app"

# 2. Verify corruption
python utils/model_validator.py --model ner11_v3 --checksum-only

# 3. Restore from most recent backup
LATEST_BACKUP=$(ls -td /mnt/d/1_Apps_to_Build/AEON_Cyber_Digital_Twin_backups/ner11_v3_* | head -1)
echo "Restoring from: $LATEST_BACKUP"

rm -rf models/ner11_v3
cp -r "$LATEST_BACKUP/ner11_v3" models/

# 4. Verify restored model
python utils/model_validator.py --model ner11_v3 --checksum-only

# 5. Restart API
uvicorn serve_model:app --host 0.0.0.0 --port 8000 &

# 6. Run full validation
sleep 30
python utils/model_validator.py --model ner11_v3 --api-url http://localhost:8000
```

### 10.3 Qdrant Collection Corrupted

```bash
# 1. Check collection status
curl http://localhost:6333/collections/ner11_entities_hierarchical

# 2. If corrupted, delete and recreate
curl -X DELETE http://localhost:6333/collections/ner11_entities_hierarchical

# 3. Recreate collection with correct configuration
curl -X PUT http://localhost:6333/collections/ner11_entities_hierarchical \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    }
  }'

# 4. Re-ingest documents
python scripts/ingest_wiki_documents.py --wiki-root "/path/to/documents" --all
```

### 10.4 Emergency Contact Information

```yaml
escalation_contacts:
  level_1_support:
    description: "API issues, service restarts"
    response_time: "30 minutes"

  level_2_support:
    description: "Data corruption, recovery procedures"
    response_time: "2 hours"

  level_3_support:
    description: "Model retraining, architecture changes"
    response_time: "24 hours"
```

---

## Appendix A: Environment Setup Script

```bash
#!/bin/bash
# setup_environment.sh

# Set all required environment variables
export MODEL_PATH="models/ner11_v3/model-best"
export FALLBACK_MODEL="en_core_web_trf"
export USE_FALLBACK_NER="true"
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="neo4j@openspg"
export QDRANT_HOST="localhost"
export QDRANT_PORT="6333"
export QDRANT_COLLECTION="ner11_entities_hierarchical"
export NER_API_URL="http://localhost:8000"
export LOG_LEVEL="INFO"

echo "Environment configured for NER11 Gold Standard"
echo "Model: $MODEL_PATH"
echo "Neo4j: $NEO4J_URI"
echo "Qdrant: $QDRANT_HOST:$QDRANT_PORT"
```

---

## Appendix B: Cron Job Configuration

```bash
# /etc/cron.d/ner11_maintenance

# Health check every 5 minutes
*/5 * * * * jim /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/health_monitor.sh

# Weekly maintenance every Sunday at 2 AM
0 2 * * 0 jim /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/weekly_maintenance.sh

# Monthly maintenance on 1st of month at 3 AM
0 3 1 * * jim /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/monthly_maintenance.sh

# Daily log rotation at midnight
0 0 * * * jim /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/rotate_logs.sh

# Weekly backup every Saturday at 4 AM
0 4 * * 6 jim /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/backup_all.sh
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2025-12-03 | Initial comprehensive operations manual |

---

**Document End**
