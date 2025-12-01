#!/usr/bin/env python3
"""
Analyze Neo4j CVE node relationships to assess CVE ID normalization impact.
DO THE ACTUAL WORK - query the database and report findings.
"""

from neo4j import GraphDatabase
import json
from collections import defaultdict

# Database connection
BOLT_URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

def analyze_cve_relationships():
    """Execute actual database analysis - not a framework, real queries."""

    driver = GraphDatabase.driver(BOLT_URI, auth=AUTH)
    results = {
        "relationship_types": [],
        "relationship_properties": [],
        "external_references": [],
        "sample_data": [],
        "risk_assessment": {}
    }

    try:
        with driver.session() as session:

            # QUERY 1: All relationship types connected to CVE nodes
            print("Query 1: Finding all CVE relationship types...")
            rel_types_result = session.run("""
                MATCH (cve:CVE)-[r]->(other)
                RETURN DISTINCT type(r) as rel_type,
                       labels(other)[0] as target_label,
                       count(*) as outgoing_count
                ORDER BY outgoing_count DESC
            """)

            outgoing_rels = []
            for record in rel_types_result:
                outgoing_rels.append({
                    "relationship_type": record["rel_type"],
                    "target_label": record["target_label"],
                    "count": record["outgoing_count"],
                    "direction": "OUTGOING"
                })

            # Incoming relationships
            incoming_result = session.run("""
                MATCH (other)-[r]->(cve:CVE)
                RETURN DISTINCT type(r) as rel_type,
                       labels(other)[0] as source_label,
                       count(*) as incoming_count
                ORDER BY incoming_count DESC
            """)

            incoming_rels = []
            for record in incoming_result:
                incoming_rels.append({
                    "relationship_type": record["rel_type"],
                    "source_label": record["source_label"],
                    "count": record["incoming_count"],
                    "direction": "INCOMING"
                })

            results["relationship_types"] = outgoing_rels + incoming_rels

            # QUERY 2: Check relationship properties that might contain CVE IDs
            print("Query 2: Checking relationship properties...")
            prop_check_result = session.run("""
                MATCH (cve:CVE)-[r]-()
                WITH type(r) as rel_type, keys(r) as props
                UNWIND props as prop_name
                RETURN DISTINCT rel_type, collect(DISTINCT prop_name) as properties
            """)

            rel_properties = []
            for record in prop_check_result:
                rel_properties.append({
                    "relationship_type": record["rel_type"],
                    "properties": record["properties"]
                })

            results["relationship_properties"] = rel_properties

            # QUERY 3: Sample actual CVE relationships with data
            print("Query 3: Sampling actual relationship data...")
            sample_result = session.run("""
                MATCH (cve:CVE)-[r]->(other)
                WITH cve, r, other
                LIMIT 20
                RETURN cve.id as cve_id,
                       type(r) as rel_type,
                       properties(r) as rel_props,
                       labels(other)[0] as target_label,
                       other.id as target_id
            """)

            samples = []
            for record in sample_result:
                # Convert Neo4j DateTime objects to strings
                rel_props = dict(record["rel_props"]) if record["rel_props"] else {}
                for key, value in rel_props.items():
                    if hasattr(value, 'iso_format'):  # Neo4j DateTime
                        rel_props[key] = value.iso_format()

                samples.append({
                    "cve_id": record["cve_id"],
                    "relationship_type": record["rel_type"],
                    "relationship_properties": rel_props,
                    "target_label": record["target_label"],
                    "target_id": record["target_id"]
                })

            results["sample_data"] = samples

            # QUERY 4: Check if any nodes reference CVE.id in their properties
            print("Query 4: Checking for external CVE ID references...")
            external_refs_result = session.run("""
                MATCH (n)
                WHERE n.cve_id IS NOT NULL OR n.cve IS NOT NULL OR n.cve_ids IS NOT NULL
                RETURN labels(n)[0] as label,
                       count(*) as count,
                       collect(DISTINCT keys(n))[0] as sample_properties
                LIMIT 10
            """)

            external_refs = []
            for record in external_refs_result:
                external_refs.append({
                    "node_label": record["label"],
                    "count": record["count"],
                    "properties": record["sample_properties"]
                })

            results["external_references"] = external_refs

            # QUERY 5: Check CVE node properties to understand current ID format
            print("Query 5: Analyzing CVE node ID formats...")
            cve_format_result = session.run("""
                MATCH (cve:CVE)
                WHERE cve.id IS NOT NULL
                RETURN cve.id as cve_id
                LIMIT 100
            """)

            cve_id_samples = [record["cve_id"] for record in cve_format_result if record["cve_id"]]

            # Analyze ID formats
            formats = defaultdict(int)
            for cve_id in cve_id_samples:
                if cve_id:
                    if cve_id.startswith("CVE-"):
                        formats["CVE-YYYY-NNNNN"] += 1
                    elif cve_id.startswith("cve-"):
                        formats["cve-yyyy-nnnnn"] += 1
                    else:
                        formats["other"] += 1

            # QUERY 6: Check VULNERABLE_TO relationship cve_id property specifically
            print("Query 6: Analyzing VULNERABLE_TO.cve_id property values...")
            vuln_cve_id_result = session.run("""
                MATCH ()-[r:VULNERABLE_TO]->(cve:CVE)
                WHERE r.cve_id IS NOT NULL
                RETURN r.cve_id as rel_cve_id, cve.id as node_cve_id
                LIMIT 50
            """)

            vuln_cve_id_mismatches = []
            vuln_cve_id_samples = []
            for record in vuln_cve_id_result:
                rel_id = record["rel_cve_id"]
                node_id = record["node_cve_id"]
                vuln_cve_id_samples.append({"relationship_cve_id": rel_id, "node_cve_id": node_id})
                if rel_id != node_id:
                    vuln_cve_id_mismatches.append({
                        "relationship_cve_id": rel_id,
                        "node_cve_id": node_id
                    })

            results["vulnerable_to_cve_id_analysis"] = {
                "sample_count": len(vuln_cve_id_samples),
                "mismatches": vuln_cve_id_mismatches,
                "samples": vuln_cve_id_samples[:10]
            }

            # RISK ASSESSMENT
            print("Performing risk assessment...")
            risk_assessment = {
                "total_relationships": len(outgoing_rels) + len(incoming_rels),
                "relationship_types_count": len(set([r["relationship_type"] for r in results["relationship_types"]])),
                "properties_with_potential_cve_refs": len([p for p in rel_properties if any("cve" in prop.lower() for prop in p["properties"])]),
                "external_nodes_with_cve_refs": len(external_refs),
                "cve_id_format_distribution": dict(formats),
                "vulnerable_to_cve_id_property_usage": len(vuln_cve_id_samples),
                "vulnerable_to_mismatches": len(vuln_cve_id_mismatches),
                "risk_level": "UNKNOWN",
                "recommendations": []
            }

            # Determine risk level
            if risk_assessment["vulnerable_to_cve_id_property_usage"] > 0:
                risk_assessment["risk_level"] = "CRITICAL"
                risk_assessment["recommendations"].append(
                    f"CRITICAL: VULNERABLE_TO relationships store cve_id property ({risk_assessment['vulnerable_to_cve_id_property_usage']} instances found)"
                )
                if risk_assessment["vulnerable_to_mismatches"] > 0:
                    risk_assessment["recommendations"].append(
                        f"CRITICAL: {risk_assessment['vulnerable_to_mismatches']} mismatches between relationship.cve_id and CVE.id"
                    )
                risk_assessment["recommendations"].append(
                    "REQUIRED: Update all VULNERABLE_TO.cve_id properties after normalizing CVE.id"
                )
            elif risk_assessment["properties_with_potential_cve_refs"] > 0:
                risk_assessment["risk_level"] = "HIGH"
                risk_assessment["recommendations"].append(
                    "Relationships have properties that may contain CVE IDs - inspect before normalization"
                )
            elif risk_assessment["external_nodes_with_cve_refs"] > 0:
                risk_assessment["risk_level"] = "MEDIUM"
                risk_assessment["recommendations"].append(
                    "External nodes reference CVE IDs - verify reference format compatibility"
                )
            else:
                risk_assessment["risk_level"] = "LOW"
                risk_assessment["recommendations"].append(
                    "No direct property dependencies detected - normalization should be safe"
                )

            # Check if CVE.id is used as relationship endpoint
            if any(r["relationship_type"] in ["HAS_CVE", "REFERENCES_CVE", "AFFECTS_CVE"] for r in results["relationship_types"]):
                risk_assessment["recommendations"].append(
                    "Relationships use CVE node as target - ensure node matching uses normalized IDs"
                )

            results["risk_assessment"] = risk_assessment

    finally:
        driver.close()

    return results

