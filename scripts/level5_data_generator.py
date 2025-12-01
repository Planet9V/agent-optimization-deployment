#!/usr/bin/env python3
"""
Level 5 Data Generator - AEON Digital Twin
Generates 6,000 Level 5 nodes for Information Streams layer
"""

import json
import random
import uuid
from datetime import datetime, timedelta
import hashlib

# Configuration
TOTAL_NODES = 6000
INFORMATION_EVENTS = 5000
GEOPOLITICAL_EVENTS = 500
THREAT_FEEDS = 3
COGNITIVE_BIASES = 30  # 7 existing + 23 new
EVENT_PROCESSORS = 10

# Event types for InformationEvent
EVENT_TYPES = [
    'CVE_DISCLOSURE', 'BREACH_REPORT', 'VULNERABILITY_SCAN',
    'PATCH_RELEASE', 'THREAT_INTEL', 'ZERO_DAY', 'MALWARE_DETECTION',
    'RANSOMWARE_ATTACK', 'SUPPLY_CHAIN', 'INSIDER_THREAT'
]

# Sources for information events
SOURCES = [
    'NVD', 'CISA', 'SecurityFeed', 'MediaReport', 'Internal',
    'FireEye', 'CrowdStrike', 'Mandiant', 'Talos', 'X-Force',
    'SANS', 'US-CERT', 'FBI', 'DHS', 'NSA'
]

# Severity levels
SEVERITIES = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
SEVERITY_WEIGHTS = [10, 25, 40, 20, 5]  # Percentage distribution

# 16 Critical Infrastructure Sectors
SECTORS = [
    'Energy', 'Water', 'Transportation', 'Healthcare',
    'Financial', 'Communications', 'Manufacturing', 'IT',
    'Chemical', 'Nuclear', 'Defense', 'Food',
    'Government', 'Emergency', 'Dams', 'Commercial'
]

# Geopolitical event types
GEO_EVENT_TYPES = [
    'SANCTIONS', 'CONFLICT', 'DIPLOMATIC', 'ECONOMIC',
    'ELECTION', 'TRADE_WAR', 'CYBER_WARFARE', 'ESPIONAGE',
    'TREATY', 'SUMMIT'
]

# APT Groups
APT_GROUPS = [
    'APT1', 'APT28', 'APT29', 'Lazarus', 'Carbanak',
    'FIN7', 'Cobalt', 'DarkHydrus', 'OilRig', 'MuddyWater',
    'Turla', 'Equation', 'Sofacy', 'CozyBear', 'FancyBear'
]

# Cognitive biases (7 existing + 23 new)
COGNITIVE_BIASES = {
    # Existing 7
    'availability_bias': 'MEMORY',
    'confirmation_bias': 'PERCEPTION',
    'anchoring_bias': 'DECISION',
    'overconfidence_effect': 'DECISION',
    'groupthink': 'SOCIAL',
    'framing_effect': 'PERCEPTION',
    'status_quo_bias': 'DECISION',
    # 23 new biases
    'recency_bias': 'MEMORY',
    'normalcy_bias': 'PERCEPTION',
    'authority_bias': 'SOCIAL',
    'bandwagon_effect': 'SOCIAL',
    'hindsight_bias': 'MEMORY',
    'planning_fallacy': 'DECISION',
    'sunk_cost_fallacy': 'DECISION',
    'zero_risk_bias': 'DECISION',
    'neglect_of_probability': 'PERCEPTION',
    'clustering_illusion': 'PERCEPTION',
    'gamblers_fallacy': 'DECISION',
    'hot_hand_fallacy': 'DECISION',
    'illusion_of_control': 'PERCEPTION',
    'overconfidence_bias': 'DECISION',
    'pessimism_bias': 'PERCEPTION',
    'optimism_bias': 'PERCEPTION',
    'self_serving_bias': 'SOCIAL',
    'attribution_bias': 'SOCIAL',
    'halo_effect': 'SOCIAL',
    'horn_effect': 'SOCIAL',
    'contrast_effect': 'PERCEPTION',
    'primacy_effect': 'MEMORY',
    'dunning_kruger_effect': 'DECISION'
}

