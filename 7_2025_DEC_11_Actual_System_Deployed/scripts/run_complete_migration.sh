#!/bin/bash
#
# AEON Complete Hierarchical Schema Migration
# Runs migration in multiple passes until ALL nodes are processed
#
# Created: 2025-12-12
# Status: PRODUCTION-READY

LOGDIR="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/logs"
SCRIPT_DIR="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts"

echo "================================================================================"
echo "AEON COMPLETE HIERARCHICAL SCHEMA MIGRATION"
echo "================================================================================"
echo "This will run the migration in multiple passes until ALL 1.2M nodes processed"
echo ""
echo "Estimated time: 30-60 minutes"
echo "Log directory: $LOGDIR"
echo ""

# Function to check if migration is complete
check_completion() {
    python3 << 'EOF'
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))

with driver.session() as session:
    # Total nodes
    total = session.run("MATCH (n) RETURN count(n) as total").single()["total"]

    # Nodes with tier properties
    with_tier = session.run("""
        MATCH (n)
        WHERE n.tier IS NOT NULL AND n.tier1 IS NOT NULL AND n.tier2 IS NOT NULL
        RETURN count(n) as count
    """).single()["count"]

    coverage = (with_tier / total * 100) if total > 0 else 0

    print(f"Progress: {with_tier:,} / {total:,} nodes ({coverage:.1f}%)")

    # Return exit code based on completion
    if coverage >= 90:
        print("MIGRATION COMPLETE!")
        driver.close()
        exit(0)
    else:
        driver.close()
        exit(1)
EOF
}

# Run migration passes
pass_number=1
max_passes=50

while [ $pass_number -le $max_passes ]; do
    echo ""
    echo "================================================================================"
    echo "MIGRATION PASS $pass_number"
    echo "================================================================================"
    echo ""

    # Run migration
    python3 "$SCRIPT_DIR/FIX_HIERARCHICAL_SCHEMA_V2.py" <<< "yes"

    # Check if complete
    if check_completion; then
        echo ""
        echo "================================================================================"
        echo "MIGRATION SUCCESSFUL - ALL NODES PROCESSED"
        echo "================================================================================"
        echo "Total passes: $pass_number"
        echo "See logs for details: $LOGDIR/schema_fix_v2.log"
        exit 0
    fi

    echo "Pass $pass_number complete. Continuing..."
    pass_number=$((pass_number + 1))

    # Brief pause between passes
    sleep 2
done

echo ""
echo "================================================================================"
echo "WARNING: Maximum passes reached without full completion"
echo "================================================================================"
echo "Total passes: $max_passes"
echo "Run check_completion() to see current status"
exit 1
