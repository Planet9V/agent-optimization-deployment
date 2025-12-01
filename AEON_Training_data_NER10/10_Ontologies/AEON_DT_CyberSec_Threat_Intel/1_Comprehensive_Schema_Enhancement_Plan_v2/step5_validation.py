#!/usr/bin/env python3
"""
STEP 5 VALIDATION SCRIPT
File: step5_validation.py
Created: 2025-10-30
Purpose: Reliable validation of Customer/Organization implementation
"""

from neo4j import GraphDatabase
import sys
from datetime import datetime

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "adminadmin"

class ValidationRunner:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def close(self):
        self.driver.close()

    def run_query(self, query, description):
        """Execute a single query and return results"""
        try:
            with self.driver.session() as session:
                result = session.run(query)
                return list(result)
        except Exception as e:
            print(f"❌ Error executing {description}: {str(e)}")
            return None

    def validation_1_cve_count(self):
        """VALIDATION 1: CVE Count Verification"""
        print("=" * 50)
        print("VALIDATION 1: CVE Count Verification")
        print("EXPECTED: 147,923 CVEs")
        print("=" * 50)

        query = "MATCH (cve:CVE) RETURN count(cve) AS cve_count;"
        result = self.run_query(query, "CVE Count")

        if result:
            cve_count = result[0]['cve_count']
            print(f"Result: {cve_count:,} CVEs found")

            if cve_count == 147923:
                print("✅ PASS: CVE count matches expected value")
                self.results['validation_1'] = 'PASS'
                return True
            else:
                print(f"❌ FAIL: CVE count mismatch! Expected 147,923, got {cve_count}")
                print("⚠️ WARNING: This may indicate wrong database or data loss")
                self.results['validation_1'] = 'FAIL'
                return False
        else:
            print("❌ FAIL: Could not retrieve CVE count")
            self.results['validation_1'] = 'ERROR'
            return False

    def validation_2_cve_modification(self):
        """VALIDATION 2: CVE Modification Check"""
        print("\n" + "=" * 50)
        print("VALIDATION 2: CVE Modification Check")
        print("EXPECTED: 0 (no CVEs should have customer properties)")
        print("=" * 50)

        query = """
        MATCH (cve:CVE)
        WHERE EXISTS(cve.customer_id)
           OR EXISTS(cve.organization_id)
           OR EXISTS(cve.asset_owner)
        RETURN count(cve) AS incorrectly_modified_cves;
        """
        result = self.run_query(query, "CVE Modification Check")

        if result:
            modified_count = result[0]['incorrectly_modified_cves']
            print(f"Result: {modified_count} CVEs with customer properties")

            if modified_count == 0:
                print("✅ PASS: No CVEs were incorrectly modified")
                self.results['validation_2'] = 'PASS'
                return True
            else:
                print(f"❌ FAIL: {modified_count} CVEs have customer properties!")
                print("⚠️ CRITICAL: CVE nodes should NEVER have customer properties")
                print("ACTION REQUIRED: Execute rollback procedure immediately")
                self.results['validation_2'] = 'FAIL'
                return False
        else:
            print("❌ FAIL: Could not check CVE modifications")
            self.results['validation_2'] = 'ERROR'
            return False

    def validation_3_customer_filtering(self):
        """VALIDATION 3: Customer Filtering Test"""
        print("\n" + "=" * 50)
        print("VALIDATION 3: Customer Filtering Test")
        print("Testing Customer CUST-001-ENERGY equipment filtering")
        print("=" * 50)

        query = """
        MATCH (c:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset)
        RETURN
          labels(asset)[0] AS asset_type,
          count(asset) AS my_equipment_count
        ORDER BY my_equipment_count DESC;
        """
        result = self.run_query(query, "Customer Filtering")

        if result:
            if len(result) > 0:
                print("Equipment owned by CUST-001-ENERGY:")
                total_count = 0
                for record in result:
                    asset_type = record['asset_type']
                    count = record['my_equipment_count']
                    total_count += count
                    print(f"  - {asset_type}: {count} units")

                print(f"\nTotal: {total_count} pieces of equipment")
                print("✅ PASS: Customer filtering returns equipment")
                self.results['validation_3'] = 'PASS'
                return True
            else:
                print("⚠️ WARNING: No equipment found for customer")
                print("This may indicate incomplete Step 3 execution")
                self.results['validation_3'] = 'WARNING'
                return False
        else:
            print("❌ FAIL: Could not execute customer filtering query")
            self.results['validation_3'] = 'ERROR'
            return False

    def validation_4_cve_impact_query(self):
        """VALIDATION 4: CVE Impact Query Test (Question 1)"""
        print("\n" + "=" * 50)
        print("VALIDATION 4: CVE Impact Query Test (Question 1)")
        print("Testing MY equipment vulnerability query")
        print("=" * 50)

        query = """
        MATCH (customer:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(server:Server)
        MATCH (server)-[:RUNS]->(app:Application)
              -[:CONTAINS]->(comp:SoftwareComponent)
              -[:HAS_VULNERABILITY]->(cve:CVE)
        WHERE cve.cvss_base_score >= 7.0
        RETURN
          server.hostname AS my_equipment,
          comp.name AS vulnerable_component,
          cve.cve_id AS cve_id,
          cve.cvss_base_score AS severity
        ORDER BY cve.cvss_base_score DESC
        LIMIT 5;
        """
        result = self.run_query(query, "CVE Impact Query")

        if result:
            if len(result) > 0:
                print(f"Found {len(result)} vulnerabilities affecting customer equipment:")
                for i, record in enumerate(result, 1):
                    print(f"\n{i}. Equipment: {record['my_equipment']}")
                    print(f"   Component: {record['vulnerable_component']}")
                    print(f"   CVE: {record['cve_id']}")
                    print(f"   Severity: {record['severity']}")

                print("\n✅ PASS: CVE impact query returns results")
                self.results['validation_4'] = 'PASS'
                return True
            else:
                print("ℹ️ INFO: No high-severity vulnerabilities found")
                print("This may be expected if customer equipment is well-maintained")
                self.results['validation_4'] = 'INFO'
                return True  # Not a failure
        else:
            print("❌ FAIL: Could not execute CVE impact query")
            self.results['validation_4'] = 'ERROR'
            return False

    def validation_5_multi_customer_isolation(self):
        """VALIDATION 5: Multi-Customer Isolation Test"""
        print("\n" + "=" * 50)
        print("VALIDATION 5: Multi-Customer Isolation Test")
        print("EXPECTED: 0 (no incorrectly shared assets)")
        print("=" * 50)

        query = """
        MATCH (c1:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset1)
        MATCH (c2:Customer {customer_id: 'CUST-002-WATER'})-[:OWNS_EQUIPMENT]->(asset2)
        WHERE asset1 = asset2 AND asset1.shared_asset <> true
        RETURN count(asset1) AS incorrectly_shared_assets;
        """
        result = self.run_query(query, "Multi-Customer Isolation")

        if result:
            shared_count = result[0]['incorrectly_shared_assets']
            print(f"Result: {shared_count} incorrectly shared assets")

            if shared_count == 0:
                print("✅ PASS: Customer isolation maintained")
                self.results['validation_5'] = 'PASS'
                return True
            else:
                print(f"❌ FAIL: {shared_count} assets incorrectly shared between customers")
                print("⚠️ WARNING: Multi-tenant isolation compromised")
                print("ACTION REQUIRED: Review Step 3 asset assignments")
                self.results['validation_5'] = 'FAIL'
                return False
        else:
            print("❌ FAIL: Could not check customer isolation")
            self.results['validation_5'] = 'ERROR'
            return False

    def validation_6_comprehensive_report(self):
        """VALIDATION 6: Comprehensive Validation Report"""
        print("\n" + "=" * 50)
        print("VALIDATION 6: Comprehensive Validation Report")
        print("=" * 50)

        query = """
        CALL {
          MATCH (cve:CVE) RETURN count(cve) AS cve_count
        }
        CALL {
          MATCH (c:Customer) RETURN count(c) AS customer_count
        }
        CALL {
          MATCH (o:Organization) RETURN count(o) AS organization_count
        }
        CALL {
          MATCH (asset)
          WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device)
            AND asset.customer_id IS NOT NULL
          RETURN count(asset) AS assigned_assets
        }
        CALL {
          MATCH (:Customer)-[r:OWNS_EQUIPMENT]->()
          RETURN count(r) AS ownership_relationships
        }
        RETURN
          cve_count,
          customer_count,
          organization_count,
          assigned_assets,
          ownership_relationships,
          CASE WHEN cve_count = 147923 THEN '✅ PASS' ELSE '❌ FAIL' END AS cve_preservation_check;
        """
        result = self.run_query(query, "Comprehensive Report")

        if result:
            record = result[0]
            print("\nImplementation Summary:")
            print(f"  CVE Nodes:                 {record['cve_count']:,}")
            print(f"  Customers:                 {record['customer_count']}")
            print(f"  Organizations:             {record['organization_count']}")
            print(f"  Assigned Assets:           {record['assigned_assets']}")
            print(f"  Ownership Relationships:   {record['ownership_relationships']}")
            print(f"\nCVE Preservation Check:    {record['cve_preservation_check']}")

            if record['cve_preservation_check'] == '✅ PASS':
                print("\n✅ PASS: Comprehensive validation successful")
                self.results['validation_6'] = 'PASS'
                return True
            else:
                print("\n❌ FAIL: CVE preservation check failed")
                self.results['validation_6'] = 'FAIL'
                return False
        else:
            print("❌ FAIL: Could not generate comprehensive report")
            self.results['validation_6'] = 'ERROR'
            return False

    def run_all_validations(self):
        """Execute all validation tests"""
        print("\n" + "=" * 60)
        print("STEP 5: CRITICAL VALIDATION EXECUTION")
        print("=" * 60)
        print(f"Timestamp: {self.timestamp}")
        print("=" * 60 + "\n")

        # Run all validations
        v1 = self.validation_1_cve_count()
        v2 = self.validation_2_cve_modification()
        v3 = self.validation_3_customer_filtering()
        v4 = self.validation_4_cve_impact_query()
        v5 = self.validation_5_multi_customer_isolation()
        v6 = self.validation_6_comprehensive_report()

        # Final Summary
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Timestamp: {self.timestamp}")
        print()
        print(f"Validation 1 (CVE Count):              {self.results.get('validation_1', 'NOT RUN')}")
        print(f"Validation 2 (CVE Modification):       {self.results.get('validation_2', 'NOT RUN')}")
        print(f"Validation 3 (Customer Filtering):     {self.results.get('validation_3', 'NOT RUN')}")
        print(f"Validation 4 (CVE Impact Query):       {self.results.get('validation_4', 'NOT RUN')}")
        print(f"Validation 5 (Multi-Customer Isolation): {self.results.get('validation_5', 'NOT RUN')}")
        print(f"Validation 6 (Comprehensive Report):   {self.results.get('validation_6', 'NOT RUN')}")
        print()

        # GO/NO-GO Decision
        critical_pass = (
            self.results.get('validation_1') == 'PASS' and
            self.results.get('validation_2') == 'PASS' and
            self.results.get('validation_5') == 'PASS'
        )

        if critical_pass:
            print("=" * 60)
            print("✅ FINAL DECISION: GO")
            print("=" * 60)
            print("All critical validations passed.")
            print("Customer/Organization implementation is successful.")
            print("CVE preservation confirmed.")
            print("Multi-tenant isolation validated.")
            print()
            print("READY FOR PRODUCTION USE")
            print("=" * 60)
            return 0
        else:
            print("=" * 60)
            print("❌ FINAL DECISION: NO-GO")
            print("=" * 60)
            print("Critical validation failures detected.")
            print("DO NOT PROCEED TO PRODUCTION.")
            print()
            print("RECOMMENDED ACTIONS:")

            if self.results.get('validation_1') == 'FAIL':
                print("  1. Verify correct database connection")
                print("  2. Check if production database has 147,923 CVEs")

            if self.results.get('validation_2') == 'FAIL':
                print("  1. Execute rollback procedure for Step 3")
                print("  2. Remove customer properties from CVE nodes")

            if self.results.get('validation_5') == 'FAIL':
                print("  1. Review Step 3 asset assignment logic")
                print("  2. Fix incorrectly shared assets")

            print()
            print("Execute rollback procedure before retry.")
            print("=" * 60)
            return 1

def main():
    """Main execution"""
    print("\n🚀 Starting STEP 5 Validation...\n")

    validator = ValidationRunner(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        exit_code = validator.run_all_validations()
        validator.close()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        validator.close()
        sys.exit(2)

if __name__ == "__main__":
    main()
