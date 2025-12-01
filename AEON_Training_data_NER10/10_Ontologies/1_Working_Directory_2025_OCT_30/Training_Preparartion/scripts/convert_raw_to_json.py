#!/usr/bin/env python3
"""
Convert raw CSV data to JSON for easier processing
Handles complex CSV with embedded commas and quotes
"""

import json
import re
from pathlib import Path

def parse_csv_line(line: str) -> list:
    """Parse CSV line with proper quote handling"""
    fields = []
    current_field = []
    in_quotes = False

    i = 0
    while i < len(line):
        char = line[i]

        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                # Escaped quote
                current_field.append('"')
                i += 1
            else:
                # Toggle quote state
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            # Field separator
            fields.append(''.join(current_field).strip())
            current_field = []
        else:
            current_field.append(char)

        i += 1

    # Add last field
    if current_field or line.endswith(','):
        fields.append(''.join(current_field).strip())

    return fields

def convert_cve_cwe():
    """Convert CVE-CWE raw data to JSON"""
    input_path = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/raw_cve_cwe_data.txt')
    output_path = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/cve_cwe_data.json')

    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        # Skip header
        header_line = f.readline().strip()
        headers = [h.strip() for h in parse_csv_line(header_line)]

        for line_num, line in enumerate(f, 2):
            line = line.strip()
            if not line:
                continue

            try:
                fields = parse_csv_line(line)
                if len(fields) >= 5:
                    # Clean quotes from field values
                    fields = [f.strip('"').strip() for f in fields]

                    record = {
                        'cve_id': fields[0],
                        'cve_description': fields[1],
                        'cwe_id': fields[2],
                        'cwe_name': fields[3],
                        'cwe_description': fields[4] if len(fields) > 4 else ''
                    }

                    # Skip deprecated entries
                    if 'DEPRECATED' not in record['cwe_name']:
                        data.append(record)
            except Exception as e:
                print(f"Error parsing line {line_num}: {e}")
                continue

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(data)} CVE-CWE records to {output_path}")
    return len(data)

def convert_capec_attack():
    """Convert CAPEC-ATTACK raw data to JSON"""
    input_path = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/capec_attack_raw.txt')
    output_path = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/data/ner_training/capec_attack_data.json')

    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        # Skip header
        header_line = f.readline().strip()

        for line_num, line in enumerate(f, 2):
            line = line.strip()
            if not line:
                continue

            try:
                fields = parse_csv_line(line)
                if len(fields) >= 4:
                    # Clean quotes
                    fields = [f.strip('"').strip() for f in fields]

                    record = {
                        'capec_id': fields[0],
                        'capec_name': fields[1],
                        'capec_description': fields[2],
                        'attack_id': fields[3] if len(fields) > 3 else '',
                        'attack_name': fields[4] if len(fields) > 4 else '',
                        'attack_description': fields[5] if len(fields) > 5 else ''
                    }

                    # Skip NULL attack entries
                    if record['attack_name'] and record['attack_name'] != 'NULL':
                        data.append(record)
            except Exception as e:
                print(f"Error parsing line {line_num}: {e}")
                continue

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(data)} CAPEC-ATTACK records to {output_path}")
    return len(data)

def main():
    print("Converting raw CSV data to JSON...")
    print()

    cve_count = convert_cve_cwe()
    attack_count = convert_capec_attack()

    print()
    print(f"Total records converted: {cve_count + attack_count}")
    print("  CVE-CWE: {} records".format(cve_count))
    print("  CAPEC-ATTACK: {} records".format(attack_count))

if __name__ == '__main__':
    main()
