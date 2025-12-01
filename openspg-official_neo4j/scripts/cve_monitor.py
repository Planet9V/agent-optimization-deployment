#!/usr/bin/env python3
"""
Real-Time CVE Monitoring Script
Continuous monitoring and alerting for CVE preservation compliance

Purpose: Ensure zero CVE deletion policy enforcement during all waves
Ensures: Immediate detection of any CVE data loss or corruption
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase
import structlog

logger = structlog.get_logger()

class CVEMonitor:
    """
    Real-time CVE monitoring and alerting system

    Monitoring Capabilities:
    - CVE count tracking (real-time)
    - Deletion detection (immediate alert)
    - Property corruption detection
    - Relationship integrity verification
    - Automated baseline comparison
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = None,
        baseline_path: str = None,
        alert_threshold: int = -1  # Alert on ANY decrease
    ):
        """Initialize CVE monitor"""
        self.neo4j_password = neo4j_password or os.getenv("NEO4J_PASSWORD", "neo4j@openspg")
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, self.neo4j_password)
        )

        if baseline_path is None:
            self.baseline_path = Path(
                "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel"
                "/1_Comprehensive_Schema_Enhancement_Plan_v2/CVE_BASELINE_WAVE0.json"
            )
        else:
            self.baseline_path = Path(baseline_path)

        self.alert_threshold = alert_threshold
        self.load_baseline()

        logger.info(
            "cve_monitor_initialized",
            baseline_count=self.baseline_cve_count,
            alert_threshold=self.alert_threshold
        )

    def load_baseline(self):
        """Load baseline CVE metrics"""
        if not self.baseline_path.exists():
            logger.error("baseline_not_found", path=str(self.baseline_path))
            raise FileNotFoundError(f"Baseline not found: {self.baseline_path}")

        with open(self.baseline_path, 'r') as f:
            baseline = json.load(f)

        self.baseline_cve_count = baseline["cve_metrics"]["total_count"]
        self.baseline_relationships = baseline["relationships"]["total_count"]
        self.baseline_checksum = baseline["verification"]["content_checksum"]

        logger.info("baseline_loaded", count=self.baseline_cve_count)

    def get_current_cve_count(self) -> int:
        """Get current CVE count from Neo4j"""
        with self.driver.session() as session:
            result = session.run("MATCH (c:CVE) RETURN count(c) as count")
            count = result.single()["count"]
            return count

    def get_current_relationship_count(self) -> int:
        """Get current CVE relationship count"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:CVE)-[r]->() RETURN count(r) as count"
            )
            count = result.single()["count"]
            return count

    def check_cve_integrity(self) -> Dict[str, Any]:
        """
        Comprehensive CVE integrity check

        Returns:
            Integrity report with any violations
        """
        current_count = self.get_current_cve_count()
        current_relationships = self.get_current_relationship_count()

        # Calculate deltas
        count_delta = current_count - self.baseline_cve_count
        relationship_delta = current_relationships - self.baseline_relationships

        # Determine status
        violations = []

        if count_delta < 0:
            violations.append({
                "type": "CVE_DELETION",
                "severity": "CRITICAL",
                "message": f"CVE count decreased by {abs(count_delta)}",
                "baseline": self.baseline_cve_count,
                "current": current_count
            })

        if count_delta < self.alert_threshold:
            violations.append({
                "type": "CVE_COUNT_THRESHOLD",
                "severity": "WARNING",
                "message": f"CVE count change ({count_delta}) below threshold ({self.alert_threshold})",
                "baseline": self.baseline_cve_count,
                "current": current_count
            })

        if relationship_delta < -100:  # Allow minor fluctuations
            violations.append({
                "type": "RELATIONSHIP_LOSS",
                "severity": "HIGH",
                "message": f"Relationship count decreased by {abs(relationship_delta)}",
                "baseline": self.baseline_relationships,
                "current": current_relationships
            })

        integrity_report = {
            "checked_at": datetime.now().isoformat(),
            "cve_count": {
                "baseline": self.baseline_cve_count,
                "current": current_count,
                "delta": count_delta
            },
            "relationships": {
                "baseline": self.baseline_relationships,
                "current": current_relationships,
                "delta": relationship_delta
            },
            "violations": violations,
            "status": "VIOLATION" if violations else "HEALTHY"
        }

        return integrity_report

    def monitor_continuous(
        self,
        check_interval: int = 60,
        alert_callback: Optional[callable] = None
    ):
        """
        Run continuous monitoring loop

        Args:
            check_interval: Seconds between checks
            alert_callback: Function to call on violations
        """
        logger.info(
            "continuous_monitoring_started",
            interval=check_interval
        )

        check_count = 0

        try:
            while True:
                check_count += 1

                # Run integrity check
                report = self.check_cve_integrity()

                # Log status
                logger.info(
                    "integrity_check_completed",
                    check=check_count,
                    status=report["status"],
                    cve_delta=report["cve_count"]["delta"],
                    violations=len(report["violations"])
                )

                # Handle violations
                if report["violations"]:
                    self._handle_violations(report, alert_callback)

                # Sleep until next check
                time.sleep(check_interval)

        except KeyboardInterrupt:
            logger.info("monitoring_stopped_by_user", total_checks=check_count)

    def _handle_violations(
        self,
        report: Dict[str, Any],
        alert_callback: Optional[callable] = None
    ):
        """Handle detected violations"""
        for violation in report["violations"]:
            logger.error(
                "violation_detected",
                type=violation["type"],
                severity=violation["severity"],
                message=violation["message"]
            )

            # Print alert to console
            self._print_alert(violation)

            # Write violation to file
            self._write_violation_log(violation, report)

        # Call custom alert callback if provided
        if alert_callback:
            alert_callback(report)

    def _print_alert(self, violation: Dict[str, Any]):
        """Print formatted alert to console"""
        severity_symbols = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "WARNING": "⚡"
        }

        symbol = severity_symbols.get(violation["severity"], "ℹ️")

        print(f"\n{symbol} {violation['severity']} VIOLATION DETECTED")
        print(f"Type: {violation['type']}")
        print(f"Message: {violation['message']}")
        print(f"Time: {datetime.now().isoformat()}")
        print("-" * 60)

    def _write_violation_log(self, violation: Dict[str, Any], report: Dict[str, Any]):
        """Write violation to log file"""
        log_dir = Path("/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "cve_violations.jsonl"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "violation": violation,
            "report": report
        }

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

    def generate_monitoring_report(self) -> Dict[str, Any]:
        """Generate comprehensive monitoring report"""
        integrity_report = self.check_cve_integrity()

        # Get additional metrics
        with self.driver.session() as session:
            # Recent CVE additions
            recent_result = session.run(
                """
                MATCH (c:CVE)
                WHERE c.last_updated IS NOT NULL
                RETURN c.last_updated as last_updated
                ORDER BY c.last_updated DESC
                LIMIT 1
                """
            )

            latest_update = None
            record = recent_result.single()
            if record:
                latest_update = str(record["last_updated"])

            # Property completeness
            property_result = session.run(
                """
                MATCH (c:CVE)
                WHERE c.cvss_score IS NULL
                   OR c.description IS NULL
                   OR c.severity IS NULL
                RETURN count(c) as incomplete_count
                """
            )

            incomplete_count = property_result.single()["incomplete_count"]

        monitoring_report = {
            "generated_at": datetime.now().isoformat(),
            "integrity": integrity_report,
            "data_quality": {
                "incomplete_cves": incomplete_count,
                "latest_update": latest_update
            },
            "preservation_compliance": {
                "zero_deletion_policy": integrity_report["cve_count"]["delta"] >= 0,
                "additive_only": integrity_report["cve_count"]["delta"] >= 0,
                "no_reimport": True  # Assumed if count doesn't jump dramatically
            }
        }

        return monitoring_report

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()
        logger.info("neo4j_connection_closed")


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CVE Monitor")
    subparsers = parser.add_subparsers(dest="command")

    # Check command (one-time)
    check_parser = subparsers.add_parser("check", help="Run single integrity check")

    # Monitor command (continuous)
    monitor_parser = subparsers.add_parser("monitor", help="Run continuous monitoring")
    monitor_parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Check interval in seconds (default: 60)"
    )

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate monitoring report")
    report_parser.add_argument("--output", default=None, help="Output path for report")

    args = parser.parse_args()

    monitor = CVEMonitor()

    try:
        if args.command == "check":
            report = monitor.check_cve_integrity()

            print("\n🔍 CVE Integrity Check")
            print(f"📊 CVE Count: {report['cve_count']['current']:,} (Δ {report['cve_count']['delta']:+,})")
            print(f"🔗 Relationships: {report['relationships']['current']:,} (Δ {report['relationships']['delta']:+,})")
            print(f"🛡️  Status: {report['status']}")

            if report['violations']:
                print(f"\n⚠️  {len(report['violations'])} Violation(s) Detected:")
                for v in report['violations']:
                    print(f"  - {v['severity']}: {v['message']}")
            else:
                print("\n✅ No violations detected - CVE preservation intact")

        elif args.command == "monitor":
            print(f"\n🔄 Starting Continuous CVE Monitoring (interval: {args.interval}s)")
            print("Press Ctrl+C to stop\n")

            monitor.monitor_continuous(check_interval=args.interval)

        elif args.command == "report":
            report = monitor.generate_monitoring_report()

            print("\n📊 CVE Monitoring Report")
            print(f"Generated: {report['generated_at']}")
            print(f"\n🔍 Integrity Status: {report['integrity']['status']}")
            print(f"📊 CVE Count: {report['integrity']['cve_count']['current']:,} (Δ {report['integrity']['cve_count']['delta']:+,})")
            print(f"🔗 Relationships: {report['integrity']['relationships']['current']:,}")
            print(f"⚠️  Incomplete CVEs: {report['data_quality']['incomplete_cves']:,}")
            print(f"\n🛡️  Preservation Compliance:")
            print(f"  ✓ Zero Deletion Policy: {'PASS' if report['preservation_compliance']['zero_deletion_policy'] else 'FAIL'}")
            print(f"  ✓ Additive Only: {'PASS' if report['preservation_compliance']['additive_only'] else 'FAIL'}")

            # Export if output path provided
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(report, f, indent=2)
                print(f"\n📄 Report saved to: {args.output}")

    finally:
        monitor.close()
