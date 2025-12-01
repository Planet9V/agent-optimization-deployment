#!/bin/bash
#
# Post-Task Hook - Qdrant Knowledge Storage
# Automatically triggered after task completion
# Stores findings, decisions, and learnings for future reuse
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_CMD="python3"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Task context
TASK_DESCRIPTION="${1:-${TASK_DESCRIPTION:-}}"
WAVE_NUMBER="${2:-${WAVE_NUMBER:-}}"
AGENT_NAME="${3:-${AGENT_NAME:-claude-flow}}"
TASK_OUTCOME="${4:-${TASK_OUTCOME:-success}}"
FINDING="${5:-${FINDING:-}}"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}💾 POST-TASK KNOWLEDGE STORAGE${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Task: ${TASK_DESCRIPTION}"
echo -e "Wave: ${WAVE_NUMBER:-Not specified}"
echo -e "Agent: ${AGENT_NAME}"
echo -e "Outcome: ${TASK_OUTCOME}"
echo ""

# Execute post-task workflow
$PYTHON_CMD << EOF
import sys
sys.path.insert(0, '${PROJECT_ROOT}')

from qdrant_agents.workflows.post_task_workflow import PostTaskWorkflow

workflow = PostTaskWorkflow()
result = workflow.execute(
    task_description="${TASK_DESCRIPTION}",
    wave_number=${WAVE_NUMBER:-None},
    agent_name="${AGENT_NAME}",
    task_outcome="${TASK_OUTCOME}",
    finding="${FINDING}"
)

if result['success']:
    print("${GREEN}✓ Knowledge storage complete${NC}")
    print("")

    if result.get('finding_stored'):
        print(f"✓ Finding stored: {result['finding_id'][:20]}...")

    if result.get('decision_recorded'):
        print(f"✓ Decision recorded: {result['decision_id'][:20]}...")

    if result.get('sync_completed'):
        print(f"✓ Synchronized with local backup")

    print("")
    print("${GREEN}✓ Knowledge preserved for future agents${NC}")
else:
    print("${YELLOW}⚠️  Storage encountered issues${NC}")
    print(f"Error: {result.get('error', 'Unknown')}")

EOF

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
