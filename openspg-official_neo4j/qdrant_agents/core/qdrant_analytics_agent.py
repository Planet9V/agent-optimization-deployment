#!/usr/bin/env python3
"""
Qdrant Analytics Agent - Performance Monitoring and Optimization
Tracks usage, costs, performance metrics, and provides optimization recommendations
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import json
import structlog

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.collection_manager import CollectionManager
from utils.query_optimizer import QueryOptimizer
from utils.cost_tracker import CostTracker

logger = structlog.get_logger()

class QdrantAnalyticsAgent:
    """
    Specialized agent for performance monitoring and analytics

    Capabilities:
    - Performance monitoring across all collections
    - Cost tracking and budget alerts
    - Usage analytics and patterns
    - Optimization recommendations
    - Report generation
    """

    def __init__(
        self,
        url: str = "http://localhost:6333",
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        report_frequency: str = "daily",
        metrics_retention_days: int = 90
    ):
        """Initialize analytics agent"""
        self.url = url
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.report_frequency = report_frequency
        self.metrics_retention_days = metrics_retention_days

        # Initialize components
        self.collection_mgr = CollectionManager(url=self.url, api_key=self.api_key)
        self.query_optimizer = QueryOptimizer()
        self.cost_tracker = CostTracker(
            daily_budget=10.0,   # $10/day default
            monthly_budget=100.0  # $100/month default
        )

        # Metrics storage
        self.metrics_path = Path(
            "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup/analytics"
        )
        self.metrics_path.mkdir(parents=True, exist_ok=True)

        logger.info(
            "qdrant_analytics_agent_initialized",
            report_frequency=self.report_frequency
        )

    def collect_system_metrics(self) -> Dict[str, Any]:
        """
        Collect comprehensive system metrics

        Returns:
            Complete metrics snapshot
        """
        try:
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "collections": {},
                "performance": {},
                "costs": {},
                "usage": {}
            }

            # Collection metrics
            collections = self.collection_mgr.list_collections()
            for collection in collections:
                collection_name = collection["name"]
                stats = self.collection_mgr.get_collection_stats(collection_name)
                health = self.collection_mgr.health_check(collection_name)

                metrics["collections"][collection_name] = {
                    "vectors_count": stats.get("vectors_count", 0),
                    "segments_count": stats.get("segments_count", 0),
                    "status": stats.get("status", "unknown"),
                    "healthy": health.get("healthy", False)
                }

            # Performance metrics
            perf_stats = self.query_optimizer.get_performance_stats()
            metrics["performance"] = {
                "total_queries": perf_stats.get("total_queries", 0),
                "avg_duration_ms": perf_stats.get("avg_duration_ms", 0),
                "cache_hit_rate": perf_stats.get("cache_hit_rate", 0)
            }

            # Cost metrics
            cost_summary = self.cost_tracker.get_cost_summary()
            metrics["costs"] = {
                "today": cost_summary["today"]["cost_usd"],
                "this_month": cost_summary["this_month"]["cost_usd"],
                "total": cost_summary["total"]["cost_usd"]
            }

            # Usage patterns
            metrics["usage"] = self._analyze_usage_patterns()

            # Store metrics
            self._store_metrics(metrics)

            logger.info(
                "system_metrics_collected",
                collections=len(collections),
                queries=perf_stats.get("total_queries", 0)
            )

            return metrics

        except Exception as e:
            logger.error("metrics_collection_failed", error=str(e))
            return {}

    def _analyze_usage_patterns(self) -> Dict[str, Any]:
        """Analyze usage patterns across the system"""
        try:
            # Get query patterns
            pattern_analysis = self.query_optimizer.analyze_query_patterns()

            usage = {
                "most_queried_collections": [],
                "peak_usage_times": [],
                "common_query_types": []
            }

            # Analyze collections by query frequency
            collections = pattern_analysis.get("collections", {})
            if collections:
                sorted_collections = sorted(
                    collections.items(),
                    key=lambda x: x[1].get("total_queries", 0),
                    reverse=True
                )
                usage["most_queried_collections"] = [
                    {"name": name, "queries": stats.get("total_queries", 0)}
                    for name, stats in sorted_collections[:5]
                ]

            return usage

        except Exception as e:
            logger.error("usage_analysis_failed", error=str(e))
            return {}

    def _store_metrics(self, metrics: Dict[str, Any]):
        """Store metrics for historical analysis"""
        try:
            # Daily metrics file
            date_str = datetime.now().strftime("%Y-%m-%d")
            metrics_file = self.metrics_path / f"metrics_{date_str}.json"

            # Load existing if present
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    daily_metrics = json.load(f)
            else:
                daily_metrics = {"date": date_str, "snapshots": []}

            # Append snapshot
            daily_metrics["snapshots"].append(metrics)

            # Save
            with open(metrics_file, 'w') as f:
                json.dump(daily_metrics, f, indent=2)

            # Cleanup old metrics
            self._cleanup_old_metrics()

        except Exception as e:
            logger.error("metrics_storage_failed", error=str(e))

    def _cleanup_old_metrics(self):
        """Remove metrics older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.metrics_retention_days)

            for metrics_file in self.metrics_path.glob("metrics_*.json"):
                try:
                    # Extract date from filename
                    date_str = metrics_file.stem.replace("metrics_", "")
                    file_date = datetime.strptime(date_str, "%Y-%m-%d")

                    if file_date < cutoff_date:
                        metrics_file.unlink()
                        logger.debug("old_metrics_deleted", file=metrics_file.name)

                except Exception as e:
                    logger.warning("metrics_cleanup_failed", file=metrics_file.name, error=str(e))

        except Exception as e:
            logger.error("metrics_cleanup_error", error=str(e))

    def generate_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate recommendations for optimization

        Returns:
            List of recommendations with priority
        """
        try:
            recommendations = []

            # Analyze query performance
            perf_stats = self.query_optimizer.get_performance_stats()

            # Slow queries
            if perf_stats.get("avg_duration_ms", 0) > 1000:
                recommendations.append({
                    "priority": "high",
                    "category": "performance",
                    "issue": "Slow average query time",
                    "current_value": f"{perf_stats['avg_duration_ms']:.0f}ms",
                    "recommendation": "Consider reducing top_k or increasing score_threshold to limit result set size",
                    "estimated_impact": "30-50% query time reduction"
                })

            # Low cache hit rate
            cache_hit_rate = perf_stats.get("cache_hit_rate", 0)
            if cache_hit_rate < 0.3:
                recommendations.append({
                    "priority": "medium",
                    "category": "performance",
                    "issue": "Low cache hit rate",
                    "current_value": f"{cache_hit_rate:.1%}",
                    "recommendation": "Increase cache TTL or review query patterns for more reuse opportunities",
                    "estimated_impact": "20-40% latency reduction for repeated queries"
                })

            # Cost analysis
            cost_summary = self.cost_tracker.get_cost_summary()
            if cost_summary["warnings"]:
                recommendations.append({
                    "priority": "high",
                    "category": "cost",
                    "issue": "Budget exceeded",
                    "current_value": f"${cost_summary['this_month']['cost_usd']:.2f}",
                    "recommendation": "Enable aggressive caching or reduce embedding generation frequency",
                    "estimated_impact": f"${cost_summary['this_month']['cost_usd'] * 0.3:.2f} monthly savings"
                })

            # Collection health
            collections = self.collection_mgr.list_collections()
            for collection in collections:
                health = self.collection_mgr.health_check(collection["name"])

                if not health.get("healthy"):
                    recommendations.append({
                        "priority": "high",
                        "category": "reliability",
                        "issue": f"Unhealthy collection: {collection['name']}",
                        "current_value": f"Status: {health.get('stats', {}).get('status', 'unknown')}",
                        "recommendation": health.get("recommendations", ["Check collection configuration"])[0],
                        "estimated_impact": "Improved query reliability"
                    })

            # High segment count
            for collection in collections:
                stats = self.collection_mgr.get_collection_stats(collection["name"])
                if stats.get("segments_count", 0) > 10:
                    recommendations.append({
                        "priority": "low",
                        "category": "maintenance",
                        "issue": f"High segment count in {collection['name']}",
                        "current_value": f"{stats['segments_count']} segments",
                        "recommendation": "Run collection optimization to compact segments",
                        "estimated_impact": "10-20% query performance improvement"
                    })

            # Sort by priority
            priority_order = {"high": 0, "medium": 1, "low": 2}
            recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))

            logger.info(
                "optimization_recommendations_generated",
                total=len(recommendations),
                high_priority=sum(1 for r in recommendations if r["priority"] == "high")
            )

            return recommendations

        except Exception as e:
            logger.error("recommendation_generation_failed", error=str(e))
            return []

    def generate_daily_report(self) -> str:
        """
        Generate comprehensive daily report

        Returns:
            Report content
        """
        try:
            metrics = self.collect_system_metrics()
            recommendations = self.generate_optimization_recommendations()

            report = f"""# Qdrant System Analytics Report
