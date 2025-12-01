#!/usr/bin/env python3
"""
Update sector-schema-registry.json with FINANCIAL_SERVICES sector
"""

import json
from datetime import datetime

REGISTRY_PATH = '/home/jim/2_OXOT_Projects_Dev/docs/schema-governance/sector-schema-registry.json'

# Load existing registry
with open(REGISTRY_PATH, 'r') as f:
    registry = json.load(f)

# Add FINANCIAL_SERVICES to sectors_registered if not already there
if 'FINANCIAL_SERVICES' not in registry['sectors_registered']:
    registry['sectors_registered'].append('FINANCIAL_SERVICES')

# Update last_updated timestamp
registry['last_updated'] = datetime.utcnow().isoformat() + 'Z'

# Add FINANCIAL_SERVICES sector details
registry['gold_standard_sectors']['FINANCIAL_SERVICES'] = {
    "total_nodes": 28000,
    "validation_status": "DEPLOYED",
    "expected_range": "26000-35000",
    "variance_from_expected": "Within expected range",
    "deployment_date": "2025-11-22T03:45:00Z",
    "deployment_time_seconds": 1.57,
    "node_types": {
        "Measurement": {
            "count": 17000,
            "percentage": 60.7,
            "description": "Transaction metrics tracking financial system performance"
        },
        "Property": {
            "count": 5000,
            "percentage": 17.9,
            "description": "Financial services properties and compliance attributes"
        },
        "Device": {
            "count": 3500,
            "percentage": 12.5,
            "description": "Financial services equipment including ATMs, terminals, and trading systems"
        },
        "Process": {
            "count": 1200,
            "percentage": 4.3,
            "description": "Financial transaction workflows and operational procedures"
        },
        "Control": {
            "count": 600,
            "percentage": 2.1,
            "description": "Risk management, compliance, and security controls"
        },
        "Alert": {
            "count": 400,
            "percentage": 1.4,
            "description": "Critical notifications for fraud, failures, and compliance issues"
        },
        "Zone": {
            "count": 250,
            "percentage": 0.9,
            "description": "Geographic regions, regulatory jurisdictions, and network segments"
        },
        "Asset": {
            "count": 50,
            "percentage": 0.2,
            "description": "Major financial facilities and infrastructure"
        }
    },
    "specialized_node_types": {
        "FinancialServicesDevice": {
            "count": 3500,
            "label_count": 5,
            "parent_labels": ["Device", "FinancialServicesDevice", "Monitoring", "FINANCIAL_SERVICES", "Subsector"]
        },
        "TransactionMetric": {
            "count": 17000,
            "label_count": 5,
            "parent_labels": ["Measurement", "TransactionMetric", "TimeSeries", "Monitoring", "FINANCIAL_SERVICES"]
        },
        "FinancialServicesProperty": {
            "count": 5000,
            "label_count": 5,
            "parent_labels": ["Property", "FinancialServicesProperty", "Configuration", "FINANCIAL_SERVICES", "Subsector"]
        },
        "FinancialProcess": {
            "count": 1200,
            "label_count": 4,
            "parent_labels": ["Process", "FinancialProcess", "Workflow", "FINANCIAL_SERVICES"]
        },
        "FinancialControl": {
            "count": 600,
            "label_count": 4,
            "parent_labels": ["Control", "FinancialControl", "Governance", "FINANCIAL_SERVICES"]
        },
        "FinancialAlert": {
            "count": 400,
            "label_count": 4,
            "parent_labels": ["Alert", "FinancialAlert", "Notification", "FINANCIAL_SERVICES"]
        },
        "FinancialZone": {
            "count": 250,
            "label_count": 4,
            "parent_labels": ["Zone", "FinancialZone", "Geography", "FINANCIAL_SERVICES"]
        },
        "MajorFacility": {
            "count": 50,
            "label_count": 5,
            "parent_labels": ["Asset", "MajorFacility", "Infrastructure", "Critical", "FINANCIAL_SERVICES"]
        }
    },
    "relationships": {
        "total_relationships": 0,
        "breakdown": {
            "PROCESSES": {
                "count": 0,
                "percentage": 0,
                "description": "Device processes transactions (pending deployment)"
            },
            "HAS_PROPERTY": {
                "count": 0,
                "percentage": 0,
                "description": "Entity has configuration or attribute (pending deployment)"
            },
            "EXECUTES": {
                "count": 0,
                "percentage": 0,
                "description": "System executes financial process (pending deployment)"
            },
            "CONTROLS": {
                "count": 0,
                "percentage": 0,
                "description": "Control system governs operations (pending deployment)"
            },
            "TRIGGERS": {
                "count": 0,
                "percentage": 0,
                "description": "Event triggers alert (pending deployment)"
            },
            "LOCATED_IN": {
                "count": 0,
                "percentage": 0,
                "description": "Entity located in zone (pending deployment)"
            },
            "SUPPORTS": {
                "count": 0,
                "percentage": 0,
                "description": "Facility supports operations (pending deployment)"
            }
        }
    },
    "labels_per_node_avg": 5.1,
    "labels_per_node_range": {
        "minimum": 4,
        "maximum": 6,
        "median": 5,
        "mode": 5
    },
    "label_distribution": {
        "4_labels": {
            "count": 2500,
            "percentage": 8.93,
            "description": "Control, Process, Alert, Zone nodes with basic structure"
        },
        "5_labels": {
            "count": 22500,
            "percentage": 80.36,
            "description": "Core nodes with full classification hierarchy"
        },
        "6_labels": {
            "count": 3000,
            "percentage": 10.71,
            "description": "Device nodes with enhanced monitoring attributes"
        }
    },
    "subsectors": {
        "Banking": {
            "count": 9630,
            "percentage": 34.4,
            "primary_node_types": ["Measurement (6800)", "Property (1800)", "Device (1400)"],
            "description": "Retail, commercial, investment, and digital banking operations"
        },
        "CapitalMarkets": {
            "count": 9329,
            "percentage": 33.3,
            "primary_node_types": ["Measurement (5950)", "Property (1654)", "Device (1225)"],
            "description": "Securities trading, asset management, and investment services"
        },
        "PaymentSystems": {
            "count": 9041,
            "percentage": 32.3,
            "primary_node_types": ["Measurement (4250)", "Property (1546)", "Device (875)"],
            "description": "Payment processing, clearing, settlement, and money transfer"
        }
    },
    "ontology_integration": {
        "compliance_frameworks": {
            "PCI_DSS": 450,
            "SOX": 320,
            "Basel_III": 280,
            "Dodd_Frank": 250
        },
        "monitoring_framework": {
            "total_monitoring_nodes": 20500,
            "percentage_of_total": 73.21,
            "key_label": "Monitoring"
        }
    },
    "unique_label_names": 29,
    "total_label_assignments": 142800,
    "governance_model": "Multi-subsector hierarchical with financial regulatory compliance",
    "compliance_focus": "PCI-DSS, SOX, Basel III, Dodd-Frank with real-time transaction monitoring",
    "security_emphasis": "Critical - fraud detection, AML/KYC controls, and regulatory compliance tracking"
}

# Update completeness percentage
registry['metadata']['registry_completeness'] = f"{(len(registry['sectors_registered']) / registry['total_sectors_target']) * 100:.2f}% ({len(registry['sectors_registered'])} of {registry['total_sectors_target']} sectors registered)"

# Save updated registry
with open(REGISTRY_PATH, 'w') as f:
    json.dump(registry, f, indent=2)

print("✓ Updated sector-schema-registry.json with FINANCIAL_SERVICES")
print(f"  Total sectors registered: {len(registry['sectors_registered'])}")
print(f"  Registry completeness: {registry['metadata']['registry_completeness']}")
