#!/bin/bash

# EMERGENCY_SERVICES Schema Validator - Monitoring Script
# Watches for Agent 2 completion and auto-executes validation

MAPPING_FILE="/home/jim/2_OXOT_Projects_Dev/temp/sector-EMERGENCY_SERVICES-node-type-mapping.json"
VALIDATOR_SCRIPT="/home/jim/2_OXOT_Projects_Dev/temp/schema-validation-engine.py"
LOG_FILE="/home/jim/2_OXOT_Projects_Dev/temp/validator-monitor.log"
OUTPUT_FILE="/home/jim/2_OXOT_Projects_Dev/temp/sector-EMERGENCY_SERVICES-schema-validation.json"

echo "EMERGENCY_SERVICES Schema Validator - Monitoring Started" >> "$LOG_FILE"
echo "Timestamp: $(date)" >> "$LOG_FILE"
echo "Watching for: $MAPPING_FILE" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

# Check interval (seconds)
CHECK_INTERVAL=5
MAX_WAIT_TIME=600  # 10 minutes
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT_TIME ]; do
    if [ -f "$MAPPING_FILE" ]; then
        echo "FOUND: Agent 2 mapping file created at $(date)" >> "$LOG_FILE"

        # Validate the JSON structure
        if python3 -m json.tool "$MAPPING_FILE" > /dev/null 2>&1; then
            echo "VALID: JSON structure validated" >> "$LOG_FILE"

            # Execute validator
            echo "EXECUTING: Schema validation at $(date)" >> "$LOG_FILE"
            python3 "$VALIDATOR_SCRIPT" >> "$LOG_FILE" 2>&1

            # Check results
            if [ -f "$OUTPUT_FILE" ]; then
                VALIDATION_STATUS=$(python3 -c "import json; f=open('$OUTPUT_FILE'); d=json.load(f); print(d['validation_report']['validation_status'])" 2>/dev/null)
                COMPLIANCE=$(python3 -c "import json; f=open('$OUTPUT_FILE'); d=json.load(f); print(d['validation_report']['pass_percentage'])" 2>/dev/null)

                echo "RESULT: $VALIDATION_STATUS" >> "$LOG_FILE"
                echo "COMPLIANCE: $COMPLIANCE%" >> "$LOG_FILE"

                # Print to console
                echo ""
                echo "========================================"
                echo "VALIDATION COMPLETE"
                echo "========================================"
                echo "Status: $VALIDATION_STATUS"
                echo "Compliance: $COMPLIANCE%"
                echo "Results: $OUTPUT_FILE"
                echo ""

                exit 0
            fi
        else
            echo "ERROR: Invalid JSON in mapping file" >> "$LOG_FILE"
        fi
    fi

    ELAPSED=$((ELAPSED + CHECK_INTERVAL))
    sleep $CHECK_INTERVAL
done

echo "TIMEOUT: No mapping file found after ${MAX_WAIT_TIME}s" >> "$LOG_FILE"
echo "Validation monitoring abandoned at $(date)" >> "$LOG_FILE"
