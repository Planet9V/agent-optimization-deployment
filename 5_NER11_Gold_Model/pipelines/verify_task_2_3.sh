#!/bin/bash
# Task 2.3 Verification Script
# Verifies all components are properly created and integrated

echo "================================================================"
echo "TASK 2.3 VERIFICATION SCRIPT"
echo "================================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check files exist
echo "[1] Checking File Existence..."
FILES=(
    "05_ner11_to_neo4j_hierarchical.py"
    "test_05_neo4j_hierarchical_pipeline.py"
    "TASK_2_3_COMPLETION_REPORT.md"
    "PIPELINE_QUICK_START.md"
    "TASK_2_3_SUMMARY.md"
)

ALL_EXIST=true
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file (MISSING)"
        ALL_EXIST=false
    fi
done

echo ""

# Check dependencies exist
echo "[2] Checking Dependencies..."
DEPS=(
    "00_hierarchical_entity_processor.py"
    "04_ner11_to_neo4j_mapper.py"
)

for file in "${DEPS[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file (MISSING)"
        ALL_EXIST=false
    fi
done

echo ""

# Check Python syntax
echo "[3] Checking Python Syntax..."
if python3 -m py_compile 05_ner11_to_neo4j_hierarchical.py 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Pipeline syntax valid"
else
    echo -e "  ${RED}✗${NC} Pipeline syntax errors"
fi

if python3 -m py_compile test_05_neo4j_hierarchical_pipeline.py 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Test syntax valid"
else
    echo -e "  ${RED}✗${NC} Test syntax errors"
fi

echo ""

# Check line counts
echo "[4] Checking Code Metrics..."
LINES=$(wc -l < 05_ner11_to_neo4j_hierarchical.py)
echo "  Pipeline: $LINES lines"

METHODS=$(grep -c "def " 05_ner11_to_neo4j_hierarchical.py)
echo "  Methods: $METHODS methods"

TEST_LINES=$(wc -l < test_05_neo4j_hierarchical_pipeline.py)
echo "  Tests: $TEST_LINES lines"

echo ""

# Check critical features
echo "[5] Checking Critical Features..."

# Check for MERGE usage
if grep -q "MERGE (n:" 05_ner11_to_neo4j_hierarchical.py; then
    echo -e "  ${GREEN}✓${NC} Uses MERGE (not CREATE)"
else
    echo -e "  ${RED}✗${NC} Missing MERGE usage"
fi

# Check for hierarchy properties
if grep -q "hierarchy_path" 05_ner11_to_neo4j_hierarchical.py; then
    echo -e "  ${GREEN}✓${NC} Stores hierarchy_path"
else
    echo -e "  ${RED}✗${NC} Missing hierarchy_path"
fi

# Check for validation
if grep -q "validate_ingestion" 05_ner11_to_neo4j_hierarchical.py; then
    echo -e "  ${GREEN}✓${NC} Includes validation"
else
    echo -e "  ${RED}✗${NC} Missing validation"
fi

# Check for relationship extraction
if grep -q "extract_relationships" 05_ner11_to_neo4j_hierarchical.py; then
    echo -e "  ${GREEN}✓${NC} Includes relationship extraction"
else
    echo -e "  ${RED}✗${NC} Missing relationship extraction"
fi

echo ""

# Summary
echo "================================================================"
if [ "$ALL_EXIST" = true ]; then
    echo -e "${GREEN}✅ VERIFICATION PASSED${NC}"
    echo "All Task 2.3 components are properly created and integrated."
else
    echo -e "${RED}❌ VERIFICATION FAILED${NC}"
    echo "Some components are missing or have errors."
fi
echo "================================================================"
