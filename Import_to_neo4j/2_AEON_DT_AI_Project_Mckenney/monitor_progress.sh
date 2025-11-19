#!/bin/bash
# Monitor document processing progress

echo "==================================="
echo "DOCUMENT PROCESSING MONITOR"
echo "==================================="
echo

# Check database state
echo "📊 Current Database State:"
python3 check_neo4j_status.py
echo

# Check processing log
if [ -f "FINAL_REPROCESSING.log" ]; then
    echo "📝 Recent Processing Activity:"
    echo "---"
    tail -30 FINAL_REPROCESSING.log | grep -E "(Processed|Skipped|Failed|Processing)" | tail -15
    echo "---"
    echo

    # Count successes and failures
    SUCCESSFUL=$(grep -c "Processed:" FINAL_REPROCESSING.log 2>/dev/null || echo "0")
    DUPLICATES=$(grep -c "Skipped.*already processed" FINAL_REPROCESSING.log 2>/dev/null || echo "0")
    FAILED=$(grep -c "Failed:" FINAL_REPROCESSING.log 2>/dev/null || echo "0")

    echo "📈 Processing Statistics:"
    echo "  ✅ Successfully processed: $SUCCESSFUL"
    echo "  ⊗  Skipped (duplicates): $DUPLICATES"
    echo "  ❌ Failed: $FAILED"
    echo "  📦 Total attempted: $((SUCCESSFUL + DUPLICATES + FAILED))"
    echo
fi

# Check if process is still running
if pgrep -f "process_all_documents.py" > /dev/null; then
    echo "✅ Processing is RUNNING"
    echo
    echo "To view live processing output:"
    echo "  tail -f FINAL_REPROCESSING.log"
else
    echo "⚠️  Processing appears to have STOPPED"
    echo "Check FINAL_REPROCESSING.log for completion or errors"
fi

echo
echo "==================================="
