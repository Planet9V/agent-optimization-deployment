#!/usr/bin/env python3
"""
Data Integrity Checker - Validate graph data integrity and consistency
"""

import json
from typing import List, Dict, Set
from dataclasses import dataclass
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IntegrityIssue:
    """Represents a data integrity issue"""
    severity: str  # critical/warning/info
    category: str
    description: str
    affected_nodes: List[str]
    fix_query: str = ""


class DataIntegrityChecker:
    """Check and validate graph data integrity"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.issues: List[IntegrityIssue] = []

    def close(self):
        self.driver.close()

    def run_all_checks(self) -> Dict:
        """Run all integrity checks"""
        logger.info("Starting comprehensive integrity checks...")

        self.check_orphaned_nodes()
        self.check_duplicate_entities()
        self.check_relationship_consistency()
        self.check_property_completeness()
        self.check_constraint_violations()

        return self.generate_report()

    def check_orphaned_nodes(self):
        """Find nodes with no relationships"""
        query = '''
        MATCH (n)
        WHERE NOT (n)--()
        RETURN labels(n) as labels, n.id as id, n.name as name, count(*) as count
        '''

        with self.driver.session() as session:
            result = session.run(query)

            for record in result:
                node_labels = record["labels"]
                node_id = record["id"] or record["name"] or "unknown"

                # Skip certain node types that are expected to be isolated
                if "Configuration" in node_labels or "Metadata" in node_labels:
                    continue

                self.issues.append(IntegrityIssue(
                    severity="warning",
                    category="orphaned_nodes",
                    description=f"Orphaned {node_labels[0]} node with no relationships",
                    affected_nodes=[str(node_id)],
                    fix_query=f"MATCH (n {{id: '{node_id}'}}) DETACH DELETE n"
                ))

        logger.info(f"Checked for orphaned nodes")

    def check_duplicate_entities(self):
        """Find duplicate nodes based on key properties"""
        # Check for duplicate CVEs
        cve_query = '''
        MATCH (v:Vulnerability)
        WITH v.id as cve_id, collect(v) as nodes
        WHERE size(nodes) > 1
        RETURN cve_id, size(nodes) as count
        '''

        # Check for duplicate components
        component_query = '''
        MATCH (c:Component)
        WITH c.name as name, c.type as type, collect(c) as nodes
        WHERE size(nodes) > 1
        RETURN name, type, size(nodes) as count
        '''

        with self.driver.session() as session:
            # Check CVE duplicates
            result = session.run(cve_query)
            for record in result:
                self.issues.append(IntegrityIssue(
                    severity="critical",
                    category="duplicate_entities",
                    description=f"Duplicate CVE {record['cve_id']} ({record['count']} instances)",
                    affected_nodes=[record["cve_id"]],
                    fix_query=f"// Manual merge required for CVE {record['cve_id']}"
                ))

            # Check component duplicates
            result = session.run(component_query)
            for record in result:
                self.issues.append(IntegrityIssue(
                    severity="warning",
                    category="duplicate_entities",
                    description=f"Duplicate component {record['name']} ({record['count']} instances)",
                    affected_nodes=[record["name"]],
                    fix_query=f"// Manual merge required for {record['name']}"
                ))

        logger.info("Checked for duplicate entities")

    def check_relationship_consistency(self):
        """Check relationship logical consistency"""
        checks = [
            {
                "name": "vulnerability_without_cvss",
                "query": '''
                    MATCH (v:Vulnerability)
                    WHERE v.cvss_score IS NULL OR v.cvss_score < 0 OR v.cvss_score > 10
                    RETURN v.id as id, v.cvss_score as score
                ''',
                "severity": "warning",
                "description": "Vulnerability with invalid CVSS score"
            },
            {
                "name": "affects_without_component",
                "query": '''
                    MATCH (v:Vulnerability)-[r:AFFECTS]->()
                    WHERE NOT exists((v)-[:AFFECTS]->(:Component))
                    RETURN v.id as id
                ''',
                "severity": "warning",
                "description": "AFFECTS relationship not pointing to Component"
            },
            {
                "name": "circular_dependencies",
                "query": '''
                    MATCH path = (c:Component)-[:DEPENDS_ON*]->(c)
                    RETURN c.name as name, length(path) as cycle_length
                    LIMIT 10
                ''',
                "severity": "critical",
                "description": "Circular dependency detected"
            },
            {
                "name": "disconnected_cpe",
                "query": '''
                    MATCH (cpe:CPE)
                    WHERE NOT exists((cpe)<-[:AFFECTS]-())
                    RETURN cpe.criteria as criteria
                    LIMIT 100
                ''',
                "severity": "info",
                "description": "CPE not linked to any vulnerabilities"
            }
        ]

        with self.driver.session() as session:
            for check in checks:
                result = session.run(check["query"])

                for record in result:
                    affected = [str(v) for v in record.values() if v]

                    self.issues.append(IntegrityIssue(
                        severity=check["severity"],
                        category="relationship_consistency",
                        description=check["description"],
                        affected_nodes=affected
                    ))

        logger.info("Checked relationship consistency")

    def check_property_completeness(self):
        """Check for missing required properties"""
        checks = [
            {
                "label": "Vulnerability",
                "required_props": ["id", "cvss_score", "description"],
                "query": '''
                    MATCH (v:Vulnerability)
                    WHERE v.{prop} IS NULL OR v.{prop} = ''
                    RETURN v.id as id
                    LIMIT 50
                '''
            },
            {
                "label": "Component",
                "required_props": ["name", "type", "criticality"],
                "query": '''
                    MATCH (c:Component)
                    WHERE c.{prop} IS NULL OR c.{prop} = ''
                    RETURN c.name as name
                    LIMIT 50
                '''
            },
            {
                "label": "Software",
                "required_props": ["name", "vendor", "product"],
                "query": '''
                    MATCH (s:Software)
                    WHERE s.{prop} IS NULL OR s.{prop} = ''
                    RETURN s.name as name
                    LIMIT 50
                '''
            }
        ]

        with self.driver.session() as session:
            for check in checks:
                for prop in check["required_props"]:
                    query = check["query"].replace("{prop}", prop)
                    result = session.run(query)

                    count = 0
                    affected = []
                    for record in result:
                        count += 1
                        affected.append(str(list(record.values())[0]))

                    if count > 0:
                        self.issues.append(IntegrityIssue(
                            severity="warning",
                            category="property_completeness",
                            description=f"{check['label']} nodes missing required property '{prop}' ({count} nodes)",
                            affected_nodes=affected[:10]  # Limit to 10 examples
                        ))

        logger.info("Checked property completeness")

    def check_constraint_violations(self):
        """Check for constraint and index violations"""
        # Check for constraint existence
        constraint_check_query = '''
        SHOW CONSTRAINTS
        '''

        with self.driver.session() as session:
            try:
                result = session.run(constraint_check_query)
                constraints = list(result)

                if len(constraints) == 0:
                    self.issues.append(IntegrityIssue(
                        severity="warning",
                        category="constraints",
                        description="No constraints defined on graph",
                        affected_nodes=[],
                        fix_query="// Review and add appropriate uniqueness constraints"
                    ))

                # Check for index existence
                index_check_query = '''
                SHOW INDEXES
                '''
                result = session.run(index_check_query)
                indexes = list(result)

                if len(indexes) < 3:
                    self.issues.append(IntegrityIssue(
                        severity="info",
                        category="performance",
                        description="Limited indexes defined, may impact query performance",
                        affected_nodes=[],
                        fix_query="// Consider adding indexes on frequently queried properties"
                    ))

            except Exception as e:
                logger.warning(f"Could not check constraints: {e}")

        logger.info("Checked constraints and indexes")

    def generate_report(self) -> Dict:
        """Generate comprehensive integrity report"""
        critical = [i for i in self.issues if i.severity == "critical"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        info = [i for i in self.issues if i.severity == "info"]

        # Group by category
        by_category = {}
        for issue in self.issues:
            if issue.category not in by_category:
                by_category[issue.category] = []
            by_category[issue.category].append(issue)

        report = {
            "summary": {
                "total_issues": len(self.issues),
                "critical": len(critical),
                "warnings": len(warnings),
                "info": len(info),
                "health_score": self._calculate_health_score()
            },
            "by_severity": {
                "critical": [
                    {
                        "category": i.category,
                        "description": i.description,
                        "affected": i.affected_nodes[:5],
                        "fix_query": i.fix_query
                    }
                    for i in critical
                ],
                "warnings": [
                    {
                        "category": i.category,
                        "description": i.description,
                        "affected_count": len(i.affected_nodes)
                    }
                    for i in warnings[:20]  # Limit to 20 warnings
                ]
            },
            "by_category": {
                category: {
                    "count": len(issues),
                    "severity_breakdown": {
                        "critical": sum(1 for i in issues if i.severity == "critical"),
                        "warning": sum(1 for i in issues if i.severity == "warning"),
                        "info": sum(1 for i in issues if i.severity == "info")
                    }
                }
                for category, issues in by_category.items()
            }
        }

        return report

    def _calculate_health_score(self) -> float:
        """Calculate overall graph health score (0-100)"""
        if not self.issues:
            return 100.0

        # Weight by severity
        penalties = {
            "critical": 10,
            "warning": 3,
            "info": 1
        }

        total_penalty = sum(
            penalties.get(issue.severity, 1)
            for issue in self.issues
        )

        # Cap at 100 points max penalty
        health_score = max(0, 100 - total_penalty)

        return round(health_score, 2)

    def export_report(self, output_file: str):
        """Export report to JSON file"""
        report = self.generate_report()

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report exported to {output_file}")

    def auto_fix(self, dry_run: bool = True):
        """Attempt to auto-fix issues (with dry-run mode)"""
        fixed = 0
        failed = 0

        with self.driver.session() as session:
            for issue in self.issues:
                if not issue.fix_query or issue.fix_query.startswith("//"):
                    continue  # Skip manual fixes

                try:
                    if not dry_run:
                        session.run(issue.fix_query)
                    logger.info(f"Fixed: {issue.description}")
                    fixed += 1
                except Exception as e:
                    logger.error(f"Failed to fix {issue.description}: {e}")
                    failed += 1

        mode = "DRY RUN" if dry_run else "LIVE"
        logger.info(f"{mode}: Fixed {fixed} issues, {failed} failed")

        return fixed, failed


def main():
    """Example usage"""
    checker = DataIntegrityChecker(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Run all checks
        report = checker.run_all_checks()

        # Print summary
        print("\n=== Data Integrity Report ===")
        print(f"Total Issues: {report['summary']['total_issues']}")
        print(f"Critical: {report['summary']['critical']}")
        print(f"Warnings: {report['summary']['warnings']}")
        print(f"Info: {report['summary']['info']}")
        print(f"Health Score: {report['summary']['health_score']}/100")

        # Print critical issues
        if report['by_severity']['critical']:
            print("\n=== Critical Issues ===")
            for issue in report['by_severity']['critical']:
                print(f"- {issue['description']}")
                if issue['affected']:
                    print(f"  Affected: {', '.join(issue['affected'])}")

        # Export full report
        checker.export_report("/tmp/integrity_report.json")

        # Auto-fix (dry run)
        fixed, failed = checker.auto_fix(dry_run=True)
        print(f"\nAuto-fix DRY RUN: {fixed} fixable, {failed} require manual intervention")

    finally:
        checker.close()


if __name__ == "__main__":
    main()
