#!/usr/bin/env python3
"""
Comprehensive Attack Chain Analysis
Evaluates current Neo4j state + STIX data + ICS-SEC-KG for complete attack chain coverage
"""

import json
from neo4j import GraphDatabase
from pathlib import Path
from collections import defaultdict

# Database connection
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'neo4j@openspg'))

def analyze_neo4j_coverage():
    """Analyze current Neo4j attack chain coverage"""
    results = {}

    with driver.session() as session:
        # 1. Node counts
        result = session.run("""
            MATCH (n)
            RETURN labels(n)[0] as label, count(n) as count
            ORDER BY count DESC
        """)
        results['node_counts'] = {r['label']: r['count'] for r in result}

        # 2. CVE→CWE relationships
        result = session.run("""
            MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
            RETURN count(r) as count
        """)
        results['cve_cwe_rels'] = result.single()['count']

        # 3. CWE→CAPEC relationships
        result = session.run("""
            MATCH (cwe:CWE)-[r:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            RETURN count(r) as count
        """)
        results['cwe_capec_rels'] = result.single()['count']

        # 4. CAPEC→ATT&CK relationships
        result = session.run("""
            MATCH (capec:CAPEC)-[r:USES_TECHNIQUE]->(att:AttackTechnique)
            RETURN count(r) as count
        """)
        results['capec_attack_rels'] = result.single()['count']

        # 5. Complete chains (CVE→CWE→CAPEC→ATT&CK)
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                  -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                  -[:USES_TECHNIQUE]->(att:AttackTechnique)
            RETURN count(DISTINCT cve) as complete_chains
        """)
        results['complete_chains'] = result.single()['complete_chains']

        # 6. CVE with ANY path to ATT&CK
        result = session.run("""
            MATCH (cve:CVE)-[*1..4]-(att:AttackTechnique)
            RETURN count(DISTINCT cve) as cve_with_attack_paths
        """)
        results['cve_with_attack_paths'] = result.single()['cve_with_attack_paths']

        # 7. ATT&CK techniques reachable from CVE
        result = session.run("""
            MATCH (cve:CVE)-[*1..4]-(att:AttackTechnique)
            RETURN count(DISTINCT att) as reachable_techniques
        """)
        results['reachable_attack_techniques'] = result.single()['reachable_techniques']

        # 8. CWE overlap between CVE and CAPEC
        result = session.run("""
            MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe1:CWE)
            WITH collect(DISTINCT cwe1.id) as cve_cwes
            MATCH (cwe2:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
            WITH cve_cwes, collect(DISTINCT cwe2.id) as capec_cwes
            RETURN
                size(cve_cwes) as cve_cwe_count,
                size(capec_cwes) as capec_cwe_count,
                size([x IN cve_cwes WHERE x IN capec_cwes]) as overlap_count
        """)
        overlap = result.single()
        results['cwe_overlap'] = {
            'cve_cwes': overlap['cve_cwe_count'],
            'capec_cwes': overlap['capec_cwe_count'],
            'overlap': overlap['overlap_count'],
            'overlap_pct': round(overlap['overlap_count'] / max(overlap['cve_cwe_count'], 1) * 100, 2)
        }

        # 9. Sample complete chain (if any exist)
        result = session.run("""
            MATCH path=(cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                      -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                      -[:USES_TECHNIQUE]->(att:AttackTechnique)
            RETURN
                cve.id as cve_id,
                cwe.id as cwe_id,
                capec.capecId as capec_id,
                att.techniqueId as attack_id
            LIMIT 5
        """)
        results['sample_chains'] = [dict(r) for r in result]

    return results

def analyze_stix_mappings():
    """Analyze MITRE ATT&CK STIX data for CVE references"""
    stix_file = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/MITRE-ATT-CK-STIX/enterprise-attack/enterprise-attack-17.0.json')

    if not stix_file.exists():
        return {'error': 'STIX file not found'}

    with open(stix_file, 'r') as f:
        data = json.load(f)

    cve_mappings = []
    technique_cve_map = defaultdict(list)

    for obj in data.get('objects', []):
        if obj.get('type') in ['attack-pattern', 'malware', 'tool', 'intrusion-set']:
            ext_refs = obj.get('external_references', [])
            obj_id = obj.get('id', '')
            obj_name = obj.get('name', '')

            cves = []
            mitre_id = None

            for ref in ext_refs:
                source = ref.get('source_name', '')
                ext_id = ref.get('external_id', '')

                if 'mitre-attack' in source.lower():
                    mitre_id = ext_id
                elif 'cve' in source.lower() or ext_id.startswith('CVE-'):
                    cves.append(ext_id)

            if cves and mitre_id:
                for cve in cves:
                    cve_mappings.append({
                        'cve': cve,
                        'attack_id': mitre_id,
                        'attack_name': obj_name,
                        'type': obj.get('type')
                    })
                    technique_cve_map[mitre_id].append(cve)

    return {
        'total_cve_references': len(cve_mappings),
        'unique_cves': len(set(m['cve'] for m in cve_mappings)),
        'unique_techniques': len(technique_cve_map),
        'sample_mappings': cve_mappings[:10],
        'techniques_with_most_cves': sorted(
            [(k, len(v)) for k, v in technique_cve_map.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
    }

def check_ics_sec_kg():
    """Check ICS-SEC-KG for existing mappings"""
    kg_dir = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/ICS-SEC-KG/src/main/resources/owl')

    if not kg_dir.exists():
        return {'error': 'ICS-SEC-KG directory not found'}

    results = {
        'files_found': [],
        'cross_references': {}
    }

    for owl_file in kg_dir.glob('*.ttl'):
        results['files_found'].append(owl_file.name)

        # Check for cross-references
        content = owl_file.read_text()

        has_cve = 'CVE' in content or 'cve' in content
        has_cwe = 'CWE' in content or 'cwe' in content
        has_capec = 'CAPEC' in content or 'capec' in content
        has_attack = 'attack' in content.lower() or 'ATTACK' in content

        if any([has_cve, has_cwe, has_capec, has_attack]):
            results['cross_references'][owl_file.name] = {
                'has_cve': has_cve,
                'has_cwe': has_cwe,
                'has_capec': has_capec,
                'has_attack': has_attack
            }

    return results

def main():
    print("="*80)
    print("COMPREHENSIVE ATTACK CHAIN ANALYSIS")
    print("="*80)
    print()

    # Part 1: Neo4j current state
    print("📊 PART 1: Neo4j Database Current State")
    print("-"*80)
    neo4j_results = analyze_neo4j_coverage()

    print(f"\n🔢 Node Counts:")
    for label, count in list(neo4j_results['node_counts'].items())[:10]:
        print(f"  {label:30s}: {count:,}")

    print(f"\n🔗 Relationship Coverage:")
    print(f"  CVE→CWE relationships:        {neo4j_results['cve_cwe_rels']:,}")
    print(f"  CWE→CAPEC relationships:      {neo4j_results['cwe_capec_rels']:,}")
    print(f"  CAPEC→ATT&CK relationships:   {neo4j_results['capec_attack_rels']:,}")
    print(f"  Complete chains (CVE→ATT&CK): {neo4j_results['complete_chains']:,}")
    print(f"  CVEs with ANY ATT&CK path:    {neo4j_results['cve_with_attack_paths']:,}")
    print(f"  ATT&CK techniques reachable:  {neo4j_results['reachable_attack_techniques']:,}")

    print(f"\n⚠️  CWE Overlap Analysis:")
    overlap = neo4j_results['cwe_overlap']
    print(f"  CVE-connected CWEs:  {overlap['cve_cwes']}")
    print(f"  CAPEC-connected CWEs: {overlap['capec_cwes']}")
    print(f"  Overlap count:        {overlap['overlap']}")
    print(f"  Overlap percentage:   {overlap['overlap_pct']}%")

    if neo4j_results['sample_chains']:
        print(f"\n✅ Sample Complete Chains:")
        for i, chain in enumerate(neo4j_results['sample_chains'], 1):
            print(f"  {i}. {chain['cve_id']} → {chain['cwe_id']} → {chain['capec_id']} → {chain['attack_id']}")
    else:
        print(f"\n❌ No complete CVE→CWE→CAPEC→ATT&CK chains found in database")

    # Part 2: MITRE ATT&CK STIX analysis
    print(f"\n\n📚 PART 2: MITRE ATT&CK STIX Data Analysis")
    print("-"*80)
    stix_results = analyze_stix_mappings()

    if 'error' not in stix_results:
        print(f"\n✅ STIX CVE→ATT&CK Mappings Found:")
        print(f"  Total CVE references:     {stix_results['total_cve_references']:,}")
        print(f"  Unique CVEs:              {stix_results['unique_cves']:,}")
        print(f"  Unique ATT&CK techniques: {stix_results['unique_techniques']:,}")

        print(f"\n📋 Sample CVE→ATT&CK Mappings:")
        for mapping in stix_results['sample_mappings'][:5]:
            print(f"  {mapping['cve']:15s} → {mapping['attack_id']:10s} ({mapping['attack_name']})")

        print(f"\n🔝 Techniques with Most CVE References:")
        for tech_id, cve_count in stix_results['techniques_with_most_cves'][:5]:
            print(f"  {tech_id:10s}: {cve_count} CVEs")
    else:
        print(f"\n❌ {stix_results['error']}")

    # Part 3: ICS-SEC-KG analysis
    print(f"\n\n🏗️  PART 3: ICS-SEC-KG Ontology Analysis")
    print("-"*80)
    kg_results = check_ics_sec_kg()

    if 'error' not in kg_results:
        print(f"\n📁 OWL Files Found: {len(kg_results['files_found'])}")
        for filename in kg_results['files_found']:
            print(f"  - {filename}")

        print(f"\n🔗 Cross-Reference Analysis:")
        for filename, refs in kg_results['cross_references'].items():
            has_refs = [k for k, v in refs.items() if v]
            if has_refs:
                print(f"  {filename:20s}: {', '.join(has_refs)}")
    else:
        print(f"\n❌ {kg_results['error']}")

    # Summary and recommendations
    print(f"\n\n🎯 CRITICAL FINDINGS & RECOMMENDATIONS")
    print("="*80)

    # Calculate gap
    total_cves = neo4j_results['node_counts'].get('CVE', 0)
    cves_with_chains = neo4j_results['complete_chains']
    gap_pct = 100 - (cves_with_chains / max(total_cves, 1) * 100)

    print(f"\n📉 Current Attack Chain Coverage:")
    print(f"  Total CVEs in database:        {total_cves:,}")
    print(f"  CVEs with complete chains:     {cves_with_chains:,}")
    print(f"  Coverage gap:                  {gap_pct:.2f}%")

    print(f"\n🔍 Root Causes Identified:")
    if overlap['overlap_pct'] < 5:
        print(f"  ❌ CRITICAL: CWE overlap only {overlap['overlap_pct']}% - semantic mismatch")
        print(f"     → CVEs use implementation CWEs, CAPECs use attack CWEs")

    if neo4j_results['cve_cwe_rels'] < total_cves * 0.3:
        print(f"  ⚠️  WARNING: Only {neo4j_results['cve_cwe_rels']:,} CVE→CWE relationships")
        print(f"     → {total_cves - neo4j_results['cve_cwe_rels']:,} CVEs lack CWE classification")

    print(f"\n💡 Available Solutions:")

    if stix_results.get('unique_cves', 0) > 0:
        print(f"  ✅ SOLUTION 1: MITRE STIX CVE→ATT&CK Direct Mappings")
        print(f"     → {stix_results['unique_cves']:,} CVEs already mapped to ATT&CK techniques")
        print(f"     → Import these mappings to bypass CWE semantic gap")
        print(f"     → Create direct CVE→AttackTechnique relationships")

    if kg_results.get('cross_references'):
        integrated_file = kg_results['cross_references'].get('integrated.ttl', {})
        if integrated_file.get('has_cve') and integrated_file.get('has_attack'):
            print(f"  ✅ SOLUTION 2: ICS-SEC-KG Integrated Ontology")
            print(f"     → Existing OWL ontology with CVE↔ATT&CK mappings")
            print(f"     → Import semantic relationships from TTL files")
            print(f"     → Leverage ontology reasoning for inference")

    print(f"\n🚀 Recommended Approach:")
    print(f"  1. Import MITRE STIX CVE→ATT&CK direct mappings ({stix_results.get('unique_cves', 0):,} CVEs)")
    print(f"  2. Import ICS-SEC-KG ontology relationships as backup/validation")
    print(f"  3. Use CAPEC as conceptual bridge for unmapped CVEs")
    print(f"  4. Train NER + Relation Extraction on combined dataset")
    print(f"  5. Enable graph reasoning for inference-time chain completion")

    # Save results
    output = {
        'analysis_date': '2025-11-08',
        'neo4j_state': neo4j_results,
        'stix_mappings': stix_results,
        'ics_sec_kg': kg_results
    }

    output_file = Path('docs/COMPREHENSIVE_ATTACK_CHAIN_ANALYSIS.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n📄 Full results saved to: {output_file}")
    print()

if __name__ == '__main__':
    main()
    driver.close()
