#!/usr/bin/env python3
"""
Performance Benchmarker - Benchmark query performance and track regressions
"""

import json
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
from neo4j import GraphDatabase
import statistics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Result from a single benchmark execution"""
    query_name: str
    execution_time_ms: float
    db_hits: int
    rows_returned: int
    memory_kb: float
    query_plan: Dict
    timestamp: str


class PerformanceBenchmarker:
    """Benchmark query performance and detect regressions"""

    # Standard benchmark queries representing common use cases
    BENCHMARK_QUERIES = {
        "find_critical_vulns": {
            "description": "Find critical vulnerabilities affecting critical assets",
            "query": '''
            MATCH (v:Vulnerability)-[:AFFECTS]->(c:Component {criticality: 'critical'})
            WHERE v.cvss_score >= 9.0
            RETURN v.id, v.cvss_score, c.name
            ORDER BY v.cvss_score DESC
            LIMIT 100
            ''',
            "target_ms": 100
        },
        "attack_path_discovery": {
            "description": "Find attack paths from DMZ to critical assets",
            "query": '''
            MATCH path = (src:NetworkInterface {zone: 'dmz'})
                         -[:CONNECTS_TO*1..5]->(target:Component {criticality: 'critical'})
            WHERE ALL(r IN relationships(path) WHERE r.allowed = true)
            RETURN path, length(path) as hops
            ORDER BY hops ASC
            LIMIT 50
            ''',
            "target_ms": 500
        },
        "vulnerability_correlation": {
            "description": "Correlate vulnerabilities to assets via CPE",
            "query": '''
            MATCH (v:Vulnerability)-[:AFFECTS]->(cpe:CPE)
            MATCH (c:Component)-[:RUNS]->(s:Software)
            WHERE s.vendor = cpe.vendor AND s.product = cpe.product
            RETURN v.id, c.name, s.name, v.cvss_score
            LIMIT 200
            ''',
            "target_ms": 200
        },
        "transitive_dependencies": {
            "description": "Find transitive dependency vulnerabilities",
            "query": '''
            MATCH path = (c:Component {name: 'web-server-1'})
                         -[:DEPENDS_ON*1..3]->(dep:Component)
            MATCH (v:Vulnerability)-[:AFFECTS]->(dep)
            RETURN c.name, dep.name, v.id, length(path) as depth
            ORDER BY depth
            LIMIT 100
            ''',
            "target_ms": 300
        },
        "zone_crossing_analysis": {
            "description": "Analyze network zone crossings",
            "query": '''
            MATCH path = (src:NetworkInterface)-[:CONNECTS_TO*1..4]->(dst:NetworkInterface)
            WHERE src.zone <> dst.zone
            WITH path, [n IN nodes(path) | n.zone] as zones
            RETURN DISTINCT zones, length(path) as hops
            ORDER BY hops
            LIMIT 100
            ''',
            "target_ms": 250
        },
        "exploit_availability": {
            "description": "Find vulnerabilities with available exploits",
            "query": '''
            MATCH (v:Vulnerability)-[:HAS_EXPLOIT]->(e:Exploit)
            WHERE e.maturity IN ['weaponized', 'functional']
            MATCH (v)-[:AFFECTS]->(c:Component)
            RETURN v.id, v.cvss_score, e.maturity, count(c) as affected_assets
            ORDER BY v.cvss_score DESC, affected_assets DESC
            LIMIT 100
            ''',
            "target_ms": 150
        },
        "threat_intel_correlation": {
            "description": "Correlate threat intelligence with vulnerabilities",
            "query": '''
            MATCH (t:ThreatIntel)-[:MENTIONS]->(v:Vulnerability)
            WHERE datetime(t.timestamp) > datetime() - duration({days: 30})
            MATCH (v)-[:AFFECTS]->(c:Component)
            RETURN v.id, count(DISTINCT t) as mentions,
                   count(DISTINCT c) as affected_components,
                   max(v.cvss_score) as max_cvss
            ORDER BY mentions DESC
            LIMIT 50
            ''',
            "target_ms": 200
        }
    }

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.results: List[BenchmarkResult] = []
        self.baseline: Dict[str, float] = {}

    def close(self):
        self.driver.close()

    def run_benchmark(self, query_name: str = None, iterations: int = 5) -> Dict:
        """
        Run benchmark suite or specific query

        Args:
            query_name: Specific query to benchmark, or None for all
            iterations: Number of iterations per query
        """
        queries_to_run = {}

        if query_name:
            if query_name not in self.BENCHMARK_QUERIES:
                logger.error(f"Unknown query: {query_name}")
                return {}
            queries_to_run[query_name] = self.BENCHMARK_QUERIES[query_name]
        else:
            queries_to_run = self.BENCHMARK_QUERIES

        logger.info(f"Running {len(queries_to_run)} benchmark queries with {iterations} iterations each")

        results = {}

        for name, query_info in queries_to_run.items():
            logger.info(f"Benchmarking: {name}")

            times = []
            db_hits_list = []
            rows_list = []

            for i in range(iterations):
                result = self._execute_and_profile(name, query_info["query"])

                if result:
                    times.append(result.execution_time_ms)
                    db_hits_list.append(result.db_hits)
                    rows_list.append(result.rows_returned)
                    self.results.append(result)

            if times:
                stats = {
                    "description": query_info["description"],
                    "target_ms": query_info["target_ms"],
                    "iterations": len(times),
                    "avg_time_ms": statistics.mean(times),
                    "median_time_ms": statistics.median(times),
                    "min_time_ms": min(times),
                    "max_time_ms": max(times),
                    "std_dev_ms": statistics.stdev(times) if len(times) > 1 else 0,
                    "p95_ms": self._percentile(times, 95),
                    "p99_ms": self._percentile(times, 99),
                    "avg_db_hits": statistics.mean(db_hits_list),
                    "avg_rows": statistics.mean(rows_list),
                    "within_target": statistics.mean(times) <= query_info["target_ms"]
                }

                results[name] = stats

        return results

    def _execute_and_profile(self, query_name: str, query: str) -> BenchmarkResult:
        """Execute query with profiling"""
        with self.driver.session() as session:
            # Use PROFILE to get execution statistics
            profiled_query = f"PROFILE {query}"

            start_time = time.time()

            try:
                result = session.run(profiled_query)

                # Consume all results
                records = list(result)
                rows_returned = len(records)

                # Get profiling info
                profile = result.consume().profile

                end_time = time.time()
                execution_time_ms = (end_time - start_time) * 1000

                # Extract metrics from profile
                db_hits = profile.get("dbHits", 0) if profile else 0
                memory_kb = profile.get("memory", 0) / 1024 if profile else 0

                return BenchmarkResult(
                    query_name=query_name,
                    execution_time_ms=execution_time_ms,
                    db_hits=db_hits,
                    rows_returned=rows_returned,
                    memory_kb=memory_kb,
                    query_plan=self._extract_plan_summary(profile) if profile else {},
                    timestamp=datetime.now().isoformat()
                )

            except Exception as e:
                logger.error(f"Error executing {query_name}: {e}")
                return None

    def _extract_plan_summary(self, profile) -> Dict:
        """Extract summary from query execution plan"""
        if not profile:
            return {}

        return {
            "operator": profile.get("operatorType", "unknown"),
            "db_hits": profile.get("dbHits", 0),
            "rows": profile.get("rows", 0),
            "has_children": len(profile.get("children", [])) > 0
        }

    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile"""
        if not data:
            return 0.0

        sorted_data = sorted(data)
        index = int((percentile / 100.0) * len(sorted_data))
        index = min(index, len(sorted_data) - 1)

        return sorted_data[index]

    def check_indexes(self) -> Dict:
        """Check index effectiveness"""
        query = '''
        SHOW INDEXES
        '''

        with self.driver.session() as session:
            try:
                result = session.run(query)
                indexes = []

                for record in result:
                    indexes.append({
                        "name": record.get("name", "unknown"),
                        "type": record.get("type", "unknown"),
                        "entity_type": record.get("entityType", "unknown"),
                        "properties": record.get("properties", []),
                        "state": record.get("state", "unknown")
                    })

                return {
                    "total_indexes": len(indexes),
                    "indexes": indexes,
                    "recommendations": self._generate_index_recommendations(indexes)
                }

            except Exception as e:
                logger.error(f"Error checking indexes: {e}")
                return {"error": str(e)}

    def _generate_index_recommendations(self, indexes: List[Dict]) -> List[str]:
        """Generate index recommendations based on benchmarks"""
        recommendations = []

        # Check for common index needs
        indexed_props = set()
        for idx in indexes:
            indexed_props.update(idx.get("properties", []))

        # Recommended indexes for threat intel queries
        recommended = [
            ("Vulnerability", "id"),
            ("Vulnerability", "cvss_score"),
            ("Component", "name"),
            ("Component", "criticality"),
            ("NetworkInterface", "zone"),
            ("Software", "vendor"),
            ("Software", "product"),
            ("ThreatIntel", "timestamp")
        ]

        for label, prop in recommended:
            if prop not in indexed_props:
                recommendations.append(
                    f"CREATE INDEX FOR (n:{label}) ON (n.{prop})"
                )

        return recommendations

    def set_baseline(self, results: Dict):
        """Set performance baseline for regression detection"""
        for query_name, stats in results.items():
            self.baseline[query_name] = stats["avg_time_ms"]

        logger.info(f"Baseline set for {len(self.baseline)} queries")

    def detect_regressions(self, results: Dict, threshold: float = 1.2) -> List[Dict]:
        """
        Detect performance regressions

        Args:
            results: Current benchmark results
            threshold: Regression threshold (1.2 = 20% slower)
        """
        if not self.baseline:
            logger.warning("No baseline set, cannot detect regressions")
            return []

        regressions = []

        for query_name, stats in results.items():
            if query_name not in self.baseline:
                continue

            baseline_time = self.baseline[query_name]
            current_time = stats["avg_time_ms"]

            if current_time > baseline_time * threshold:
                regression_pct = ((current_time - baseline_time) / baseline_time) * 100

                regressions.append({
                    "query": query_name,
                    "baseline_ms": baseline_time,
                    "current_ms": current_time,
                    "regression_pct": regression_pct,
                    "severity": "critical" if regression_pct > 50 else "warning"
                })

        return regressions

    def generate_report(self, results: Dict, regressions: List[Dict] = None) -> Dict:
        """Generate comprehensive performance report"""
        # Calculate overall stats
        all_times = [stats["avg_time_ms"] for stats in results.values()]
        total_queries = len(results)
        within_target = sum(1 for stats in results.values() if stats["within_target"])

        report = {
            "summary": {
                "timestamp": datetime.now().isoformat(),
                "total_queries": total_queries,
                "within_target": within_target,
                "target_success_rate": (within_target / total_queries * 100) if total_queries else 0,
                "avg_execution_time_ms": statistics.mean(all_times) if all_times else 0,
                "max_execution_time_ms": max(all_times) if all_times else 0
            },
            "query_results": results,
            "slow_queries": [
                {"query": name, "avg_time_ms": stats["avg_time_ms"], "target_ms": stats["target_ms"]}
                for name, stats in results.items()
                if not stats["within_target"]
            ]
        }

        if regressions:
            report["regressions"] = regressions

        return report

    def export_results(self, report: Dict, output_file: str):
        """Export benchmark results"""
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Results exported to {output_file}")


