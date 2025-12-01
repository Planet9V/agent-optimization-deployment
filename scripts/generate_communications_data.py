#!/usr/bin/env python3
"""
COMMUNICATIONS Sector Data Generator - TASKMASTER v5.0
Generates 28,000 nodes with proper distribution and relationships
"""

import json
import random
from datetime import datetime, timedelta

# Configuration
TOTAL_NODES = 28000
OUTPUT_FILE = "/home/jim/2_OXOT_Projects_Dev/temp/sector-COMMUNICATIONS-generated-data.json"

# Node type distribution
NODE_DISTRIBUTION = {
    "NetworkMeasurement": 18000,
    "CommunicationsProperty": 5000,
    "CommunicationsDevice": 3000,
    "RoutingProcess": 1000,
    "NetworkManagementSystem": 500,
    "CommunicationsAlert": 300,
    "CommunicationsZone": 150,
    "MajorAsset": 50
}

# Subsector distribution
SUBSECTOR_DISTRIBUTION = {
    "Telecom_Infrastructure": 0.60,  # 16,800 nodes
    "Data_Centers": 0.35,            # 9,800 nodes
    "Satellite_Systems": 0.05        # 1,400 nodes
}

# Device types by subsector
DEVICE_TYPES = {
    "Telecom_Infrastructure": [
        "Core_Router", "Edge_Router", "Switch", "Cell_Tower", "Base_Station",
        "Gateway", "Optical_Transport", "Multiplexer", "Access_Point"
    ],
    "Data_Centers": [
        "Server", "Storage_System", "Load_Balancer", "Firewall",
        "Top_of_Rack_Switch", "Spine_Switch", "Cooling_System", "UPS"
    ],
    "Satellite_Systems": [
        "Ground_Station", "Satellite_Uplink", "Antenna_System",
        "Signal_Processor", "Tracking_System"
    ]
}

# Measurement types
MEASUREMENT_TYPES = [
    "bandwidth", "latency", "packet_loss", "jitter", "throughput",
    "error_rate", "signal_strength", "uptime", "cpu_usage", "memory_usage"
]

# Alert types
ALERT_TYPES = [
    "Network_Outage", "High_Latency", "Bandwidth_Saturation",
    "Security_Breach", "Device_Failure", "Signal_Degradation"
]

# Process types
PROCESS_TYPES = [
    "BGP_Routing", "OSPF_Routing", "Packet_Forwarding",
    "Load_Balancing", "Traffic_Shaping", "QoS_Management"
]

# NMS types
NMS_TYPES = [
    "SNMP_Manager", "SDN_Controller", "Network_Monitor",
    "Configuration_Manager", "Performance_Analyzer"
]

def generate_id(node_type, subsector, index):
    """Generate unique node ID"""
    return f"COMM_{node_type}_{subsector}_{index:06d}"

def select_subsector():
    """Randomly select subsector based on distribution"""
    rand = random.random()
    cumulative = 0
    for subsector, prob in SUBSECTOR_DISTRIBUTION.items():
        cumulative += prob
        if rand <= cumulative:
            return subsector
    return "Telecom_Infrastructure"  # fallback

def generate_network_measurement(index, subsector):
    """Generate NetworkMeasurement node"""
    meas_type = random.choice(MEASUREMENT_TYPES)

    # Generate realistic measurement values
    values = {
        "bandwidth": random.uniform(100, 10000),  # Mbps
        "latency": random.uniform(1, 100),        # ms
        "packet_loss": random.uniform(0, 5),      # %
        "jitter": random.uniform(0, 50),          # ms
        "throughput": random.uniform(50, 9500),   # Mbps
        "error_rate": random.uniform(0, 0.1),     # %
        "signal_strength": random.uniform(-90, -30),  # dBm
        "uptime": random.uniform(95, 100),        # %
        "cpu_usage": random.uniform(10, 90),      # %
        "memory_usage": random.uniform(20, 85)    # %
    }

    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))

    return {
        "id": generate_id("MEAS", subsector, index),
        "labels": ["Measurement", "NetworkMeasurement", "Monitoring", "COMMUNICATIONS", subsector],
        "properties": {
            "measurement_type": meas_type,
            "value": values[meas_type],
            "unit": "Mbps" if "bandwidth" in meas_type or "throughput" in meas_type else ("ms" if "latency" in meas_type or "jitter" in meas_type else "%"),
            "timestamp": timestamp.isoformat(),
            "subsector": subsector,
            "quality": random.choice(["good", "fair", "poor"]),
            "node_type": "NetworkMeasurement"
        }
    }

def generate_communications_property(index, subsector):
    """Generate CommunicationsProperty node"""
    property_types = [
        "Device_Configuration", "Network_Settings", "Protocol_Parameters",
        "QoS_Policy", "Security_Settings", "Performance_Thresholds"
    ]

    prop_type = random.choice(property_types)

    return {
        "id": generate_id("PROP", subsector, index),
        "labels": ["Property", "CommunicationsProperty", "Communications", "Monitoring", "COMMUNICATIONS", subsector],
        "properties": {
            "property_type": prop_type,
            "property_name": f"{prop_type}_{index}",
            "value": f"config_value_{random.randint(1000, 9999)}",
            "subsector": subsector,
            "last_updated": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            "node_type": "CommunicationsProperty"
        }
    }

