#!/bin/bash
# Neo4j Full Data Backup Script
# Purpose: Create complete database backup before CVE ID normalization
# Method: neo4j-admin database dump

set -e  # Exit on error

# Configuration
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/backups/pre_normalization_$(date +%Y-%m-%d_%H-%M-%S)"
NEO4J_CONTAINER="openspg-neo4j"
DATABASE_NAME="neo4j"

echo "========================================="
echo "Neo4j Full Database Backup"
echo "========================================="
echo "Container: $NEO4J_CONTAINER"
echo "Database: $DATABASE_NAME"
echo "Backup Directory: $BACKUP_DIR"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Step 1: Stop Neo4j (required for dump)
echo "[1/4] Stopping Neo4j container..."
docker stop $NEO4J_CONTAINER

# Step 2: Create database dump
echo "[2/4] Creating database dump..."
docker run --rm \
  --volumes-from $NEO4J_CONTAINER \
  -v "$BACKUP_DIR:/backup" \
  neo4j:latest \
  neo4j-admin database dump $DATABASE_NAME --to-path=/backup

# Verify dump file created
if [ -f "$BACKUP_DIR/$DATABASE_NAME.dump" ]; then
  echo "✅ Database dump created: $BACKUP_DIR/$DATABASE_NAME.dump"
  DUMP_SIZE=$(du -h "$BACKUP_DIR/$DATABASE_NAME.dump" | cut -f1)
  echo "   Size: $DUMP_SIZE"
else
  echo "❌ ERROR: Database dump not found at $BACKUP_DIR/$DATABASE_NAME.dump"
  docker start $NEO4J_CONTAINER
  exit 1
fi

# Step 3: Start Neo4j
echo "[3/4] Starting Neo4j container..."
docker start $NEO4J_CONTAINER

# Wait for Neo4j to be ready
echo "Waiting for Neo4j to be ready..."
sleep 10

# Verify Neo4j is running
if docker ps | grep -q $NEO4J_CONTAINER; then
  echo "✅ Neo4j container started successfully"
else
  echo "❌ ERROR: Neo4j container failed to start"
  exit 1
fi

# Step 4: Create backup summary
echo "[4/4] Creating backup summary..."
cat > "$BACKUP_DIR/BACKUP_INFO.txt" <<EOF
Neo4j Full Database Backup
==========================

Backup Created: $(date +"%Y-%m-%d %H:%M:%S %Z")
Backup Directory: $BACKUP_DIR
Database: $DATABASE_NAME
Container: $NEO4J_CONTAINER

Backup Files:
- $DATABASE_NAME.dump (Neo4j database dump)
- BACKUP_INFO.txt (this file)

Backup Size: $DUMP_SIZE

Purpose:
Pre-normalization backup before CVE ID normalization from "cve-CVE-*" to "CVE-*"

Restoration Command:
--------------------
# Stop Neo4j
docker stop $NEO4J_CONTAINER

# Restore database
docker run --rm \\
  --volumes-from $NEO4J_CONTAINER \\
  -v "$BACKUP_DIR:/backup" \\
  neo4j:latest \\
  neo4j-admin database load $DATABASE_NAME --from-path=/backup --overwrite-destination=true

# Start Neo4j
docker start $NEO4J_CONTAINER

# Wait for Neo4j to be ready
sleep 10

# Verify restoration
docker exec $NEO4J_CONTAINER cypher-shell \\
  -a bolt://localhost:7687 -u neo4j -p "neo4j@openspg" \\
  "MATCH (n) RETURN COUNT(n) AS total_nodes;"

--------------------

Risk Assessment Reference:
/home/jim/2_OXOT_Projects_Dev/docs/CVE_ID_NORMALIZATION_RISK_ASSESSMENT.md

Normalization Script:
/home/jim/2_OXOT_Projects_Dev/scripts/merge_duplicate_cve_nodes.cypher

Created by: create_neo4j_full_backup.sh
Version: v1.0.0
EOF

echo ""
echo "========================================="
echo "✅ BACKUP COMPLETE"
echo "========================================="
echo "Backup Location: $BACKUP_DIR"
echo "Backup Size: $DUMP_SIZE"
echo ""
echo "Next Steps:"
echo "1. Verify backup: cat $BACKUP_DIR/BACKUP_INFO.txt"
echo "2. Review risk assessment: docs/CVE_ID_NORMALIZATION_RISK_ASSESSMENT.md"
echo "3. Execute normalization: scripts/merge_duplicate_cve_nodes.cypher"
echo "========================================="
