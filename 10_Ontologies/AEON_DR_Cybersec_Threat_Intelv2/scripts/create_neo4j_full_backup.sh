#!/bin/bash
# Full Neo4j Database Backup Script
# Created: 2025-11-01
# Purpose: Create complete backup before CVE re-import operation

set -e  # Exit on error

BACKUP_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/backups/v2_pre_cve_reimport_${BACKUP_TIMESTAMP}"
CONTAINER_NAME="openspg-neo4j"
DATABASE_NAME="neo4j"

echo "=========================================="
echo "Neo4j Full Backup Script"
echo "=========================================="
echo "Timestamp: ${BACKUP_TIMESTAMP}"
echo "Backup Directory: ${BACKUP_DIR}"
echo ""

# Create backup directory
echo "Creating backup directory..."
mkdir -p "${BACKUP_DIR}"

# Execute neo4j-admin dump inside Docker container
echo "Executing neo4j-admin database dump..."
echo "This may take several minutes for large databases..."
docker exec ${CONTAINER_NAME} neo4j-admin database dump ${DATABASE_NAME} \
    --to-path=/backups \
    --verbose

# Copy backup file from container to host
echo "Copying backup from container to host..."
docker cp ${CONTAINER_NAME}:/backups/${DATABASE_NAME}.dump "${BACKUP_DIR}/"

# Get backup file size
BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${DATABASE_NAME}.dump" | cut -f1)

echo ""
echo "=========================================="
echo "Backup Complete!"
echo "=========================================="
echo "Backup Location: ${BACKUP_DIR}/${DATABASE_NAME}.dump"
echo "Backup Size: ${BACKUP_SIZE}"
echo ""
echo "To restore this backup:"
echo "  1. Stop Neo4j: docker stop ${CONTAINER_NAME}"
echo "  2. Copy dump to container: docker cp ${BACKUP_DIR}/${DATABASE_NAME}.dump ${CONTAINER_NAME}:/backups/"
echo "  3. Restore: docker exec ${CONTAINER_NAME} neo4j-admin database load ${DATABASE_NAME} --from-path=/backups"
echo "  4. Start Neo4j: docker start ${CONTAINER_NAME}"
echo ""