def generate_communications_device(index, subsector):
    """Generate CommunicationsDevice node"""
    device_type = random.choice(DEVICE_TYPES[subsector])

    return {
        "id": generate_id("DEV", subsector, index),
        "labels": ["Device", "CommunicationsDevice", "Communications", "Monitoring", "COMMUNICATIONS", subsector],
        "properties": {
            "device_type": device_type,
            "device_name": f"{device_type}_{subsector}_{index}",
            "manufacturer": random.choice(["Cisco", "Juniper", "Huawei", "Nokia", "Ericsson"]),
            "model": f"MODEL_{random.randint(1000, 9999)}",
            "ip_address": f"{random.randint(10, 192)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
            "status": random.choice(["operational", "degraded", "offline"]),
            "subsector": subsector,
            "install_date": (datetime.now() - timedelta(days=random.randint(0, 3650))).isoformat(),
            "node_type": "CommunicationsDevice"
        }
    }

def generate_routing_process(index, subsector):
    """Generate RoutingProcess node"""
    process_type = random.choice(PROCESS_TYPES)

    return {
        "id": generate_id("PROC", subsector, index),
        "labels": ["Process", "RoutingProcess", "Communications", "COMMUNICATIONS", subsector],
        "properties": {
            "process_type": process_type,
            "process_name": f"{process_type}_{index}",
            "protocol": random.choice(["BGP", "OSPF", "EIGRP", "RIP", "IS-IS"]),
            "status": random.choice(["running", "stopped", "error"]),
            "subsector": subsector,
            "priority": random.randint(1, 10),
            "node_type": "RoutingProcess"
        }
    }

def generate_network_management_system(index, subsector):
    """Generate NetworkManagementSystem node"""
    nms_type = random.choice(NMS_TYPES)

    return {
        "id": generate_id("NMS", subsector, index),
        "labels": ["Control", "NetworkManagementSystem", "Communications", "COMMUNICATIONS", subsector],
        "properties": {
            "nms_type": nms_type,
            "nms_name": f"{nms_type}_{index}",
            "version": f"v{random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "status": random.choice(["active", "standby", "offline"]),
            "subsector": subsector,
            "managed_devices_count": random.randint(10, 500),
            "node_type": "NetworkManagementSystem"
        }
    }

def generate_communications_alert(index, subsector):
    """Generate CommunicationsAlert node"""
    alert_type = random.choice(ALERT_TYPES)

    return {
        "id": generate_id("ALERT", subsector, index),
        "labels": ["CommunicationsAlert", "Alert", "Monitoring", "COMMUNICATIONS", subsector],
        "properties": {
            "alert_type": alert_type,
            "severity": random.choice(["critical", "warning", "info"]),
            "message": f"{alert_type} detected in {subsector}",
            "timestamp": (datetime.now() - timedelta(hours=random.randint(0, 168))).isoformat(),
            "subsector": subsector,
            "status": random.choice(["active", "acknowledged", "resolved"]),
            "node_type": "CommunicationsAlert"
        }
    }

def generate_communications_zone(index, subsector):
    """Generate CommunicationsZone node"""
    zone_types = {
        "Telecom_Infrastructure": ["Network_Region", "Coverage_Area", "Routing_Domain"],
        "Data_Centers": ["Data_Center_Zone", "Rack_Row", "Availability_Zone"],
        "Satellite_Systems": ["Ground_Segment", "Space_Segment", "Orbital_Zone"]
    }

    zone_type = random.choice(zone_types[subsector])

    return {
        "id": generate_id("ZONE", subsector, index),
        "labels": ["CommunicationsZone", "Zone", "Asset", "COMMUNICATIONS", subsector],
        "properties": {
            "zone_type": zone_type,
            "zone_name": f"{zone_type}_{index}",
            "capacity": random.randint(50, 500),
            "current_load": random.randint(10, 400),
            "subsector": subsector,
            "location": random.choice(["US-East", "US-West", "EU", "APAC"]),
            "node_type": "CommunicationsZone"
        }
    }

def generate_major_asset(index, subsector):
    """Generate MajorAsset node"""
    asset_types = {
        "Telecom_Infrastructure": ["Central_Office", "Switching_Center", "Network_Operations_Center"],
        "Data_Centers": ["Primary_Data_Center", "Disaster_Recovery_Site", "Edge_Data_Center"],
        "Satellite_Systems": ["Ground_Control_Station", "Launch_Facility", "Tracking_Station"]
    }

    asset_type = random.choice(asset_types[subsector])

    return {
        "id": generate_id("ASSET", subsector, index),
        "labels": ["MajorAsset", "Asset", "COMMUNICATIONS", subsector],
        "properties": {
            "asset_type": asset_type,
            "asset_name": f"{asset_type}_{index}",
            "value": random.randint(1000000, 100000000),
            "criticality": random.choice(["high", "medium", "low"]),
            "subsector": subsector,
            "location": random.choice(["US-East", "US-West", "EU", "APAC"]),
            "node_type": "MajorAsset"
        }
    }

