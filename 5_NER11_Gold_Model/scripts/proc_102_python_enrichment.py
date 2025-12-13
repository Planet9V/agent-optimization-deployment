#!/usr/bin/env python3
"""
PROC-102: Kaggle CVE/CWE Enrichment - Python Implementation
Handles CSV parsing issues with proper quoting and error handling
"""

import csv
import sys
from neo4j import GraphDatabase
from datetime import datetime

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "neo4j@openspg"
CSV_PATH = "/tmp/kaggle_enrichment/CVE_CWE_2025.csv"
BATCH_SIZE = 5000

def connect_neo4j():
    """Connect to Neo4j"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    return driver

def enrich_cvss_batch(tx, batch):
    """Enrich CVEs with CVSS scores in batch"""
    query = """
    UNWIND $records AS record
    MATCH (cve:CVE {id: record.cve_id})
    SET cve.cvssV31BaseScore = record.cvss_v3,
        cve.cvssV2BaseScore = record.cvss_v2,
        cve.cvssV4BaseScore = record.cvss_v4,
        cve.cvssV31BaseSeverity = record.severity,
        cve.kaggle_enriched = datetime()
    RETURN count(*) as enriched
    """
    result = tx.run(query, records=batch)
    return result.single()["enriched"]

def create_cwe_relationships_batch(tx, batch):
    """Create CVE->CWE relationships in batch"""
    query = """
    UNWIND $records AS record
    MATCH (cve:CVE {id: record.cve_id})
    MERGE (cwe:CWE {id: record.cwe_id})
    ON CREATE SET cwe.source = 'kaggle:cve_cwe_2025',
                  cwe.created_timestamp = datetime()
    MERGE (cve)-[r:IS_WEAKNESS_TYPE]->(cwe)
    ON CREATE SET r.source = 'kaggle:cve_cwe_2025',
                  r.created_timestamp = datetime()
    RETURN count(*) as relationships
    """
    result = tx.run(query, records=batch)
    return result.single()["relationships"]

def parse_float_safe(value):
    """Safely parse float, return None if invalid"""
    if not value or value.strip() == '':
        return None
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return None

def main():
    print(f"[{datetime.now()}] Starting PROC-102 Kaggle Enrichment")

    # Connect to Neo4j
    print(f"[{datetime.now()}] Connecting to Neo4j...")
    driver = connect_neo4j()

    # Create CWE constraint
    print(f"[{datetime.now()}] Creating CWE constraint...")
    with driver.session(database="neo4j") as session:
        session.run("CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE")

    # Process CSV
    print(f"[{datetime.now()}] Processing CSV file: {CSV_PATH}")

    cvss_batch = []
    cwe_batch = []
    processed = 0
    enriched_count = 0
    cwe_rel_count = 0
    errors = 0

    try:
        with open(CSV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)

            for row in reader:
                processed += 1

                try:
                    cve_id = row.get('CVE-ID', '').strip()
                    if not cve_id or not cve_id.startswith('CVE-'):
                        continue

                    # Parse CVSS scores
                    cvss_v3 = parse_float_safe(row.get('CVSS-V3'))
                    cvss_v2 = parse_float_safe(row.get('CVSS-V2'))
                    cvss_v4 = parse_float_safe(row.get('CVSS-V4'))
                    severity = row.get('SEVERITY', '').strip().upper() if row.get('SEVERITY') else None

                    # Add to CVSS batch if any score exists
                    if cvss_v3 or cvss_v2 or cvss_v4:
                        cvss_batch.append({
                            'cve_id': cve_id,
                            'cvss_v3': cvss_v3,
                            'cvss_v2': cvss_v2,
                            'cvss_v4': cvss_v4,
                            'severity': severity
                        })

                    # Parse CWE
                    cwe_id = row.get('CWE-ID', '').strip()
                    if cwe_id and cwe_id not in ['', 'NVD-CWE-Other', 'NVD-CWE-noinfo']:
                        cwe_batch.append({
                            'cve_id': cve_id,
                            'cwe_id': cwe_id
                        })

                    # Process batches
                    if len(cvss_batch) >= BATCH_SIZE:
                        with driver.session(database="neo4j") as session:
                            count = session.execute_write(enrich_cvss_batch, cvss_batch)
                            enriched_count += count
                        print(f"[{datetime.now()}] Enriched {enriched_count} CVEs (batch {processed // BATCH_SIZE})")
                        cvss_batch = []

                    if len(cwe_batch) >= BATCH_SIZE:
                        with driver.session(database="neo4j") as session:
                            count = session.execute_write(create_cwe_relationships_batch, cwe_batch)
                            cwe_rel_count += count
                        print(f"[{datetime.now()}] Created {cwe_rel_count} CWE relationships (batch {processed // BATCH_SIZE})")
                        cwe_batch = []

                except Exception as e:
                    errors += 1
                    if errors % 100 == 0:
                        print(f"[{datetime.now()}] WARNING: {errors} errors encountered (last: {str(e)[:100]})")

                if processed % 10000 == 0:
                    print(f"[{datetime.now()}] Processed {processed} rows...")

        # Process remaining batches
        if cvss_batch:
            with driver.session(database="neo4j") as session:
                count = session.execute_write(enrich_cvss_batch, cvss_batch)
                enriched_count += count

        if cwe_batch:
            with driver.session(database="neo4j") as session:
                count = session.execute_write(create_cwe_relationships_batch, cwe_batch)
                cwe_rel_count += count

        print(f"\n[{datetime.now()}] ========================================")
        print(f"PROC-102 COMPLETED")
        print(f"Total rows processed: {processed}")
        print(f"CVEs enriched with CVSS: {enriched_count}")
        print(f"CWE relationships created: {cwe_rel_count}")
        print(f"Errors encountered: {errors}")
        print(f"========================================\n")

    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {str(e)}")
        sys.exit(1)
    finally:
        driver.close()

if __name__ == "__main__":
    main()
