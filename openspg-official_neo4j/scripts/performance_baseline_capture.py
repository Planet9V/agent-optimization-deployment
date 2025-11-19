#!/usr/bin/env python3
"""
Performance Baseline Capture Script
Benchmarks Neo4j query performance before schema enhancement

Purpose: Establish baseline performance metrics for post-wave comparison
Ensures: Performance regression detection across all 12 waves
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
from neo4j import GraphDatabase
import structlog
import statistics

logger = structlog.get_logger()

class PerformanceBaselineCapture:
    """
    Captures comprehensive performance baseline for Neo4j queries

    Benchmark Categories:
    - Node Lookups (by ID, by property)
    - Relationship Traversals (1-hop, 2-hop, multi-hop)
    - Aggregations (count, group by)
    - Pattern Matching (simple, complex)
    - Full-text Search (if enabled)
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = None
    ):
        """Initialize Neo4j connection"""
        self.neo4j_password = neo4j_password or os.getenv("NEO4J_PASSWORD", "neo4j@openspg")
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, self.neo4j_password)
        )

        logger.info("performance_baseline_initialized", uri=neo4j_uri)

    def _benchmark_query(
        self,
        query: str,
        params: Dict[str, Any] = None,
        iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Run query multiple times and collect performance metrics

        Returns:
            Performance statistics (mean, median, min, max, std_dev)
        """
        execution_times = []

        with self.driver.session() as session:
            # Warm-up run
            session.run(query, params or {}).consume()

            # Actual benchmark runs
            for _ in range(iterations):
                start_time = time.time()
                result = session.run(query, params or {})
                result.consume()  # Ensure all results are fetched
                execution_time = (time.time() - start_time) * 1000  # Convert to ms

                execution_times.append(execution_time)

        metrics = {
            "mean_ms": statistics.mean(execution_times),
            "median_ms": statistics.median(execution_times),
            "min_ms": min(execution_times),
            "max_ms": max(execution_times),
            "std_dev_ms": statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            "iterations": iterations,
            "raw_times": execution_times
        }

        return metrics

    def benchmark_node_lookups(self) -> Dict[str, Any]:
        """Benchmark node lookup operations"""
        logger.info("benchmarking_node_lookups")

        benchmarks = {}

        # CVE by ID lookup
        benchmarks["cve_by_id"] = self._benchmark_query(
            "MATCH (c:CVE {cve_id: $cve_id}) RETURN c",
            {"cve_id": "CVE-2016-1846"}
        )

        # CVE by year lookup
        benchmarks["cve_by_year"] = self._benchmark_query(
            "MATCH (c:CVE) WHERE c.year = $year RETURN count(c) as count",
            {"year": 2024}
        )

        # CVE by severity range
        benchmarks["cve_by_severity_range"] = self._benchmark_query(
            "MATCH (c:CVE) WHERE c.cvss_score >= $min_score AND c.cvss_score <= $max_score RETURN count(c) as count",
            {"min_score": 7.0, "max_score": 10.0}
        )

        # All CVE count
        benchmarks["all_cve_count"] = self._benchmark_query(
            "MATCH (c:CVE) RETURN count(c) as count"
        )

        logger.info("node_lookups_completed", benchmarks=len(benchmarks))
        return benchmarks

    def benchmark_relationship_traversals(self) -> Dict[str, Any]:
        """Benchmark relationship traversal operations"""
        logger.info("benchmarking_relationship_traversals")

        benchmarks = {}

        # 1-hop traversal
        benchmarks["one_hop_from_cve"] = self._benchmark_query(
            """
            MATCH (c:CVE)-[r]->(target)
            WHERE c.cve_id = $cve_id
            RETURN type(r) as relationship_type, count(target) as count
            """,
            {"cve_id": "CVE-2016-1846"}
        )

        # 2-hop traversal
        benchmarks["two_hop_from_cve"] = self._benchmark_query(
            """
            MATCH path = (c:CVE)-[r1]->(intermediate)-[r2]->(target)
            WHERE c.cve_id = $cve_id
            RETURN length(path) as path_length, count(target) as count
            LIMIT 100
            """,
            {"cve_id": "CVE-2016-1846"}
        )

        # Variable length path (1-3 hops)
        benchmarks["variable_path_traversal"] = self._benchmark_query(
            """
            MATCH path = (c:CVE)-[*1..3]->(target)
            WHERE c.cve_id = $cve_id
            RETURN length(path) as path_length, count(path) as count
            LIMIT 100
            """,
            {"cve_id": "CVE-2016-1846"}
        )

        logger.info("relationship_traversals_completed", benchmarks=len(benchmarks))
        return benchmarks

    def benchmark_aggregations(self) -> Dict[str, Any]:
        """Benchmark aggregation operations"""
        logger.info("benchmarking_aggregations")

        benchmarks = {}

        # Count by year
        benchmarks["cve_count_by_year"] = self._benchmark_query(
            """
            MATCH (c:CVE)
            RETURN c.year as year, count(c) as count
            ORDER BY c.year DESC
            LIMIT 10
            """
        )

        # Average CVSS score by year
        benchmarks["avg_cvss_by_year"] = self._benchmark_query(
            """
            MATCH (c:CVE)
            WHERE c.cvss_score IS NOT NULL
            RETURN c.year as year, avg(c.cvss_score) as avg_score
            ORDER BY c.year DESC
            LIMIT 10
            """
        )

        # Severity distribution
        benchmarks["severity_distribution"] = self._benchmark_query(
            """
            MATCH (c:CVE)
            RETURN c.severity as severity, count(c) as count
            """
        )

        # Relationship type counts
        benchmarks["relationship_type_counts"] = self._benchmark_query(
            """
            MATCH (c:CVE)-[r]->()
            RETURN type(r) as relationship_type, count(r) as count
            """
        )

        logger.info("aggregations_completed", benchmarks=len(benchmarks))
        return benchmarks

    def benchmark_pattern_matching(self) -> Dict[str, Any]:
        """Benchmark pattern matching operations"""
        logger.info("benchmarking_pattern_matching")

        benchmarks = {}

        # Simple pattern: CVEs with specific pattern
        benchmarks["simple_pattern"] = self._benchmark_query(
            """
            MATCH (c:CVE)
            WHERE c.cvss_score > 9.0
            RETURN count(c) as count
            """
        )

        # Complex pattern: CVEs with relationships and filtering
        benchmarks["complex_pattern"] = self._benchmark_query(
            """
            MATCH (c:CVE)-[r]->(target)
            WHERE c.year = 2024 AND c.cvss_score >= 7.0
            RETURN c.cve_id, type(r), count(target) as target_count
            LIMIT 100
            """
        )

        # Optional pattern matching
        benchmarks["optional_pattern"] = self._benchmark_query(
            """
            MATCH (c:CVE)
            WHERE c.year = 2024
            OPTIONAL MATCH (c)-[r]->(target)
            RETURN c.cve_id, count(r) as relationship_count
            LIMIT 100
            """
        )

        logger.info("pattern_matching_completed", benchmarks=len(benchmarks))
        return benchmarks

    def benchmark_property_searches(self) -> Dict[str, Any]:
        """Benchmark property-based search operations"""
        logger.info("benchmarking_property_searches")

        benchmarks = {}

        # String contains search
        benchmarks["description_contains"] = self._benchmark_query(
            """
            MATCH (c:CVE)
            WHERE c.description CONTAINS 'buffer overflow'
            RETURN count(c) as count
            LIMIT 100
            """
        )

        # Regex search (if supported)
        benchmarks["description_regex"] = self._benchmark_query(
            """
            MATCH (c:CVE)
            WHERE c.description =~ '.*remote.*code.*execution.*'
            RETURN count(c) as count
            LIMIT 100
            """
        )

        # Multi-property search
        benchmarks["multi_property_search"] = self._benchmark_query(
            """
            MATCH (c:CVE)
            WHERE c.year IN [2023, 2024]
              AND c.cvss_score >= 8.0
              AND c.severity IN ['HIGH', 'CRITICAL']
            RETURN count(c) as count
            """
        )

        logger.info("property_searches_completed", benchmarks=len(benchmarks))
        return benchmarks

    def capture_baseline(self, output_path: str = None) -> Dict[str, Any]:
        """
        Capture comprehensive performance baseline

        Returns:
            Complete baseline with all benchmark categories
        """
        if output_path is None:
            output_path = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/1_Comprehensive_Schema_Enhancement_Plan_v2/PERFORMANCE_BASELINE_WAVE0.json"

        logger.info("performance_baseline_capture_started")

        # Run all benchmark categories
        node_lookups = self.benchmark_node_lookups()
        relationship_traversals = self.benchmark_relationship_traversals()
        aggregations = self.benchmark_aggregations()
        pattern_matching = self.benchmark_pattern_matching()
        property_searches = self.benchmark_property_searches()

        # Calculate overall statistics
        all_benchmarks = []
        for category in [node_lookups, relationship_traversals, aggregations, pattern_matching, property_searches]:
            for benchmark in category.values():
                all_benchmarks.append(benchmark["mean_ms"])

        overall_stats = {
            "total_benchmarks": len(all_benchmarks),
            "overall_mean_ms": statistics.mean(all_benchmarks),
            "overall_median_ms": statistics.median(all_benchmarks),
            "overall_min_ms": min(all_benchmarks),
            "overall_max_ms": max(all_benchmarks)
        }

        # Build baseline
        baseline = {
            "metadata": {
                "captured_at": datetime.now().isoformat(),
                "wave": 0,
                "purpose": "Pre-enhancement performance baseline for regression detection",
                "neo4j_version": "5.26-community"
            },
            "benchmarks": {
                "node_lookups": node_lookups,
                "relationship_traversals": relationship_traversals,
                "aggregations": aggregations,
                "pattern_matching": pattern_matching,
                "property_searches": property_searches
            },
            "overall_statistics": overall_stats,
            "performance_targets": {
                "node_lookup_max_ms": 100,
                "relationship_traversal_max_ms": 500,
                "aggregation_max_ms": 1000,
                "pattern_matching_max_ms": 500,
                "property_search_max_ms": 1000
            }
        }

        # Export baseline
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(baseline, f, indent=2)

        logger.info(
            "performance_baseline_capture_completed",
            total_benchmarks=overall_stats["total_benchmarks"],
            overall_mean_ms=overall_stats["overall_mean_ms"],
            output=output_path
        )

        return baseline

    def compare_against_baseline(self, baseline_path: str) -> Dict[str, Any]:
        """
        Compare current performance against baseline

        Returns:
            Comparison report with regression analysis
        """
        # Load baseline
        with open(baseline_path, 'r') as f:
            baseline = json.load(f)

        # Capture current performance
        current_node_lookups = self.benchmark_node_lookups()
        current_relationship_traversals = self.benchmark_relationship_traversals()
        current_aggregations = self.benchmark_aggregations()
        current_pattern_matching = self.benchmark_pattern_matching()
        current_property_searches = self.benchmark_property_searches()

        current_benchmarks = {
            "node_lookups": current_node_lookups,
            "relationship_traversals": current_relationship_traversals,
            "aggregations": current_aggregations,
            "pattern_matching": current_pattern_matching,
            "property_searches": current_property_searches
        }

        # Compare each category
        comparison = {
            "compared_at": datetime.now().isoformat(),
            "baseline_captured_at": baseline["metadata"]["captured_at"],
            "categories": {},
            "regressions": [],
            "improvements": []
        }

        for category, benchmarks in current_benchmarks.items():
            category_comparison = {}

            for name, current_metrics in benchmarks.items():
                baseline_metrics = baseline["benchmarks"][category].get(name, {})

                if baseline_metrics:
                    baseline_mean = baseline_metrics["mean_ms"]
                    current_mean = current_metrics["mean_ms"]
                    delta_ms = current_mean - baseline_mean
                    delta_percent = (delta_ms / baseline_mean) * 100 if baseline_mean > 0 else 0

                    category_comparison[name] = {
                        "baseline_mean_ms": baseline_mean,
                        "current_mean_ms": current_mean,
                        "delta_ms": delta_ms,
                        "delta_percent": delta_percent,
                        "regression": delta_percent > 20  # >20% slower is regression
                    }

                    if delta_percent > 20:
                        comparison["regressions"].append({
                            "category": category,
                            "benchmark": name,
                            "delta_percent": delta_percent
                        })
                    elif delta_percent < -10:  # >10% faster is improvement
                        comparison["improvements"].append({
                            "category": category,
                            "benchmark": name,
                            "delta_percent": delta_percent
                        })

            comparison["categories"][category] = category_comparison

        comparison["summary"] = {
            "total_regressions": len(comparison["regressions"]),
            "total_improvements": len(comparison["improvements"]),
            "performance_status": "PASS" if len(comparison["regressions"]) == 0 else "FAIL"
        }

        logger.info(
            "performance_comparison_completed",
            regressions=len(comparison["regressions"]),
            improvements=len(comparison["improvements"]),
            status=comparison["summary"]["performance_status"]
        )

        return comparison

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()
        logger.info("neo4j_connection_closed")


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Performance Baseline Capture Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Capture command
    capture_parser = subparsers.add_parser("capture", help="Capture performance baseline")
    capture_parser.add_argument("--output", default=None, help="Output path for baseline JSON")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare against baseline")
    compare_parser.add_argument(
        "--baseline",
        default="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/1_Comprehensive_Schema_Enhancement_Plan_v2/PERFORMANCE_BASELINE_WAVE0.json",
        help="Path to baseline JSON"
    )
    compare_parser.add_argument("--output", default=None, help="Output path for comparison report")

    args = parser.parse_args()

    capturer = PerformanceBaselineCapture()

    try:
        if args.command == "capture":
            baseline = capturer.capture_baseline(output_path=args.output)

            print("\n✅ Performance Baseline Captured Successfully")
            print(f"📊 Total Benchmarks: {baseline['overall_statistics']['total_benchmarks']}")
            print(f"⏱️  Overall Mean: {baseline['overall_statistics']['overall_mean_ms']:.2f} ms")
            print(f"⚡ Fastest Query: {baseline['overall_statistics']['overall_min_ms']:.2f} ms")
            print(f"🐌 Slowest Query: {baseline['overall_statistics']['overall_max_ms']:.2f} ms")

        elif args.command == "compare":
            comparison = capturer.compare_against_baseline(args.baseline)

            print("\n🔍 Performance Comparison Report")
            print(f"📈 Improvements: {comparison['summary']['total_improvements']}")
            print(f"📉 Regressions: {comparison['summary']['total_regressions']}")
            print(f"🎯 Status: {comparison['summary']['performance_status']}")

            if comparison['regressions']:
                print("\n⚠️  Performance Regressions Detected:")
                for regression in comparison['regressions']:
                    print(f"  - {regression['category']}/{regression['benchmark']}: +{regression['delta_percent']:.1f}%")

            if comparison['improvements']:
                print("\n✅ Performance Improvements:")
                for improvement in comparison['improvements']:
                    print(f"  - {improvement['category']}/{improvement['benchmark']}: {improvement['delta_percent']:.1f}%")

            # Export comparison if output path provided
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(comparison, f, indent=2)
                print(f"\n📄 Comparison report saved to: {args.output}")

    finally:
        capturer.close()
