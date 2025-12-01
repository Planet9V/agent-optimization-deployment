#!/usr/bin/env python3
"""
Quick fix: Bulk import ALL CVEs without date filtering
NVD API v2.0 doesn't support year-based date filters - use pagination only
"""

import requests
import time
import yaml
from neo4j import GraphDatabase

# Load config
with open('config.yaml') as f:
    config = yaml.safe_load(f)

API_KEY = config['nvd_api_key']
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Neo4j connection
driver = GraphDatabase.driver(
    config['neo4j']['uri'],
    auth=(config['neo4j']['user'], config['neo4j']['password'])
)

def rate_limit(request_count, window_start):
    """Enforce 50 req/30s rate limit"""
    if request_count >= 50:
        elapsed = time.time() - window_start
        if elapsed < 30:
            time.sleep(30 - elapsed)
        return 0, time.time()
    return request_count, window_start

def upsert_cve(session, cve_data):
    """Upsert CVE to Neo4j"""
    query = """
    MERGE (cve:CVE {id: $cve_id})
    SET cve.description = $description,
        cve.published_date = datetime($published),
        cve.modified_date = datetime($modified),
        cve.cvss_score = $cvss_score,
        cve.cvss_vector = $cvss_vector
    """
    session.run(query, cve_data)

# Fetch ALL CVEs using pagination
start_index = 0
total_imported = 0
request_count = 0
window_start = time.time()

print("Starting bulk import of ALL CVEs (no date filter)...")
print(f"API Key: {API_KEY[:8]}...")

while True:
    # Rate limiting
    request_count, window_start = rate_limit(request_count, window_start)

    # Fetch batch
    response = requests.get(
        NVD_API,
        params={'resultsPerPage': 2000, 'startIndex': start_index},
        headers={'apiKey': API_KEY}
    )

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text[:200]}")
        break

    data = response.json()
    vulnerabilities = data.get('vulnerabilities', [])
    total_results = data['totalResults']

    if not vulnerabilities:
        break

    # Import batch to Neo4j
    with driver.session() as session:
        for vuln in vulnerabilities:
            cve = vuln['cve']
            cve_data = {
                'cve_id': cve['id'],
                'description': cve['descriptions'][0]['value'] if cve.get('descriptions') else '',
                'published': cve.get('published', ''),
                'modified': cve.get('lastModified', ''),
                'cvss_score': None,  # Extract from metrics
                'cvss_vector': None
            }
            upsert_cve(session, cve_data)

    total_imported += len(vulnerabilities)
    request_count += 1

    print(f"Progress: {total_imported}/{total_results} CVEs ({total_imported/total_results*100:.1f}%)")

    if start_index + 2000 >= total_results:
        break

    start_index += 2000

print(f"\nBulk import complete! Imported {total_imported} CVEs")
driver.close()
