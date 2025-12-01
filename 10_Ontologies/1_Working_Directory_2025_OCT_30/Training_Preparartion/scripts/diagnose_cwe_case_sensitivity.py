#!/usr/bin/env python3
"""
CWE CASE SENSITIVITY DIAGNOSTIC
Diagnose the root cause of missing CWE relationships
"""
import sys
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def diagnose_cwe_case_sensitivity():
    """Comprehensive CWE case sensitivity diagnostic."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    print("=" * 80)
    print("CWE CASE SENSITIVITY DIAGNOSTIC")
    print("=" * 80)

    try:
        with driver.session() as session:
            # Test 1: Check CWE ID format distribution
            print("\n1. CWE ID FORMAT DISTRIBUTION")
            print("-" * 80)

            result = session.run("""
                MATCH (w:CWE)
                WITH w.id AS cwe_id
                WITH cwe_id,
                     CASE
                         WHEN cwe_id STARTS WITH 'CWE-' THEN 'UPPERCASE'
                         WHEN cwe_id STARTS WITH 'cwe-' THEN 'lowercase'
                         WHEN cwe_id IS NULL THEN 'NULL'
                         ELSE 'OTHER'
                     END AS format_type
                RETURN format_type, count(*) AS count
                ORDER BY count DESC
            """)

            for record in result:
                print(f"  {record['format_type']}: {record['count']:,} CWEs")

            # Test 2: Sample CWE IDs by format
            print("\n2. SAMPLE CWE IDS BY FORMAT")
            print("-" * 80)

            result = session.run("""
                MATCH (w:CWE)
                WHERE w.id STARTS WITH 'CWE-'
                RETURN w.id AS id LIMIT 10
            """)

            uppercase_samples = [record['id'] for record in result]
            if uppercase_samples:
                print(f"  UPPERCASE samples: {uppercase_samples[:5]}")
            else:
                print("  UPPERCASE samples: NONE")

            result = session.run("""
                MATCH (w:CWE)
                WHERE w.id STARTS WITH 'cwe-'
                RETURN w.id AS id LIMIT 10
            """)

            lowercase_samples = [record['id'] for record in result]
            if lowercase_samples:
                print(f"  lowercase samples: {lowercase_samples[:5]}")
            else:
                print("  lowercase samples: NONE")

            # Test 3: Check critical missing CWEs
            print("\n3. CRITICAL MISSING CWEs CHECK")
            print("-" * 80)

            critical_cwes = ['cwe-20', 'cwe-119', 'cwe-125', 'cwe-327', 'cwe-290',
                           'cwe-522', 'cwe-434', 'cwe-120', 'cwe-200', 'cwe-269',
                           'cwe-88', 'cwe-400']

            for cwe_id in critical_cwes:
                # Try lowercase
                result_lower = session.run("""
                    MATCH (w:CWE {id: $cwe_id})
                    RETURN w.id AS id, w.name AS name
                """, cwe_id=cwe_id)

                lower_found = list(result_lower)

                # Try uppercase
                cwe_upper = cwe_id.upper()
                result_upper = session.run("""
                    MATCH (w:CWE {id: $cwe_id})
                    RETURN w.id AS id, w.name AS name
                """, cwe_id=cwe_upper)

                upper_found = list(result_upper)

                # Try case-insensitive
                result_insensitive = session.run("""
                    MATCH (w:CWE)
                    WHERE toLower(w.id) = toLower($cwe_id)
                    RETURN w.id AS id, w.name AS name
                """, cwe_id=cwe_id)

                insensitive_found = list(result_insensitive)

                status = "❌ NOT FOUND"
                if lower_found:
                    status = f"✅ FOUND (lowercase): {lower_found[0]['id']}"
                elif upper_found:
                    status = f"✅ FOUND (UPPERCASE): {upper_found[0]['id']}"
                elif insensitive_found:
                    status = f"⚠️ FOUND (case-insensitive): {insensitive_found[0]['id']}"

                print(f"  {cwe_id}: {status}")

            # Test 4: Check number property (alternative ID field)
            print("\n4. CWE NUMBER PROPERTY CHECK")
            print("-" * 80)

            result = session.run("""
                MATCH (w:CWE)
                WHERE w.number IS NOT NULL
                RETURN count(w) AS count_with_number, collect(w.number)[0..5] AS samples
            """)

            for record in result:
                print(f"  CWEs with 'number' property: {record['count_with_number']:,}")
                print(f"  Sample numbers: {record['samples']}")

            # Test 5: Total CWEs and properties
            print("\n5. TOTAL CWE COUNT AND PROPERTIES")
            print("-" * 80)

            result = session.run("""
                MATCH (w:CWE)
                RETURN count(w) AS total_cwes,
                       count(w.id) AS cwes_with_id,
                       count(w.number) AS cwes_with_number,
                       count(w.name) AS cwes_with_name
            """)

            for record in result:
                print(f"  Total CWEs: {record['total_cwes']:,}")
                print(f"  CWEs with 'id' property: {record['cwes_with_id']:,}")
                print(f"  CWEs with 'number' property: {record['cwes_with_number']:,}")
                print(f"  CWEs with 'name' property: {record['cwes_with_name']:,}")

            # Test 6: CVE→CWE relationship check
            print("\n6. EXISTING CVE→CWE RELATIONSHIPS")
            print("-" * 80)

            result = session.run("""
                MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
                WITH cwe.id AS cwe_id, count(r) AS rel_count
                RETURN cwe_id, rel_count
                ORDER BY rel_count DESC
                LIMIT 10
            """)

            relationships = list(result)
            if relationships:
                print(f"  Total unique CWEs with relationships: {len(relationships)}")
                print("  Top 10 CWEs by relationship count:")
                for record in relationships:
                    print(f"    {record['cwe_id']}: {record['rel_count']} CVEs")
            else:
                print("  No CVE→CWE relationships found")

            # Test 7: Recommendation
            print("\n7. RECOMMENDATION")
            print("-" * 80)

            result = session.run("""
                MATCH (w:CWE)
                WHERE w.id STARTS WITH 'CWE-'
                RETURN count(w) AS uppercase_count
            """)

            uppercase_count = result.single()['uppercase_count']

            result = session.run("""
                MATCH (w:CWE)
                WHERE w.id STARTS WITH 'cwe-'
                RETURN count(w) AS lowercase_count
            """)

            lowercase_count = result.single()['lowercase_count']

            if uppercase_count > lowercase_count:
                print("  ✅ DATABASE USES UPPERCASE 'CWE-' FORMAT")
                print("  ⚠️ SCRIPTS MUST USE UPPERCASE FORMAT IN QUERIES")
                print(f"  📊 Distribution: {uppercase_count:,} UPPERCASE vs {lowercase_count:,} lowercase")
            elif lowercase_count > uppercase_count:
                print("  ✅ DATABASE USES lowercase 'cwe-' FORMAT")
                print("  ⚠️ SCRIPTS MUST USE lowercase FORMAT IN QUERIES")
                print(f"  📊 Distribution: {lowercase_count:,} lowercase vs {uppercase_count:,} UPPERCASE")
            else:
                print("  ⚠️ MIXED CASE FORMATS DETECTED - DATABASE INCONSISTENCY")
                print(f"  📊 Distribution: {uppercase_count:,} UPPERCASE, {lowercase_count:,} lowercase")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.close()

    print("\n" + "=" * 80)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    diagnose_cwe_case_sensitivity()
