#!/usr/bin/env python3
"""
Audit Report Generator - Generate compliance and audit reports
"""

import json
from typing import Dict, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AuditMetric:
    """Single audit metric"""
    name: str
    value: float
    unit: str
    status: str  # pass/warning/fail
    threshold: float
    description: str


class AuditReportGenerator:
    """Generate audit and compliance reports"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def generate_full_audit(self) -> Dict:
        """Generate comprehensive audit report"""
        logger.info("Generating full audit report...")

        report = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "report_type": "comprehensive_audit",
                "version": "1.0"
            },
            "data_freshness": self.audit_data_freshness(),
            "coverage": self.audit_coverage(),
            "update_history": self.audit_update_history(),
            "query_activity": self.audit_query_activity(),
            "compliance": self.audit_compliance_status()
        }

        # Calculate overall health score
        report["overall_health"] = self._calculate_overall_health(report)

        return report

    def audit_data_freshness(self) -> Dict:
        """Audit data freshness and staleness"""
        query = '''
        // Check CVE data freshness
        MATCH (v:Vulnerability)
        WHERE v.last_modified IS NOT NULL
        WITH v, datetime(v.last_modified) as last_mod, datetime() as now
        WITH duration.between(last_mod, now).days as days_old, count(*) as count
        RETURN days_old, count
        ORDER BY days_old
        '''

        with self.driver.session() as session:
            result = session.run(query)

            freshness_buckets = {
                "fresh_7d": 0,
                "recent_30d": 0,
                "stale_90d": 0,
                "very_stale": 0
            }

            total_vulns = 0

            for record in result:
                days = record["days_old"]
                count = record["count"]
                total_vulns += count

                if days <= 7:
                    freshness_buckets["fresh_7d"] += count
                elif days <= 30:
                    freshness_buckets["recent_30d"] += count
                elif days <= 90:
                    freshness_buckets["stale_90d"] += count
                else:
                    freshness_buckets["very_stale"] += count

            # Check threat intel freshness
            threat_query = '''
            MATCH (t:ThreatIntel)
            WHERE datetime(t.timestamp) > datetime() - duration({days: 7})
            RETURN count(*) as recent_count
            '''

            result = session.run(threat_query)
            recent_threat_intel = result.single()["recent_count"]

            metrics = [
                AuditMetric(
                    name="cve_data_freshness",
                    value=freshness_buckets["fresh_7d"] / max(total_vulns, 1) * 100,
                    unit="percent",
                    status="pass" if freshness_buckets["fresh_7d"] / max(total_vulns, 1) > 0.8 else "warning",
                    threshold=80.0,
                    description="Percentage of CVEs updated in last 7 days"
                ),
                AuditMetric(
                    name="stale_data_count",
                    value=freshness_buckets["very_stale"],
                    unit="count",
                    status="pass" if freshness_buckets["very_stale"] < 100 else "warning",
                    threshold=100,
                    description="CVEs not updated in 90+ days"
                ),
                AuditMetric(
                    name="recent_threat_intel",
                    value=recent_threat_intel,
                    unit="count",
                    status="pass" if recent_threat_intel > 0 else "warning",
                    threshold=1,
                    description="Threat intel reports in last 7 days"
                )
            ]

            return {
                "metrics": [vars(m) for m in metrics],
                "distribution": freshness_buckets,
                "total_vulnerabilities": total_vulns
            }

    def audit_coverage(self) -> Dict:
        """Audit coverage of assets and vulnerabilities"""
        queries = {
            "total_assets": "MATCH (c:Component) RETURN count(*) as count",
            "assets_with_vulns": '''
                MATCH (c:Component)<-[:AFFECTS]-(v:Vulnerability)
                RETURN count(DISTINCT c) as count
            ''',
            "assets_with_software": '''
                MATCH (c:Component)-[:RUNS]->(s:Software)
                RETURN count(DISTINCT c) as count
            ''',
            "total_vulns": "MATCH (v:Vulnerability) RETURN count(*) as count",
            "vulns_with_exploits": '''
                MATCH (v:Vulnerability)-[:HAS_EXPLOIT]->()
                RETURN count(DISTINCT v) as count
            ''',
            "vulns_with_cpe": '''
                MATCH (v:Vulnerability)-[:AFFECTS]->(cpe:CPE)
                RETURN count(DISTINCT v) as count
            '''
        }

        results = {}

        with self.driver.session() as session:
            for metric, query in queries.items():
                result = session.run(query)
                results[metric] = result.single()["count"]

        # Calculate coverage percentages
        asset_vuln_coverage = (results["assets_with_vulns"] / max(results["total_assets"], 1)) * 100
        asset_software_coverage = (results["assets_with_software"] / max(results["total_assets"], 1)) * 100
        vuln_exploit_coverage = (results["vulns_with_exploits"] / max(results["total_vulns"], 1)) * 100
        vuln_cpe_coverage = (results["vulns_with_cpe"] / max(results["total_vulns"], 1)) * 100

        metrics = [
            AuditMetric(
                name="asset_vulnerability_coverage",
                value=asset_vuln_coverage,
                unit="percent",
                status="pass" if asset_vuln_coverage > 70 else "warning",
                threshold=70.0,
                description="Percentage of assets with vulnerability assessments"
            ),
            AuditMetric(
                name="asset_software_coverage",
                value=asset_software_coverage,
                unit="percent",
                status="pass" if asset_software_coverage > 80 else "warning",
                threshold=80.0,
                description="Percentage of assets with software inventory"
            ),
            AuditMetric(
                name="vulnerability_exploit_coverage",
                value=vuln_exploit_coverage,
                unit="percent",
                status="pass" if vuln_exploit_coverage > 30 else "info",
                threshold=30.0,
                description="Percentage of vulnerabilities with exploit information"
            ),
            AuditMetric(
                name="vulnerability_cpe_coverage",
                value=vuln_cpe_coverage,
                unit="percent",
                status="pass" if vuln_cpe_coverage > 60 else "warning",
                threshold=60.0,
                description="Percentage of vulnerabilities with CPE mappings"
            )
        ]

        return {
            "metrics": [vars(m) for m in metrics],
            "counts": results
        }

    def audit_update_history(self, days: int = 30) -> Dict:
        """Audit update history and trends"""
        query = '''
        MATCH (v:Vulnerability)
        WHERE v.last_modified IS NOT NULL
        WITH datetime(v.last_modified) as mod_date
        WHERE mod_date > datetime() - duration({days: $days})
        WITH date(mod_date) as update_date
        RETURN update_date, count(*) as updates
        ORDER BY update_date DESC
        LIMIT 30
        '''

        with self.driver.session() as session:
            result = session.run(query, days=days)

            updates_by_date = []
            total_updates = 0

            for record in result:
                updates = record["updates"]
                total_updates += updates
                updates_by_date.append({
                    "date": str(record["update_date"]),
                    "updates": updates
                })

            avg_daily_updates = total_updates / min(days, len(updates_by_date))

            return {
                "total_updates_period": total_updates,
                "avg_daily_updates": round(avg_daily_updates, 2),
                "period_days": days,
                "updates_by_date": updates_by_date,
                "status": "healthy" if avg_daily_updates > 1 else "stale"
            }

    def audit_query_activity(self, days: int = 7) -> Dict:
        """Audit query activity (requires query logging)"""
        # This would typically query audit logs
        # Placeholder implementation
        query = '''
        // Check for recent graph modifications
        MATCH (n)
        WHERE n.created_at IS NOT NULL
        WITH datetime(n.created_at) as created
        WHERE created > datetime() - duration({days: $days})
        RETURN count(*) as recent_creations
        '''

        with self.driver.session() as session:
            try:
                result = session.run(query, days=days)
                recent_activity = result.single()["recent_creations"]

                return {
                    "recent_creations": recent_activity,
                    "period_days": days,
                    "activity_status": "active" if recent_activity > 0 else "inactive"
                }
            except:
                return {
                    "error": "Query logging not available",
                    "recommendation": "Enable query logging for detailed activity auditing"
                }

    def audit_compliance_status(self) -> Dict:
        """Audit compliance with security standards"""
        # IEC 62443 and NERC-CIP compliance checks
        compliance_checks = {
            "iec_62443": {
                "asset_inventory": self._check_asset_inventory(),
                "vulnerability_management": self._check_vulnerability_management(),
                "network_segmentation": self._check_network_segmentation()
            },
            "nerc_cip": {
                "critical_asset_identification": self._check_critical_assets(),
                "security_monitoring": self._check_security_monitoring()
            }
        }

        # Calculate compliance scores
        for standard, checks in compliance_checks.items():
            passed = sum(1 for check in checks.values() if check["status"] == "pass")
            total = len(checks)
            compliance_checks[standard]["score"] = (passed / total * 100) if total else 0
            compliance_checks[standard]["status"] = "compliant" if passed == total else "partial"

        return compliance_checks

    def _check_asset_inventory(self) -> Dict:
        """Check asset inventory completeness"""
        query = '''
        MATCH (c:Component)
        WITH count(*) as total,
             sum(CASE WHEN c.name IS NOT NULL AND c.type IS NOT NULL THEN 1 ELSE 0 END) as complete
        RETURN total, complete, (complete * 100.0 / total) as completeness
        '''

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            completeness = record["completeness"] if record else 0

            return {
                "check": "Asset Inventory Completeness",
                "status": "pass" if completeness >= 95 else "fail",
                "value": completeness,
                "threshold": 95.0,
                "description": "All assets must have name and type defined"
            }

    def _check_vulnerability_management(self) -> Dict:
        """Check vulnerability management coverage"""
        query = '''
        MATCH (c:Component {criticality: 'critical'})
        OPTIONAL MATCH (c)<-[:AFFECTS]-(v:Vulnerability)
        WITH count(DISTINCT c) as critical_assets,
             count(DISTINCT CASE WHEN v IS NOT NULL THEN c END) as assessed_assets
        RETURN critical_assets, assessed_assets,
               (assessed_assets * 100.0 / critical_assets) as coverage
        '''

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            coverage = record["coverage"] if record else 0

            return {
                "check": "Critical Asset Vulnerability Assessment",
                "status": "pass" if coverage >= 100 else "fail",
                "value": coverage,
                "threshold": 100.0,
                "description": "All critical assets must have vulnerability assessments"
            }

    def _check_network_segmentation(self) -> Dict:
        """Check network segmentation"""
        query = '''
        MATCH (ext:NetworkInterface {zone: 'external'})
              -[:CONNECTS_TO*1..2]->(crit:Component {criticality: 'critical'})
        RETURN count(DISTINCT crit) as direct_exposure
        '''

        with self.driver.session() as session:
            result = session.run(query)
            exposure = result.single()["direct_exposure"]

            return {
                "check": "Network Segmentation - Critical Asset Isolation",
                "status": "pass" if exposure == 0 else "fail",
                "value": exposure,
                "threshold": 0,
                "description": "Critical assets must not be directly reachable from external zone"
            }

    def _check_critical_assets(self) -> Dict:
        """Check critical asset identification"""
        query = '''
        MATCH (c:Component)
        WHERE c.criticality IS NULL
        RETURN count(*) as unclassified
        '''

        with self.driver.session() as session:
            result = session.run(query)
            unclassified = result.single()["unclassified"]

            return {
                "check": "Asset Criticality Classification",
                "status": "pass" if unclassified == 0 else "fail",
                "value": unclassified,
                "threshold": 0,
                "description": "All assets must have criticality classification"
            }

    def _check_security_monitoring(self) -> Dict:
        """Check security monitoring capability"""
        query = '''
        MATCH (t:ThreatIntel)
        WHERE datetime(t.timestamp) > datetime() - duration({days: 7})
        RETURN count(*) as recent_intel
        '''

        with self.driver.session() as session:
            result = session.run(query)
            recent_intel = result.single()["recent_intel"]

            return {
                "check": "Active Threat Intelligence Monitoring",
                "status": "pass" if recent_intel > 0 else "fail",
                "value": recent_intel,
                "threshold": 1,
                "description": "Threat intelligence must be actively collected"
            }

    def _calculate_overall_health(self, report: Dict) -> Dict:
        """Calculate overall system health score"""
        scores = []

        # Data freshness score
        if "data_freshness" in report and "metrics" in report["data_freshness"]:
            freshness_score = sum(
                100 if m["status"] == "pass" else 50 if m["status"] == "warning" else 0
                for m in report["data_freshness"]["metrics"]
            ) / len(report["data_freshness"]["metrics"])
            scores.append(("freshness", freshness_score))

        # Coverage score
        if "coverage" in report and "metrics" in report["coverage"]:
            coverage_score = sum(
                100 if m["status"] == "pass" else 50 if m["status"] == "warning" else 0
                for m in report["coverage"]["metrics"]
            ) / len(report["coverage"]["metrics"])
            scores.append(("coverage", coverage_score))

        # Compliance score
        if "compliance" in report:
            compliance_scores = [
                info["score"]
                for standard, info in report["compliance"].items()
                if "score" in info
            ]
            if compliance_scores:
                avg_compliance = sum(compliance_scores) / len(compliance_scores)
                scores.append(("compliance", avg_compliance))

        # Calculate weighted average
        if scores:
            overall = sum(score for _, score in scores) / len(scores)
        else:
            overall = 0

        return {
            "score": round(overall, 2),
            "grade": self._score_to_grade(overall),
            "components": dict(scores)
        }

    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def export_report(self, report: Dict, output_file: str):
        """Export audit report to file"""
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Audit report exported to {output_file}")


def main():
    """Example usage"""
    auditor = AuditReportGenerator(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Generate full audit
        report = auditor.generate_full_audit()

        print("\n=== Audit Report ===")
        print(f"Timestamp: {report['metadata']['timestamp']}")
        print(f"\nOverall Health: {report['overall_health']['score']:.1f} (Grade: {report['overall_health']['grade']})")

        # Print compliance status
        print("\n=== Compliance Status ===")
        for standard, info in report['compliance'].items():
            if 'score' in info:
                print(f"{standard.upper()}: {info['score']:.1f}% ({info['status']})")

        # Print data freshness
        print("\n=== Data Freshness ===")
        if 'distribution' in report['data_freshness']:
            dist = report['data_freshness']['distribution']
            print(f"Fresh (7d): {dist['fresh_7d']}")
            print(f"Recent (30d): {dist['recent_30d']}")
            print(f"Stale (90d+): {dist['very_stale']}")

        # Export report
        auditor.export_report(report, "/tmp/audit_report.json")

    finally:
        auditor.close()


if __name__ == "__main__":
    main()
