#!/bin/bash
# Wait for XML Parser Agent to create parsed_entities.json, then validate

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_FILE="$SCRIPT_DIR/parsed_entities.json"
VALIDATOR="$SCRIPT_DIR/entity_validator.py"

echo "🔍 Entity Validation Agent - Waiting for parsed_entities.json"
echo "=================================================="
echo ""
echo "Monitoring: $INPUT_FILE"
echo "Will execute: $VALIDATOR"
echo ""

# Wait for file with timeout (5 minutes = 300 seconds)
TIMEOUT=300
ELAPSED=0
INTERVAL=2

while [ $ELAPSED -lt $TIMEOUT ]; do
    if [ -f "$INPUT_FILE" ]; then
        echo ""
        echo "✅ Found parsed_entities.json!"
        echo "⚡ Starting validation..."
        echo ""

        # Execute validation
        python3 "$VALIDATOR"
        EXIT_CODE=$?

        if [ $EXIT_CODE -eq 0 ]; then
            echo ""
            echo "🎉 VALIDATION COMPLETE - SUCCESS"
        else
            echo ""
            echo "⚠️  VALIDATION COMPLETE - REVIEW NEEDED"
        fi

        exit $EXIT_CODE
    fi

    # Show progress every 10 seconds
    if [ $((ELAPSED % 10)) -eq 0 ] && [ $ELAPSED -gt 0 ]; then
        echo "⏳ Still waiting... (${ELAPSED}s elapsed)"
    fi

    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
done

echo ""
echo "❌ TIMEOUT: parsed_entities.json not created after ${TIMEOUT} seconds"
echo "   The XML Parser Agent may not have run yet."
echo ""
echo "To run validation manually when the file is ready:"
echo "   python3 $VALIDATOR"
echo ""
exit 1
