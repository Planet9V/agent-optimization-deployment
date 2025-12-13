# Migration Recovery and Validation Procedures

**File**: RECOVERY_PROCEDURES.md
**Created**: 2025-12-04
**Purpose**: Comprehensive recovery procedures for migration failures
**Status**: ACTIVE

## Table of Contents
1. [Database Recovery](#database-recovery)
2. [Model Recovery](#model-recovery)
3. [File System Recovery](#file-system-recovery)
4. [Network and Docker Recovery](#network-and-docker-recovery)
5. [Git Repository Recovery](#git-repository-recovery)
6. [Emergency Rollback](#emergency-rollback)

---

## 1. Database Recovery

### 1.1 Neo4j Recovery

#### **Data Consistency Validation**
```bash
# Check node counts and relationship integrity
cypher-shell -u neo4j -p password <<EOF
MATCH (n) RETURN count(n) as node_count;
MATCH ()-[r]->() RETURN count(r) as relationship_count;
CALL apoc.meta.stats() YIELD nodeCount, relCount, labelCount;
EOF

# Expected output:
# node_count: [expected number]
# relationship_count: [expected number]
# Verify counts match source database
```

#### **Transaction Log Recovery**
```bash
# Check transaction log status
neo4j-admin check-consistency --database=neo4j --verbose

# Expected output:
# Consistency check passed
# No orphaned relationships
# No missing nodes

# If inconsistencies found:
neo4j-admin database restore \
  --from=/Volumes/USB/neo4j-backup/neo4j-backup-YYYY-MM-DD.backup \
  --database=neo4j \
  --force
```

#### **Partial Restoration Recovery**
```bash
# Identify interrupted transfer point
cypher-shell -u neo4j -p password <<EOF
MATCH (n)
WITH labels(n)[0] as label, count(n) as count
RETURN label, count
ORDER BY label;
EOF

# Compare with source counts and restore missing labels
cypher-shell -u neo4j -p password < /Volumes/USB/neo4j-backup/partial-restore-[LABEL].cypher
```

#### **Connection Pool Reset**
```bash
# Reset connection pool
cypher-shell -u neo4j -p password <<EOF
CALL dbms.killConnections();
EOF

# Restart Neo4j service
brew services restart neo4j

# Verify connectivity
cypher-shell -u neo4j -p password "RETURN 'Connected' as status;"
# Expected: status: "Connected"
```

### 1.2 MySQL Recovery

#### **Data Consistency Validation**
```bash
# Check table row counts and checksums
mysql -u root -p <<EOF
USE ner11_production;
SELECT table_name, table_rows
FROM information_schema.tables
WHERE table_schema = 'ner11_production';
CHECKSUM TABLE threat_intelligence, incident_data, vulnerability_scans;
EOF

# Expected output:
# Table row counts matching source
# Checksums matching pre-migration values
```

#### **Transaction Recovery and Rollback**
```bash
# Check binary log position
mysql -u root -p -e "SHOW MASTER STATUS\G"

# If restoration needed:
mysql -u root -p <<EOF
STOP SLAVE;
RESET SLAVE;
SOURCE /Volumes/USB/mysql-backup/ner11_production-YYYY-MM-DD.sql;
START SLAVE;
EOF

# Verify import
mysql -u root -p -e "SELECT COUNT(*) FROM ner11_production.threat_intelligence;"
```

#### **Partial Restoration Recovery**
```bash
# Identify missing tables
mysql -u root -p <<EOF
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ner11_production';
EOF

# Restore specific tables
mysql -u root -p ner11_production < /Volumes/USB/mysql-backup/specific-table.sql

# Verify foreign key constraints
mysql -u root -p <<EOF
SELECT constraint_name, table_name, referenced_table_name
FROM information_schema.key_column_usage
WHERE table_schema = 'ner11_production' AND referenced_table_name IS NOT NULL;
EOF
```

#### **Connection Pool Reset**
```bash
# Kill existing connections
mysql -u root -p <<EOF
SELECT CONCAT('KILL ', id, ';') FROM information_schema.processlist
WHERE user != 'root' INTO OUTFILE '/tmp/kill_connections.sql';
SOURCE /tmp/kill_connections.sql;
EOF

# Restart MySQL
brew services restart mysql

# Verify connectivity
mysql -u root -p -e "SELECT 'Connected' as status;"
```

### 1.3 Qdrant Recovery

#### **Vector Collection Validation**
```bash
# Check collection status and point counts
curl -X GET "http://localhost:6333/collections/threat_vectors" | jq '
{
  status: .result.status,
  vectors_count: .result.vectors_count,
  points_count: .result.points_count,
  config: .result.config
}'

# Expected output:
# status: "green"
# vectors_count: [expected number]
# points_count: [expected number]
```

#### **Partial Collection Recovery**
```bash
# Check snapshot status
curl -X GET "http://localhost:6333/collections/threat_vectors/snapshots" | jq '.result[]'

# Restore from specific snapshot
curl -X PUT "http://localhost:6333/collections/threat_vectors/snapshots/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "snapshot=@/Volumes/USB/qdrant-backup/threat_vectors-YYYY-MM-DD.snapshot"

# Verify restoration
curl -X GET "http://localhost:6333/collections/threat_vectors" | jq '.result.vectors_count'
```

#### **Vector Integrity Validation**
```bash
# Sample random vectors and verify dimensions
curl -X POST "http://localhost:6333/collections/threat_vectors/points/scroll" \
  -H "Content-Type: application/json" \
  -d '{
    "limit": 10,
    "with_vector": true,
    "with_payload": true
  }' | jq '.result.points[] | {id: .id, vector_length: (.vector | length)}'

# Expected: vector_length should match model output dimension (e.g., 768)
```

#### **Connection Pool Reset**
```bash
# Restart Qdrant service
docker restart qdrant

# Wait for service availability
timeout 30 bash -c 'until curl -sf http://localhost:6333/collections > /dev/null; do sleep 1; done'

# Verify collections
curl -X GET "http://localhost:6333/collections" | jq '.result.collections[].name'
# Expected: ["threat_vectors", "incident_embeddings", ...]
```

---

## 2. Model Recovery

### 2.1 Archive Integrity Validation

```bash
# Verify tar archive integrity
tar -tzf /Volumes/USB/models/ner11_gold_model.tar.gz > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "Archive integrity: OK"
else
  echo "Archive integrity: FAILED - Re-download from source"
  exit 1
fi

# Verify checksum
cd /Volumes/USB/models/
sha256sum -c checksums.txt | grep "ner11_gold_model.tar.gz"
# Expected: ner11_gold_model.tar.gz: OK
```

### 2.2 Partial Extraction Recovery

```bash
# Check extracted files
EXPECTED_FILES=(
  "model.safetensors"
  "config.json"
  "tokenizer.json"
  "tokenizer_config.json"
  "special_tokens_map.json"
  "vocab.txt"
)

for file in "${EXPECTED_FILES[@]}"; do
  if [ ! -f "~/models/ner11_gold/$file" ]; then
    echo "Missing: $file - Extracting from archive"
    tar -xzf /Volumes/USB/models/ner11_gold_model.tar.gz \
      --directory ~/models/ner11_gold \
      --wildcards "*/$file"
  fi
done
```

### 2.3 Symbolic Link Verification

```bash
# Verify all symbolic links
find ~/models -type l -exec bash -c '
  if [ ! -e "$1" ]; then
    echo "Broken symlink: $1"
    target=$(readlink "$1")
    echo "Target should be: $target"

    # Attempt to recreate
    rm "$1"
    ln -s "$target" "$1"
    echo "Recreated symlink: $1 -> $target"
  fi
' _ {} \;

# Expected output: No broken symlinks, or "Recreated symlink" messages
```

### 2.4 Model Loading Validation

```bash
# Test model loading with Python
python3 <<EOF
import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer

try:
    model = AutoModelForTokenClassification.from_pretrained("~/models/ner11_gold")
    tokenizer = AutoTokenizer.from_pretrained("~/models/ner11_gold")

    # Test inference
    text = "CVE-2024-1234 affects Apache Struts 2.x"
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)

    print("Model validation: OK")
    print(f"Model output shape: {outputs.logits.shape}")
except Exception as e:
    print(f"Model validation: FAILED - {str(e)}")
    exit(1)
EOF

# Expected output:
# Model validation: OK
# Model output shape: torch.Size([1, X, Y])
```

---

## 3. File System Recovery

### 3.1 USB Mount Verification

```bash
# Check USB mount status
mount | grep /Volumes/USB
# Expected: /dev/disk2s1 on /Volumes/USB (exfat, local, nodev, nosuid, journaled)

# If not mounted, remount
diskutil list | grep "USB"
# Note the disk identifier (e.g., disk2s1)

diskutil mount disk2s1
# Expected: Volume USB on disk2s1 mounted
```

### 3.2 File Permission Recovery

```bash
# Verify ownership and permissions
ls -la ~/models/ner11_gold | head -10
# Expected: drwxr-xr-x user group

# If incorrect permissions:
sudo chown -R $(whoami):staff ~/models/ner11_gold
chmod -R 755 ~/models/ner11_gold
chmod -R 644 ~/models/ner11_gold/*.{json,txt,safetensors}

# Verify ACLs
ls -le ~/models/ner11_gold
# Expected: No extended attributes beyond standard permissions
```

### 3.3 Disk Space Recovery

```bash
# Check available space
df -h /Volumes/USB
# Expected: Sufficient space for remaining transfers

# If space insufficient:
# 1. Clean temporary files
find /Volumes/USB -name ".DS_Store" -delete
find /Volumes/USB -name "._*" -delete

# 2. Compress old backups
cd /Volumes/USB/backups
for dir in old-backup-*; do
  if [ -d "$dir" ]; then
    tar -czf "${dir}.tar.gz" "$dir"
    rm -rf "$dir"
  fi
done

# 3. Verify cleanup
df -h /Volumes/USB
```

### 3.4 Filesystem Consistency Checks

```bash
# Unmount USB for filesystem check
diskutil unmount /Volumes/USB

# Run filesystem check
sudo fsck_exfat -d /dev/disk2s1
# Expected: ** The volume USB appears to be OK

# Remount
diskutil mount disk2s1

# Verify file integrity after fsck
cd /Volumes/USB
find . -type f -exec md5 {} \; > /tmp/usb_checksums_post_fsck.txt
diff /tmp/usb_checksums_pre_migration.txt /tmp/usb_checksums_post_fsck.txt
# Expected: No differences
```

---

## 4. Network and Docker Recovery

### 4.1 Container Health Diagnostics

```bash
# Check container status
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
# Expected: All containers "Up" status

# Inspect unhealthy containers
for container in $(docker ps -a --filter "health=unhealthy" --format "{{.Names}}"); do
  echo "=== $container ==="
  docker inspect "$container" | jq '.[0].State.Health.Log[-1]'
  docker logs --tail 50 "$container"
done
```

### 4.2 Network Connectivity Verification

```bash
# Inspect Docker network
docker network inspect ner11_network | jq '.[0].Containers'
# Expected: All containers listed with IP addresses

# Test DNS resolution
docker exec ner11_api nslookup neo4j
# Expected: Name resolution successful

# Test inter-container connectivity
docker exec ner11_api ping -c 3 neo4j
# Expected: 0% packet loss

# If connectivity fails, recreate network:
docker network rm ner11_network
docker network create --driver bridge \
  --subnet=172.25.0.0/16 \
  --gateway=172.25.0.1 \
  ner11_network
```

### 4.3 Volume Mount Verification

```bash
# Check volume mounts
docker inspect ner11_api | jq '.[0].Mounts[] | {Type: .Type, Source: .Source, Destination: .Destination}'
# Expected: All required volumes present

# Verify volume data integrity
docker exec ner11_api ls -la /app/models/
# Expected: Model files present with correct permissions

# If volumes corrupted, recreate:
docker volume rm ner11_models
docker volume create ner11_models
docker cp ~/models/ner11_gold/. ner11_api:/app/models/
```

### 4.4 Docker Daemon Restart

```bash
# Save running container states
docker ps --format "{{.Names}}" > /tmp/running_containers.txt

# Restart Docker daemon
sudo systemctl restart docker  # Linux
# OR
osascript -e 'quit app "Docker"' && open -a Docker  # macOS

# Wait for daemon ready
timeout 60 bash -c 'until docker info > /dev/null 2>&1; do sleep 1; done'

# Restart containers
while read container; do
  docker start "$container"
done < /tmp/running_containers.txt

# Verify all containers running
docker ps --format "{{.Names}}" | diff - /tmp/running_containers.txt
# Expected: No differences
```

---

## 5. Git Repository Recovery

### 5.1 Bundle Extraction Validation

```bash
# Verify bundle integrity
git bundle verify /Volumes/USB/git-repos/ner11-gold-model.bundle
# Expected: The bundle records a complete history

# List bundle contents
git bundle list-heads /Volumes/USB/git-repos/ner11-gold-model.bundle
# Expected: List of all branches and tags

# Clone from bundle
cd ~/projects
git clone /Volumes/USB/git-repos/ner11-gold-model.bundle ner11-gold-model

# Verify clone
cd ner11-gold-model
git log --oneline | head -5
git branch -a
```

### 5.2 Branch/Tag Integrity Verification

```bash
# Check all branches exist
git branch -a | grep -E "(main|develop|feature|release)" | wc -l
# Compare with expected branch count

# Verify tags
git tag -l | wc -l
# Compare with expected tag count

# Check remote tracking
git remote -v
# Expected: origin pointing to bundle or upstream repository

# If remote missing:
git remote add origin https://github.com/organization/ner11-gold-model.git
```

### 5.3 Merge Conflict Resolution

```bash
# Check for unmerged files
git status | grep "both modified"

# For each conflicted file:
git checkout --ours path/to/file    # Keep local version
# OR
git checkout --theirs path/to/file  # Keep remote version
# OR
git mergetool  # Use merge tool

# After resolving conflicts:
git add path/to/resolved/file
git commit -m "Resolved merge conflicts during migration"
```

### 5.4 Remote Tracking Restoration

```bash
# Re-establish remote tracking
git fetch origin

# Reset branch tracking
for branch in $(git branch | sed 's/\*//' | xargs); do
  git branch --set-upstream-to=origin/$branch $branch 2>/dev/null || echo "No remote branch for $branch"
done

# Verify tracking
git branch -vv
# Expected: Each branch shows tracking relationship

# Sync with remote
git pull --all
```

---

## 6. Emergency Rollback

### 6.1 Full System Rollback

```bash
#!/bin/bash
# emergency_rollback.sh

echo "=== EMERGENCY ROLLBACK INITIATED ==="

# Stop all services
docker-compose down
brew services stop neo4j mysql

# Restore databases from USB backup
echo "Restoring databases..."
neo4j-admin database restore --from=/Volumes/USB/neo4j-backup/neo4j-backup-YYYY-MM-DD.backup --database=neo4j --force
mysql -u root -p < /Volumes/USB/mysql-backup/ner11_production-YYYY-MM-DD.sql

# Restore Qdrant collections
echo "Restoring Qdrant collections..."
docker start qdrant
sleep 5
for snapshot in /Volumes/USB/qdrant-backup/*.snapshot; do
  collection=$(basename "$snapshot" .snapshot | cut -d'-' -f1)
  curl -X PUT "http://localhost:6333/collections/$collection/snapshots/upload" \
    -F "snapshot=@$snapshot"
done

# Restore models
echo "Restoring models..."
rm -rf ~/models/ner11_gold
tar -xzf /Volumes/USB/models/ner11_gold_model.tar.gz -C ~/models/

# Restore Git repositories
echo "Restoring Git repositories..."
cd ~/projects
rm -rf ner11-gold-model
git clone /Volumes/USB/git-repos/ner11-gold-model.bundle

# Restart services
echo "Restarting services..."
brew services start neo4j mysql
docker-compose up -d

echo "=== ROLLBACK COMPLETE ==="
echo "Verify system status with health checks"
```

### 6.2 Validation After Rollback

```bash
# Run comprehensive health checks
./scripts/health_check.sh

# Verify data integrity
cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n);"
mysql -u root -p -e "SELECT COUNT(*) FROM ner11_production.threat_intelligence;"
curl -X GET "http://localhost:6333/collections/threat_vectors" | jq '.result.vectors_count'

# Test model inference
python3 scripts/test_model_inference.py

# Check service connectivity
docker-compose ps
curl -f http://localhost:8000/health
```

---

## Recovery Procedure Checklist

### Before Starting Recovery:
- [ ] Identify failure point from logs
- [ ] Document error messages
- [ ] Verify USB backup integrity
- [ ] Estimate recovery time
- [ ] Notify stakeholders

### During Recovery:
- [ ] Follow procedures step-by-step
- [ ] Log all commands executed
- [ ] Verify each step before proceeding
- [ ] Monitor system resources
- [ ] Document any deviations

### After Recovery:
- [ ] Run comprehensive validation
- [ ] Update recovery documentation
- [ ] Perform root cause analysis
- [ ] Implement preventive measures
- [ ] Schedule post-recovery review

---

## Emergency Contacts

- **System Administrator**: [Contact Info]
- **Database Admin**: [Contact Info]
- **DevOps Lead**: [Contact Info]
- **Escalation Path**: [Escalation Procedure]

---

**Document Maintenance**: Update after each recovery incident with lessons learned.
