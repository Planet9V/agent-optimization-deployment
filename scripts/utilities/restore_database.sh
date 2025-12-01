#!/bin/bash
# Neo4j database restoration with validation
# Usage: ./restore_database.sh <backup-file> [--verify-only]

set -e

# Configuration
BACKUP_FILE="${1:?Error: backup file required}"
VERIFY_ONLY="${2:-}"
DB_NAME="neo4j"
NEO4J_HOME="${NEO4J_HOME:-/var/lib/neo4j}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Neo4j Database Restoration Utility    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Verify backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}✗ Error: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

# Handle compressed files
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Extracting compressed backup..."
    EXTRACT_DIR=$(mktemp -d)
    gunzip -c "$BACKUP_FILE" > "$EXTRACT_DIR/backup.dump"
    BACKUP_FILE="$EXTRACT_DIR/backup.dump"
    echo -e "${GREEN}✓ Backup extracted to temporary directory${NC}"
fi

# Verify backup integrity
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Verifying backup file..."
if ! file "$BACKUP_FILE" | grep -q "data"; then
    echo -e "${RED}✗ Error: Invalid backup file format${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Backup file verified${NC}"

# Check if verification only
if [ "$VERIFY_ONLY" == "--verify-only" ]; then
    echo -e "${GREEN}Verification completed successfully${NC}"
    exit 0
fi

# Safety check
echo ""
echo -e "${YELLOW}WARNING: This will replace the current $DB_NAME database!${NC}"
echo -e "${YELLOW}Current time: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""
read -p "Type 'YES' to proceed with restoration: " CONFIRM

if [ "$CONFIRM" != "YES" ]; then
    echo -e "${RED}Restoration cancelled${NC}"
    exit 1
fi

# Check Neo4j service status
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Checking Neo4j service status..."
if command -v systemctl &> /dev/null; then
    if systemctl is-active --quiet neo4j; then
        echo -e "${YELLOW}⚠ Neo4j service is running, attempting to stop...${NC}"
        sudo systemctl stop neo4j || true
        sleep 2
    fi
fi

# Perform restoration
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Starting database restoration..."
if command -v neo4j-admin &> /dev/null; then
    if neo4j-admin load --from-path="$(dirname $BACKUP_FILE)" --database=$DB_NAME --overwrite-destination=true; then
        echo -e "${GREEN}✓ Database restored successfully${NC}"
    else
        echo -e "${RED}✗ Error: Database restoration failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Error: neo4j-admin command not found${NC}"
    exit 1
fi

# Restart Neo4j service
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} Restarting Neo4j service..."
if command -v systemctl &> /dev/null; then
    sudo systemctl start neo4j
    sleep 3

    if systemctl is-active --quiet neo4j; then
        echo -e "${GREEN}✓ Neo4j service started successfully${NC}"
    else
        echo -e "${RED}✗ Error: Failed to start Neo4j service${NC}"
        exit 1
    fi
fi

# Cleanup temporary files
if [ -n "$EXTRACT_DIR" ] && [ -d "$EXTRACT_DIR" ]; then
    rm -rf "$EXTRACT_DIR"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}Database restoration completed successfully!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