def main():
    """Example usage"""
    benchmarker = PerformanceBenchmarker(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Check indexes first
        print("\n=== Index Analysis ===")
        index_report = benchmarker.check_indexes()
        print(f"Total Indexes: {index_report['total_indexes']}")

        if index_report.get('recommendations'):
            print("\nRecommended Indexes:")
            for rec in index_report['recommendations'][:5]:
                print(f"  {rec}")

        # Run benchmark suite
        print("\n=== Running Benchmarks ===")
        results = benchmarker.run_benchmark(iterations=5)

        # Set baseline
        benchmarker.set_baseline(results)

        # Generate report
        report = benchmarker.generate_report(results)

        print(f"\n=== Performance Report ===")
        print(f"Queries within target: {report['summary']['within_target']}/{report['summary']['total_queries']}")
        print(f"Success rate: {report['summary']['target_success_rate']:.1f}%")
        print(f"Average execution time: {report['summary']['avg_execution_time_ms']:.2f}ms")

        # Print slow queries
        if report['slow_queries']:
            print("\n=== Slow Queries ===")
            for query in report['slow_queries']:
                print(f"  {query['query']}: {query['avg_time_ms']:.2f}ms (target: {query['target_ms']}ms)")

        # Export
        benchmarker.export_results(report, "/tmp/performance_report.json")

    finally:
        benchmarker.close()


if __name__ == "__main__":
    main()
