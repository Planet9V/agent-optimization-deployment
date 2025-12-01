#!/usr/bin/env python3
"""
Graph Statistics - Collect and analyze graph statistics and metrics
"""

import json
from typing import Dict, List
from datetime import datetime
from collections import defaultdict
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphStatistics:
    """Collect comprehensive graph statistics"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def collect_all_statistics(self) -> Dict:
        """Collect all graph statistics"""
        logger.info("Collecting comprehensive graph statistics...")

        stats = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "database": self._get_database_info()
            },
            "node_counts": self.get_node_counts(),
            "relationship_counts": self.get_relationship_counts(),
            "growth_trends": self.get_growth_trends(),
            "density_metrics": self.calculate_density(),
            "hotspots": self.identify_hotspots(),
            "distribution": self.analyze_distribution()
        }

        return stats

    def _get_database_info(self) -> Dict:
        """Get database metadata"""
        with self.driver.session() as session:
            # Get database name
            try:
                result = session.run("CALL db.info()")
                db_info = result.single()
                return {
                    "name": db_info.get("name", "unknown"),
                    "version": db_info.get("version", "unknown")
                }
            except:
                return {"name": "neo4j", "version": "unknown"}

    def get_node_counts(self) -> Dict:
        """Get node counts by label"""
        query = '''
        CALL db.labels() YIELD label
        CALL {
            WITH label
            MATCH (n)
            WHERE label IN labels(n)
            RETURN count(*) as count
        }
        RETURN label, count
        ORDER BY count DESC
        '''

        with self.driver.session() as session:
            result = session.run(query)

            counts = {}
            total = 0

            for record in result:
                label = record["label"]
                count = record["count"]
                counts[label] = count
                total += count

            counts["_total"] = total

            logger.info(f"Collected node counts: {total} total nodes")
            return counts

    def get_relationship_counts(self) -> Dict:
        """Get relationship counts by type"""
        query = '''
        CALL db.relationshipTypes() YIELD relationshipType
        CALL {
            WITH relationshipType
            MATCH ()-[r]->()
            WHERE type(r) = relationshipType
            RETURN count(r) as count
        }
        RETURN relationshipType, count
        ORDER BY count DESC
        '''

        with self.driver.session() as session:
            result = session.run(query)

            counts = {}
            total = 0

            for record in result:
                rel_type = record["relationshipType"]
                count = record["count"]
                counts[rel_type] = count
                total += count

            counts["_total"] = total

            logger.info(f"Collected relationship counts: {total} total relationships")
            return counts

    def get_growth_trends(self, days: int = 30) -> Dict:
        """Analyze growth trends over time"""
        # This requires timestamps on nodes/relationships
        query = '''
        MATCH (n)
        WHERE n.created_at IS NOT NULL
        WITH datetime(n.created_at) as created, labels(n)[0] as label
        WHERE created > datetime() - duration({days: $days})
        WITH date(created) as date, label
        RETURN date, label, count(*) as count
        ORDER BY date DESC
        '''

        with self.driver.session() as session:
            result = session.run(query, days=days)

            trends = defaultdict(list)
            total_by_date = defaultdict(int)

            for record in result:
                date_str = str(record["date"])
                label = record["label"]
                count = record["count"]

                trends[label].append({
                    "date": date_str,
                    "count": count
                })

                total_by_date[date_str] += count

            # Calculate daily averages
            daily_totals = list(total_by_date.values())
            avg_daily_growth = sum(daily_totals) / len(daily_totals) if daily_totals else 0

            return {
                "by_label": dict(trends),
                "total_by_date": dict(total_by_date),
                "avg_daily_growth": round(avg_daily_growth, 2),
                "period_days": days
            }

    def calculate_density(self) -> Dict:
        """Calculate graph density metrics"""
        query = '''
        MATCH (n)
        WITH count(n) as node_count
        MATCH ()-[r]->()
        WITH node_count, count(r) as rel_count
        RETURN node_count, rel_count,
               (rel_count * 1.0) / (node_count * (node_count - 1)) as density
        '''

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            if not record:
                return {"error": "Unable to calculate density"}

            node_count = record["node_count"]
            rel_count = record["rel_count"]
            density = record["density"] if record["density"] else 0

            # Calculate additional metrics
            avg_degree = (2 * rel_count) / node_count if node_count > 0 else 0

            return {
                "total_nodes": node_count,
                "total_relationships": rel_count,
                "density": round(density, 6),
                "avg_degree": round(avg_degree, 2),
                "density_category": self._categorize_density(density)
            }

    def _categorize_density(self, density: float) -> str:
        """Categorize graph density"""
        if density < 0.01:
            return "very_sparse"
        elif density < 0.05:
            return "sparse"
        elif density < 0.2:
            return "moderate"
        elif density < 0.5:
            return "dense"
        else:
            return "very_dense"

    def identify_hotspots(self, limit: int = 20) -> Dict:
        """Identify highly connected nodes (hotspots)"""
        query = '''
        MATCH (n)
        WITH n, size((n)--()) as degree
        WHERE degree > 0
        RETURN labels(n) as labels,
               n.id as id,
               n.name as name,
               degree
        ORDER BY degree DESC
        LIMIT $limit
        '''

        with self.driver.session() as session:
            result = session.run(query, limit=limit)

            hotspots = []
            degrees = []

            for record in result:
                degree = record["degree"]
                degrees.append(degree)

                hotspots.append({
                    "labels": record["labels"],
                    "id": record["id"],
                    "name": record["name"],
                    "degree": degree
                })

            # Calculate distribution stats
            if degrees:
                import statistics
                stats = {
                    "max_degree": max(degrees),
                    "avg_degree": round(statistics.mean(degrees), 2),
                    "median_degree": statistics.median(degrees)
                }
            else:
                stats = {}

            return {
                "top_nodes": hotspots,
                "statistics": stats
            }

    def analyze_distribution(self) -> Dict:
        """Analyze degree distribution"""
        query = '''
        MATCH (n)
        WITH n, size((n)--()) as degree
        WITH degree, count(*) as count
        RETURN degree, count
        ORDER BY degree
        '''

        with self.driver.session() as session:
            result = session.run(query)

            distribution = []
            total_nodes = 0

            for record in result:
                degree = record["degree"]
                count = record["count"]
                total_nodes += count

                distribution.append({
                    "degree": degree,
                    "count": count
                })

            # Calculate percentiles
            isolated_nodes = distribution[0]["count"] if distribution and distribution[0]["degree"] == 0 else 0
            low_connectivity = sum(d["count"] for d in distribution if d["degree"] <= 2)
            high_connectivity = sum(d["count"] for d in distribution if d["degree"] >= 10)

            return {
                "distribution": distribution,
                "summary": {
                    "total_nodes": total_nodes,
                    "isolated_nodes": isolated_nodes,
                    "low_connectivity": low_connectivity,
                    "high_connectivity": high_connectivity,
                    "isolated_pct": round((isolated_nodes / max(total_nodes, 1)) * 100, 2),
                    "high_connectivity_pct": round((high_connectivity / max(total_nodes, 1)) * 100, 2)
                }
            }

    def generate_dashboard_data(self) -> Dict:
        """Generate data for statistics dashboard"""
        stats = self.collect_all_statistics()

        # Format for dashboard consumption
        dashboard = {
            "summary_cards": [
                {
                    "title": "Total Nodes",
                    "value": stats["node_counts"]["_total"],
                    "icon": "nodes"
                },
                {
                    "title": "Total Relationships",
                    "value": stats["relationship_counts"]["_total"],
                    "icon": "relationships"
                },
                {
                    "title": "Graph Density",
                    "value": f"{stats['density_metrics']['density']:.4f}",
                    "category": stats['density_metrics']['density_category'],
                    "icon": "density"
                },
                {
                    "title": "Avg Daily Growth",
                    "value": stats["growth_trends"]["avg_daily_growth"],
                    "icon": "growth"
                }
            ],
            "node_distribution": {
                "labels": list(stats["node_counts"].keys())[:-1],  # Exclude _total
                "values": [stats["node_counts"][k] for k in list(stats["node_counts"].keys())[:-1]]
            },
            "relationship_distribution": {
                "types": list(stats["relationship_counts"].keys())[:-1],
                "values": [stats["relationship_counts"][k] for k in list(stats["relationship_counts"].keys())[:-1]]
            },
            "top_hotspots": stats["hotspots"]["top_nodes"][:10],
            "degree_distribution": stats["distribution"]["summary"]
        }

        return dashboard

    def export_statistics(self, output_file: str):
        """Export statistics to JSON file"""
        stats = self.collect_all_statistics()

        with open(output_file, 'w') as f:
            json.dump(stats, f, indent=2)

        logger.info(f"Statistics exported to {output_file}")

    def print_summary(self):
        """Print summary statistics to console"""
        stats = self.collect_all_statistics()

        print("\n" + "=" * 60)
        print("GRAPH STATISTICS SUMMARY")
        print("=" * 60)

        print(f"\n📊 Node Counts:")
        for label, count in sorted(stats["node_counts"].items(), key=lambda x: x[1], reverse=True):
            if label != "_total":
                print(f"  {label}: {count:,}")
        print(f"  TOTAL: {stats['node_counts']['_total']:,}")

        print(f"\n🔗 Relationship Counts:")
        for rel_type, count in sorted(stats["relationship_counts"].items(), key=lambda x: x[1], reverse=True)[:10]:
            if rel_type != "_total":
                print(f"  {rel_type}: {count:,}")
        print(f"  TOTAL: {stats['relationship_counts']['_total']:,}")

        print(f"\n📈 Density Metrics:")
        print(f"  Density: {stats['density_metrics']['density']:.6f} ({stats['density_metrics']['density_category']})")
        print(f"  Average Degree: {stats['density_metrics']['avg_degree']:.2f}")

        print(f"\n🔥 Top Hotspots:")
        for i, node in enumerate(stats["hotspots"]["top_nodes"][:5], 1):
            name = node.get("name") or node.get("id") or "unknown"
            print(f"  {i}. {name} ({node['labels'][0]}): {node['degree']} connections")

        print(f"\n📊 Distribution Summary:")
        dist = stats["distribution"]["summary"]
        print(f"  Isolated nodes: {dist['isolated_nodes']:,} ({dist['isolated_pct']:.1f}%)")
        print(f"  Low connectivity (≤2): {dist['low_connectivity']:,}")
        print(f"  High connectivity (≥10): {dist['high_connectivity']:,} ({dist['high_connectivity_pct']:.1f}%)")

        print("\n" + "=" * 60)


def main():
    """Example usage"""
    stats_collector = GraphStatistics(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Print summary to console
        stats_collector.print_summary()

        # Export full statistics
        stats_collector.export_statistics("/tmp/graph_statistics.json")

        # Generate dashboard data
        dashboard = stats_collector.generate_dashboard_data()
        with open("/tmp/dashboard_data.json", 'w') as f:
            json.dump(dashboard, f, indent=2)

        print("\n✅ Statistics collected and exported successfully")

    finally:
        stats_collector.close()


if __name__ == "__main__":
    main()
