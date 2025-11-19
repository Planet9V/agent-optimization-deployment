#!/usr/bin/env python3
"""
Pre-Task Workflow - Knowledge Retrieval Before Task Execution
Retrieves relevant context from all Qdrant collections
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.claude_flow_bridge import get_bridge
import structlog

logger = structlog.get_logger()

class PreTaskWorkflow:
    """
    Pre-task workflow for retrieving relevant knowledge before task execution
    """

    def __init__(self):
        """Initialize workflow with bridge"""
        self.bridge = get_bridge()
        logger.info("pre_task_workflow_initialized")

    def execute(
        self,
        task_description: str,
        wave_number: Optional[int] = None,
        agent_name: str = "claude-flow"
    ) -> Dict[str, Any]:
        """
        Execute pre-task knowledge retrieval

        Args:
            task_description: Description of task about to be executed
            wave_number: Optional wave number for filtering
            agent_name: Name of agent executing task

        Returns:
            Retrieved knowledge and context
        """
        try:
            logger.info(
                "pre_task_workflow_executing",
                task=task_description[:100],
                wave=wave_number,
                agent=agent_name
            )

            result = {
                "success": True,
                "task": task_description,
                "wave": wave_number,
                "agent": agent_name
            }

            # 1. Search schema knowledge
            schema_result = self.bridge.search_knowledge(
                query=task_description,
                wave=wave_number,
                top_k=5
            )
            result["schema_knowledge"] = schema_result.get("results", [])

            # 2. Retrieve past experiences
            experiences_result = self.bridge.retrieve_experiences(
                query=task_description,
                wave_filter=wave_number,
                top_k=3
            )
            result["experiences"] = experiences_result.get("experiences", [])

            # 3. Find similar implementations
            impl_result = self.bridge.find_implementations(
                description=task_description,
                top_k=3
            )
            result["implementations"] = impl_result.get("similar_implementations", [])

            # 4. Find related decisions
            decisions_result = self.bridge.find_decisions(
                query=task_description,
                wave=wave_number,
                top_k=3
            )
            result["decisions"] = decisions_result.get("decisions", [])

            # 5. Generate contextual summary
            result["summary"] = self._generate_summary(result)

            logger.info(
                "pre_task_workflow_completed",
                schema_items=len(result["schema_knowledge"]),
                experiences=len(result["experiences"]),
                implementations=len(result["implementations"]),
                decisions=len(result["decisions"])
            )

            return result

        except Exception as e:
            logger.error("pre_task_workflow_failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "task": task_description
            }

    def _generate_summary(self, result: Dict[str, Any]) -> str:
        """Generate contextual summary for agent"""
        lines = []

        if result.get("schema_knowledge"):
            lines.append(
                f"Schema Knowledge: {len(result['schema_knowledge'])} relevant items found"
            )

        if result.get("experiences"):
            lines.append(
                f"Past Experiences: {len(result['experiences'])} similar cases from agents"
            )

        if result.get("implementations"):
            lines.append(
                f"Similar Implementations: {len(result['implementations'])} found"
            )

        if result.get("decisions"):
            lines.append(
                f"Related Decisions: {len(result['decisions'])} architectural decisions"
            )

        return "\n".join(lines) if lines else "No relevant context found"


if __name__ == "__main__":
    # CLI testing
    import argparse

    parser = argparse.ArgumentParser(description="Pre-Task Workflow")
    parser.add_argument("task", help="Task description")
    parser.add_argument("--wave", type=int, help="Wave number")
    parser.add_argument("--agent", default="test", help="Agent name")

    args = parser.parse_args()

    workflow = PreTaskWorkflow()
    result = workflow.execute(
        task_description=args.task,
        wave_number=args.wave,
        agent_name=args.agent
    )

    print(f"\n{'='*60}")
    print("PRE-TASK KNOWLEDGE RETRIEVAL")
    print(f"{'='*60}")
    print(f"\nTask: {result['task']}")
    print(f"Wave: {result.get('wave', 'N/A')}")
    print(f"\n{result.get('summary', 'No summary')}")
