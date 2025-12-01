#!/usr/bin/env python3
"""
Qdrant Decision Agent - Implementation Decision Tracker
Records and analyzes architectural and implementation decisions
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import uuid
import json
import structlog

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.embedding_generator import EmbeddingGenerator
from utils.collection_manager import CollectionManager

logger = structlog.get_logger()

class QdrantDecisionAgent:
    """
    Specialized agent for tracking implementation decisions

    Capabilities:
    - Record architectural and implementation decisions
    - Track decision rationale and alternatives considered
    - Analyze decision impacts and dependencies
    - Detect inconsistent decisions
    - Generate decision reports
    """

    def __init__(
        self,
        url: str = "http://localhost:6333",
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        max_impact_depth: int = 3
    ):
        """Initialize decision agent"""
        self.url = url
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.max_impact_depth = max_impact_depth

        # Initialize components
        self.qdrant = QdrantClient(url=self.url, api_key=self.api_key)
        self.embedder = EmbeddingGenerator(
            api_key=self.openai_api_key,
            model="text-embedding-3-large",
            dimensions=3072
        )
        self.collection_mgr = CollectionManager(url=self.url, api_key=self.api_key)

        logger.info(
            "qdrant_decision_agent_initialized",
            max_impact_depth=self.max_impact_depth
        )

    def record_decision(
        self,
        decision: str,
        rationale: str,
        alternatives: Optional[List[str]] = None,
        impact_areas: Optional[List[str]] = None,
        decision_type: str = "implementation",
        wave: Optional[int] = None,
        dependencies: Optional[List[str]] = None,
        made_by: Optional[str] = None
    ) -> str:
        """
        Record an implementation decision

        Args:
            decision: The decision made
            rationale: Why this decision was made
            alternatives: What alternatives were considered
            impact_areas: What areas this affects (e.g., ["performance", "security"])
            decision_type: "architectural", "implementation", "tooling", etc.
            wave: Wave number if applicable
            dependencies: IDs of decisions this depends on
            made_by: Agent or person who made the decision

        Returns:
            Decision ID
        """
        try:
            decision_id = str(uuid.uuid4())

            # Generate embedding from decision + rationale
            decision_text = f"{decision} {rationale}"
            embedding = self.embedder.create(decision_text)

            # Prepare payload
            payload = {
                "decision_id": decision_id,
                "decision": decision,
                "rationale": rationale,
                "alternatives": alternatives or [],
                "impact_areas": impact_areas or [],
                "decision_type": decision_type,
                "wave": wave,
                "dependencies": dependencies or [],
                "made_by": made_by or "unknown",
                "timestamp": datetime.now().isoformat(),
                "status": "active"
            }

            # Store in Qdrant
            point = PointStruct(
                id=decision_id,
                vector=embedding,
                payload=payload
            )

            self.qdrant.upsert(
                collection_name="implementation_decisions",
                points=[point],
                wait=True
            )

            logger.info(
                "decision_recorded",
                decision_id=decision_id,
                type=decision_type,
                wave=wave
            )

            return decision_id

        except Exception as e:
            logger.error("decision_recording_failed", error=str(e))
            raise

    def find_related_decisions(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.6,
        decision_type: Optional[str] = None,
        wave_filter: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Find decisions related to a topic

        Args:
            query: What to search for
            top_k: Number of decisions
            score_threshold: Minimum relevance
            decision_type: Filter by decision type
            wave_filter: Filter by wave

        Returns:
            Related decisions
        """
        try:
            query_vector = self.embedder.create(query)

            # Build filter
            filter_conditions = []
            if decision_type:
                filter_conditions.append(
                    FieldCondition(
                        key="decision_type",
                        match=MatchValue(value=decision_type)
                    )
                )
            if wave_filter is not None:
                filter_conditions.append(
                    FieldCondition(
                        key="wave",
                        match=MatchValue(value=wave_filter)
                    )
                )

            query_filter = Filter(must=filter_conditions) if filter_conditions else None

            results = self.qdrant.search(
                collection_name="implementation_decisions",
                query_vector=query_vector,
                query_filter=query_filter,
                limit=top_k,
                score_threshold=score_threshold,
                with_payload=True
            )

            decisions = []
            for result in results:
                decisions.append({
                    "score": result.score,
                    "decision_id": result.payload.get("decision_id", ""),
                    "decision": result.payload.get("decision", ""),
                    "rationale": result.payload.get("rationale", ""),
                    "alternatives": result.payload.get("alternatives", []),
                    "decision_type": result.payload.get("decision_type", ""),
                    "wave": result.payload.get("wave"),
                    "impact_areas": result.payload.get("impact_areas", []),
                    "timestamp": result.payload.get("timestamp", "")
                })

            logger.info(
                "related_decisions_found",
                query=query[:50],
                results=len(decisions)
            )

            return decisions

        except Exception as e:
            logger.error("decision_search_failed", error=str(e))
            return []

    def analyze_decision_impact(
        self,
        decision_id: str,
        depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Analyze the impact of a decision

        Args:
            decision_id: Decision to analyze
            depth: How many dependency levels to traverse

        Returns:
            Impact analysis
        """
        try:
            depth = depth or self.max_impact_depth

            # Get the decision
            results = self.qdrant.retrieve(
                collection_name="implementation_decisions",
                ids=[decision_id]
            )

            if not results:
                return {"error": "Decision not found"}

            decision = results[0].payload

            # Find decisions that depend on this one
            dependent_decisions = self._find_dependent_decisions(decision_id, depth)

            # Analyze impact areas
            direct_impacts = decision.get("impact_areas", [])
            indirect_impacts = set()
            for dep in dependent_decisions:
                indirect_impacts.update(dep.get("impact_areas", []))

            analysis = {
                "decision_id": decision_id,
                "decision": decision.get("decision", ""),
                "direct_impacts": direct_impacts,
                "indirect_impacts": list(indirect_impacts),
                "dependent_decisions": dependent_decisions,
                "dependency_depth": depth,
                "total_affected_decisions": len(dependent_decisions),
                "risk_level": self._calculate_risk_level(decision, dependent_decisions)
            }

            logger.info(
                "decision_impact_analyzed",
                decision_id=decision_id,
                affected_decisions=len(dependent_decisions)
            )

            return analysis

        except Exception as e:
            logger.error("decision_impact_analysis_failed", error=str(e))
            return {"error": str(e)}

    def _find_dependent_decisions(
        self,
        decision_id: str,
        depth: int,
        visited: Optional[set] = None
    ) -> List[Dict[str, Any]]:
        """Recursively find decisions that depend on this one"""
        if visited is None:
            visited = set()

        if decision_id in visited or depth <= 0:
            return []

        visited.add(decision_id)

        # Find decisions with this ID in their dependencies
        all_decisions, _ = self.qdrant.scroll(
            collection_name="implementation_decisions",
            limit=10000,
            with_payload=True
        )

        dependents = []
        for point in all_decisions:
            dependencies = point.payload.get("dependencies", [])
            if decision_id in dependencies:
                dependent_info = {
                    "decision_id": point.payload.get("decision_id", ""),
                    "decision": point.payload.get("decision", ""),
                    "impact_areas": point.payload.get("impact_areas", []),
                    "wave": point.payload.get("wave")
                }
                dependents.append(dependent_info)

                # Recursively find transitive dependencies
                transitive = self._find_dependent_decisions(
                    dependent_info["decision_id"],
                    depth - 1,
                    visited
                )
                dependents.extend(transitive)

        return dependents

    def _calculate_risk_level(
        self,
        decision: Dict[str, Any],
        dependent_decisions: List[Dict[str, Any]]
    ) -> str:
        """Calculate risk level based on decision characteristics"""
        risk_score = 0

        # More dependents = higher risk
        if len(dependent_decisions) > 5:
            risk_score += 2
        elif len(dependent_decisions) > 2:
            risk_score += 1

        # Architectural decisions = higher risk
        if decision.get("decision_type") == "architectural":
            risk_score += 2

        # Multiple impact areas = higher risk
        if len(decision.get("impact_areas", [])) > 3:
            risk_score += 1

        # Map score to level
        if risk_score >= 4:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"

    def detect_inconsistencies(
        self,
        similarity_threshold: float = 0.85
    ) -> List[Dict[str, Any]]:
        """
        Detect potentially inconsistent decisions

        Args:
            similarity_threshold: How similar decisions need to be to check

        Returns:
            Potential inconsistencies
        """
        try:
            # Get all decisions
            decisions, _ = self.qdrant.scroll(
                collection_name="implementation_decisions",
                limit=10000,
                with_payload=True,
                with_vectors=True
            )

            inconsistencies = []

            # Compare all pairs of decisions
            for i, decision1 in enumerate(decisions):
                for decision2 in decisions[i+1:]:
                    # Calculate similarity
                    similarity = self._cosine_similarity(
                        decision1.vector,
                        decision2.vector
                    )

                    # High similarity but different decisions = potential inconsistency
                    if similarity >= similarity_threshold:
                        # Check if decisions are actually different
                        if decision1.payload.get("decision") != decision2.payload.get("decision"):
                            inconsistencies.append({
                                "similarity": similarity,
                                "decision_1": {
                                    "id": decision1.payload.get("decision_id"),
                                    "decision": decision1.payload.get("decision", ""),
                                    "wave": decision1.payload.get("wave"),
                                    "type": decision1.payload.get("decision_type", "")
                                },
                                "decision_2": {
                                    "id": decision2.payload.get("decision_id"),
                                    "decision": decision2.payload.get("decision", ""),
                                    "wave": decision2.payload.get("wave"),
                                    "type": decision2.payload.get("decision_type", "")
                                },
                                "warning": "Similar context but different decisions"
                            })

            logger.info("inconsistencies_detected", count=len(inconsistencies))

            return inconsistencies

        except Exception as e:
            logger.error("inconsistency_detection_failed", error=str(e))
            return []

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        import numpy as np
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)

    def get_decision_timeline(
        self,
        wave: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get chronological decision timeline

        Args:
            wave: Optional wave filter

        Returns:
            Decisions in chronological order
        """
        try:
            # Get decisions
            if wave is not None:
                decisions = self.collection_mgr.get_points_by_filter(
                    collection_name="implementation_decisions",
                    filter_dict={"wave": wave},
                    limit=1000
                )
            else:
                decisions, _ = self.qdrant.scroll(
                    collection_name="implementation_decisions",
                    limit=1000,
                    with_payload=True
                )

            # Sort by timestamp
            timeline = []
            for point in decisions:
                payload = point.payload if hasattr(point, 'payload') else point
                timeline.append({
                    "decision_id": payload.get("decision_id", ""),
                    "decision": payload.get("decision", ""),
                    "decision_type": payload.get("decision_type", ""),
                    "wave": payload.get("wave"),
                    "made_by": payload.get("made_by", ""),
                    "timestamp": payload.get("timestamp", "")
                })

            # Sort by timestamp
            timeline.sort(key=lambda x: x["timestamp"])

            logger.info("decision_timeline_generated", decisions=len(timeline), wave=wave)

            return timeline

        except Exception as e:
            logger.error("timeline_generation_failed", error=str(e))
            return []

    def generate_decision_report(
        self,
        wave: Optional[int] = None,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate comprehensive decision report

        Args:
            wave: Optional wave filter
            output_path: Where to save report

        Returns:
            Report content
        """
        try:
            timeline = self.get_decision_timeline(wave=wave)
            inconsistencies = self.detect_inconsistencies()

            # Generate report
            report = f"""# Implementation Decision Report
Generated: {datetime.now().isoformat()}
Wave: {wave if wave is not None else 'All'}

## Summary
- **Total Decisions**: {len(timeline)}
- **Potential Inconsistencies**: {len(inconsistencies)}

## Decision Timeline
"""
            for i, decision in enumerate(timeline, 1):
                report += f"\n### {i}. {decision['decision']}\n"
                report += f"- **Type**: {decision['decision_type']}\n"
                report += f"- **Made By**: {decision['made_by']}\n"
                report += f"- **Wave**: {decision.get('wave', 'N/A')}\n"
                report += f"- **Timestamp**: {decision['timestamp']}\n"

            if inconsistencies:
                report += "\n## ⚠️ Potential Inconsistencies\n"
                for i, inc in enumerate(inconsistencies, 1):
                    report += f"\n### Inconsistency {i}\n"
                    report += f"- **Similarity**: {inc['similarity']:.2f}\n"
                    report += f"- **Decision 1**: {inc['decision_1']['decision']}\n"
                    report += f"- **Decision 2**: {inc['decision_2']['decision']}\n"
                    report += f"- **Warning**: {inc['warning']}\n"

            # Save if output path provided
            if output_path:
                output_path.write_text(report)
                logger.info("decision_report_saved", path=str(output_path))

            return report

        except Exception as e:
            logger.error("report_generation_failed", error=str(e))
            return f"Error generating report: {str(e)}"


# CLI Interface for Testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Qdrant Decision Agent")
    subparsers = parser.add_subparsers(dest="command")

    # Record command
    record_parser = subparsers.add_parser("record", help="Record a decision")
    record_parser.add_argument("decision", help="Decision made")
    record_parser.add_argument("--rationale", required=True, help="Why this decision")
    record_parser.add_argument("--type", default="implementation", help="Decision type")
    record_parser.add_argument("--wave", type=int, help="Wave number")
    record_parser.add_argument("--made-by", help="Who made the decision")

    # Find command
    find_parser = subparsers.add_parser("find", help="Find related decisions")
    find_parser.add_argument("query", help="Search query")
    find_parser.add_argument("--type", help="Filter by type")
    find_parser.add_argument("--wave", type=int, help="Filter by wave")

    # Impact command
    impact_parser = subparsers.add_parser("impact", help="Analyze decision impact")
    impact_parser.add_argument("decision_id", help="Decision ID")

    # Timeline command
    timeline_parser = subparsers.add_parser("timeline", help="Show decision timeline")
    timeline_parser.add_argument("--wave", type=int, help="Filter by wave")

    # Inconsistencies command
    subparsers.add_parser("inconsistencies", help="Detect inconsistencies")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate decision report")
    report_parser.add_argument("--wave", type=int, help="Filter by wave")
    report_parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    agent = QdrantDecisionAgent()

    if args.command == "record":
        decision_id = agent.record_decision(
            decision=args.decision,
            rationale=args.rationale,
            decision_type=args.type,
            wave=args.wave,
            made_by=args.made_by
        )
        print(f"✓ Decision recorded: {decision_id}")

    elif args.command == "find":
        results = agent.find_related_decisions(
            query=args.query,
            decision_type=args.type,
            wave_filter=args.wave
        )
        print(f"\n🔍 Query: {args.query}")
        print(f"📊 Results: {len(results)}\n")
        for i, dec in enumerate(results, 1):
            print(f"{i}. Score: {dec['score']:.3f} | Type: {dec['decision_type']}")
            print(f"   Decision: {dec['decision']}")
            print(f"   Rationale: {dec['rationale']}\n")

    elif args.command == "impact":
        analysis = agent.analyze_decision_impact(args.decision_id)
        print(f"\n📊 Impact Analysis: {args.decision_id}\n")
        print(f"Decision: {analysis.get('decision', 'N/A')}")
        print(f"Risk Level: {analysis.get('risk_level', 'N/A')}")
        print(f"Affected Decisions: {analysis.get('total_affected_decisions', 0)}")
        print(f"Direct Impacts: {analysis.get('direct_impacts', [])}")
        print(f"Indirect Impacts: {analysis.get('indirect_impacts', [])}")

    elif args.command == "timeline":
        timeline = agent.get_decision_timeline(wave=args.wave)
        print(f"\n📅 Decision Timeline\n")
        for i, dec in enumerate(timeline, 1):
            print(f"{i}. {dec['timestamp'][:10]} | {dec['decision_type']}")
            print(f"   {dec['decision']}\n")

    elif args.command == "inconsistencies":
        inconsistencies = agent.detect_inconsistencies()
        print(f"\n⚠️  Inconsistencies: {len(inconsistencies)}\n")
        for i, inc in enumerate(inconsistencies, 1):
            print(f"{i}. Similarity: {inc['similarity']:.2f}")
            print(f"   Decision 1: {inc['decision_1']['decision']}")
            print(f"   Decision 2: {inc['decision_2']['decision']}\n")

    elif args.command == "report":
        output_path = Path(args.output) if args.output else None
        report = agent.generate_decision_report(wave=args.wave, output_path=output_path)
        print(report)