# Event processors
EVENT_PROCESSOR_TYPES = [
    'CVE_Processor', 'Media_Analyzer', 'Sentiment_Calculator',
    'Correlation_Engine', 'Bias_Activator', 'Risk_Scorer',
    'Impact_Assessor', 'Trend_Detector', 'Alert_Generator',
    'Report_Builder'
]

def generate_information_events(count=5000):
    """Generate InformationEvent nodes"""
    events = []
    base_time = datetime.now() - timedelta(days=180)

    for i in range(count):
        event_id = f"IE-{uuid.uuid4().hex[:12]}"
        timestamp = base_time + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        # Select severity with proper distribution
        severity = random.choices(SEVERITIES, weights=SEVERITY_WEIGHTS)[0]

        # Generate scores based on severity
        if severity == 'CRITICAL':
            cvss_score = round(random.uniform(9.0, 10.0), 1)
            epss_score = round(random.uniform(0.7, 1.0), 3)
            fear_factor = round(random.uniform(8.0, 10.0), 1)
            reality_factor = round(random.uniform(7.0, 9.5), 1)
        elif severity == 'HIGH':
            cvss_score = round(random.uniform(7.0, 8.9), 1)
            epss_score = round(random.uniform(0.4, 0.7), 3)
            fear_factor = round(random.uniform(6.0, 8.0), 1)
            reality_factor = round(random.uniform(5.0, 7.0), 1)
        elif severity == 'MEDIUM':
            cvss_score = round(random.uniform(4.0, 6.9), 1)
            epss_score = round(random.uniform(0.1, 0.4), 3)
            fear_factor = round(random.uniform(3.0, 6.0), 1)
            reality_factor = round(random.uniform(3.0, 5.0), 1)
        elif severity == 'LOW':
            cvss_score = round(random.uniform(1.0, 3.9), 1)
            epss_score = round(random.uniform(0.01, 0.1), 3)
            fear_factor = round(random.uniform(1.0, 3.0), 1)
            reality_factor = round(random.uniform(0.5, 2.0), 1)
        else:  # INFO
            cvss_score = round(random.uniform(0.0, 0.9), 1)
            epss_score = round(random.uniform(0.001, 0.01), 3)
            fear_factor = round(random.uniform(0.0, 1.0), 1)
            reality_factor = round(random.uniform(0.0, 0.5), 1)

        fear_reality_gap = round(fear_factor - reality_factor, 1)

        # Select affected sectors
        num_sectors = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]
        affected_sectors = random.sample(SECTORS, num_sectors)

        # Media and social metrics
        media_articles = random.choices(
            [0, random.randint(1, 10), random.randint(10, 100), random.randint(100, 1000)],
            weights=[20, 40, 30, 10]
        )[0]

        social_amplification = min(100, int(media_articles * random.uniform(0.1, 2.0)))

        event = {
            'eventId': event_id,
            'eventType': random.choice(EVENT_TYPES),
            'timestamp': timestamp.isoformat(),
            'source': random.choice(SOURCES),
            'severity': severity,
            'cvssScore': cvss_score,
            'epssScore': epss_score,
            'affectedSectors': affected_sectors,
            'affectedAssets': random.randint(10, 100000),
            'fearFactor': fear_factor,
            'realityFactor': reality_factor,
            'fearRealityGap': fear_reality_gap,
            'mediaArticles': media_articles,
            'socialAmplification': social_amplification,
            'description': f"{severity} {random.choice(EVENT_TYPES).lower().replace('_', ' ')} affecting {', '.join(affected_sectors[:2])} sectors",
            'metadata': {
                'confidence': round(random.uniform(0.6, 1.0), 2),
                'verified': random.choice([True, True, True, False]),
                'actionable': severity in ['CRITICAL', 'HIGH']
            }
        }
        events.append(event)

    return events