def main():
    """Execute analysis and output results."""
    print("=" * 80)
    print("CVE RELATIONSHIP ANALYSIS - ACTUAL EXECUTION")
    print("=" * 80)

    results = analyze_cve_relationships()

    # Print summary report
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)

    print(f"\n1. RELATIONSHIP TYPES ({len(results['relationship_types'])} found):")
    print("-" * 80)
    for rel in results['relationship_types']:
        direction = "→" if rel['direction'] == "OUTGOING" else "←"
        target = rel.get('target_label') or rel.get('source_label')
        print(f"  {direction} {rel['relationship_type']:30} to {target:20} (count: {rel['count']})")

    print(f"\n2. RELATIONSHIP PROPERTIES ({len(results['relationship_properties'])} types):")
    print("-" * 80)
    for rel_prop in results['relationship_properties']:
        print(f"  {rel_prop['relationship_type']:30} → {', '.join(rel_prop['properties'])}")

    print(f"\n3. SAMPLE RELATIONSHIP DATA (first 20):")
    print("-" * 80)
    for i, sample in enumerate(results['sample_data'][:5], 1):  # Show first 5
        print(f"  Sample {i}:")
        print(f"    CVE: {sample['cve_id']}")
        print(f"    Relationship: {sample['relationship_type']} → {sample['target_label']}")
        print(f"    Properties: {sample['relationship_properties']}")
        print()

    print(f"\n4. EXTERNAL CVE REFERENCES ({len(results['external_references'])} node types):")
    print("-" * 80)
    if results['external_references']:
        for ref in results['external_references']:
            print(f"  {ref['node_label']:30} (count: {ref['count']})")
    else:
        print("  None found")

    print(f"\n5. VULNERABLE_TO.cve_id ANALYSIS:")
    print("-" * 80)
    vuln_analysis = results.get('vulnerable_to_cve_id_analysis', {})
    print(f"  Relationships with cve_id property: {vuln_analysis.get('sample_count', 0)}")
    print(f"  Mismatches found: {len(vuln_analysis.get('mismatches', []))}")
    if vuln_analysis.get('samples'):
        print(f"\n  Sample relationships (first 5):")
        for sample in vuln_analysis['samples'][:5]:
            print(f"    Rel cve_id: {sample['relationship_cve_id']} | Node id: {sample['node_cve_id']}")

    print(f"\n6. RISK ASSESSMENT:")
    print("-" * 80)
    risk = results['risk_assessment']
    print(f"  Risk Level: {risk['risk_level']}")
    print(f"  Total Relationships: {risk['total_relationships']}")
    print(f"  Unique Relationship Types: {risk['relationship_types_count']}")
    print(f"  CVE ID Formats: {risk['cve_id_format_distribution']}")
    print(f"  VULNERABLE_TO with cve_id: {risk.get('vulnerable_to_cve_id_property_usage', 0)}")
    print(f"\n  Recommendations:")
    for i, rec in enumerate(risk['recommendations'], 1):
        print(f"    {i}. {rec}")

    # Save to JSON
    output_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DR_Cybersec_Threat_Intelv2/docs/cve_relationship_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n\nFull results saved to: {output_file}")
    print("=" * 80)

    return results

if __name__ == "__main__":
    main()
