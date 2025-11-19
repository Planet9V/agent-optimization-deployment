#!/bin/bash
#
# Wave Complete Hook - Pattern Discovery & Analytics
# Triggered after wave completion
# Discovers patterns, generates reports, and provides optimization recommendations
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_CMD="python3"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Wave context
WAVE_NUMBER="${1:-${WAVE_NUMBER:-}}"
WAVE_NAME="${2:-${WAVE_NAME:-}}"

if [ -z "$WAVE_NUMBER" ]; then
    echo -e "${YELLOW}⚠️  No wave number provided, skipping wave completion processing${NC}"
    exit 0
fi

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🎯 WAVE ${WAVE_NUMBER} COMPLETION PROCESSING${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Wave: ${WAVE_NUMBER} - ${WAVE_NAME:-}"
echo -e "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Execute wave completion workflow
$PYTHON_CMD << EOF
import sys
sys.path.insert(0, '${PROJECT_ROOT}')

from qdrant_agents.workflows.wave_completion_workflow import WaveCompletionWorkflow

workflow = WaveCompletionWorkflow()
result = workflow.execute(
    wave_number=${WAVE_NUMBER},
    wave_name="${WAVE_NAME}"
)

if result['success']:
    print("${GREEN}✓ Wave completion processing complete${NC}")
    print("")

    # Pattern discovery
    if result.get('patterns_discovered'):
        patterns = result['patterns_discovered']
        print(f"${CYAN}🧩 Pattern Discovery: {patterns['count']} patterns found${NC}")
        if patterns['count'] > 0:
            print(f"   Most frequent pattern: {patterns['top_pattern']['frequency']} occurrences")

    # Analytics
    if result.get('analytics'):
        analytics = result['analytics']
        print(f"${CYAN}📊 Wave Analytics:${NC}")
        print(f"   • Total findings: {analytics.get('total_findings', 0)}")
        print(f"   • Decisions made: {analytics.get('total_decisions', 0)}")
        print(f"   • Agent activity: {analytics.get('active_agents', 0)} agents")
        print(f"   • Query performance: {analytics.get('avg_query_ms', 0):.0f}ms avg")

    # Recommendations
    if result.get('recommendations'):
        recs = result['recommendations']
        print(f"${CYAN}💡 Optimization Recommendations: {len(recs)} items${NC}")
        high_priority = [r for r in recs if r.get('priority') == 'high']
        if high_priority:
            print(f"   ⚠️  {len(high_priority)} high-priority recommendations")
            for rec in high_priority[:3]:
                print(f"      • {rec['issue']}")

    # Report generation
    if result.get('report_path'):
        print(f"${CYAN}📄 Report saved: {result['report_path']}${NC}")

    print("")
    print("${GREEN}✓ Wave ${WAVE_NUMBER} knowledge extracted and preserved${NC}")
else:
    print("${YELLOW}⚠️  Wave completion processing encountered issues${NC}")
    print(f"Error: {result.get('error', 'Unknown')}")

EOF

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
