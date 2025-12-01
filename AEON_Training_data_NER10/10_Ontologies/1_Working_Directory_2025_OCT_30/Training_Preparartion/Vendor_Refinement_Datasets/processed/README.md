# Vendor Training Data - Processing Summary

**Generated**: 2025-11-06
**Purpose**: Convert vendor variations to markdown training data for NER model training

## Summary Statistics

- **Total Vendor Variations Extracted**: 517
- **Markdown Files Created**: 11
- **Total VENDOR Annotations Generated**: 4,136
- **Contexts Per Variation**: 8 sentences
- **Source Files Processed**: 2
  - `Vendor_Name_Variations.json` (73 canonical vendors, 451 unique aliases)
  - `Vendor_Aliases_Database.csv` (315 unique aliases)

## File Organization

Training data split into 11 markdown files for manageable processing:

- `vendor_training_part_01.md` - 50 variations (400 annotations)
- `vendor_training_part_02.md` - 50 variations (400 annotations)
- `vendor_training_part_03.md` - 50 variations (400 annotations)
- `vendor_training_part_04.md` - 50 variations (400 annotations)
- `vendor_training_part_05.md` - 50 variations (400 annotations)
- `vendor_training_part_06.md` - 50 variations (400 annotations)
- `vendor_training_part_07.md` - 50 variations (400 annotations)
- `vendor_training_part_08.md` - 50 variations (400 annotations)
- `vendor_training_part_09.md` - 50 variations (400 annotations)
- `vendor_training_part_10.md` - 50 variations (400 annotations)
- `vendor_training_part_11.md` - 17 variations (136 annotations)

**Total File Size**: ~432 KB

## Contextual Sentence Templates

Each vendor variation appears in 8 different contextual sentences using these patterns:

1. "The [[VENDOR]] manufactures [[EQUIPMENT]] for [[PROTOCOL]] systems."
2. "[[VENDOR]] provides advanced [[EQUIPMENT]] solutions for critical infrastructure."
3. "In [[REGION]], [[VENDOR]] is a leading supplier of [[EQUIPMENT]] technology."
4. "The [[EQUIPMENT]] system from [[VENDOR]] complies with [[PROTOCOL]] standards."
5. "[[VENDOR]] offers comprehensive [[EQUIPMENT]] platforms for [[INDUSTRY]] applications."
6. "Operators rely on [[VENDOR]] for secure [[EQUIPMENT]] deployment in [[PROTOCOL]] networks."
7. "[[VENDOR]] develops innovative [[EQUIPMENT]] products for modern [[INDUSTRY]] environments."
8. "The [[PROTOCOL]]-compliant [[EQUIPMENT]] from [[VENDOR]] ensures reliable operations."

## Domain Coverage

### Equipment Types (18 categories)
- SCADA systems, protection relays, automation controllers, grid monitoring equipment
- Railway signaling systems, video surveillance systems, access control systems
- Fire alarm panels, network switches, power management systems, RTUs
- Communication systems, dispatch consoles, security systems, control systems
- PLC controllers, DCS platforms, historian systems, HMI interfaces

### Protocols (13 standards)
- IEC 61850, DNP3, Modbus, PROFINET, EtherNet/IP, GOOSE, MMS
- IEC 60870-5, BACnet, OPC UA, CIP, SNMP, IEEE 802.1X

### Regions (6 areas)
- North America, Europe, Asia Pacific, Global, Middle East, Latin America

### Industries (10 sectors)
- Energy, transportation, manufacturing, security, telecommunications
- Defense, healthcare, financial services, building automation, water utilities

## Major Vendor Categories Included

1. **Energy/Power** (20 vendors): Siemens, ABB, GE, Schneider Electric, etc.
2. **Transportation** (5 vendors): Alstom, Hitachi Rail, Siemens Mobility, etc.
3. **Security/Surveillance** (15 vendors): Axis, Hikvision, Bosch, Honeywell, etc.
4. **Communications** (10 vendors): Cisco, Motorola, L3Harris, Avaya, etc.
5. **Defense** (6 vendors): Northrop Grumman, Raytheon, Lockheed Martin, etc.
6. **IT Infrastructure** (8 vendors): Dell, HPE, Juniper, Palo Alto Networks, etc.
7. **Industrial Automation** (15 vendors): Rockwell, Emerson, Yokogawa, etc.
8. **Financial Services** (2 vendors): FIS Global, Temenos, etc.

## Data Quality Features

- **Realistic Context**: Sentences mirror real-world technical documentation
- **Industry Terminology**: Uses authentic protocols, equipment types, and regions
- **Variation Coverage**: Each alias appears in multiple contexts
- **Format Consistency**: Structured markdown for easy parsing
- **Metadata Preservation**: Canonical names, regions, and industries tracked

## Usage Recommendations

1. **Training**: Use all 11 files for comprehensive NER model training
2. **Validation**: Reserve 10-15% for validation set (Part 10-11)
3. **Testing**: Use separate held-out vendor data not in this set
4. **Augmentation**: Can combine with other entity types (EQUIPMENT, PROTOCOL)

## Note on Discrepancy

Original task mentioned 2,156 variations. Actual dataset contained 517 unique vendor variations:
- JSON file: 451 unique aliases across 73 canonical vendors
- CSV file: 315 rows (257 overlapping with JSON)
- Combined unique: 517 variations

The 4,136 VENDOR annotations generated (517 × 8 contexts) provide substantial training data for vendor name recognition.

## Next Steps

1. Parse markdown files to extract VENDOR annotations
2. Convert to spaCy training format (JSONL or binary)
3. Combine with existing EQUIPMENT and PROTOCOL annotations
4. Train or fine-tune NER model with expanded entity coverage
