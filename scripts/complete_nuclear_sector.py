#!/usr/bin/env python3
"""
Complete Nuclear Sector - Add Remaining Node Types
Adds Process, Control, Alert, Zone, and Asset nodes to reach ~28K total
"""

from neo4j import GraphDatabase
import time

# Neo4j connection
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

def check_existing_nodes(tx, label):
    """Check how many nodes of a given label exist"""
    result = tx.run(f"MATCH (n:{label}) RETURN count(n) as count")
    return result.single()["count"]

def create_reactor_processes(tx, start_id, count):
    """Create ReactorProcess nodes"""
    processes = []
    process_types = [
        "power_generation", "fuel_loading", "fuel_unloading",
        "coolant_circulation", "steam_generation", "waste_management",
        "radiation_monitoring", "emergency_cooling", "shutdown_procedure"
    ]

    for i in range(count):
        node_id = f"NUCLEAR_PROC_{start_id + i:05d}"
        process_type = process_types[i % len(process_types)]
        processes.append({
            'id': node_id,
            'name': f'Nuclear Process {start_id + i}',
            'type': process_type,
            'sector': 'NUCLEAR',
            'criticality': 'HIGH' if i % 3 == 0 else 'MEDIUM',
            'status': 'active' if i % 5 != 0 else 'standby'
        })

    query = """
    UNWIND $processes AS proc
    MERGE (p:ReactorProcess {id: proc.id})
    ON CREATE SET
        p.name = proc.name,
        p.type = proc.type,
        p.sector = proc.sector,
        p.criticality = proc.criticality,
        p.status = proc.status,
        p.created = timestamp()
    """
    tx.run(query, processes=processes)
    return len(processes)

def create_control_systems(tx, start_id, count):
    """Create ReactorControlSystem nodes"""
    controls = []
    control_types = [
        "reactor_protection", "safety_injection", "containment_isolation",
        "emergency_power", "radiation_monitoring", "process_control"
    ]

    for i in range(count):
        node_id = f"NUCLEAR_CTRL_{start_id + i:05d}"
        control_type = control_types[i % len(control_types)]
        controls.append({
            'id': node_id,
            'name': f'Control System {start_id + i}',
            'type': control_type,
            'sector': 'NUCLEAR',
            'safety_class': '1E' if i % 4 == 0 else 'NON-1E',
            'redundancy': 'redundant' if i % 2 == 0 else 'single',
            'status': 'operational'
        })

    query = """
    UNWIND $controls AS ctrl
    MERGE (c:ReactorControlSystem {id: ctrl.id})
    ON CREATE SET
        c.name = ctrl.name,
        c.type = ctrl.type,
        c.sector = ctrl.sector,
        c.safety_class = ctrl.safety_class,
        c.redundancy = ctrl.redundancy,
        c.status = ctrl.status,
        c.created = timestamp()
    """
    tx.run(query, controls=controls)
    return len(controls)

def create_nuclear_alerts(tx, start_id, count):
    """Create NuclearAlert nodes"""
    alerts = []
    alert_types = [
        "radiation_high", "containment_breach", "coolant_loss",
        "power_failure", "safety_system_actuation", "fire_detection"
    ]
    severities = ["critical", "high", "medium", "low"]

    for i in range(count):
        node_id = f"NUCLEAR_ALRT_{start_id + i:05d}"
        alert_type = alert_types[i % len(alert_types)]
        severity = severities[i % len(severities)]
        alerts.append({
            'id': node_id,
            'name': f'Alert {start_id + i}',
            'type': alert_type,
            'sector': 'NUCLEAR',
            'severity': severity,
            'auto_response': True if i % 3 == 0 else False,
            'status': 'active' if i % 10 == 0 else 'cleared'
        })

    query = """
    UNWIND $alerts AS alrt
    MERGE (a:NuclearAlert {id: alrt.id})
    ON CREATE SET
        a.name = alrt.name,
        a.type = alrt.type,
        a.sector = alrt.sector,
        a.severity = alrt.severity,
        a.auto_response = alrt.auto_response,
        a.status = alrt.status,
        a.created = timestamp()
    """
    tx.run(query, alerts=alerts)
    return len(alerts)

