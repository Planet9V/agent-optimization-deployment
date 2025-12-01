#!/bin/bash
# Neo4j database backup with compression and S3 upload
# Usage: ./backup_database.sh [backup-dir] [bucket-name]

set -e

# Configuration
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="${1:-.}"
BUCKET_NAME="${2:-cyber-dt-backups}"
DB_NAME="neo4j"
NEO4J_HOME="${NEO4J_HOME:-/var/lib/neo4j}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Starting Neo4j database backup..."

# Verify backup directory
if [ ! -d "$BACKUP_DIR" ]; then
    echo -e "${YELLOW}Creating backup directory: $BACKUP_DIR${NC}"
    mkdir -p "$BACKUP_DIR"
fi

# Create backup filename
BACKUP_FILE="$BACKUP_DIR/neo4j-$DATE.dump"
BACKUP_FILE_GZ="$BACKUP_FILE.gz"

echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Creating database dump..."
if command -v neo4j-admin &> /dev/null; then
    neo4j-admin dump --database=$DB_NAME --to=$BACKUP_FILE
else
    echo -e "${RED}Error: neo4j-admin command not found${NC}"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: Database dump failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Database dump created${NC}"

# Compress backup
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Compressing backup..."
gzip "$BACKUP_FILE"

if [ ! -f "$BACKUP_FILE_GZ" ]; then
    echo -e "${RED}Error: Compression failed${NC}"
    exit 1
fi

# Get file size
SIZE=$(du -h "$BACKUP_FILE_GZ" | cut -f1)
echo -e "${GREEN}✓ Backup compressed (${SIZE})${NC}"

# Upload to S3 if AWS CLI is configured
if command -v aws &> /dev/null; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Uploading to S3..."

    if aws s3 cp "$BACKUP_FILE_GZ" "s3://$BUCKET_NAME/" 2>/dev/null; then
        echo -e "${GREEN}✓ Backup uploaded to S3${NC}"
        echo -e "${GREEN}Location: s3://$BUCKET_NAME/$(basename $BACKUP_FILE_GZ)${NC}"
    else
        echo -e "${YELLOW}⚠ S3 upload failed (check AWS credentials)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ AWS CLI not found, skipping S3 upload${NC}"
fi

# Create checksum
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Creating checksum..."
sha256sum "$BACKUP_FILE_GZ" > "$BACKUP_FILE_GZ.sha256"
echo -e "${GREEN}✓ Checksum created${NC}"

# Summary
echo ""
echo -e "${GREEN}Backup complete!${NC}"
echo "File: $BACKUP_FILE_GZ"
echo "Size: $SIZE"
echo "Checksum: $BACKUP_FILE_GZ.sha256"
echo ""
