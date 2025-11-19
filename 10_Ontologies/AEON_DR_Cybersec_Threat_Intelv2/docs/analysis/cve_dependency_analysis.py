#!/usr/bin/env python3
"""
CVE Dependency Analysis Script
Analyzes relationships and dependencies for CVE nodes in Neo4j
"""

from neo4j import GraphDatabase
import json
from datetime import datetime
from collections import defaultdict

class CVEDependencyAnalyzer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'incoming_relationships': [],
            'outgoing_relationships': [],
            'relationship_properties': {},
            'node_counts': {},
            'sample_relationships': {},
            'orphan_risk': {},
            'reconstruction_complexity': {}
        }

    def close(self):
        self.driver.close()

    def analyze_incoming_relationships(self):
        """Analyze all relationships pointing TO CVE nodes"""
        print("Analyzing incoming relationships to CVE nodes...")
        with self.driver.session() as session:
            result = session.run("""
                MATCH (other)-[r]->(cve:CVE)
                RETURN DISTINCT labels(other) as source_labels,
                       type(r) as rel_type,
                       count(*) as count
                ORDER BY count DESC
            """)

            incoming = []
            for record in result:
                incoming.append({
                    'source_labels': record['source_labels'],
                    'relationship_type': record['rel_type'],
                    'count': record['count']
                })
                print(f"  {record['source_labels']} -[{record['rel_type']}]-> CVE: {record['count']:,}")

            self.results['incoming_relationships'] = incoming
            return incoming

    def analyze_outgoing_relationships(self):
        """Analyze all relationships FROM CVE nodes"""
        print("\nAnalyzing outgoing relationships from CVE nodes...")
        with self.driver.session() as session:
            result = session.run("""
                MATCH (cve:CVE)-[r]->(other)
                RETURN DISTINCT labels(other) as target_labels,
                       type(r) as rel_type,
                       count(*) as count
                ORDER BY count DESC
            """)

            outgoing = []
            for record in result:
                outgoing.append({
                    'target_labels': record['target_labels'],
                    'relationship_type': record['rel_type'],
                    'count': record['count']
                })
                print(f"  CVE -[{record['rel_type']}]-> {record['target_labels']}: {record['count']:,}")

            self.results['outgoing_relationships'] = outgoing
            return outgoing

    def analyze_relationship_properties(self):
        """Sample relationship properties to identify metadata"""
        print("\nAnalyzing relationship properties...")
        with self.driver.session() as session:
            # Sample incoming relationships
            incoming_props = session.run("""
                MATCH (other)-[r]->(cve:CVE)
                WITH type(r) as rel_type, r
                LIMIT 100
                RETURN rel_type, keys(r) as prop_keys, properties(r) as props
                LIMIT 10
            """)

            # Sample outgoing relationships
            outgoing_props = session.run("""
                MATCH (cve:CVE)-[r]->(other)
                WITH type(r) as rel_type, r
                LIMIT 100
                RETURN rel_type, keys(r) as prop_keys, properties(r) as props
                LIMIT 10
            """)

            rel_props = defaultdict(set)

            for record in incoming_props:
                rel_type = record['rel_type']
                for key in record['prop_keys']:
                    rel_props[f"INCOMING_{rel_type}"].add(key)
                    print(f"  INCOMING {rel_type}: {record['props']}")

            for record in outgoing_props:
                rel_type = record['rel_type']
                for key in record['prop_keys']:
                    rel_props[f"OUTGOING_{rel_type}"].add(key)
                    print(f"  OUTGOING {rel_type}: {record['props']}")

            # Convert sets to lists for JSON serialization
            self.results['relationship_properties'] = {k: list(v) for k, v in rel_props.items()}

    def count_affected_nodes(self):
        """Count nodes that would be affected by CVE deletion"""
        print("\nCounting potentially affected nodes...")
        with self.driver.session() as session:
            # SBOM nodes
            sbom_count = session.run("""
                MATCH (sbom:SBOM)-[r]-(cve:CVE)
                RETURN count(DISTINCT sbom) as count
            """).single()

            # Software nodes
            software_count = session.run("""
                MATCH (sw:Software)-[r]-(cve:CVE)
                RETURN count(DISTINCT sw) as count
            """).single()

            # Vulnerability nodes
            vuln_count = session.run("""
                MATCH (vuln:Vulnerability)-[r]-(cve:CVE)
                RETURN count(DISTINCT vuln) as count
            """).single()

            # Weakness nodes (CWE)
            weakness_count = session.run("""
                MATCH (weak:Weakness)-[r]-(cve:CVE)
                RETURN count(DISTINCT weak) as count
            """).single()

            # Product nodes
            product_count = session.run("""
                MATCH (prod:Product)-[r]-(cve:CVE)
                RETURN count(DISTINCT prod) as count
            """).single()

            counts = {
                'SBOM': sbom_count['count'] if sbom_count else 0,
                'Software': software_count['count'] if software_count else 0,
                'Vulnerability': vuln_count['count'] if vuln_count else 0,
                'Weakness': weakness_count['count'] if weakness_count else 0,
                'Product': product_count['count'] if product_count else 0
            }

            for node_type, count in counts.items():
                print(f"  {node_type} nodes connected to CVEs: {count:,}")

            self.results['node_counts'] = counts
            return counts

    def sample_cve_nodes(self):
        """Sample CVE nodes to understand current data structure"""
        print("\nSampling CVE node structure...")
        with self.driver.session() as session:
            samples = session.run("""
                MATCH (cve:CVE)
                RETURN cve.id as id,
                       cve.cve_id as cve_id,
                       keys(cve) as properties
                LIMIT 10
            """)

            sample_data = []
            for record in samples:
                sample_data.append({
                    'id': record['id'],
                    'cve_id': record['cve_id'],
                    'properties': record['properties']
                })
                print(f"  {record['id']} (cve_id: {record['cve_id']})")
                print(f"    Properties: {record['properties']}")

            self.results['sample_cve_nodes'] = sample_data

    def assess_orphan_risk(self):
        """Assess risk of orphaning data by deleting CVEs"""
        print("\nAssessing orphan risk...")
        with self.driver.session() as session:
            # Check for nodes ONLY connected to CVEs
            only_cve_connections = session.run("""
                MATCH (n)
                WHERE NOT n:CVE
                WITH n,
                     [(n)-[]-(other) | labels(other)] as connected_labels
                WITH n,
                     [label IN connected_labels WHERE label <> ['CVE']] as non_cve_labels
                WHERE size(non_cve_labels) = 0 AND size(connected_labels) > 0
                RETURN labels(n) as node_labels, count(n) as count
            """)

            orphan_risk = []
            for record in only_cve_connections:
                risk_entry = {
                    'node_type': record['node_labels'],
                    'count': record['count'],
                    'risk': 'HIGH - Only connected to CVE nodes'
                }
                orphan_risk.append(risk_entry)
                print(f"  {record['node_labels']}: {record['count']:,} nodes only connected to CVEs")

            self.results['orphan_risk'] = orphan_risk

    def analyze_cve_id_references(self):
        """Check if relationships can be reconstructed from CVE ID properties"""
        print("\nAnalyzing CVE ID references in other nodes...")
        with self.driver.session() as session:
            # Check for CVE ID properties in non-CVE nodes
            cve_refs = session.run("""
                MATCH (n)
                WHERE NOT n:CVE
                WITH n, [key IN keys(n) WHERE key =~ '(?i).*cve.*'] as cve_keys
                WHERE size(cve_keys) > 0
                RETURN labels(n) as node_labels,
                       cve_keys,
                       count(n) as count
            """)

            references = []
            for record in cve_refs:
                ref_entry = {
                    'node_type': record['node_labels'],
                    'cve_properties': record['cve_keys'],
                    'count': record['count'],
                    'reconstruction_potential': 'HIGH - Can use CVE ID properties'
                }
                references.append(ref_entry)
                print(f"  {record['node_labels']} has CVE properties {record['cve_keys']}: {record['count']:,}")

            self.results['cve_id_references'] = references

    def estimate_nvd_import_timeline(self, total_cves=267487, has_api_key=False):
        """Estimate time needed for NVD API re-import"""
        print("\nEstimating NVD API re-import timeline...")

        # API rate limits
        if has_api_key:
            requests_per_30s = 50
            batch_size = 2000  # CVEs per request
        else:
            requests_per_30s = 5
            batch_size = 2000

        total_requests = (total_cves + batch_size - 1) // batch_size
        batches_per_30s = requests_per_30s

        time_30s_intervals = (total_requests + batches_per_30s - 1) // batches_per_30s
        total_seconds = time_30s_intervals * 30

        hours = total_seconds / 3600
        days = hours / 24

        timeline = {
            'total_cves': total_cves,
            'api_key_available': has_api_key,
            'requests_per_30s': requests_per_30s,
            'batch_size': batch_size,
            'total_requests': total_requests,
            'estimated_seconds': total_seconds,
            'estimated_hours': round(hours, 2),
            'estimated_days': round(days, 2),
            'recommendation': 'Use API key for faster import' if not has_api_key else 'Acceptable timeline with API key'
        }

        print(f"  Total CVEs: {total_cves:,}")
        print(f"  API Key: {'Yes' if has_api_key else 'No'}")
        print(f"  Rate Limit: {requests_per_30s} requests/30s")
        print(f"  Total Requests: {total_requests:,}")
        print(f"  Estimated Time: {hours:.2f} hours ({days:.2f} days)")

        self.results['nvd_import_timeline'] = timeline
        return timeline

    def generate_report(self):
        """Generate comprehensive feasibility report"""
        print("\n" + "="*60)
        print("CVE RE-IMPORT FEASIBILITY REPORT")
        print("="*60)

        report = {
            'executive_summary': {
                'total_cve_nodes': 267487,
                'malformed_ids': 267487,
                'needs_normalization': 179522,
                'analysis_timestamp': self.results['timestamp']
            },
            'dependency_analysis': {
                'incoming_relationships': self.results['incoming_relationships'],
                'outgoing_relationships': self.results['outgoing_relationships'],
                'relationship_metadata': self.results['relationship_properties']
            },
            'impact_assessment': {
                'affected_node_counts': self.results['node_counts'],
                'orphan_risk': self.results['orphan_risk'],
                'reconstruction_potential': self.results.get('cve_id_references', [])
            },
            'import_timeline': self.results['nvd_import_timeline'],
            'recommendations': [],
            'critical_blockers': [],
            'risk_level': 'MEDIUM'
        }

        # Generate recommendations based on findings
        if self.results['orphan_risk']:
            report['recommendations'].append({
                'priority': 'HIGH',
                'action': 'Export orphan-risk nodes before deletion',
                'reason': f"{sum(r['count'] for r in self.results['orphan_risk']):,} nodes only connected to CVEs"
            })

        if self.results.get('cve_id_references'):
            report['recommendations'].append({
                'priority': 'MEDIUM',
                'action': 'Implement relationship reconstruction from CVE ID properties',
                'reason': 'Multiple node types contain CVE ID references for reconstruction'
            })

        # Determine critical blockers
        total_affected = sum(self.results['node_counts'].values())
        if total_affected > 100000:
            report['critical_blockers'].append({
                'issue': 'High-volume relationship reconstruction required',
                'impact': f"{total_affected:,} nodes need relationship recreation",
                'mitigation': 'Implement batch relationship creation from CVE IDs'
            })

        # Risk assessment
        if self.results['orphan_risk']:
            report['risk_level'] = 'HIGH'
            report['critical_blockers'].append({
                'issue': 'Potential data orphaning',
                'impact': 'Nodes with only CVE connections will become isolated',
                'mitigation': 'Pre-export affected data and verify reconstruction logic'
            })

        self.results['final_report'] = report
        return report

    def save_results(self, filepath):
        """Save analysis results to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {filepath}")

    def run_full_analysis(self):
        """Execute complete analysis workflow"""
        print("Starting CVE Dependency Analysis...")
        print("="*60)

        self.analyze_incoming_relationships()
        self.analyze_outgoing_relationships()
        self.analyze_relationship_properties()
        self.count_affected_nodes()
        self.sample_cve_nodes()
        self.assess_orphan_risk()
        self.analyze_cve_id_references()
        self.estimate_nvd_import_timeline(has_api_key=True)

        report = self.generate_report()

        return report

if __name__ == "__main__":
    analyzer = CVEDependencyAnalyzer(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="neo4j@openspg"
    )

    try:
        report = analyzer.run_full_analysis()

        # Save results
        output_path = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DR_Cybersec_Threat_Intelv2/docs/analysis/cve_reimport_feasibility.json"
        analyzer.save_results(output_path)

        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Risk Level: {report['risk_level']}")
        print(f"Critical Blockers: {len(report['critical_blockers'])}")
        print(f"Recommendations: {len(report['recommendations'])}")
        print("\nCritical Blockers:")
        for blocker in report['critical_blockers']:
            print(f"  - {blocker['issue']}")
            print(f"    Impact: {blocker['impact']}")
            print(f"    Mitigation: {blocker['mitigation']}")

        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  [{rec['priority']}] {rec['action']}")
            print(f"    Reason: {rec['reason']}")

    finally:
        analyzer.close()