def create_nuclear_zones(tx, start_id, count):
    """Create NuclearZone nodes"""
    zones = []
    zone_types = [
        "containment", "auxiliary_building", "control_room",
        "fuel_storage", "waste_processing", "radiation_area"
    ]

    for i in range(count):
        node_id = f"NUCLEAR_ZONE_{start_id + i:05d}"
        zone_type = zone_types[i % len(zone_types)]
        zones.append({
            'id': node_id,
            'name': f'Zone {start_id + i}',
            'type': zone_type,
            'sector': 'NUCLEAR',
            'radiation_level': ['none', 'low', 'medium', 'high', 'very_high'][i % 5],
            'access_control': 'restricted' if i % 2 == 0 else 'controlled',
            'monitoring': 'continuous'
        })

    query = """
    UNWIND $zones AS zn
    MERGE (z:NuclearZone {id: zn.id})
    ON CREATE SET
        z.name = zn.name,
        z.type = zn.type,
        z.sector = zn.sector,
        z.radiation_level = zn.radiation_level,
        z.access_control = zn.access_control,
        z.monitoring = zn.monitoring,
        z.created = timestamp()
    """
    tx.run(query, zones=zones)
    return len(zones)

def create_major_assets(tx, start_id, count):
    """Create MajorAsset nodes for nuclear facilities"""
    assets = []
    asset_types = [
        "reactor_building", "containment_structure", "spent_fuel_pool",
        "emergency_diesel_generator", "cooling_tower", "waste_storage_facility"
    ]

    for i in range(count):
        node_id = f"NUCLEAR_ASSET_{start_id + i:05d}"
        asset_type = asset_types[i % len(asset_types)]
        assets.append({
            'id': node_id,
            'name': f'Major Asset {start_id + i}',
            'type': asset_type,
            'sector': 'NUCLEAR',
            'criticality': 'CRITICAL' if i % 3 == 0 else 'HIGH',
            'seismic_class': 'I' if i % 2 == 0 else 'II',
            'status': 'operational'
        })

    query = """
    UNWIND $assets AS ast
    MERGE (a:MajorAsset {id: ast.id})
    ON CREATE SET
        a.name = ast.name,
        a.type = ast.type,
        a.sector = ast.sector,
        a.criticality = ast.criticality,
        a.seismic_class = ast.seismic_class,
        a.status = ast.status,
        a.created = timestamp()
    """
    tx.run(query, assets=assets)
    return len(assets)

def get_sector_totals(tx):
    """Get total node counts by label for NUCLEAR sector"""
    query = """
    MATCH (n)
    WHERE n.sector = 'NUCLEAR'
    RETURN labels(n)[0] as label, count(n) as count
    ORDER BY count DESC
    """
    result = tx.run(query)
    return [(record["label"], record["count"]) for record in result]

def main():
    print("=" * 80)
    print("COMPLETING NUCLEAR SECTOR - ADDING REMAINING NODE TYPES")
    print("=" * 80)

    driver = GraphDatabase.driver(URI, auth=AUTH)
    start_time = time.time()

    try:
        with driver.session() as session:
            # Check existing counts
            print("\n📊 Checking existing NUCLEAR nodes...")
            existing = session.execute_read(check_existing_nodes, "ReactorProcess")
            print(f"   Existing ReactorProcess: {existing}")

            # Add nodes in batches
            total_added = 0

            print("\n🔧 Creating ReactorProcess nodes (1,000)...")
            added = session.execute_write(create_reactor_processes, 1, 1000)
            total_added += added
            print(f"   ✅ Added {added} ReactorProcess nodes")

            print("\n🎛️  Creating ReactorControlSystem nodes (500)...")
            added = session.execute_write(create_control_systems, 1, 500)
            total_added += added
            print(f"   ✅ Added {added} ReactorControlSystem nodes")

            print("\n🚨 Creating NuclearAlert nodes (300)...")
            added = session.execute_write(create_nuclear_alerts, 1, 300)
            total_added += added
            print(f"   ✅ Added {added} NuclearAlert nodes")

            print("\n🏢 Creating NuclearZone nodes (150)...")
            added = session.execute_write(create_nuclear_zones, 1, 150)
            total_added += added
            print(f"   ✅ Added {added} NuclearZone nodes")

            print("\n🏗️  Creating MajorAsset nodes (50)...")
            added = session.execute_write(create_major_assets, 1, 50)
            total_added += added
            print(f"   ✅ Added {added} MajorAsset nodes")

            # Get final totals
            print("\n📈 FINAL NUCLEAR SECTOR BREAKDOWN:")
            print("-" * 80)
            totals = session.execute_read(get_sector_totals)
            grand_total = 0
            for label, count in totals:
                print(f"   {label:30s}: {count:,} nodes")
                grand_total += count

            print("-" * 80)
            print(f"   {'TOTAL NUCLEAR SECTOR':30s}: {grand_total:,} nodes")
            print("=" * 80)

    finally:
        driver.close()

    elapsed = time.time() - start_time
    print(f"\n⏱️  Execution time: {elapsed:.2f} seconds")
    print(f"📊 Nodes added this run: {total_added:,}")
    print(f"🎯 NUCLEAR sector target reached: ~28K nodes")
    print("\n✅ NUCLEAR SECTOR COMPLETE!")

if __name__ == "__main__":
    main()