**Generated**: {datetime.now().isoformat()}
**Period**: Daily

## System Health

### Collections
"""
            for name, stats in metrics.get("collections", {}).items():
                status_icon = "✓" if stats["healthy"] else "⚠️"
                report += f"\n- {status_icon} **{name}**: {stats['vectors_count']:,} vectors, {stats['segments_count']} segments"

            report += f"""

### Performance
- **Total Queries**: {metrics['performance']['total_queries']:,}
- **Average Duration**: {metrics['performance']['avg_duration_ms']:.0f}ms
- **Cache Hit Rate**: {metrics['performance']['cache_hit_rate']:.1%}

### Costs
- **Today**: ${metrics['costs']['today']:.2f}
- **This Month**: ${metrics['costs']['this_month']:.2f}
- **Total**: ${metrics['costs']['total']:.2f}

### Usage Patterns
"""
            usage = metrics.get("usage", {})
            most_queried = usage.get("most_queried_collections", [])
            if most_queried:
                report += "\n**Most Queried Collections**:\n"
                for coll in most_queried[:5]:
                    report += f"- {coll['name']}: {coll['queries']} queries\n"

            # Add recommendations
            if recommendations:
                report += "\n## 🎯 Optimization Recommendations\n"

                high_priority = [r for r in recommendations if r["priority"] == "high"]
                if high_priority:
                    report += "\n### ⚠️ High Priority\n"
                    for rec in high_priority:
                        report += f"\n**{rec['issue']}**\n"
                        report += f"- Current: {rec['current_value']}\n"
                        report += f"- Action: {rec['recommendation']}\n"
                        report += f"- Impact: {rec['estimated_impact']}\n"

                medium_priority = [r for r in recommendations if r["priority"] == "medium"]
                if medium_priority:
                    report += "\n### 🔧 Medium Priority\n"
                    for rec in medium_priority:
                        report += f"\n**{rec['issue']}**\n"
                        report += f"- Current: {rec['current_value']}\n"
                        report += f"- Action: {rec['recommendation']}\n"

            # Save report
            report_file = self.metrics_path / f"report_{datetime.now().strftime('%Y-%m-%d')}.md"
            report_file.write_text(report)

            logger.info("daily_report_generated", path=str(report_file))

            return report

        except Exception as e:
            logger.error("report_generation_failed", error=str(e))
            return f"Error generating report: {str(e)}"

    def get_historical_trends(
        self,
        days: int = 7,
        metric: str = "queries"
    ) -> Dict[str, Any]:
        """
        Get historical trends for a metric

        Args:
            days: Number of days to analyze
            metric: "queries", "cost", "vectors", or "cache_hit_rate"

        Returns:
            Trend data
        """
        try:
            trends = {
                "metric": metric,
                "period_days": days,
                "data_points": []
            }

            for i in range(days):
                date = datetime.now() - timedelta(days=i)
                date_str = date.strftime("%Y-%m-%d")
                metrics_file = self.metrics_path / f"metrics_{date_str}.json"

                if not metrics_file.exists():
                    continue

                with open(metrics_file, 'r') as f:
                    daily_metrics = json.load(f)

                # Get last snapshot of the day
                if daily_metrics.get("snapshots"):
                    snapshot = daily_metrics["snapshots"][-1]

                    # Extract metric
                    if metric == "queries":
                        value = snapshot.get("performance", {}).get("total_queries", 0)
                    elif metric == "cost":
                        value = snapshot.get("costs", {}).get("today", 0)
                    elif metric == "cache_hit_rate":
                        value = snapshot.get("performance", {}).get("cache_hit_rate", 0)
                    elif metric == "vectors":
                        total_vectors = sum(
                            c.get("vectors_count", 0)
                            for c in snapshot.get("collections", {}).values()
                        )
                        value = total_vectors
                    else:
                        value = 0

                    trends["data_points"].append({
                        "date": date_str,
                        "value": value
                    })

            # Sort chronologically
            trends["data_points"].sort(key=lambda x: x["date"])

            # Calculate trend direction
            if len(trends["data_points"]) >= 2:
                first = trends["data_points"][0]["value"]
                last = trends["data_points"][-1]["value"]
                change = ((last - first) / first * 100) if first > 0 else 0
                trends["trend"] = "increasing" if change > 5 else ("decreasing" if change < -5 else "stable")
                trends["change_percent"] = change
            else:
                trends["trend"] = "unknown"

            logger.info("historical_trends_analyzed", metric=metric, days=days)

            return trends

        except Exception as e:
            logger.error("trend_analysis_failed", error=str(e))
            return {}


# CLI Interface for Testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Qdrant Analytics Agent")
    subparsers = parser.add_subparsers(dest="command")

    # Metrics command
    subparsers.add_parser("metrics", help="Collect current metrics")

    # Recommendations command
    subparsers.add_parser("recommend", help="Generate optimization recommendations")

    # Report command
    subparsers.add_parser("report", help="Generate daily report")

    # Trends command
    trends_parser = subparsers.add_parser("trends", help="Show historical trends")
    trends_parser.add_argument("--metric", choices=["queries", "cost", "vectors", "cache_hit_rate"],
                              default="queries", help="Metric to analyze")
    trends_parser.add_argument("--days", type=int, default=7, help="Number of days")

    args = parser.parse_args()

    agent = QdrantAnalyticsAgent()

    if args.command == "metrics":
        metrics = agent.collect_system_metrics()
        print("\n📊 System Metrics\n")
        print(f"Timestamp: {metrics['timestamp']}")
        print(f"\nCollections:")
        for name, stats in metrics['collections'].items():
            print(f"  {name}: {stats['vectors_count']:,} vectors, {stats['status']}")
        print(f"\nPerformance:")
        print(f"  Queries: {metrics['performance']['total_queries']}")
        print(f"  Avg Duration: {metrics['performance']['avg_duration_ms']:.0f}ms")
        print(f"  Cache Hit Rate: {metrics['performance']['cache_hit_rate']:.1%}")
        print(f"\nCosts:")
        print(f"  Today: ${metrics['costs']['today']:.2f}")
        print(f"  This Month: ${metrics['costs']['this_month']:.2f}")

    elif args.command == "recommend":
        recommendations = agent.generate_optimization_recommendations()
        print(f"\n🎯 Optimization Recommendations: {len(recommendations)}\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. [{rec['priority'].upper()}] {rec['category']}")
            print(f"   Issue: {rec['issue']}")
            print(f"   Current: {rec['current_value']}")
            print(f"   Action: {rec['recommendation']}")
            print(f"   Impact: {rec['estimated_impact']}\n")

    elif args.command == "report":
        report = agent.generate_daily_report()
        print(report)

    elif args.command == "trends":
        trends = agent.get_historical_trends(
            days=args.days,
            metric=args.metric
        )
        print(f"\n📈 Historical Trends: {args.metric}\n")
        print(f"Period: {trends['period_days']} days")
        print(f"Trend: {trends.get('trend', 'unknown')}")
        if "change_percent" in trends:
            print(f"Change: {trends['change_percent']:+.1f}%")
        print(f"\nData Points:")
        for point in trends['data_points']:
            print(f"  {point['date']}: {point['value']}")
