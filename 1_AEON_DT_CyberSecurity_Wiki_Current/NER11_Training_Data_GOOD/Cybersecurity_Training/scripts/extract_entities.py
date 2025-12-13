#!/usr/bin/env python3
"""
Entity Extraction Script for IoC Files
Extracts ALL entities from 40+ IoC markdown files
"""

import re
import json
import os
from pathlib import Path
from typing import Dict, List, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

# Base directory
BASE_DIR = Path("/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/NER11_Training_Data_GOOD/Cybersecurity_Training")
OUTPUT_DIR = BASE_DIR / "docs" / "e01_apt_ingestion"

# Entity tag patterns
ENTITY_PATTERNS = {
    'INDICATOR': r'<INDICATOR>(.*?)</INDICATOR>',
    'THREAT_ACTOR': r'<THREAT_ACTOR>(.*?)</THREAT_ACTOR>',
    'CAMPAIGN': r'<CAMPAIGN>(.*?)</CAMPAIGN>',
    'VULNERABILITY': r'<VULNERABILITY>(.*?)</VULNERABILITY>',
    'MALWARE': r'<MALWARE>(.*?)</MALWARE>',
    'SECTOR': r'<SECTOR>(.*?)</SECTOR>',
    'TECHNIQUE': r'<TECHNIQUE>(.*?)</TECHNIQUE>',
    'ATTACK_PATTERN': r'<ATTACK_PATTERN>(.*?)</ATTACK_PATTERN>',
}

# IoC classification patterns
IOC_PATTERNS = {
    'IP': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
    'IP_RANGE': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$',
    'DOMAIN': r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)+(\[\.\])?$',
    'MD5': r'^[a-fA-F0-9]{32}$',
    'SHA1': r'^[a-fA-F0-9]{40}$',
    'SHA256': r'^[a-fA-F0-9]{64}$',
    'EMAIL': r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-\[\]]+$',
    'REGISTRY': r'^HK(LM|CU|CR|U|CC)\\',
    'URL': r'^hxxp[s]?://|^http[s]?://',
    'FILE_PATH': r'^[A-Z]:\\|^/|^\\\\',
    'MUTEX': r'(Global\\|Local\\)',
    'CVE': r'^CVE-\d{4}-\d{4,}$',
    'AS_NUMBER': r'^AS\d+$',
    'PORT': r'^:\d{1,5}$|^port\s+\d{1,5}$',
}

def classify_ioc(value: str) -> str:
    """Classify an IoC by type"""
    value = value.strip()

    # Check specific patterns
    for ioc_type, pattern in IOC_PATTERNS.items():
        if re.search(pattern, value, re.IGNORECASE):
            return ioc_type

    # Default classification
    if '\\' in value and not value.startswith('http'):
        return 'FILE_PATH'
    elif '.' in value and len(value.split('.')) > 1:
        return 'DOMAIN_OR_FILE'
    else:
        return 'OTHER'

def extract_context(content: str, match_start: int, match_end: int, context_length: int = 100) -> Dict[str, str]:
    """Extract context around a match"""
    before_start = max(0, match_start - context_length)
    after_end = min(len(content), match_end + context_length)

    return {
        'before': content[before_start:match_start].strip(),
        'after': content[match_end:after_end].strip()
    }

def extract_from_file(file_path: Path) -> Dict:
    """Extract all entities from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        file_entities = {
            'file': file_path.name,
            'entities': {},
            'statistics': {}
        }

        # Extract each entity type
        for entity_type, pattern in ENTITY_PATTERNS.items():
            matches = re.finditer(pattern, content, re.DOTALL)
            entities = []

            for match in matches:
                value = match.group(1).strip()

                # Get context
                context = extract_context(content, match.start(), match.end())

                entity_data = {
                    'value': value,
                    'type': entity_type,
                    'context_before': context['before'][-100:],  # Last 100 chars
                    'context_after': context['after'][:100],     # First 100 chars
                }

                # Additional classification for INDICATOR type
                if entity_type == 'INDICATOR':
                    entity_data['ioc_type'] = classify_ioc(value)

                entities.append(entity_data)

            file_entities['entities'][entity_type] = entities
            file_entities['statistics'][entity_type] = len(entities)

        # Calculate total
        file_entities['statistics']['TOTAL'] = sum(file_entities['statistics'].values())

        return file_entities

    except Exception as e:
        print(f"Error processing {file_path.name}: {e}")
        return {
            'file': file_path.name,
            'error': str(e),
            'entities': {},
            'statistics': {}
        }

def process_all_files(file_list: List[str]) -> Dict:
    """Process all files in parallel"""
    all_entities = {
        'files_processed': 0,
        'total_entities': 0,
        'entity_counts': {},
        'ioc_type_counts': {},
        'files': []
    }

    # Get full paths
    file_paths = [BASE_DIR / fname for fname in file_list]

    # Process in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(extract_from_file, path): path for path in file_paths}

        for future in as_completed(futures):
            file_data = future.result()
            all_entities['files'].append(file_data)
            all_entities['files_processed'] += 1

            # Update statistics
            for entity_type, count in file_data.get('statistics', {}).items():
                if entity_type != 'TOTAL':
                    all_entities['entity_counts'][entity_type] = \
                        all_entities['entity_counts'].get(entity_type, 0) + count

            # Count IoC types for INDICATOR entities
            for entity in file_data.get('entities', {}).get('INDICATOR', []):
                ioc_type = entity.get('ioc_type', 'OTHER')
                all_entities['ioc_type_counts'][ioc_type] = \
                    all_entities['ioc_type_counts'].get(ioc_type, 0) + 1

            print(f"Processed: {file_data['file']} - {file_data.get('statistics', {}).get('TOTAL', 0)} entities")

    # Calculate total
    all_entities['total_entities'] = sum(all_entities['entity_counts'].values())

    return all_entities

def main():
    """Main extraction process"""
    print("Starting entity extraction from IoC files...")

    # Get list of IoC files
    ioc_files = []
    for file in os.listdir(BASE_DIR):
        if ('IoC' in file or 'Indicator' in file) and file.endswith('.md'):
            ioc_files.append(file)

    ioc_files.sort()

    print(f"Found {len(ioc_files)} IoC files to process")

    # Process all files
    results = process_all_files(ioc_files)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save results
    output_file = OUTPUT_DIR / "parsed_entities.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "="*60)
    print("EXTRACTION COMPLETE")
    print("="*60)
    print(f"Files processed: {results['files_processed']}")
    print(f"Total entities extracted: {results['total_entities']}")
    print("\nEntity counts by type:")
    for entity_type, count in sorted(results['entity_counts'].items()):
        print(f"  {entity_type}: {count}")
    print("\nIoC type distribution:")
    for ioc_type, count in sorted(results['ioc_type_counts'].items()):
        print(f"  {ioc_type}: {count}")
    print(f"\nResults saved to: {output_file}")
    print("="*60)

if __name__ == "__main__":
    main()
