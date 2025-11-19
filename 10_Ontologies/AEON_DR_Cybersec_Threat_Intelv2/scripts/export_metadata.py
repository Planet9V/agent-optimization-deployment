#!/usr/bin/env python3
"""
Export Critical Metadata Before CVE Deletion
Created: 2025-11-01
Purpose: Export all critical relationship metadata for reconstruction after clean CVE re-import
"""

import json
import csv
import logging
from datetime import datetime
from neo4j import GraphDatabase
from neo4j.time import DateTime, Date
from pathlib import Path

# Custom JSON encoder for Neo4j DateTime and Date objects
class Neo4jDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (DateTime, Date)):
            return obj.iso_format()
        return super().default(obj)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"
EXPORT_DIR = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DR_Cybersec_Threat_Intelv2/exports")
TIMESTAMP = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

class MetadataExporter:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.export_dir = EXPORT_DIR / f"metadata_export_{TIMESTAMP}"
        self.export_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Export directory: {self.export_dir}")

    def close(self):
        self.driver.close()

    def export_grid_stability_relationships(self):
        """Export THREATENS_GRID_STABILITY relationships (CRITICAL)"""
        logger.info("Exporting THREATENS_GRID_STABILITY relationships...")

        query = """
        MATCH (n)-[r:THREATENS_GRID_STABILITY]->(cve:CVE)
        RETURN
            id(n) as source_node_id,
            labels(n)[0] as source_label,
            n.id as source_id,
            cve.id as cve_id,
            r.population_impact as population_impact,
            r.grid_severity as grid_severity,
            r.cascade_risk as cascade_risk,
            r.recovery_time_hours as recovery_time_hours,
            properties(r) as all_properties
        ORDER BY cve.id
        """

        with self.driver.session() as session:
            result = session.run(query)
            records = list(result)

        # Export as both CSV and JSON
        csv_file = self.export_dir / "threatens_grid_stability.csv"
        json_file = self.export_dir / "threatens_grid_stability.json"

        # CSV export
        if records:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                for record in records:
                    # Convert all_properties dict to JSON string for CSV
                    row = dict(record)
                    row['all_properties'] = json.dumps(row['all_properties'], cls=Neo4jDateTimeEncoder)
                    writer.writerow(row)

        # JSON export (preserves nested structures)
        with open(json_file, 'w') as f:
            json.dump([dict(record) for record in records], f, indent=2, cls=Neo4jDateTimeEncoder)

        logger.info(f"Exported {len(records)} THREATENS_GRID_STABILITY relationships")
        return len(records)

    def export_vulnerable_to_relationships(self):
        """Export VULNERABLE_TO relationships (24,000+ relationships)"""
        logger.info("Exporting VULNERABLE_TO relationships...")

        query = """
        MATCH (n)-[r:VULNERABLE_TO]->(cve:CVE)
        RETURN
            labels(n)[0] as source_label,
            n.id as source_id,
            cve.id as cve_id,
            r.cve_id as relationship_cve_id,
            r.severity as severity,
            r.exploitability as exploitability,
            properties(r) as all_properties
        ORDER BY cve.id
        """

        with self.driver.session() as session:
            result = session.run(query)
            records = list(result)

        csv_file = self.export_dir / "vulnerable_to_relationships.csv"
        json_file = self.export_dir / "vulnerable_to_relationships.json"

        if records:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                for record in records:
                    row = dict(record)
                    row['all_properties'] = json.dumps(row['all_properties'], cls=Neo4jDateTimeEncoder)
                    writer.writerow(row)

        with open(json_file, 'w') as f:
            json.dump([dict(record) for record in records], f, indent=2, cls=Neo4jDateTimeEncoder)

        logger.info(f"Exported {len(records)} VULNERABLE_TO relationships")
        return len(records)

    def export_all_cve_relationships(self):
        """Export all relationships with cve_id properties"""
        logger.info("Exporting all CVE relationships with cve_id properties...")

        query = """
        MATCH (cve:CVE)-[r]-(n)
        WHERE r.cve_id IS NOT NULL
        RETURN
            cve.id as cve_id,
            type(r) as relationship_type,
            labels(n)[0] as connected_node_label,
            n.id as connected_node_id,
            r.cve_id as relationship_cve_id,
            properties(r) as all_properties
        ORDER BY cve.id, type(r)
        """

        with self.driver.session() as session:
            result = session.run(query)
            records = list(result)

        csv_file = self.export_dir / "all_cve_relationships.csv"
        json_file = self.export_dir / "all_cve_relationships.json"

        if records:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                for record in records:
                    row = dict(record)
                    row['all_properties'] = json.dumps(row['all_properties'], cls=Neo4jDateTimeEncoder)
                    writer.writerow(row)

        with open(json_file, 'w') as f:
            json.dump([dict(record) for record in records], f, indent=2, cls=Neo4jDateTimeEncoder)

        logger.info(f"Exported {len(records)} CVE relationships with cve_id properties")
        return len(records)

    def export_cve_node_properties(self):
        """Export CVE node properties for validation"""
        logger.info("Exporting CVE node properties...")

        query = """
        MATCH (cve:CVE)
        WHERE cve.id IS NOT NULL
        RETURN
            cve.id as cve_id,
            cve.description as description,
            cve.published_date as published_date,
            cve.modified_date as modified_date,
            cve.cvss_score as cvss_score,
            cve.cvss_vector as cvss_vector,
            cve.epss_score as epss_score,
            cve.epss_percentile as epss_percentile,
            properties(cve) as all_properties
        ORDER BY cve.id
        """

        with self.driver.session() as session:
            result = session.run(query)
            records = list(result)

        csv_file = self.export_dir / "cve_node_properties.csv"
        json_file = self.export_dir / "cve_node_properties.json"

        if records:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                for record in records:
                    row = dict(record)
                    row['all_properties'] = json.dumps(row['all_properties'], cls=Neo4jDateTimeEncoder)
                    writer.writerow(row)

        with open(json_file, 'w') as f:
            json.dump([dict(record) for record in records], f, indent=2, cls=Neo4jDateTimeEncoder)

        logger.info(f"Exported {len(records)} CVE node properties")
        return len(records)

    def export_summary_statistics(self):
        """Export database statistics before deletion"""
        logger.info("Collecting database statistics...")

        with self.driver.session() as session:
            # Total CVEs
            total_cves = session.run("MATCH (cve:CVE) RETURN count(cve) as count").single()['count']

            # Total relationships
            total_rels = session.run("MATCH (cve:CVE)-[r]-() RETURN count(r) as count").single()['count']

            # Relationship types
            rel_types = session.run("""
                MATCH (cve:CVE)-[r]-()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            rel_type_counts = {record['rel_type']: record['count'] for record in rel_types}

            # CVE ID formats
            null_ids = session.run("MATCH (cve:CVE) WHERE cve.id IS NULL RETURN count(cve) as count").single()['count']
            malformed_ids = session.run("MATCH (cve:CVE) WHERE cve.id =~ 'cve-CVE-.*' RETURN count(cve) as count").single()['count']
            correct_ids = session.run("MATCH (cve:CVE) WHERE cve.id =~ 'CVE-.*' AND NOT cve.id =~ 'cve-CVE-.*' RETURN count(cve) as count").single()['count']

        stats = {
            'export_timestamp': TIMESTAMP,
            'total_cve_nodes': total_cves,
            'total_relationships': total_rels,
            'relationship_type_counts': rel_type_counts,
            'cve_id_formats': {
                'null_ids': null_ids,
                'malformed_ids': malformed_ids,
                'correct_ids': correct_ids
            }
        }

        stats_file = self.export_dir / "database_statistics.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)

        logger.info(f"Exported database statistics")
        return stats

    def create_export_summary(self, counts):
        """Create summary report of export"""
        summary = f"""
METADATA EXPORT SUMMARY
=======================
Export Timestamp: {TIMESTAMP}
Export Directory: {self.export_dir}

Exported Data:
- THREATENS_GRID_STABILITY relationships: {counts['grid_stability']:,}
- VULNERABLE_TO relationships: {counts['vulnerable_to']:,}
- All CVE relationships with cve_id: {counts['all_relationships']:,}
- CVE node properties: {counts['cve_properties']:,}

Database Statistics:
- Total CVE nodes: {counts['stats']['total_cve_nodes']:,}
- Total relationships: {counts['stats']['total_relationships']:,}
- NULL IDs: {counts['stats']['cve_id_formats']['null_ids']:,}
- Malformed IDs: {counts['stats']['cve_id_formats']['malformed_ids']:,}
- Correct IDs: {counts['stats']['cve_id_formats']['correct_ids']:,}

Files Created:
- threatens_grid_stability.csv & .json
- vulnerable_to_relationships.csv & .json
- all_cve_relationships.csv & .json
- cve_node_properties.csv & .json
- database_statistics.json
- EXPORT_SUMMARY.txt

Status: EXPORT COMPLETE ✅
"""

        summary_file = self.export_dir / "EXPORT_SUMMARY.txt"
        with open(summary_file, 'w') as f:
            f.write(summary)

        logger.info("\n" + summary)
        return summary

def main():
    """Main execution"""
    exporter = MetadataExporter()

    try:
        logger.info("=" * 80)
        logger.info("CRITICAL METADATA EXPORT - BEFORE CVE DELETION")
        logger.info("=" * 80)

        counts = {}

        # Export all critical data
        counts['grid_stability'] = exporter.export_grid_stability_relationships()
        counts['vulnerable_to'] = exporter.export_vulnerable_to_relationships()
        counts['all_relationships'] = exporter.export_all_cve_relationships()
        counts['cve_properties'] = exporter.export_cve_node_properties()
        counts['stats'] = exporter.export_summary_statistics()

        # Create summary report
        exporter.create_export_summary(counts)

        logger.info("=" * 80)
        logger.info("EXPORT COMPLETE")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"Fatal error during export: {str(e)}", exc_info=True)
        raise
    finally:
        exporter.close()

if __name__ == "__main__":
    main()
