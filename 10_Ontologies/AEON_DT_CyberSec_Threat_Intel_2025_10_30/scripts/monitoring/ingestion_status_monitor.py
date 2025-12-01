#!/usr/bin/env python3
"""
Ingestion Status Monitor - Monitor document ingestion and entity extraction status
"""

import json
import time
from typing import Dict, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IngestionStatus:
    """Status of ingestion process"""
    total_documents: int
    processed_documents: int
    failed_documents: int
    total_entities: int
    processing_rate: float
    errors: List[Dict]
    eta_seconds: float


class IngestionStatusMonitor:
    """Monitor document ingestion and entity extraction"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.start_time = time.time()
        self.baseline_counts = {}

    def close(self):
        self.driver.close()

    def set_baseline(self):
        """Set baseline counts for monitoring"""
        with self.driver.session() as session:
            # Count existing entities
            query = '''
            CALL db.labels() YIELD label
            CALL {
                WITH label
                MATCH (n)
                WHERE label IN labels(n)
                RETURN count(*) as count
            }
            RETURN label, count
            '''

            result = session.run(query)

            for record in result:
                self.baseline_counts[record["label"]] = record["count"]

        logger.info(f"Baseline set with {sum(self.baseline_counts.values())} entities")

    def get_current_status(self) -> IngestionStatus:
        """Get current ingestion status"""
        with self.driver.session() as session:
            # Count documents processed (assuming Document node type)
            doc_query = '''
            MATCH (d:Document)
            WITH count(*) as total,
                 sum(CASE WHEN d.processed = true THEN 1 ELSE 0 END) as processed,
                 sum(CASE WHEN d.status = 'failed' THEN 1 ELSE 0 END) as failed
            RETURN total, processed, failed
            '''

            try:
                result = session.run(doc_query)
                doc_record = result.single()

                if doc_record:
                    total_docs = doc_record["total"]
                    processed_docs = doc_record["processed"]
                    failed_docs = doc_record["failed"]
                else:
                    total_docs = processed_docs = failed_docs = 0
            except:
                # Document tracking not available
                total_docs = processed_docs = failed_docs = 0

            # Count total entities
            entity_query = '''
            MATCH (n)
            RETURN count(*) as total
            '''

            result = session.run(entity_query)
            total_entities = result.single()["total"]

            # Calculate processing rate
            elapsed_time = time.time() - self.start_time
            new_entities = total_entities - sum(self.baseline_counts.values())
            processing_rate = new_entities / elapsed_time if elapsed_time > 0 else 0

            # Calculate ETA
            remaining_docs = total_docs - processed_docs
            eta_seconds = (remaining_docs / processing_rate) if processing_rate > 0 else 0

            # Get recent errors
            error_query = '''
            MATCH (d:Document)
            WHERE d.status = 'failed' AND d.error_message IS NOT NULL
            RETURN d.filename as filename, d.error_message as error, d.timestamp as timestamp
            ORDER BY d.timestamp DESC
            LIMIT 10
            '''

            try:
                result = session.run(error_query)
                errors = [
                    {
                        "filename": record["filename"],
                        "error": record["error"],
                        "timestamp": str(record["timestamp"])
                    }
                    for record in result
                ]
            except:
                errors = []

            return IngestionStatus(
                total_documents=total_docs,
                processed_documents=processed_docs,
                failed_documents=failed_docs,
                total_entities=total_entities,
                processing_rate=processing_rate,
                errors=errors,
                eta_seconds=eta_seconds
            )

    def get_entity_breakdown(self) -> Dict:
        """Get breakdown of entities by type"""
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

            breakdown = {}
            total = 0

            for record in result:
                label = record["label"]
                count = record["count"]
                baseline = self.baseline_counts.get(label, 0)
                new_count = count - baseline

                breakdown[label] = {
                    "total": count,
                    "baseline": baseline,
                    "new": new_count
                }

                total += count

            breakdown["_total"] = {
                "total": total,
                "baseline": sum(self.baseline_counts.values()),
                "new": total - sum(self.baseline_counts.values())
            }

            return breakdown

    def get_processing_timeline(self, hours: int = 24) -> Dict:
        """Get processing timeline for last N hours"""
        query = '''
        MATCH (n)
        WHERE n.created_at IS NOT NULL
        WITH datetime(n.created_at) as created
        WHERE created > datetime() - duration({hours: $hours})
        WITH datetime.truncate('hour', created) as hour
        RETURN hour, count(*) as entities
        ORDER BY hour
        '''

        with self.driver.session() as session:
            result = session.run(query, hours=hours)

            timeline = []

            for record in result:
                timeline.append({
                    "hour": str(record["hour"]),
                    "entities": record["entities"]
                })

            return {
                "timeline": timeline,
                "period_hours": hours
            }

    def calculate_metrics(self, status: IngestionStatus) -> Dict:
        """Calculate key performance metrics"""
        completion_pct = (status.processed_documents / max(status.total_documents, 1)) * 100
        error_rate = (status.failed_documents / max(status.total_documents, 1)) * 100

        metrics = {
            "completion_percentage": round(completion_pct, 2),
            "error_rate": round(error_rate, 2),
            "processing_rate_per_second": round(status.processing_rate, 2),
            "processing_rate_per_hour": round(status.processing_rate * 3600, 2),
            "eta_formatted": self._format_eta(status.eta_seconds),
            "health_status": self._calculate_health_status(status, error_rate)
        }

        return metrics

    def _format_eta(self, seconds: float) -> str:
        """Format ETA in human-readable form"""
        if seconds <= 0:
            return "Complete"
        elif seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds / 60)}m"
        elif seconds < 86400:
            return f"{int(seconds / 3600)}h {int((seconds % 3600) / 60)}m"
        else:
            days = int(seconds / 86400)
            hours = int((seconds % 86400) / 3600)
            return f"{days}d {hours}h"

    def _calculate_health_status(self, status: IngestionStatus, error_rate: float) -> str:
        """Calculate overall ingestion health"""
        if error_rate > 10:
            return "critical"
        elif error_rate > 5:
            return "warning"
        elif status.processing_rate > 0:
            return "healthy"
        else:
            return "idle"

    def generate_report(self) -> Dict:
        """Generate comprehensive ingestion status report"""
        status = self.get_current_status()
        metrics = self.calculate_metrics(status)
        breakdown = self.get_entity_breakdown()
        timeline = self.get_processing_timeline()

        report = {
            "timestamp": datetime.now().isoformat(),
            "status": {
                "total_documents": status.total_documents,
                "processed_documents": status.processed_documents,
                "failed_documents": status.failed_documents,
                "pending_documents": status.total_documents - status.processed_documents - status.failed_documents
            },
            "metrics": metrics,
            "entities": {
                "total": status.total_entities,
                "breakdown": breakdown
            },
            "timeline": timeline,
            "errors": status.errors
        }

        return report

    def print_status_dashboard(self):
        """Print status dashboard to console"""
        status = self.get_current_status()
        metrics = self.calculate_metrics(status)
        breakdown = self.get_entity_breakdown()

        print("\n" + "=" * 70)
        print("INGESTION STATUS DASHBOARD")
        print("=" * 70)

        # Status overview
        print(f"\n📄 Document Processing:")
        print(f"  Total Documents: {status.total_documents}")
        print(f"  Processed: {status.processed_documents} ({metrics['completion_percentage']:.1f}%)")
        print(f"  Failed: {status.failed_documents} ({metrics['error_rate']:.1f}% error rate)")
        print(f"  Pending: {status.total_documents - status.processed_documents - status.failed_documents}")

        # Performance metrics
        print(f"\n⚡ Performance:")
        print(f"  Processing Rate: {metrics['processing_rate_per_second']:.2f} entities/sec")
        print(f"  Estimated Completion: {metrics['eta_formatted']}")
        print(f"  Health Status: {metrics['health_status'].upper()}")

        # Entity breakdown
        print(f"\n📊 Entity Extraction:")
        print(f"  Total Entities: {status.total_entities}")
        print(f"  New Entities: {breakdown['_total']['new']}")

        print(f"\n  Breakdown:")
        for label, counts in sorted(breakdown.items(), key=lambda x: x[1].get("total", 0), reverse=True)[:10]:
            if label != "_total":
                print(f"    {label}: {counts['total']} (new: {counts['new']})")

        # Recent errors
        if status.errors:
            print(f"\n⚠️  Recent Errors ({len(status.errors)}):")
            for error in status.errors[:5]:
                print(f"    • {error['filename']}: {error['error'][:60]}...")

        print("\n" + "=" * 70)

    def monitor_continuous(self, interval_seconds: int = 10, duration_minutes: int = 60):
        """Continuously monitor ingestion for specified duration"""
        logger.info(f"Starting continuous monitoring for {duration_minutes} minutes...")

        self.set_baseline()
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        iteration = 0

        while time.time() < end_time:
            iteration += 1

            print(f"\n{'=' * 70}")
            print(f"Update #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'=' * 70}")

            self.print_status_dashboard()

            if time.time() + interval_seconds < end_time:
                time.sleep(interval_seconds)
            else:
                break

        logger.info("Monitoring complete")

    def export_report(self, output_file: str):
        """Export status report to file"""
        report = self.generate_report()

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report exported to {output_file}")


def main():
    """Example usage"""
    monitor = IngestionStatusMonitor(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Set baseline
        monitor.set_baseline()

        # Display current status
        monitor.print_status_dashboard()

        # Export report
        monitor.export_report("/tmp/ingestion_status.json")

        # Optional: Continuous monitoring
        # monitor.monitor_continuous(interval_seconds=10, duration_minutes=60)

    finally:
        monitor.close()


if __name__ == "__main__":
    main()