def generate_geopolitical_events(count=500):
    """Generate GeopoliticalEvent nodes"""
    events = []
    base_time = datetime.now() - timedelta(days=365)

    # Country codes for geopolitical events
    countries = [
        'US', 'CN', 'RU', 'IR', 'KP', 'IL', 'SA', 'IN', 'PK',
        'GB', 'FR', 'DE', 'JP', 'KR', 'TW', 'UA', 'SY', 'AF'
    ]

    for i in range(count):
        event_id = f"GE-{uuid.uuid4().hex[:12]}"
        timestamp = base_time + timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23)
        )

        # Select countries involved
        num_countries = random.choices([2, 3, 4], weights=[60, 30, 10])[0]
        involved_countries = random.sample(countries, num_countries)

        # Tension and correlation
        tension_level = round(random.uniform(1, 10), 1)
        cyber_correlation = round(tension_level / 10 * random.uniform(0.5, 1.2), 2)
        cyber_correlation = min(1.0, cyber_correlation)

        # Related APT groups based on countries
        num_apts = random.choices([0, 1, 2, 3], weights=[30, 40, 20, 10])[0]
        apt_groups = random.sample(APT_GROUPS, num_apts) if num_apts > 0 else []

        # Economic impact varies by event type
        event_type = random.choice(GEO_EVENT_TYPES)
        if event_type in ['SANCTIONS', 'TRADE_WAR']:
            economic_impact = random.randint(1000000, 1000000000)
        else:
            economic_impact = random.randint(100000, 100000000)

        event = {
            'eventId': event_id,
            'eventType': event_type,
            'timestamp': timestamp.isoformat(),
            'countries': involved_countries,
            'tensionLevel': tension_level,
            'cyberCorrelation': cyber_correlation,
            'aptGroups': apt_groups,
            'historicalPattern': f"Similar to {random.randint(2010, 2023)} incident",
            'economicImpact': economic_impact,
            'description': f"{event_type} involving {', '.join(involved_countries[:2])} with tension level {tension_level}"
        }
        events.append(event)

    return events

def generate_threat_feeds():
    """Generate ThreatFeed nodes"""
    feeds = [
        {
            'feedId': 'TF-001',
            'feedName': 'CISA_AIS',
            'feedType': 'STIX',
            'reliability': 0.95,
            'latency': 2,
            'coverage': 0.60,
            'lastUpdate': datetime.now().isoformat(),
            'eventsProcessed': random.randint(50000, 100000),
            'configuration': {
                'endpoint': 'https://ais.cisa.gov/api/v2',
                'auth': 'api_key',
                'format': 'STIX 2.1',
                'update_frequency': '5 minutes'
            }
        },
        {
            'feedId': 'TF-002',
            'feedName': 'Commercial_Aggregate',
            'feedType': 'Multiple',
            'reliability': 0.85,
            'latency': 5,
            'coverage': 0.80,
            'lastUpdate': datetime.now().isoformat(),
            'eventsProcessed': random.randint(100000, 200000),
            'configuration': {
                'providers': ['FireEye', 'CrowdStrike', 'Mandiant'],
                'auth': 'oauth2',
                'format': 'JSON',
                'update_frequency': '10 minutes'
            }
        },
        {
            'feedId': 'TF-003',
            'feedName': 'OSINT_Collection',
            'feedType': 'Custom',
            'reliability': 0.70,
            'latency': 15,
            'coverage': 0.90,
            'lastUpdate': datetime.now().isoformat(),
            'eventsProcessed': random.randint(200000, 500000),
            'configuration': {
                'sources': ['Twitter', 'Reddit', 'HackerNews', 'GitHub'],
                'auth': 'mixed',
                'format': 'Custom',
                'update_frequency': '30 minutes'
            }
        }
    ]
    return feeds

def generate_cognitive_biases():
    """Generate CognitiveBias nodes (expanded set)"""
    biases = []

    for bias_name, category in COGNITIVE_BIASES.items():
        bias_id = f"CB-{hashlib.md5(bias_name.encode()).hexdigest()[:8]}"

        # Different thresholds for different categories
        if category == 'DECISION':
            activation_threshold = round(random.uniform(4.0, 7.0), 1)
        elif category == 'SOCIAL':
            activation_threshold = round(random.uniform(3.0, 6.0), 1)
        elif category == 'MEMORY':
            activation_threshold = round(random.uniform(5.0, 8.0), 1)
        else:  # PERCEPTION
            activation_threshold = round(random.uniform(4.0, 7.0), 1)

        current_level = round(random.uniform(0.0, activation_threshold * 0.8), 1)

        # Decision types affected
        decision_types = [
            'patch_prioritization', 'budget_allocation', 'incident_response',
            'threat_assessment', 'risk_evaluation', 'vendor_selection',
            'security_investment', 'staffing_decisions', 'policy_changes'
        ]
        affected_decisions = random.sample(decision_types, random.randint(2, 5))

        # Mitigation strategies
        mitigation_strategies = [
            'structured_analysis', 'peer_review', 'red_team_exercise',
            'data_driven_decisions', 'external_audit', 'diverse_perspectives',
            'devil_advocate', 'pre_mortem_analysis', 'decision_journal'
        ]
        mitigations = random.sample(mitigation_strategies, random.randint(2, 4))

        # Sector susceptibility
        sector_susceptibility = {}
        for sector in SECTORS:
            sector_susceptibility[sector] = round(random.uniform(0.3, 1.0), 2)

        bias = {
            'biasId': bias_id,
            'biasName': bias_name,
            'category': category,
            'activationThreshold': activation_threshold,
            'currentLevel': current_level,
            'affectedDecisions': affected_decisions,
            'mitigationStrategies': mitigations,
            'sectorSusceptibility': sector_susceptibility
        }
        biases.append(bias)

    return biases

