#!/usr/bin/env python3
import os
import re
import zipfile
from collections import defaultdict

def extract_docx_text(filepath):
    """Extract text from DOCX file"""
    try:
        with zipfile.ZipFile(filepath) as docx:
            xml_content = docx.read('word/document.xml').decode('utf-8')
            text = re.sub('<[^>]+>', ' ', xml_content)
            return ' '.join(text.split())
    except Exception as e:
        return ""

def extract_threat_data(text):
    """Extract threat intelligence from text"""
    data = {
        'threat_actors': set(),
        'apt_groups': set(),
        'mitre_techniques': set(),
        'cves': set(),
        'ips': set(),
        'domains': set(),
        'hashes': set(),
        'protocols': set(),
        'sectors': set()
    }
    
    # APT groups and threat actors
    apt_pattern = r'(APT\d+|APT-\d+|Volt Typhoon|Lazarus|Sandworm|Cozy Bear|FrostyGoop|RansomHub|BlackCat|Qilin|DragonForce|LockBit|Rhysida|Akira|Play|Scattered Spider|Cl0p|VOLTZITE|CYBERAV3NGERS)'
    data['apt_groups'].update(re.findall(apt_pattern, text, re.IGNORECASE))
    
    # MITRE ATT&CK techniques
    mitre_pattern = r'T\d{4}(?:\.\d{3})?'
    data['mitre_techniques'].update(re.findall(mitre_pattern, text))
    
    # CVEs
    cve_pattern = r'CVE-\d{4}-\d{4,}'
    data['cves'].update(re.findall(cve_pattern, text))
    
    # IP addresses
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    potential_ips = re.findall(ip_pattern, text)
    data['ips'].update([ip for ip in potential_ips if all(0 <= int(octet) <= 255 for octet in ip.split('.'))])
    
    # Domains (simplified)
    domain_pattern = r'\b[a-z0-9-]+\.[a-z]{2,}\b'
    data['domains'].update(re.findall(domain_pattern, text.lower()))
    
    # Hashes (MD5, SHA1, SHA256)
    hash_pattern = r'\b[a-f0-9]{32}\b|\b[a-f0-9]{40}\b|\b[a-f0-9]{64}\b'
    data['hashes'].update(re.findall(hash_pattern, text.lower()))
    
    # Protocols
    protocol_pattern = r'(Modbus|DNP3|BACnet|OPC|SCADA|IEC 61850|Profinet|EtherNet/IP)'
    data['protocols'].update(re.findall(protocol_pattern, text, re.IGNORECASE))
    
    # Critical infrastructure sectors
    sector_pattern = r'(Energy|Water|Transportation|Healthcare|Manufacturing|Chemical|Food|Rail|Utilities|Government|Finance|Critical Infrastructure)'
    data['sectors'].update(re.findall(sector_pattern, text, re.IGNORECASE))
    
    return data

# Process all DOCX files
all_data = defaultdict(set)
file_count = 0

for filename in os.listdir('.'):
    if filename.endswith('.docx'):
        file_count += 1
        filepath = os.path.join('.', filename)
        text = extract_docx_text(filepath)
        if text:
            data = extract_threat_data(text)
            for key, values in data.items():
                all_data[key].update(values)

# Output results
print(f"=== THREAT INTELLIGENCE EXTRACTION RESULTS ===")
print(f"Files Processed: {file_count}")
print()

print(f"THREAT ACTORS/APT GROUPS: {len(all_data['apt_groups'])}")
for actor in sorted(all_data['apt_groups'])[:20]:
    print(f"  - {actor}")
if len(all_data['apt_groups']) > 20:
    print(f"  ... and {len(all_data['apt_groups']) - 20} more")
print()

print(f"MITRE ATT&CK TECHNIQUES: {len(all_data['mitre_techniques'])}")
for technique in sorted(all_data['mitre_techniques'])[:15]:
    print(f"  - {technique}")
if len(all_data['mitre_techniques']) > 15:
    print(f"  ... and {len(all_data['mitre_techniques']) - 15} more")
print()

print(f"CVEs: {len(all_data['cves'])}")
for cve in sorted(all_data['cves'])[:15]:
    print(f"  - {cve}")
if len(all_data['cves']) > 15:
    print(f"  ... and {len(all_data['cves']) - 15} more")
print()

print(f"ICS/OT PROTOCOLS: {len(all_data['protocols'])}")
for protocol in sorted(all_data['protocols']):
    print(f"  - {protocol}")
print()

print(f"CRITICAL INFRASTRUCTURE SECTORS: {len(all_data['sectors'])}")
for sector in sorted(all_data['sectors']):
    print(f"  - {sector}")
print()

print(f"INDICATORS OF COMPROMISE (IoCs):")
print(f"  - IP Addresses: {len(all_data['ips'])}")
print(f"  - Domains: {len(all_data['domains'])}")
print(f"  - File Hashes: {len(all_data['hashes'])}")
print()

# Enhancement mapping
print("=== ENHANCEMENT MAPPING ===")
print(f"E01 (APT Threat Intel): {len(all_data['apt_groups'])} threat actors identified")
print(f"E02 (STIX Integration): {len(all_data['apt_groups']) + len(all_data['mitre_techniques']) + len(all_data['ips']) + len(all_data['domains'])} STIX objects possible")
print(f"E03 (SBOM Analysis): {len(all_data['cves'])} CVEs for software correlation")
print(f"E12 (NOW/NEXT/NEVER): {len(all_data['cves'])} CVEs for prioritization")
print(f"ICS/OT Focus: {len(all_data['protocols'])} industrial protocols covered")
print(f"Sector Coverage: {len(all_data['sectors'])} critical infrastructure sectors")
