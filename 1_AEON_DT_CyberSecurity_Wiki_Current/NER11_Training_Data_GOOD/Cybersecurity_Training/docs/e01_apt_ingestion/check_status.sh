#!/bin/bash
# Check status of validation pipeline

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Entity Validation Agent - Status Check"
echo "======================================"
echo ""

# Check for input file
if [ -f "$SCRIPT_DIR/parsed_entities.json" ]; then
    echo "✅ Input:  parsed_entities.json EXISTS"
    SIZE=$(stat -f%z "$SCRIPT_DIR/parsed_entities.json" 2>/dev/null || stat -c%s "$SCRIPT_DIR/parsed_entities.json" 2>/dev/null)
    echo "   Size: $SIZE bytes"
else
    echo "⏳ Input:  parsed_entities.json WAITING (XML Parser Agent not complete)"
fi

echo ""

# Check for validated output
if [ -f "$SCRIPT_DIR/validated_entities.json" ]; then
    echo "✅ Output: validated_entities.json EXISTS"
    SIZE=$(stat -f%z "$SCRIPT_DIR/validated_entities.json" 2>/dev/null || stat -c%s "$SCRIPT_DIR/validated_entities.json" 2>/dev/null)
    echo "   Size: $SIZE bytes"

    # Extract metrics from output
    if command -v jq &> /dev/null; then
        echo ""
        echo "   Metrics:"
        jq -r '.metadata | "   - Total Parsed: \(.total_parsed)\n   - Valid: \(.total_valid)\n   - Duplicates Removed: \(.duplicates_removed)\n   - Unique Entities: \(.unique_entities)\n   - F1 Score: \(.f1_score)"' "$SCRIPT_DIR/validated_entities.json"
    fi
else
    echo "⏳ Output: validated_entities.json NOT YET CREATED"
fi

echo ""

# Check for validation report
if [ -f "$SCRIPT_DIR/validation_report.txt" ]; then
    echo "✅ Report: validation_report.txt EXISTS"
    echo ""
    echo "F1 Score:"
    grep "F1 Score:" "$SCRIPT_DIR/validation_report.txt" | head -1
    echo ""
    echo "Status:"
    grep "Validation Status:" "$SCRIPT_DIR/validation_report.txt"
else
    echo "⏳ Report: validation_report.txt NOT YET CREATED"
fi

echo ""
echo "======================================"
echo ""

# Determine overall status
if [ -f "$SCRIPT_DIR/validated_entities.json" ] && [ -f "$SCRIPT_DIR/validation_report.txt" ]; then
    echo "📊 VALIDATION: COMPLETE"

    # Check F1 score if jq available
    if command -v jq &> /dev/null; then
        F1=$(jq -r '.metadata.f1_score' "$SCRIPT_DIR/validated_entities.json")
        if (( $(echo "$F1 >= 0.90" | bc -l) )); then
            echo "✅ SUCCESS: F1 >= 0.90"
        else
            echo "⚠️  WARNING: F1 < 0.90 - Review needed"
        fi
    fi
elif [ -f "$SCRIPT_DIR/parsed_entities.json" ]; then
    echo "🔄 VALIDATION: IN PROGRESS (input ready)"
    echo ""
    echo "To run validation:"
    echo "  cd $SCRIPT_DIR"
    echo "  python3 entity_validator.py"
else
    echo "⏳ VALIDATION: WAITING FOR INPUT"
    echo ""
    echo "Waiting for XML Parser Agent to create parsed_entities.json"
    echo ""
    echo "To monitor automatically:"
    echo "  cd $SCRIPT_DIR"
    echo "  ./wait_and_validate.sh"
fi

echo ""
