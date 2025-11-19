#!/bin/bash
###############################################################################
# Sequential NVD CVE Import Executor
# Automatically executes remaining imports (2020-2025) after 2018-2019 completes
###############################################################################

set -e  # Exit on error

SCRIPT_DIR="/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

echo "================================================================================"
echo "NVD CVE SEQUENTIAL IMPORT EXECUTOR"
echo "================================================================================"
echo "Start Time: $(date)"
echo ""

# Function to wait for import completion
wait_for_import() {
    local import_name=$1
    local log_file=$2
    echo "Waiting for $import_name to complete..."

    # Wait until log contains "Import completed successfully" or script process ends
    while ! grep -q "Import completed successfully" "$log_file" 2>/dev/null; do
        if ! pgrep -f "python.*import_nvd.*\.py" > /dev/null; then
            echo "⚠️  Warning: No import process detected"
            sleep 10
        fi
        sleep 60
        echo "  Still importing $import_name... ($(date))"
    done

    echo "✅ $import_name completed!"
}

# Check if 2018-2019 is still running
if pgrep -f "python.*import_nvd_2018_2019\.py" > /dev/null; then
    echo "Step 1: Waiting for 2018-2019 import to complete..."
    wait_for_import "2018-2019" "nvd_2018_2019_import.log"
else
    echo "Step 1: 2018-2019 import already complete ✅"
fi

echo ""
echo "================================================================================"
echo "Step 2: Importing 2020-2021 CVEs (~38,000-40,000)"
echo "================================================================================"
python3 import_nvd_2020_2021.py
echo "✅ 2020-2021 import completed!"

echo ""
echo "================================================================================"
echo "Step 3: Importing 2022-2023 CVEs (~50,000-52,000)"
echo "================================================================================"
python3 import_nvd_2022_2023.py
echo "✅ 2022-2023 import completed!"

echo ""
echo "================================================================================"
echo "Step 4: Importing 2024-2025 CVEs (~35,000)"
echo "================================================================================"
python3 import_nvd_2024_2025.py
echo "✅ 2024-2025 import completed!"

echo ""
echo "================================================================================"
echo "ALL IMPORTS COMPLETED SUCCESSFULLY"
echo "================================================================================"
echo "End Time: $(date)"
echo ""
echo "Next steps:"
echo "1. Run schema enhancement: python3 enhance_cve_schema.py"
echo "2. Generate final report: python3 cve_statistics_report.py"
echo "3. Process documents: python3 process_all_documents.py"
echo "================================================================================"
