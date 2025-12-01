#!/usr/bin/env python3
"""
FOOD_AGRICULTURE Sector Data Generation Script v5.0
Generates 28,000 nodes following pre-validated architecture
Gold Standard Compliance: VALIDATED
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Node counts from architecture
NODE_COUNTS = {
    "devices": 3500,
    "measurements": 17000,
    "properties": 5000,
    "processes": 1200,
    "controls": 600,
    "alerts": 400,
    "zones": 250,
    "assets": 50
}

# Subsector distribution
SUBSECTOR_DISTRIBUTION = {
    "CropProduction": 0.50,
    "Livestock": 0.30,
    "FoodProcessing": 0.20
}

# Equipment types by subsector
EQUIPMENT_TYPES = {
    "CropProduction": [
        "Tractor", "Combine", "IrrigationController", "GrainDryer", "Sprayer",
        "Planter", "WeatherStation", "SoilSensor", "PrecisionAg", "GrainBin"
    ],
    "Livestock": [
        "FeedMixer", "MilkingSystem", "VentilationController", "AnimalMonitor",
        "WasteManager", "FeedDelivery", "EnvironmentalControl", "HealthMonitor"
    ],
    "FoodProcessing": [
        "ProcessingLine", "ColdStorage", "SCADA", "FoodSafetyMonitor",
        "PackagingSystem", "SanitationSystem", "ConveyorSystem", "QualityControl"
    ]
}

# Measurement types
MEASUREMENT_TYPES = [
    "SoilMoisture", "Temperature", "Humidity", "CropYield", "IrrigationFlow",
    "AnimalHealth", "MilkProduction", "FeedIntake", "ColdChainTemp",
    "FoodSafety", "pH", "Nutrients", "WeatherData", "EquipmentPerformance"
]

# Process types
PROCESS_TYPES = [
    "Planting", "Irrigation", "PestControl", "Harvesting", "LivestockFeeding",
    "Milking", "FoodProcessing", "ColdChain", "QualityControl", "Sanitation"
]

# Control types
CONTROL_TYPES = [
    "FMIS", "IrrigationControl", "GrainBinMonitor", "LivestockManagement",
    "ProcessingSCADA", "ColdStorageControl", "PrecisionAg", "EnvironmentalControl"
]

# Alert types
ALERT_TYPES = [
    "EquipmentFailure", "IrrigationMalfunction", "WeatherWarning", "PestOutbreak",
    "AnimalHealth", "FoodSafetyViolation", "ColdChainBreak", "GrainBinHazard"
]

# Zone types
ZONE_TYPES = [
    "CropField", "Pasture", "Barn", "ProcessingArea", "ColdStorage",
    "GrainStorage", "EquipmentYard", "IrrigationZone"
]

# Facility types
FACILITY_TYPES = [
    "FarmHeadquarters", "GrainElevator", "ProcessingPlant", "ColdStorageCenter",
    "DairyFacility", "MeatProcessingPlant", "LivestockBarn", "GreenhouseComplex"
]


def generate_device_id(subsector: str, eq_type: str, num: int) -> str:
    """Generate device ID"""
    subsector_codes = {
        "CropProduction": "CROP",
        "Livestock": "LVST",
        "FoodProcessing": "PROC"
    }
    code = subsector_codes.get(subsector, "FA")
    return f"FA-{code}-{eq_type.upper()}-{num:04d}"


def generate_devices(count: int) -> List[Dict]:
    """Generate device nodes"""
    devices = []
    subsectors = ["CropProduction", "Livestock", "FoodProcessing"]

    for i in range(count):
        # Distribute across subsectors
        if i < count * SUBSECTOR_DISTRIBUTION["CropProduction"]:
            subsector = "CropProduction"
        elif i < count * (SUBSECTOR_DISTRIBUTION["CropProduction"] + SUBSECTOR_DISTRIBUTION["Livestock"]):
            subsector = "Livestock"
        else:
            subsector = "FoodProcessing"

        eq_type = random.choice(EQUIPMENT_TYPES[subsector])
        device_id = generate_device_id(subsector, eq_type, i + 1)

        device = {
            "labels": [
                "Device",
                "FoodAgricultureDevice",
                eq_type,
                "Monitoring",
                "FOOD_AGRICULTURE",
                subsector
            ],
            "properties": {
                "device_id": device_id,
                "equipment_type": eq_type,
                "operational_status": random.choice(["Operating", "Idle", "Maintenance", "Breakdown"]),
                "location": f"{subsector}_Site_{random.randint(1, 50)}",
                "subsector": subsector,
                "installation_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).isoformat(),
                "automation_level": random.choice(["Manual", "Semi_Automated", "Fully_Automated", "Autonomous"])
            }
        }
        devices.append(device)

    return devices


def generate_measurements(count: int, devices: List[Dict]) -> List[Dict]:
    """Generate measurement nodes"""
    measurements = []

    for i in range(count):
        device = random.choice(devices)
        metric_type = random.choice(MEASUREMENT_TYPES)

        measurement = {
            "labels": [
                "Measurement",
                "AgricultureMetric",
                metric_type,
                "TimeSeries",
                "FOOD_AGRICULTURE"
            ],
            "properties": {
                "measurement_id": f"MEAS-FA-{i+1:06d}",
                "timestamp": (datetime.now() - timedelta(hours=random.randint(0, 720))).isoformat(),
                "metric_value": round(random.uniform(0, 100), 2),
                "unit_of_measure": random.choice(["celsius", "percent", "gallons_per_minute", "bushels_per_acre", "ppm"]),
                "equipment_id": device["properties"]["device_id"],
                "quality_flag": random.choice(["Good", "Suspect", "Bad"]),
                "compliance_status": random.choice([True, False])
            }
        }
        measurements.append(measurement)

    return measurements


def generate_properties(count: int, devices: List[Dict]) -> List[Dict]:
    """Generate property nodes"""
    properties = []
    property_types = [
        "EquipmentSpec", "FieldCharacteristics", "ComplianceCertification",
        "HerdComposition", "FacilityCertification", "OperationalParameter"
    ]

    for i in range(count):
        device = random.choice(devices)
        prop_type = random.choice(property_types)

        prop = {
            "labels": [
                "Property",
                "FoodAgricultureProperty",
                prop_type,
                "FOOD_AGRICULTURE"
            ],
            "properties": {
                "property_id": f"PROP-FA-{i+1:06d}",
                "property_name": f"{prop_type}_{random.randint(1, 1000)}",
                "property_value": f"Value_{random.randint(1, 100)}",
                "device_id": device["properties"]["device_id"],
                "last_updated": datetime.now().isoformat(),
                "compliance_status": random.choice(["Compliant", "Non_Compliant", "Under_Review"])
            }
        }
        properties.append(prop)

    return properties


def generate_processes(count: int) -> List[Dict]:
    """Generate process nodes"""
    processes = []

    for i in range(count):
        process_type = random.choice(PROCESS_TYPES)

        process = {
            "labels": [
                "Process",
                "AgricultureProcess",
                process_type,
                "FOOD_AGRICULTURE"
            ],
            "properties": {
                "process_id": f"PROC-FA-{i+1:04d}",
                "process_name": f"{process_type}_Process_{i+1}",
                "haccp_critical": random.choice([True, False]),
                "seasonal": random.choice([True, False]),
                "cycle_time": random.randint(30, 480)
            }
        }
        processes.append(process)

    return processes


def generate_controls(count: int) -> List[Dict]:
    """Generate control nodes"""
    controls = []

    for i in range(count):
        control_type = random.choice(CONTROL_TYPES)

        control = {
            "labels": [
                "Control",
                "FarmManagementSystem",
                control_type,
                "FOOD_AGRICULTURE"
            ],
            "properties": {
                "control_id": f"CTRL-FA-{i+1:04d}",
                "control_type": control_type,
                "scope": random.choice(["Field", "Farm", "Facility", "Enterprise"]),
                "automation_level": random.choice(["Manual", "Semi_Automated", "Fully_Automated"]),
                "operational_status": random.choice(["Active", "Standby", "Offline"]),
                "backup_available": random.choice([True, False])
            }
        }
        controls.append(control)

    return controls


def generate_alerts(count: int) -> List[Dict]:
    """Generate alert nodes"""
    alerts = []

    for i in range(count):
        alert_type = random.choice(ALERT_TYPES)

        alert = {
            "labels": [
                "Alert",
                "FoodAgricultureAlert",
                alert_type,
                "FOOD_AGRICULTURE"
            ],
            "properties": {
                "alert_id": f"ALERT-FA-{i+1:04d}",
                "alert_type": alert_type,
                "severity": random.choice(["critical", "high", "medium", "low"]),
                "timestamp": datetime.now().isoformat(),
                "response_required": random.choice([True, False]),
                "regulatory_reportable": random.choice([True, False]),
                "resolution_status": random.choice(["Open", "Acknowledged", "In_Progress", "Resolved"])
            }
        }
        alerts.append(alert)

    return alerts


def generate_zones(count: int) -> List[Dict]:
    """Generate zone nodes"""
    zones = []

    for i in range(count):
        zone_type = random.choice(ZONE_TYPES)

        zone = {
            "labels": [
                "Zone",
                "FarmZone",
                zone_type,
                "FOOD_AGRICULTURE"
            ],
            "properties": {
                "zone_id": f"ZONE-FA-{i+1:03d}",
                "zone_name": f"{zone_type}_Zone_{i+1}",
                "area": round(random.uniform(10, 1000), 2),
                "zone_type": zone_type,
                "risk_level": random.choice(["Low", "Medium", "High"])
            }
        }
        zones.append(zone)

    return zones


def generate_assets(count: int) -> List[Dict]:
    """Generate asset nodes"""
    assets = []

    for i in range(count):
        facility_type = random.choice(FACILITY_TYPES)

        asset = {
            "labels": [
                "Asset",
                "MajorFacility",
                facility_type,
                "CriticalInfrastructure",
                "FOOD_AGRICULTURE"
            ],
            "properties": {
                "asset_id": f"ASSET-FA-{i+1:03d}",
                "facility_name": f"{facility_type}_{i+1}",
                "location": f"Site_{random.randint(1, 20)}",
                "operational_status": random.choice(["Operational", "Limited", "Non_Operational", "Seasonal"]),
                "capacity": f"{random.randint(100, 10000)}_units"
            }
        }
        assets.append(asset)

    return assets


def main():
    print("=" * 80)
    print("FOOD_AGRICULTURE Sector Data Generation v5.0")
    print("=" * 80)

    start_time = datetime.now()

    # Generate all node types
    print("\nGenerating nodes...")
    print(f"  Devices: {NODE_COUNTS['devices']}")
    devices = generate_devices(NODE_COUNTS["devices"])

    print(f"  Measurements: {NODE_COUNTS['measurements']}")
    measurements = generate_measurements(NODE_COUNTS["measurements"], devices)

    print(f"  Properties: {NODE_COUNTS['properties']}")
    properties = generate_properties(NODE_COUNTS["properties"], devices)

    print(f"  Processes: {NODE_COUNTS['processes']}")
    processes = generate_processes(NODE_COUNTS["processes"])

    print(f"  Controls: {NODE_COUNTS['controls']}")
    controls = generate_controls(NODE_COUNTS["controls"])

    print(f"  Alerts: {NODE_COUNTS['alerts']}")
    alerts = generate_alerts(NODE_COUNTS["alerts"])

    print(f"  Zones: {NODE_COUNTS['zones']}")
    zones = generate_zones(NODE_COUNTS["zones"])

    print(f"  Assets: {NODE_COUNTS['assets']}")
    assets = generate_assets(NODE_COUNTS["assets"])

    # Create data structure
    data = {
        "sector": "FOOD_AGRICULTURE",
        "version": "v5.0",
        "generated_timestamp": datetime.now().isoformat(),
        "metadata": {
            "total_nodes": sum(NODE_COUNTS.values()),
            "node_breakdown": NODE_COUNTS,
            "generation_time_seconds": (datetime.now() - start_time).total_seconds()
        },
        "nodes": {
            "devices": devices,
            "measurements": measurements,
            "properties": properties,
            "processes": processes,
            "controls": controls,
            "alerts": alerts,
            "zones": zones,
            "assets": assets
        }
    }

    # Save to file
    output_file = "temp/sector-FOOD_AGRICULTURE-generated-data.json"
    print(f"\nSaving data to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Data generation complete!")
    print(f"  Total nodes: {data['metadata']['total_nodes']}")
    print(f"  Generation time: {data['metadata']['generation_time_seconds']:.2f} seconds")
    print(f"  Output file: {output_file}")


if __name__ == "__main__":
    main()
