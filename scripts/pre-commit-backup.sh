#!/bin/bash
# Pre-Commit Backup Script
# Automatically backs up critical systems before git commits
# Usage: ./scripts/pre-commit-backup.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_DIR="backups/pre-commit-$TIMESTAMP"
NEO4J_CONTAINER=$(docker ps | grep neo4j | awk '{print $1}' | head -1)

echo -e "${GREEN}🔒 Starting pre-commit backup...${NC}"
echo "Timestamp: $TIMESTAMP"
echo "Backup directory: $BACKUP_DIR"
echo ""

# Create backup directory structure
echo -e "${YELLOW}📁 Creating backup directories...${NC}"
mkdir -p "$BACKUP_DIR"/{neo4j,ner9,agentdb,docs}
echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# Backup Neo4j database
if [ -n "$NEO4J_CONTAINER" ]; then
    echo -e "${YELLOW}📦 Backing up Neo4j database...${NC}"
    echo "Container: $NEO4J_CONTAINER"

    docker cp "$NEO4J_CONTAINER:/data" "$BACKUP_DIR/neo4j/neo4j-data" 2>&1 | grep -v "permission denied" || true

    NEO4J_SIZE=$(du -sh "$BACKUP_DIR/neo4j/" | awk '{print $1}')
    echo -e "${GREEN}✅ Neo4j backed up ($NEO4J_SIZE)${NC}"
else
    echo -e "${RED}⚠️  No Neo4j container found, skipping...${NC}"
fi
echo ""

# Backup NER9 model
echo -e "${YELLOW}🧠 Backing up NER9 model...${NC}"
NER_FOUND=0

if [ -f "agents/ner_agent.py" ]; then
    cp -r agents/ner_agent.py "$BACKUP_DIR/ner9/"
    NER_FOUND=1
fi

# Check alternative locations
if [ -f "Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/agents/ner_agent.py" ]; then
    cp Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/agents/ner_agent.py "$BACKUP_DIR/ner9/"
    NER_FOUND=1
fi

if [ $NER_FOUND -eq 1 ]; then
    NER_SIZE=$(du -sh "$BACKUP_DIR/ner9/" | awk '{print $1}')
    echo -e "${GREEN}✅ NER9 backed up ($NER_SIZE)${NC}"
else
    echo -e "${RED}⚠️  NER agent not found, skipping...${NC}"
fi
echo ""

# Backup AgentDB
echo -e "${YELLOW}🗄️  Backing up AgentDB...${NC}"
AGENTDB_FOUND=0

if [ -d "lib/agentdb" ]; then
    cp -r lib/agentdb "$BACKUP_DIR/agentdb/"
    AGENTDB_FOUND=1
fi

if [ -d "tests/agentdb" ]; then
    cp -r tests/agentdb "$BACKUP_DIR/agentdb/tests/"
    AGENTDB_FOUND=1
fi

if [ $AGENTDB_FOUND -eq 1 ]; then
    AGENTDB_SIZE=$(du -sh "$BACKUP_DIR/agentdb/" | awk '{print $1}')
    echo -e "${GREEN}✅ AgentDB backed up ($AGENTDB_SIZE)${NC}"
else
    echo -e "${RED}⚠️  AgentDB not found, skipping...${NC}"
fi
echo ""

# Backup documentation
echo -e "${YELLOW}📚 Backing up documentation...${NC}"
DOC_COUNT=0

if ls docs/GAP*.md 1> /dev/null 2>&1; then
    cp docs/GAP*.md "$BACKUP_DIR/docs/" 2>/dev/null || true
    DOC_COUNT=$(ls "$BACKUP_DIR/docs/" | wc -l)
fi

if [ $DOC_COUNT -gt 0 ]; then
    DOCS_SIZE=$(du -sh "$BACKUP_DIR/docs/" | awk '{print $1}')
    echo -e "${GREEN}✅ Documentation backed up ($DOC_COUNT files, $DOCS_SIZE)${NC}"
else
    echo -e "${RED}⚠️  No GAP documentation found, skipping...${NC}"
fi
echo ""

# Summary
echo -e "${GREEN}════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Backup Complete!${NC}"
echo -e "${GREEN}════════════════════════════════════${NC}"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""
echo "Backup sizes:"
du -sh "$BACKUP_DIR"/* 2>/dev/null || echo "No backups created"
echo ""
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | awk '{print $1}')
echo -e "${GREEN}Total backup size: $TOTAL_SIZE${NC}"
echo ""

# Create backup manifest
cat > "$BACKUP_DIR/BACKUP_MANIFEST.txt" << EOF
Backup Manifest
===============

Timestamp: $TIMESTAMP
Created by: pre-commit-backup.sh
Git branch: $(git branch --show-current 2>/dev/null || echo "unknown")
Git commit: $(git rev-parse HEAD 2>/dev/null || echo "unknown")

Contents:
$(ls -lah "$BACKUP_DIR")

Sizes:
$(du -sh "$BACKUP_DIR"/*)

Total: $TOTAL_SIZE
EOF

echo -e "${GREEN}📄 Manifest created: $BACKUP_DIR/BACKUP_MANIFEST.txt${NC}"
echo ""
echo -e "${GREEN}🚀 Ready for git commit!${NC}"
