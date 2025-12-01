#!/bin/bash
#
# Pre-Task Hook - Qdrant Knowledge Retrieval
# Automatically triggered before any task execution
# Retrieves relevant knowledge and experiences for the current task
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_CMD="python3"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Task context (passed as environment variables or arguments)
TASK_DESCRIPTION="${1:-${TASK_DESCRIPTION:-}}"
WAVE_NUMBER="${2:-${WAVE_NUMBER:-}}"
AGENT_NAME="${3:-${AGENT_NAME:-claude-flow}}"

# Validate required parameters
if [ -z "$TASK_DESCRIPTION" ]; then
    echo -e "${YELLOW}⚠️  No task description provided, skipping pre-task knowledge retrieval${NC}"
    exit 0
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔍 PRE-TASK KNOWLEDGE RETRIEVAL${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Task: ${TASK_DESCRIPTION}"
echo -e "Wave: ${WAVE_NUMBER:-Not specified}"
echo -e "Agent: ${AGENT_NAME}"
echo ""

# Execute pre-task workflow
$PYTHON_CMD << EOF
import sys
sys.path.insert(0, '${PROJECT_ROOT}')

from qdrant_agents.workflows.pre_task_workflow import PreTaskWorkflow

workflow = PreTaskWorkflow()
result = workflow.execute(
    task_description="${TASK_DESCRIPTION}",
    wave_number=${WAVE_NUMBER:-None},
    agent_name="${AGENT_NAME}"
)

# Display results
if result['success']:
    print("${GREEN}✓ Knowledge retrieval complete${NC}")
    print("")

    # Schema knowledge
    if result.get('schema_knowledge'):
        print(f"📚 Schema Knowledge: {len(result['schema_knowledge'])} relevant items")
        for item in result['schema_knowledge'][:3]:
            print(f"   • {item['source_file']}: Score {item['score']:.3f}")

    # Past experiences
    if result.get('experiences'):
        print(f"💡 Past Experiences: {len(result['experiences'])} similar cases")
        for exp in result['experiences'][:3]:
            print(f"   • {exp['agent_name']}: {exp['finding'][:80]}...")

    # Similar implementations
    if result.get('implementations'):
        print(f"🔧 Similar Implementations: {len(result['implementations'])} found")
        for impl in result['implementations'][:2]:
            print(f"   • Score {impl['score']:.3f}: {impl['content'][:80]}...")

    # Related decisions
    if result.get('decisions'):
        print(f"📋 Related Decisions: {len(result['decisions'])} found")
        for dec in result['decisions'][:2]:
            print(f"   • {dec['decision_type']}: {dec['decision'][:80]}...")

    print("")
    print("${GREEN}✓ Context prepared for task execution${NC}")
else:
    print("${YELLOW}⚠️  Knowledge retrieval encountered issues${NC}")
    print(f"Error: {result.get('error', 'Unknown')}")

EOF

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
