#!/bin/bash
# Quick script to retrieve UI Developer Guide from Qdrant

echo "📚 AEON UI Developer Guide Retrieval"
echo "===================================="
echo ""

# Check if collection exists
echo "Checking Qdrant collection..."
curl -s http://localhost:6333/collections/aeon-final | python3 -m json.tool | head -20

echo ""
echo "Available sections in guide:"
echo "  - architecture (System Architecture Diagram)"
echo "  - quick_start (5-minute Quick Start)"
echo "  - api_reference (Complete API Reference)"
echo "  - database (Database Architecture)"
echo "  - workflows (Common UI Workflows)"
echo "  - components (UI Component Examples)"
echo ""

# Search for specific section
SECTION=${1:-"quick_start"}
echo "Retrieving section: $SECTION"
echo ""

curl -s -X POST http://localhost:6333/collections/aeon-final/points/scroll \
  -H "Content-Type: application/json" \
  -d "{
    \"filter\": {
      \"must\": [
        {\"key\": \"section\", \"match\": {\"value\": \"$SECTION\"}}
      ]
    },
    \"limit\": 1,
    \"with_payload\": true
  }" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('result', {}).get('points'):
    point = data['result']['points'][0]
    print('Section:', point['payload']['section'])
    print('Content preview:')
    print(point['payload']['content'][:500])
    print('...')
    print('')
    print('Full guide location:', point['payload']['full_path'])
else:
    print('No results found')
"

echo ""
echo "To view full guide:"
echo "  cat /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/UI_DEVELOPER_COMPLETE_GUIDE.md"
echo ""
echo "To retrieve different section:"
echo "  ./retrieve_ui_guide.sh architecture"
echo "  ./retrieve_ui_guide.sh api_reference"
echo "  ./retrieve_ui_guide.sh workflows"
