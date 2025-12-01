#!/usr/bin/env python3
"""
Post-Task Workflow - Knowledge Storage After Task Completion
Stores findings, decisions, and learnings
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.claude_flow_bridge import get_bridge
import structlog

logger = structlog.get_logger()

class PostTaskWorkflow:
    """
    Post-task workflow for storing knowledge after task execution
    """

    def __init__(self):
        """Initialize workflow with bridge"""
        self.bridge = get_bridge()
        logger.info("post_task_workflow_initialized")

    def execute(
        self,
        task_description: str,
        wave_number: Optional[int] = None,
        agent_name: str = "claude-flow",
        task_outcome: str = "success",
        finding: Optional[str] = None,
        decision: Optional[str] = None,
        decision_rationale: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute post-task knowledge storage

        Args:
            task_description: Task that was executed
            wave_number: Wave number
            agent_name: Agent that executed task
            task_outcome: "success", "partial", or "failed"
            finding: Key learning or discovery
            decision: Decision made during task
            decision_rationale: Why the decision was made

        Returns:
            Storage confirmation
        """
        try:
            logger.info(
                "post_task_workflow_executing",
                task=task_description[:100],
                wave=wave_number,
                agent=agent_name,
                outcome=task_outcome
            )

            result = {
                "success": True,
                "task": task_description,
                "wave": wave_number,
                "agent": agent_name,
                "outcome": task_outcome,
                "timestamp": datetime.now().isoformat()
            }

            # 1. Store finding if provided or auto-generate
            finding_to_store = finding or self._auto_generate_finding(
                task_description,
                task_outcome
            )

            finding_result = self.bridge.store_finding(
                finding=finding_to_store,
                agent_name=agent_name,
                context={
                    "task": task_description,
                    "outcome": task_outcome,
                    "timestamp": datetime.now().isoformat()
                },
                tags=self._generate_tags(task_description, task_outcome),
                wave=wave_number
            )

            result["finding_stored"] = finding_result.get("success", False)
            result["finding_id"] = finding_result.get("finding_id", "")

            # 2. Record decision if provided
            if decision and decision_rationale:
                decision_result = self.bridge.record_decision(
                    decision=decision,
                    rationale=decision_rationale,
                    decision_type="implementation",
                    wave=wave_number,
                    made_by=agent_name
                )

                result["decision_recorded"] = decision_result.get("success", False)
                result["decision_id"] = decision_result.get("decision_id", "")

            # 3. Sync to local backup
            sync_result = self.bridge.sync_memories(direction="qdrant_to_local")
            result["sync_completed"] = sync_result.get("success", False)

            logger.info(
                "post_task_workflow_completed",
                finding_stored=result["finding_stored"],
                decision_recorded=result.get("decision_recorded", False)
            )

            return result

        except Exception as e:
            logger.error("post_task_workflow_failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "task": task_description
            }

    def _auto_generate_finding(
        self,
        task_description: str,
        task_outcome: str
    ) -> str:
        """Auto-generate finding if not provided"""
        if task_outcome == "success":
            return f"Successfully completed: {task_description}"
        elif task_outcome == "failed":
            return f"Failed to complete: {task_description} - requires investigation"
        else:
            return f"Partially completed: {task_description} - needs follow-up"

    def _generate_tags(
        self,
        task_description: str,
        task_outcome: str
    ) -> list:
        """Generate tags based on task"""
        tags = [task_outcome]

        # Add context tags based on keywords
        desc_lower = task_description.lower()

        if "property" in desc_lower or "class" in desc_lower:
            tags.append("ontology")
        if "sensor" in desc_lower or "device" in desc_lower:
            tags.append("iot")
        if "query" in desc_lower or "cypher" in desc_lower:
            tags.append("query")
        if "test" in desc_lower or "validation" in desc_lower:
            tags.append("testing")
        if "error" in desc_lower or "bug" in desc_lower:
            tags.append("issue")

        return tags


if __name__ == "__main__":
    # CLI testing
    import argparse

    parser = argparse.ArgumentParser(description="Post-Task Workflow")
    parser.add_argument("task", help="Task description")
    parser.add_argument("--wave", type=int, help="Wave number")
    parser.add_argument("--agent", default="test", help="Agent name")
    parser.add_argument("--outcome", default="success",
                       choices=["success", "partial", "failed"],
                       help="Task outcome")
    parser.add_argument("--finding", help="Key finding")
    parser.add_argument("--decision", help="Decision made")
    parser.add_argument("--rationale", help="Decision rationale")

    args = parser.parse_args()

    workflow = PostTaskWorkflow()
    result = workflow.execute(
        task_description=args.task,
        wave_number=args.wave,
        agent_name=args.agent,
        task_outcome=args.outcome,
        finding=args.finding,
        decision=args.decision,
        decision_rationale=args.rationale
    )

    print(f"\n{'='*60}")
    print("POST-TASK KNOWLEDGE STORAGE")
    print(f"{'='*60}")
    print(f"\nTask: {result['task']}")
    print(f"Outcome: {result['outcome']}")
    print(f"Finding Stored: {'✓' if result.get('finding_stored') else '✗'}")
    if result.get('decision_recorded'):
        print(f"Decision Recorded: ✓")
    print(f"Synced to Local: {'✓' if result.get('sync_completed') else '✗'}")
