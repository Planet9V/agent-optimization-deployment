#!/bin/bash
# AEON Web Interface Launch Script
# Properly sets up Python paths and launches Streamlit

# Get absolute paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
WEB_INTERFACE_DIR="$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AEON Web Interface Launcher${NC}"
echo -e "${BLUE}================================${NC}\n"

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source "$WEB_INTERFACE_DIR/venv/bin/activate"

# Set PYTHONPATH to include both project root and web_interface
export PYTHONPATH="$PROJECT_ROOT:$WEB_INTERFACE_DIR:$PYTHONPATH"

echo -e "${GREEN}✅ Python paths configured:${NC}"
echo -e "   Project Root: $PROJECT_ROOT"
echo -e "   Web Interface: $WEB_INTERFACE_DIR"
echo ""

# Check if required services are running
echo -e "${BLUE}Checking system dependencies...${NC}"

# Check Neo4j
if docker ps | grep -q openspg-neo4j; then
    echo -e "${GREEN}✅ Neo4j is running${NC}"
else
    echo -e "${RED}⚠️  Neo4j container not found${NC}"
    echo -e "   Run: docker start <neo4j-container-name>"
fi

# Check Qdrant (optional)
if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Qdrant is accessible${NC}"
else
    echo -e "${BLUE}ℹ️  Qdrant not accessible (optional)${NC}"
fi

echo ""

# Launch Streamlit
echo -e "${GREEN}Starting Streamlit web interface...${NC}"
echo -e "${BLUE}Access at: http://localhost:8501${NC}\n"

cd "$WEB_INTERFACE_DIR"
streamlit run app.py
