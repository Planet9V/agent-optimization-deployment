#!/usr/bin/env python3
"""
Pattern Extraction Validator
Validates predicted pattern counts against actual extracted patterns from sector documentation.
Supports all 24 entity types:
- Baseline (7): VENDOR, EQUIPMENT, PROTOCOL, OPERATION, ARCHITECTURE, SECURITY, SUPPLIER
- Cybersecurity (17): THREAT_MODEL, TACTIC, TECHNIQUE, ATTACK_PATTERN, VULNERABILITY, WEAKNESS,
                       INDICATOR, THREAT_ACTOR, CAMPAIGN, SOFTWARE_COMPONENT, HARDWARE_COMPONENT,
                       PERSONALITY_TRAIT, COGNITIVE_BIAS, INSIDER_INDICATOR, SOCIAL_ENGINEERING,
                       ATTACK_VECTOR, MITIGATION
"""

import re
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

class PatternExtractor:
    """Extract ICS/OT entities from training documentation"""

    def __init__(self):
        self.entity_patterns = {
            # Baseline entity types (7)
            'VENDOR': self._build_vendor_patterns(),
            'EQUIPMENT': self._build_equipment_patterns(),
            'PROTOCOL': self._build_protocol_patterns(),
            'OPERATION': self._build_operation_patterns(),
            'ARCHITECTURE': self._build_architecture_patterns(),
            'SECURITY': self._build_security_patterns(),
            'SUPPLIER': self._build_supplier_patterns(),
            # Cybersecurity entity types (17)
            'THREAT_MODEL': self._build_threat_model_patterns(),
            'TACTIC': self._build_tactic_patterns(),
            'TECHNIQUE': self._build_technique_patterns(),
            'ATTACK_PATTERN': self._build_attack_pattern_patterns(),
            'VULNERABILITY': self._build_vulnerability_patterns(),
            'WEAKNESS': self._build_weakness_patterns(),
            'INDICATOR': self._build_indicator_patterns(),
            'THREAT_ACTOR': self._build_threat_actor_patterns(),
            'CAMPAIGN': self._build_campaign_patterns(),
            'SOFTWARE_COMPONENT': self._build_software_component_patterns(),
            'HARDWARE_COMPONENT': self._build_hardware_component_patterns(),
            'PERSONALITY_TRAIT': self._build_personality_trait_patterns(),
            'COGNITIVE_BIAS': self._build_cognitive_bias_patterns(),
            'INSIDER_INDICATOR': self._build_insider_indicator_patterns(),
            'SOCIAL_ENGINEERING': self._build_social_engineering_patterns(),
            'ATTACK_VECTOR': self._build_attack_vector_patterns(),
            'MITIGATION': self._build_mitigation_patterns()
        }

    def _build_vendor_patterns(self) -> List[re.Pattern]:
        """Patterns for vendor/manufacturer entities"""
        vendors = [
            r'Siemens\s+(?:Energy\s+Automation|AG|Power\s+Automation)?',
            r'ABB\s+(?:Power\s+Grids|Automation)?',
            r'Schneider\s+Electric',
            r'Honeywell\s+(?:Process\s+Solutions)?',
            r'Rockwell\s+Automation',
            r'Allen-Bradley',
            r'GE\s+(?:Grid\s+Solutions|Digital\s+Energy)?',
            r'Emerson\s+(?:Process\s+Management)?',
            r'Yokogawa',
            r'SEL\s+Schweitzer\s+Engineering',
            r'Mitsubishi\s+Electric',
            r'Omron',
            r'Cisco\s+(?:Industrial)?',
            r'Palo\s+Alto\s+Networks',
            r'Fortinet',
            r'Thales',
            r'Alstom',
            r'Motorola\s+Solutions',
            r'Harris\s+Corporation',
            r'Ericsson',
            r'Nokia'
        ]
        return [re.compile(v, re.IGNORECASE) for v in vendors]

    def _build_equipment_patterns(self) -> List[re.Pattern]:
        """Patterns for equipment/model entities"""
        equipment = [
            r'(?:Model\s+)?[A-Z]{2,}-\d{3,}[A-Z\-]*\b',  # SEL-751A, IE-4000-16T4G-E
            r'(?:Series\s+)?\d{4,}[A-Z]+\b',  # 5220-AC, 2130NGIPS
            r'ControlLogix\s+[A-Z]\d+[A-Z]?\b',  # ControlLogix L85E
            r'SICAM\s+[A-Z]+\s+[A-Z]{2,}\s*\d*',  # SICAM ARTERE PAS 8
            r'(?:RTU|PLC|DCS|HMI|SCADA)\s+\d{3,}',  # RTU-5000, PLC-7400
            r'(?:PA|FortiGate|ASA|Firepower)-\d{3,}[A-Z]*',  # PA-5220, FortiGate-200F
            r'[A-Z]{2,}\d{2,}-\d+[A-Z\-]*'  # SGT5-8000H, APX-8000XE
        ]
        return [re.compile(e) for e in equipment]

    def _build_protocol_patterns(self) -> List[re.Pattern]:
        """Patterns for protocol entities"""
        protocols = [
            r'DNP3(?:\s+Secure\s+Authentication)?(?:\s+v\d+\.\d+)?',
            r'IEC\s+6\d{4}(?:-\d+-\d+)?',  # IEC 61850, IEC 62443-3-3
            r'Modbus\s+(?:TCP|RTU|Plus)?',
            r'NERC\s+CIP-\d{3}-\d+',  # NERC CIP-005-6
            r'IEEE\s+\d{3,}(?:\.\d+)?',  # IEEE 1815-2012, IEEE 1474
            r'NIST\s+SP\s+800-\d+',  # NIST SP 800-82
            r'OPC\s+(?:UA|DA)',
            r'PROFINET\s+(?:IO|RT)?',
            r'EtherNet/IP',
            r'GOOSE',
            r'MMS',
            r'ETCS\s+Level\s+\d+',
            r'CBTC',
            r'PTC',
            r'AES-\d{3}'  # AES-256
        ]
        return [re.compile(p, re.IGNORECASE) for p in protocols]

    def _build_operation_patterns(self) -> List[re.Pattern]:
        """Patterns for operational entities"""
        operations = [
            r'(?:Load|Power|Voltage|Current|Frequency)\s+[A-Z][a-z]+\w*',
            r'Generator_\w+',
            r'Substation_\w+',
            r'Circuit_\w+',
            r'Transmission_\w+',
            r'Distribution_\w+',
            r'Control_\w+',
            r'Protection_\w+',
            r'Switchgear_\w+',
            r'Transformer_\w+',
            r'SCADA_\w+',
            r'Operations_\w+',
            r'Maintenance_\w+',
            r'Monitoring_\w+',
            r'(?:Real-Time|Automated)\s+\w+\s+(?:Operations|Monitoring|Control)',
            r'Load\s+(?:Balancing|Distribution|Transfer)',
            r'Fault\s+(?:Detection|Isolation|Recovery)'
        ]
        return [re.compile(o) for o in operations]

    def _build_architecture_patterns(self) -> List[re.Pattern]:
        """Patterns for architecture entities"""
        architecture = [
            r'(?:Network|System|Security)\s+Architecture',
            r'(?:DMZ|VLAN|VPN|ESP)\s+\w*',
            r'Purdue\s+Model\s+Level\s+\d+',
            r'(?:Hierarchical|Redundant|Distributed)\s+Architecture',
            r'(?:Primary|Secondary|Backup)\s+(?:System|Controller|Network)',
            r'(?:Hot|Cold|Warm)\s+Standby',
            r'N\+\d+\s+Redundancy',
            r'Ring\s+Topology',
            r'Star\s+Topology',
            r'Mesh\s+Network',
            r'(?:Fiber|Copper)\s+Infrastructure'
        ]
        return [re.compile(a, re.IGNORECASE) for a in architecture]

    def _build_security_patterns(self) -> List[re.Pattern]:
        """Patterns for security entities"""
        security = [
            r'(?:NGFW|Firewall|IDS|IPS)\s+\w*',
            r'Security\s+Level\s+SL\s+\d+',
            r'(?:Authentication|Authorization|Encryption)',
            r'(?:Access|Network|Perimeter)\s+Control',
            r'(?:Intrusion|Threat)\s+(?:Detection|Prevention)',
            r'DMZ\s+\w*',
            r'Electronic\s+Security\s+Perimeter',
            r'Deep\s+Packet\s+Inspection',
            r'Vulnerability\s+\w+',
            r'Security\s+(?:Audit|Assessment|Review)',
            r'Penetration\s+Testing',
            r'SIEM',
            r'Zero\s+Trust'
        ]
        return [re.compile(s, re.IGNORECASE) for s in security]

    def _build_supplier_patterns(self) -> List[re.Pattern]:
        """Patterns for supplier entities"""
        suppliers = [
            r'(?:Cable|Wire|Conductor)\s+\w+\s+(?:Supplier|Manufacturer)',
            r'(?:Transformer|Switchgear|Breaker)\s+(?:Supplier|Vendor)',
            r'Component\s+(?:Supplier|Vendor)',
            r'OEM\s+(?:Supplier|Partner)',
            r'(?:Primary|Secondary)\s+Supplier',
            r'Supply\s+Chain\s+\w+'
        ]
        return [re.compile(s, re.IGNORECASE) for s in suppliers]

    def _build_threat_model_patterns(self) -> List[re.Pattern]:
        """Patterns for threat modeling frameworks"""
        threat_models = [
            r'STRIDE\s+(?:Threat|Category|Analysis|Model)',
            r'PASTA\s+(?:Stage|Methodology|Risk|Process)',
            r'Threat\s+Model(?:ing|s)?',
            r'Attack\s+Surface\s+Analysis',
            r'DREAD\s+(?:Rating|Model)',
            r'Attack\s+Tree\s+Analysis',
            r'Threat\s+Assessment\s+Framework'
        ]
        return [re.compile(t, re.IGNORECASE) for t in threat_models]

    def _build_tactic_patterns(self) -> List[re.Pattern]:
        """Patterns for MITRE ATT&CK tactics"""
        tactics = [
            r'Initial\s+Access',
            r'Execution',
            r'Persistence',
            r'Privilege\s+Escalation',
            r'Defense\s+Evasion',
            r'Credential\s+Access',
            r'Discovery',
            r'Lateral\s+Movement',
            r'Collection',
            r'Command\s+and\s+Control',
            r'Exfiltration',
            r'Impact',
            r'TA\d{4}'
        ]
        return [re.compile(t, re.IGNORECASE) for t in tactics]

    def _build_technique_patterns(self) -> List[re.Pattern]:
        """Patterns for MITRE ATT&CK techniques"""
        techniques = [
            r'T\d{4}(?:\.\d{3})?',  # T1566, T1566.001
            r'Phishing',
            r'Spearphishing\s+(?:Attachment|Link|via\s+Service)',
            r'PowerShell',
            r'Credential\s+Dumping',
            r'Process\s+Injection',
            r'Lateral\s+Tool\s+Transfer',
            r'Remote\s+Desktop\s+Protocol',
            r'Valid\s+Accounts',
            r'Scheduled\s+Task(?:s)?',
            r'Windows\s+Management\s+Instrumentation',
            r'Masquerading',
            r'DLL\s+(?:Side-Loading|Search\s+Order\s+Hijacking)',
            r'Exploitation\s+for\s+(?:Privilege\s+Escalation|Client\s+Execution)'
        ]
        return [re.compile(t, re.IGNORECASE) for t in techniques]

    def _build_attack_pattern_patterns(self) -> List[re.Pattern]:
        """Patterns for CAPEC attack patterns"""
        attack_patterns = [
            r'CAPEC-\d{1,4}',
            r'Attack\s+Pattern',
            r'Social\s+Engineering\s+Attack',
            r'Injection\s+Attack',
            r'Denial\s+of\s+Service',
            r'Man-in-the-Middle',
            r'Spoofing\s+Attack',
            r'Resource\s+Manipulation',
            r'Abuse\s+of\s+Functionality',
            r'Data\s+Structure\s+Attacks'
        ]
        return [re.compile(a, re.IGNORECASE) for a in attack_patterns]

    def _build_vulnerability_patterns(self) -> List[re.Pattern]:
        """Patterns for CVE vulnerabilities"""
        vulnerabilities = [
            r'CVE-\d{4}-\d{4,}',
            r'Zero-Day\s+Vulnerability',
            r'Known\s+Exploited\s+Vulnerability',
            r'Critical\s+Vulnerability',
            r'High-Severity\s+Vulnerability',
            r'Unpatched\s+Vulnerability',
            r'N-Day\s+Vulnerability'
        ]
        return [re.compile(v, re.IGNORECASE) for v in vulnerabilities]

    def _build_weakness_patterns(self) -> List[re.Pattern]:
        """Patterns for CWE weaknesses"""
        weaknesses = [
            r'CWE-\d{1,5}',
            r'SQL\s+Injection',
            r'Cross-Site\s+Scripting',
            r'Buffer\s+Overflow',
            r'Improper\s+(?:Input\s+Validation|Authentication|Authorization)',
            r'Use\s+After\s+Free',
            r'Integer\s+Overflow',
            r'Path\s+Traversal',
            r'Command\s+Injection',
            r'XML\s+External\s+Entity',
            r'Security\s+Misconfiguration',
            r'Insecure\s+Deserialization',
            r'Broken\s+(?:Authentication|Access\s+Control)',
            r'Sensitive\s+Data\s+Exposure'
        ]
        return [re.compile(w, re.IGNORECASE) for w in weaknesses]

    def _build_indicator_patterns(self) -> List[re.Pattern]:
        """Patterns for STIX indicators of compromise"""
        indicators = [
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',  # IP addresses
            r'\b[a-f0-9]{32}\b',  # MD5 hashes
            r'\b[a-f0-9]{64}\b',  # SHA-256 hashes
            r'\b[a-f0-9]{40}\b',  # SHA-1 hashes
            r'hxxp[s]?://[\w\.\[\]]+',  # Defanged URLs
            r'[\w\-]+\[\.\][\w\-]+',  # Defanged domains
            r'Indicator\s+of\s+Compromise',
            r'IOC',
            r'Malicious\s+(?:IP|Domain|URL|Hash)',
            r'Command\s+and\s+Control\s+(?:Server|Infrastructure)'
        ]
        return [re.compile(i, re.IGNORECASE) for i in indicators]

    def _build_threat_actor_patterns(self) -> List[re.Pattern]:
        """Patterns for threat actor groups"""
        threat_actors = [
            r'APT\d{1,2}',
            r'Lazarus\s+Group',
            r'FIN\d+',
            r'(?:Cozy|Fancy)\s+Bear',
            r'Sandworm',
            r'Carbanak',
            r'BRONZE\s+\w+',
            r'HAFNIUM',
            r'NOBELIUM',
            r'Threat\s+Actor\s+Group',
            r'Advanced\s+Persistent\s+Threat',
            r'Nation-State\s+Actor',
            r'Cyber\s+Criminal\s+Group'
        ]
        return [re.compile(t, re.IGNORECASE) for t in threat_actors]

    def _build_campaign_patterns(self) -> List[re.Pattern]:
        """Patterns for named attack campaigns"""
        campaigns = [
            r'Operation\s+\w+',
            r'Campaign\s+\w+',
            r'NotPetya',
            r'WannaCry',
            r'SolarWinds',
            r'Colonial\s+Pipeline',
            r'Stuxnet',
            r'DarkSide',
            r'REvil',
            r'Kaseya',
            r'Log4Shell',
            r'ProxyLogon',
            r'PrintNightmare'
        ]
        return [re.compile(c, re.IGNORECASE) for c in campaigns]

    def _build_software_component_patterns(self) -> List[re.Pattern]:
        """Patterns for SBOM software components"""
        software_components = [
            r'[\w\-\.]+@\d+\.\d+\.\d+',  # package@version
            r'npm\s+package',
            r'PyPI\s+package',
            r'Maven\s+artifact',
            r'NuGet\s+package',
            r'RubyGems',
            r'Composer\s+package',
            r'Go\s+module',
            r'Cargo\s+crate',
            r'Software\s+Bill\s+of\s+Materials',
            r'SBOM',
            r'Third-Party\s+Component',
            r'Open\s+Source\s+(?:Library|Component)'
        ]
        return [re.compile(s, re.IGNORECASE) for s in software_components]

    def _build_hardware_component_patterns(self) -> List[re.Pattern]:
        """Patterns for HBOM hardware components"""
        hardware_components = [
            r'Microcontroller\s+[\w\-]+',
            r'STM32[A-Z]\d+',
            r'ESP(?:32|8266)',
            r'Arduino\s+\w+',
            r'Raspberry\s+Pi\s+\d+',
            r'FPGA\s+[\w\-]+',
            r'System\s+on\s+Chip',
            r'SoC',
            r'Hardware\s+Bill\s+of\s+Materials',
            r'HBOM',
            r'Embedded\s+System',
            r'Firmware\s+Component'
        ]
        return [re.compile(h, re.IGNORECASE) for h in hardware_components]

    def _build_personality_trait_patterns(self) -> List[re.Pattern]:
        """Patterns for Big Five and Dark Triad personality traits"""
        personality_traits = [
            r'Openness',
            r'Conscientiousness',
            r'Extraversion',
            r'Agreeableness',
            r'Neuroticism',
            r'Machiavellianism',
            r'Narcissism',
            r'Psychopathy',
            r'Big\s+Five\s+Trait',
            r'Dark\s+Triad\s+Profile',
            r'Personality\s+Assessment',
            r'Psychological\s+Profile'
        ]
        return [re.compile(p, re.IGNORECASE) for p in personality_traits]

    def _build_cognitive_bias_patterns(self) -> List[re.Pattern]:
        """Patterns for cognitive biases exploited in social engineering"""
        cognitive_biases = [
            r'Authority\s+Bias',
            r'Urgency\s+Bias',
            r'Social\s+Proof',
            r'Confirmation\s+Bias',
            r'Anchoring\s+Bias',
            r'Reciprocity\s+Bias',
            r'Scarcity\s+(?:Bias|Principle)',
            r'Liking\s+Principle',
            r'Commitment\s+and\s+Consistency',
            r'Fear\s+of\s+Missing\s+Out',
            r'FOMO',
            r'Cognitive\s+Bias'
        ]
        return [re.compile(c, re.IGNORECASE) for c in cognitive_biases]

    def _build_insider_indicator_patterns(self) -> List[re.Pattern]:
        """Patterns for CERT insider threat indicators"""
        insider_indicators = [
            r'Unauthorized\s+Access',
            r'Data\s+Exfiltration',
            r'Credential\s+Misuse',
            r'Disgruntlement',
            r'Financial\s+Stress',
            r'Policy\s+Violation',
            r'Insider\s+Threat',
            r'Malicious\s+Insider',
            r'Negligent\s+Insider',
            r'Compromised\s+Insider',
            r'Unusual\s+Access\s+Pattern',
            r'After-Hours\s+Activity',
            r'Large\s+Data\s+Transfer',
            r'Personal\s+Email\s+Usage'
        ]
        return [re.compile(i, re.IGNORECASE) for i in insider_indicators]

    def _build_social_engineering_patterns(self) -> List[re.Pattern]:
        """Patterns for social engineering tactics"""
        social_engineering = [
            r'(?:Spear)?Phishing',
            r'Pretexting',
            r'Baiting',
            r'Quid\s+Pro\s+Quo',
            r'Tailgating',
            r'Vishing',
            r'Smishing',
            r'Whaling',
            r'Business\s+Email\s+Compromise',
            r'BEC',
            r'CEO\s+Fraud',
            r'Social\s+Engineering\s+(?:Attack|Technique)',
            r'Impersonation',
            r'Watering\s+Hole'
        ]
        return [re.compile(s, re.IGNORECASE) for s in social_engineering]

    def _build_attack_vector_patterns(self) -> List[re.Pattern]:
        """Patterns for attack vectors"""
        attack_vectors = [
            r'Remote\s+Code\s+Execution',
            r'SQL\s+Injection\s+Vector',
            r'Command\s+Injection',
            r'Path\s+Traversal',
            r'Deserialization\s+Attack',
            r'XML\s+External\s+Entity',
            r'Server-Side\s+Request\s+Forgery',
            r'SSRF',
            r'Cross-Site\s+Request\s+Forgery',
            r'CSRF',
            r'File\s+Upload\s+Vulnerability',
            r'Directory\s+Traversal',
            r'Local\s+File\s+Inclusion',
            r'Remote\s+File\s+Inclusion'
        ]
        return [re.compile(a, re.IGNORECASE) for a in attack_vectors]

    def _build_mitigation_patterns(self) -> List[re.Pattern]:
        """Patterns for security controls and mitigations"""
        mitigations = [
            r'Multi-Factor\s+Authentication',
            r'MFA',
            r'Access\s+Control\s+List',
            r'ACL',
            r'Network\s+Segmentation',
            r'Intrusion\s+(?:Detection|Prevention)\s+System',
            r'(?:IDS|IPS)',
            r'Security\s+Control\s+(?:AC|AU|CA|CM|CP|IA|IR|MA|MP|PE|PL|PS|PT|RA|SA|SC|SI|SR)-\d+',
            r'NIST\s+800-53\s+Control',
            r'Input\s+Validation',
            r'Parameterized\s+Queries',
            r'Least\s+Privilege',
            r'Defense\s+in\s+Depth',
            r'Security\s+Awareness\s+Training',
            r'Patch\s+Management',
            r'Vulnerability\s+Scanning',
            r'Penetration\s+Testing',
            r'Security\s+Information\s+and\s+Event\s+Management',
            r'SIEM'
        ]
        return [re.compile(m, re.IGNORECASE) for m in mitigations]

    def extract_patterns(self, text: str) -> Dict[str, List[str]]:
        """Extract all entity patterns from text"""
        results = defaultdict(list)

        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = pattern.findall(text)
                results[entity_type].extend(matches)

        # Deduplicate while preserving order
        for entity_type in results:
            results[entity_type] = list(dict.fromkeys(results[entity_type]))

        return dict(results)

    def process_file(self, filepath: Path) -> Dict[str, any]:
        """Process a single markdown file and extract patterns"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            patterns = self.extract_patterns(content)
            total_patterns = sum(len(p) for p in patterns.values())

            return {
                'file': filepath.name,
                'word_count': len(content.split()),
                'patterns': patterns,
                'total_patterns': total_patterns,
                'distribution': {k: len(v) for k, v in patterns.items()}
            }
        except Exception as e:
            return {'file': filepath.name, 'error': str(e)}

    def process_sector(self, sector_path: Path) -> Dict[str, any]:
        """Process all markdown files in a sector directory"""
        results = {
            'sector': sector_path.name,
            'files': [],
            'total_patterns': 0,
            'total_words': 0,
            'distribution': defaultdict(int)
        }

        # Find all markdown files
        md_files = list(sector_path.rglob('*.md'))

        for md_file in md_files:
            if md_file.name in ['COMPLETION_REPORT.md', 'VALIDATION_SUMMARY.md', 'README.md']:
                continue  # Skip metadata files

            file_result = self.process_file(md_file)

            if 'error' not in file_result:
                results['files'].append(file_result)
                results['total_patterns'] += file_result['total_patterns']
                results['total_words'] += file_result['word_count']

                for entity_type, count in file_result['distribution'].items():
                    results['distribution'][entity_type] += count

        results['distribution'] = dict(results['distribution'])
        results['file_count'] = len(results['files'])

        return results


def validate_sectors(base_path: str) -> Dict[str, any]:
    """Validate all sectors and compare to predictions"""

    extractor = PatternExtractor()
    base = Path(base_path)

    # Sector predictions from completion summary
    predictions = {
        # Baseline 13 sectors
        'Energy_Sector': 885,
        'Chemical_Sector': 850,
        'Transportation_Sector': 900,
        'IT_Telecom_Sector': 950,
        'Healthcare_Sector': 800,
        'Financial_Sector': 750,
        'Food_Agriculture_Sector': 345,
        'Government_Sector': 5493,
        'Defense_Sector': 3800,
        'Dams_Sector': 700,
        'Critical_Manufacturing_Sector': 850,
        'Water_Sector_Retry': 231,
        'Nuclear_Sector': 600,
        # New CISA sectors (Option B expansion)
        'Communications_Sector': 900,
        'Emergency_Services_Sector': 700,
        'Commercial_Facilities_Sector': 600,
        # Vendor refinement
        'Vendor_Refinement_Datasets': 2200,
        # Cybersecurity training domains
        'Cybersecurity_Training': 18000  # Combined estimate for all 35 files
    }

    validation_results = {
        'sectors': {},
        'totals': {
            'predicted_patterns': sum(predictions.values()),
            'actual_patterns': 0,
            'predicted_f1': 0.94,  # Average across sectors
            'sectors_processed': 0
        },
        'comparison': []
    }

    for sector_name, predicted_count in predictions.items():
        sector_path = base / sector_name

        if not sector_path.exists():
            print(f"⚠️  Sector not found: {sector_name}")
            continue

        print(f"📊 Processing {sector_name}...")
        sector_result = extractor.process_sector(sector_path)

        actual_count = sector_result['total_patterns']
        variance = ((actual_count - predicted_count) / predicted_count * 100) if predicted_count > 0 else 0

        comparison = {
            'sector': sector_name,
            'predicted': predicted_count,
            'actual': actual_count,
            'variance_percent': round(variance, 2),
            'file_count': sector_result['file_count'],
            'word_count': sector_result['total_words'],
            'distribution': sector_result['distribution']
        }

        validation_results['sectors'][sector_name] = sector_result
        validation_results['comparison'].append(comparison)
        validation_results['totals']['actual_patterns'] += actual_count
        validation_results['totals']['sectors_processed'] += 1

        status = "✅" if abs(variance) < 15 else "⚠️"
        print(f"  {status} Predicted: {predicted_count}, Actual: {actual_count}, Variance: {variance:+.1f}%")

    return validation_results


if __name__ == "__main__":
    base_path = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion"

    print("🚀 Pattern Extraction Validation Starting...")
    print("=" * 80)

    results = validate_sectors(base_path)

    # Save results to JSON
    output_file = Path(base_path) / "Data Pipeline Builder" / "PATTERN_EXTRACTION_VALIDATION_RESULTS.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print("📊 VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Sectors Processed: {results['totals']['sectors_processed']}")
    print(f"Total Predicted Patterns: {results['totals']['predicted_patterns']:,}")
    print(f"Total Actual Patterns: {results['totals']['actual_patterns']:,}")

    variance = ((results['totals']['actual_patterns'] - results['totals']['predicted_patterns'])
                / results['totals']['predicted_patterns'] * 100)
    print(f"Overall Variance: {variance:+.2f}%")

    print(f"\n✅ Results saved to: {output_file}")
    print("\nℹ️  Next: Generate detailed validation report")
