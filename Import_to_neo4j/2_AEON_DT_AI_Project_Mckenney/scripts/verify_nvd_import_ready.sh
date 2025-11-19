#!/bin/bash
# Pre-flight check for NVD import script

echo "================================================"
echo "NVD Import Pre-flight Check"
echo "================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

# Check 1: Python installation
echo -n "1. Python 3.x installed: "
if command -v python3 &> /dev/null; then
    VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} ($VERSION)"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Python3 not found"
    ((FAIL++))
fi

# Check 2: Virtual environment
echo -n "2. Virtual environment exists: "
if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC}"
    ((PASS++))
else
    echo -e "${YELLOW}!${NC} Not found (optional)"
fi

# Check 3: Neo4j connection
echo -n "3. Neo4j connection: "
if python3 -c "from neo4j import GraphDatabase; d = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'neo4j@openspg')); d.close()" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Connected"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Cannot connect to Neo4j"
    ((FAIL++))
fi

# Check 4: Required Python packages
echo -n "4. Required packages installed: "
MISSING=""
for pkg in requests neo4j tqdm; do
    if ! python3 -c "import $pkg" 2>/dev/null; then
        MISSING="$MISSING $pkg"
    fi
done

if [ -z "$MISSING" ]; then
    echo -e "${GREEN}✓${NC}"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Missing:$MISSING"
    echo "   Install with: pip install requests neo4j tqdm"
    ((FAIL++))
fi

# Check 5: Import script exists and is executable
echo -n "5. Import script ready: "
if [ -f "import_nvd_2018_2019.py" ]; then
    if [ -x "import_nvd_2018_2019.py" ]; then
        echo -e "${GREEN}✓${NC}"
        ((PASS++))
    else
        echo -e "${YELLOW}!${NC} File exists but not executable"
        echo "   Fix with: chmod +x import_nvd_2018_2019.py"
    fi
else
    echo -e "${RED}✗${NC} Script not found"
    ((FAIL++))
fi

# Check 6: NVD API accessibility
echo -n "6. NVD API accessible: "
if curl -s -I "https://services.nvd.nist.gov/rest/json/cves/2.0" | grep -q "200 OK"; then
    echo -e "${GREEN}✓${NC}"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Cannot reach NVD API"
    ((FAIL++))
fi

# Check 7: Disk space
echo -n "7. Sufficient disk space: "
AVAILABLE=$(df -h . | awk 'NR==2 {print $4}' | sed 's/G//')
if (( $(echo "$AVAILABLE > 1" | bc -l) )); then
    echo -e "${GREEN}✓${NC} (${AVAILABLE}G available)"
    ((PASS++))
else
    echo -e "${YELLOW}!${NC} Low disk space (${AVAILABLE}G)"
fi

# Check 8: Existing progress file
echo -n "8. Previous import progress: "
if [ -f ".nvd_import_progress.json" ]; then
    LAST_DATE=$(python3 -c "import json; print(json.load(open('.nvd_import_progress.json'))['last_processed_date'])" 2>/dev/null)
    TOTAL=$(python3 -c "import json; print(json.load(open('.nvd_import_progress.json'))['total_processed'])" 2>/dev/null)
    echo -e "${YELLOW}!${NC} Found (last: $LAST_DATE, total: $TOTAL)"
    echo "   Script will resume from last checkpoint"
else
    echo -e "${GREEN}✓${NC} Clean start"
fi

echo ""
echo "================================================"
echo "Summary: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"
echo "================================================"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Ready to import.${NC}"
    echo ""
    echo "To start import:"
    echo "  ./import_nvd_2018_2019.py"
    echo ""
    echo "To run in background:"
    echo "  nohup python3 import_nvd_2018_2019.py > nvd_import.out 2>&1 &"
    echo ""
    echo "To monitor progress:"
    echo "  tail -f nvd_import_2018_2019.log"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Fix issues above before importing.${NC}"
    exit 1
fi