def generate_event_processors():
    """Generate EventProcessor nodes"""
    processors = []

    for processor_type in EVENT_PROCESSOR_TYPES:
        processor_id = f"EP-{hashlib.md5(processor_type.encode()).hexdigest()[:8]}"

        processor = {
            'processorId': processor_id,
            'processorType': processor_type,
            'status': 'ACTIVE',
            'throughput': random.randint(100, 1000),
            'latency': random.randint(10, 100),
            'errorRate': round(random.uniform(0.0, 0.05), 3),
            'lastUpdate': datetime.now().isoformat(),
            'configuration': {
                'parallelism': random.randint(2, 8),
                'batch_size': random.randint(10, 100),
                'timeout': random.randint(30, 300)
            }
        }
        processors.append(processor)

    return processors

def save_data():
    """Generate and save all Level 5 data"""
    print("Generating Level 5 Data...")

    # Generate all data
    print(f"Generating {INFORMATION_EVENTS} InformationEvents...")
    info_events = generate_information_events(INFORMATION_EVENTS)

    print(f"Generating {GEOPOLITICAL_EVENTS} GeopoliticalEvents...")
    geo_events = generate_geopolitical_events(GEOPOLITICAL_EVENTS)

    print(f"Generating {THREAT_FEEDS} ThreatFeeds...")
    threat_feeds = generate_threat_feeds()

    print(f"Generating {len(COGNITIVE_BIASES)} CognitiveBiases...")
    cognitive_biases = generate_cognitive_biases()

    print(f"Generating {EVENT_PROCESSORS} EventProcessors...")
    event_processors = generate_event_processors()

    # Combine all data
    level5_data = {
        'metadata': {
            'level': 'LEVEL_5_INFORMATION_STREAMS',
            'version': '1.0.0',
            'generated': datetime.now().isoformat(),
            'total_nodes': TOTAL_NODES,
            'node_counts': {
                'InformationEvent': len(info_events),
                'GeopoliticalEvent': len(geo_events),
                'ThreatFeed': len(threat_feeds),
                'CognitiveBias': len(cognitive_biases),
                'EventProcessor': len(event_processors)
            }
        },
        'data': {
            'information_events': info_events,
            'geopolitical_events': geo_events,
            'threat_feeds': threat_feeds,
            'cognitive_biases': cognitive_biases,
            'event_processors': event_processors
        }
    }

    # Save to file
    output_file = '/home/jim/2_OXOT_Projects_Dev/data/level5_generated_data.json'
    with open(output_file, 'w') as f:
        json.dump(level5_data, f, indent=2)

    print(f"\nData saved to: {output_file}")

    # Print summary
    total = sum([
        len(info_events),
        len(geo_events),
        len(threat_feeds),
        len(cognitive_biases),
        len(event_processors)
    ])

    print("\n=== Generation Summary ===")
    print(f"InformationEvents: {len(info_events):,}")
    print(f"GeopoliticalEvents: {len(geo_events):,}")
    print(f"ThreatFeeds: {len(threat_feeds):,}")
    print(f"CognitiveBiases: {len(cognitive_biases):,}")
    print(f"EventProcessors: {len(event_processors):,}")
    print(f"TOTAL NODES: {total:,}")

    return level5_data

if __name__ == "__main__":
    save_data()