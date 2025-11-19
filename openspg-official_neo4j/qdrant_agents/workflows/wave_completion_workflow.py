#!/usr/bin/env python3
"""
Wave Completion Workflow - Pattern Discovery & Analytics After Wave
Discovers patterns, generates analytics, and provides recommendations
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

class WaveCompletionWorkflow:
    """
    Wave completion workflow for pattern discovery and analytics
    """

    def __init__(self):
        """Initialize workflow with bridge"""
        self.bridge = get_bridge()
        logger.info("wave_completion_workflow_initialized")

    def execute(
        self,
        wave_number: int,
        wave_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute wave completion processing

        Args:
            wave_number: Wave number that completed
            wave_name: Optional wave name

        Returns:
            Pattern analysis and recommendations
        """
        try:
            logger.info(
                "wave_completion_workflow_executing",
                wave=wave_number,
                wave_name=wave_name
            )

            result = {
                "success": True,
                "wave": wave_number,
                "wave_name": wave_name,
                "timestamp": datetime.now().isoformat()
            }

            # 1. Discover patterns from wave
            patterns_result = self.bridge.discover_patterns(
                algorithm="kmeans",
                n_clusters=None  # Auto-detect optimal
            )

            result["patterns_discovered"] = {
                "count": patterns_result.get("count", 0),
                "patterns": patterns_result.get("patterns", [])
            }

            if patterns_result.get("count", 0) > 0:
                # Get top pattern by frequency
                patterns = patterns_result["patterns"]
                top_pattern = max(patterns, key=lambda p: p.get("frequency", 0))
                result["patterns_discovered"]["top_pattern"] = top_pattern

            # 2. Get wave analytics
            metrics_result = self.bridge.get_metrics()

            if metrics_result.get("success"):
                metrics = metrics_result["metrics"]
                collections = metrics.get("collections", {})

                # Count wave-specific data
                wave_findings = 0
                wave_decisions = 0

                # This would need to filter by wave in actual implementation
                # For now, showing total counts
                if "agent_shared_memory" in collections:
                    wave_findings = collections["agent_shared_memory"].get("vectors_count", 0)

                if "implementation_decisions" in collections:
                    wave_decisions = collections["implementation_decisions"].get("vectors_count", 0)

                result["analytics"] = {
                    "total_findings": wave_findings,
                    "total_decisions": wave_decisions,
                    "active_agents": len(set(
                        p.get("primary_agents", {}).keys()
                        for p in patterns_result.get("patterns", [])
                    )),
                    "avg_query_ms": metrics.get("performance", {}).get("avg_duration_ms", 0)
                }

            # 3. Get optimization recommendations
            recs_result = self.bridge.get_recommendations()

            result["recommendations"] = recs_result.get("recommendations", [])

            # 4. Generate wave report
            report_path = self._generate_wave_report(
                wave_number,
                wave_name,
                result
            )
            result["report_path"] = str(report_path)

            # 5. Sync everything to local backup
            sync_result = self.bridge.sync_memories(direction="bidirectional")
            result["sync_completed"] = sync_result.get("success", False)

            logger.info(
                "wave_completion_workflow_completed",
                wave=wave_number,
                patterns=result["patterns_discovered"]["count"],
                recommendations=len(result["recommendations"])
            )

            return result

        except Exception as e:
            logger.error("wave_completion_workflow_failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "wave": wave_number
            }

    def _generate_wave_report(
        self,
        wave_number: int,
        wave_name: Optional[str],
        result: Dict[str, Any]
    ) -> Path:
        """Generate comprehensive wave completion report"""
        report_dir = Path("/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup/wave_reports")
        report_dir.mkdir(parents=True, exist_ok=True)

        report_file = report_dir / f"wave_{wave_number}_completion_report.md"

        report = f"""# Wave {wave_number} Completion Report
**Wave Name**: {wave_name or 'N/A'}
**Completed**: {result['timestamp']}

## Summary

Wave {wave_number} has been completed. This report summarizes discovered patterns, analytics, and recommendations for future waves.

## Pattern Discovery

**Total Patterns Discovered**: {result['patterns_discovered']['count']}

"""

        if result['patterns_discovered']['count'] > 0:
            patterns = result['patterns_discovered']['patterns']
            report += "### Top Patterns\n\n"
            for i, pattern in enumerate(patterns[:5], 1):
                report += f"{i}. **Pattern {pattern.get('pattern_id', 'N/A')}**\n"
                report += f"   - Frequency: {pattern.get('frequency', 0)} occurrences\n"
                report += f"   - Cohesion Score: {pattern.get('cohesion_score', 0):.3f}\n"
                report += f"   - Primary Agents: {', '.join(pattern.get('primary_agents', {}).keys())}\n\n"

        # Analytics
        if result.get('analytics'):
            analytics = result['analytics']
            report += f"""
## Wave Analytics

- **Total Findings Stored**: {analytics.get('total_findings', 0)}
- **Decisions Recorded**: {analytics.get('total_decisions', 0)}
- **Active Agents**: {analytics.get('active_agents', 0)}
- **Average Query Time**: {analytics.get('avg_query_ms', 0):.0f}ms

"""

        # Recommendations
        if result.get('recommendations'):
            recs = result['recommendations']
            high_priority = [r for r in recs if r.get('priority') == 'high']

            report += f"## Optimization Recommendations\n\n"
            report += f"**Total Recommendations**: {len(recs)}\n\n"

            if high_priority:
                report += "### High Priority\n\n"
                for rec in high_priority:
                    report += f"- **{rec['issue']}**\n"
                    report += f"  - Current: {rec['current_value']}\n"
                    report += f"  - Action: {rec['recommendation']}\n"
                    report += f"  - Impact: {rec['estimated_impact']}\n\n"

        report += f"""
## Next Steps

1. Review discovered patterns for next wave implementation
2. Address high-priority recommendations before Wave {wave_number + 1}
3. Apply learned patterns to reduce implementation time
4. Continue cross-agent knowledge sharing

---

*Report generated by Qdrant Analytics Agent*
*Wave Completion Workflow v1.0*
"""

        report_file.write_text(report)
        logger.info("wave_report_generated", path=str(report_file))

        return report_file


if __name__ == "__main__":
    # CLI testing
    import argparse

    parser = argparse.ArgumentParser(description="Wave Completion Workflow")
    parser.add_argument("wave", type=int, help="Wave number")
    parser.add_argument("--name", help="Wave name")

    args = parser.parse_args()

    workflow = WaveCompletionWorkflow()
    result = workflow.execute(
        wave_number=args.wave,
        wave_name=args.name
    )

    print(f"\n{'='*60}")
    print(f"WAVE {args.wave} COMPLETION PROCESSING")
    print(f"{'='*60}")
    print(f"\nPatterns Discovered: {result['patterns_discovered']['count']}")
    if result.get('analytics'):
        print(f"Total Findings: {result['analytics'].get('total_findings', 0)}")
        print(f"Total Decisions: {result['analytics'].get('total_decisions', 0)}")
    print(f"Recommendations: {len(result.get('recommendations', []))}")
    print(f"\nReport: {result.get('report_path', 'Not generated')}")