def generate_relationships(nodes):
    """Generate relationships between nodes"""
    relationships = []

    devices = [n for n in nodes if n["properties"]["node_type"] == "CommunicationsDevice"]
    measurements = [n for n in nodes if n["properties"]["node_type"] == "NetworkMeasurement"]
    properties = [n for n in nodes if n["properties"]["node_type"] == "CommunicationsProperty"]
    processes = [n for n in nodes if n["properties"]["node_type"] == "RoutingProcess"]
    nms_list = [n for n in nodes if n["properties"]["node_type"] == "NetworkManagementSystem"]
    zones = [n for n in nodes if n["properties"]["node_type"] == "CommunicationsZone"]

    # HAS_MEASUREMENT (Device -> Measurement)
    for meas in measurements:
        device = random.choice(devices)
        relationships.append({
            "type": "HAS_MEASUREMENT",
            "from": device["id"],
            "to": meas["id"]
        })

    # HAS_PROPERTY (Device/Process -> Property)
    for prop in properties:
        if random.random() > 0.3:
            source = random.choice(devices)
        else:
            source = random.choice(processes) if processes else random.choice(devices)
        relationships.append({
            "type": "HAS_PROPERTY",
            "from": source["id"],
            "to": prop["id"]
        })

    # CONTROLS (NMS -> Device/Process)
    for nms in nms_list:
        num_controlled = random.randint(5, 15)
        for _ in range(num_controlled):
            target = random.choice(devices + processes)
            relationships.append({
                "type": "CONTROLS",
                "from": nms["id"],
                "to": target["id"]
            })

    # CONTAINS (Zone -> Device)
    for zone in zones:
        num_contained = random.randint(10, 30)
        for _ in range(min(num_contained, len(devices))):
            device = random.choice(devices)
            relationships.append({
                "type": "CONTAINS",
                "from": zone["id"],
                "to": device["id"]
            })

    # USES_DEVICE (Process -> Device)
    for process in processes:
        num_devices = random.randint(1, 3)
        for _ in range(num_devices):
            device = random.choice(devices)
            relationships.append({
                "type": "USES_DEVICE",
                "from": process["id"],
                "to": device["id"]
            })

    # ROUTES_THROUGH (Device -> Device)
    for _ in range(4000):
        dev1 = random.choice(devices)
        dev2 = random.choice(devices)
        if dev1["id"] != dev2["id"]:
            relationships.append({
                "type": "ROUTES_THROUGH",
                "from": dev1["id"],
                "to": dev2["id"]
            })

    # CONNECTS_TO_NETWORK (Device -> Zone)
    for device in devices:
        zone = random.choice(zones)
        relationships.append({
            "type": "CONNECTS_TO_NETWORK",
            "from": device["id"],
            "to": zone["id"]
        })

    # MANAGED_BY_NMS (Device -> NMS)
    for device in devices:
        nms = random.choice(nms_list)
        relationships.append({
            "type": "MANAGED_BY_NMS",
            "from": device["id"],
            "to": nms["id"]
        })

    return relationships

def main():
    """Generate all nodes and relationships"""
    print(f"Generating {TOTAL_NODES} COMMUNICATIONS nodes...")

    nodes = []
    generators = {
        "NetworkMeasurement": generate_network_measurement,
        "CommunicationsProperty": generate_communications_property,
        "CommunicationsDevice": generate_communications_device,
        "RoutingProcess": generate_routing_process,
        "NetworkManagementSystem": generate_network_management_system,
        "CommunicationsAlert": generate_communications_alert,
        "CommunicationsZone": generate_communications_zone,
        "MajorAsset": generate_major_asset
    }

    # Generate nodes
    for node_type, count in NODE_DISTRIBUTION.items():
        print(f"  Generating {count} {node_type} nodes...")
        generator = generators[node_type]
        for i in range(count):
            subsector = select_subsector()
            node = generator(i, subsector)
            nodes.append(node)

    print(f"Generated {len(nodes)} nodes")

    # Generate relationships
    print("Generating relationships...")
    relationships = generate_relationships(nodes)
    print(f"Generated {len(relationships)} relationships")

    # Create output
    output = {
        "sector": "COMMUNICATIONS",
        "total_nodes": len(nodes),
        "total_relationships": len(relationships),
        "subsectors": list(SUBSECTOR_DISTRIBUTION.keys()),
        "generated_at": datetime.now().isoformat(),
        "nodes": nodes,
        "relationships": relationships
    }

    # Save to file
    print(f"Saving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ SUCCESS: Generated {len(nodes)} nodes and {len(relationships)} relationships")
    print(f"   File: {OUTPUT_FILE}")
    print(f"   Size: {len(json.dumps(output)) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
