#!/usr/bin/env python3
"""
STEP 3: Add Customer Properties to Asset Nodes
Executes customer property assignments with safety checks
"""

from neo4j import GraphDatabase
import sys

# Database connection
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

def execute_step3():
    """Execute Step 3: Add customer properties to asset nodes"""

    results = {
        'servers_customer1': 0,
        'network_devices_customer2': 0,
        'ics_assets_customer3': 0,
        'saref_devices_customer1': 0,
        'shared_assets': 0,
        'validation': {},
        'cve_check': 0
    }

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session() as session:

            # 3.1 Add Customer Properties to Server Nodes (Customer 1: Energy)
            print("\n3.1 Assigning Servers to Customer 1 (Energy - DC-PRIMARY-01)...")
            result = session.run("""
                MATCH (s:Server)
                WHERE s.data_center = 'DC-PRIMARY-01'
                  AND s.customer_id IS NULL
                SET s.customer_id = 'CUST-001-ENERGY',
                    s.organization_id = 'ORG-RPA-SCADA',
                    s.asset_owner = 'Regional Power Authority',
                    s.ownership_status = 'active',
                    s.shared_asset = false,
                    s.asset_acquisition_date = date('2020-03-01'),
                    s.last_customer_update = datetime()
                RETURN count(s) AS updated_count
            """)
            record = result.single()
            results['servers_customer1'] = record['updated_count'] if record else 0
            print(f"   ✓ Updated {results['servers_customer1']} servers")

            # 3.2 Add Customer Properties to NetworkDevice Nodes (Customer 2: Water)
            print("\n3.2 Assigning NetworkDevices to Customer 2 (Water - DC-SECONDARY-02)...")
            result = session.run("""
                MATCH (nd:NetworkDevice)
                WHERE nd.data_center = 'DC-SECONDARY-02'
                  AND nd.customer_id IS NULL
                SET nd.customer_id = 'CUST-002-WATER',
                    nd.organization_id = 'ORG-MWD-TREATMENT',
                    nd.asset_owner = 'Metropolitan Water District',
                    nd.ownership_status = 'active',
                    nd.shared_asset = false,
                    nd.asset_acquisition_date = date('2021-08-15'),
                    nd.last_customer_update = datetime()
                RETURN count(nd) AS updated_count
            """)
            record = result.single()
            results['network_devices_customer2'] = record['updated_count'] if record else 0
            print(f"   ✓ Updated {results['network_devices_customer2']} network devices")

            # 3.3 Add Customer Properties to ICS_Asset Nodes (Customer 3: Manufacturing)
            print("\n3.3 Assigning ICS_Assets to Customer 3 (Manufacturing - Detroit)...")
            result = session.run("""
                MATCH (ics:ICS_Asset)
                WHERE ics.physical_location CONTAINS 'Detroit'
                  AND ics.customer_id IS NULL
                SET ics.customer_id = 'CUST-003-MFG',
                    ics.organization_id = 'ORG-AMC-ASSEMBLY',
                    ics.asset_owner = 'Advanced Manufacturing Corp',
                    ics.ownership_status = 'active',
                    ics.shared_asset = false,
                    ics.asset_acquisition_date = date('2022-05-01'),
                    ics.last_customer_update = datetime()
                RETURN count(ics) AS updated_count
            """)
            record = result.single()
            results['ics_assets_customer3'] = record['updated_count'] if record else 0
            print(f"   ✓ Updated {results['ics_assets_customer3']} ICS assets")

            # 3.4 Add Customer Properties to saref:Device Nodes (Customer 1: Energy)
            print("\n3.4 Assigning saref:Device nodes to Customer 1 (Energy - San Francisco)...")
            result = session.run("""
                MATCH (d)
                WHERE d:saref_Device
                  AND d.location CONTAINS 'San Francisco'
                  AND d.customer_id IS NULL
                SET d.customer_id = 'CUST-001-ENERGY',
                    d.organization_id = 'ORG-RPA-SCADA',
                    d.asset_owner = 'Regional Power Authority',
                    d.ownership_status = 'active',
                    d.shared_asset = false,
                    d.last_customer_update = datetime()
                RETURN count(d) AS updated_count
            """)
            record = result.single()
            results['saref_devices_customer1'] = record['updated_count'] if record else 0
            print(f"   ✓ Updated {results['saref_devices_customer1']} saref devices")

            # 3.5 Mark Shared/Multi-Tenant Assets
            print("\n3.5 Marking shared/multi-tenant assets...")
            result = session.run("""
                MATCH (s:Server)
                WHERE s.server_role CONTAINS 'Shared'
                   OR s.hostname CONTAINS 'shared'
                   OR s.server_type = 'multi_tenant'
                SET s.shared_asset = true,
                    s.ownership_status = 'multi_tenant',
                    s.tenant_list = ['CUST-001-ENERGY', 'CUST-002-WATER'],
                    s.primary_tenant = 'CUST-001-ENERGY'
                RETURN count(s) AS updated_count
            """)
            record = result.single()
            results['shared_assets'] = record['updated_count'] if record else 0
            print(f"   ✓ Marked {results['shared_assets']} shared assets")

            # 3.6 Create Indexes
            print("\n3.6 Creating indexes on customer_id and organization_id...")
            try:
                session.run("""
                    CREATE INDEX asset_customer_id_idx IF NOT EXISTS
                    FOR (n)
                    ON (n.customer_id)
                """)
                print("   ✓ Created asset_customer_id_idx")
            except Exception as e:
                print(f"   ⚠ Index asset_customer_id_idx: {e}")

            try:
                session.run("""
                    CREATE INDEX asset_organization_id_idx IF NOT EXISTS
                    FOR (n)
                    ON (n.organization_id)
                """)
                print("   ✓ Created asset_organization_id_idx")
            except Exception as e:
                print(f"   ⚠ Index asset_organization_id_idx: {e}")

            # 3.7 Validation Query
            print("\n3.7 Validation: Property assignments by asset type...")
            result = session.run("""
                MATCH (asset)
                WHERE asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device
                RETURN
                  labels(asset)[0] AS asset_type,
                  count(asset) AS total_count,
                  count(asset.customer_id) AS assigned_count,
                  count(asset) - count(asset.customer_id) AS unassigned_count
                ORDER BY asset_type
            """)

            print("\n   Asset Type Assignments:")
            print("   " + "-" * 80)
            print(f"   {'Asset Type':<20} {'Total':<10} {'Assigned':<10} {'Unassigned':<10} {'%':<10}")
            print("   " + "-" * 80)

            for record in result:
                asset_type = record['asset_type']
                total = record['total_count']
                assigned = record['assigned_count']
                unassigned = record['unassigned_count']
                percentage = (assigned / total * 100) if total > 0 else 0

                results['validation'][asset_type] = {
                    'total': total,
                    'assigned': assigned,
                    'unassigned': unassigned,
                    'percentage': percentage
                }

                print(f"   {asset_type:<20} {total:<10} {assigned:<10} {unassigned:<10} {percentage:>6.2f}%")

            print("   " + "-" * 80)

            # CRITICAL CVE CHECK
            print("\n🚨 CRITICAL CVE CHECK - Verifying no CVE modifications...")
            result = session.run("""
                MATCH (cve:CVE)
                WHERE EXISTS(cve.customer_id)
                RETURN count(cve) AS incorrectly_modified_cves
            """)
            record = result.single()
            results['cve_check'] = record['incorrectly_modified_cves'] if record else 0

            if results['cve_check'] == 0:
                print("   ✅ PASS - No CVE nodes were modified (Expected: 0)")
            else:
                print(f"   ❌ FAIL - {results['cve_check']} CVE nodes incorrectly modified!")
                print("   🚨 ABORT IMPLEMENTATION - CVE integrity compromised!")
                return False

            # Summary
            print("\n" + "=" * 80)
            print("STEP 3 EXECUTION SUMMARY")
            print("=" * 80)
            print(f"✓ Servers assigned to Customer 1 (Energy):        {results['servers_customer1']:>6}")
            print(f"✓ NetworkDevices assigned to Customer 2 (Water):  {results['network_devices_customer2']:>6}")
            print(f"✓ ICS_Assets assigned to Customer 3 (Mfg):       {results['ics_assets_customer3']:>6}")
            print(f"✓ saref_Devices assigned to Customer 1 (Energy): {results['saref_devices_customer1']:>6}")
            print(f"✓ Shared/Multi-tenant assets marked:             {results['shared_assets']:>6}")
            print("-" * 80)

            total_assigned = (results['servers_customer1'] +
                            results['network_devices_customer2'] +
                            results['ics_assets_customer3'] +
                            results['saref_devices_customer1'])

            print(f"TOTAL ASSETS ENHANCED:                           {total_assigned:>6}")
            print(f"CVE INTEGRITY CHECK:                             ✅ PASS")
            print("=" * 80)

            return True

if __name__ == "__main__":
    try:
        success = execute_step3()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
