# NER10 Training Data Reference

**File**: README_TRAINING_DATA_v3.0_2025-11-19.md
**Created**: 2025-11-19 22:00:00 UTC
**Version**: v3.0.0
**Purpose**: Reference guide to comprehensive NER10 training data
**Status**: ACTIVE

---

## Training Data Location

**Primary Location**: `/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/`

**Total**: 673 markdown files, 16 MB
**Organization**: By sector and psychometric topic

---

## Training Data Inventory

### Psychometric & Behavioral (Level 4)

**Cognitive_Biases/**: 20+ bias types, 652+ annotations
- Availability Heuristic, Anchoring, Confirmation, Normalcy, etc.
- Corporate Personality Assessments (DISC, Hogan, CliftonStrengths)

**Personality_Frameworks/**: Complete personality models
- MBTI (16 types), Enneagram (9 types), HEXACO, Attachment Theory

**Psychohistory_Demographics/**: Population modeling
- Cyber behavior patterns, demographic cohorts, generational analysis

### All 16 CISA Sectors (Level 0-3)

1. Water_Sector
2. Energy_Sector
3. Transportation_Sector
4. Healthcare_Sector
5. Chemical_Sector
6. Manufacturing_Sector
7. Communications_Sector (IT_Telecom)
8. Commercial_Sector
9. Dams_Sector
10. Defense_Sector
11. Emergency_Sector
12. Financial_Sector
13. Food_Agriculture_Sector
14. Government_Sector
15. Hydrogen_Sector
16. Nuclear (in development)

### Technical Frameworks

- **IEC_62443**: Industrial security standards
- **Cyber_Attack_Frameworks**: Attack modeling
- **Vendor_Refinement_Datasets**: Siemens, Alstom
- **Protocol_Training_Data**: Network protocols
- **Threat_Intelligence_Expanded**: Threat actor data

---

## Alignment with 6-Level Architecture

**Level 0-3**: Sector-specific equipment, facility, operational data
**Level 4**: Psychometric entities (biases, personality, behavioral patterns)
**Level 5**: Information streams and event context
**Level 6**: Predictive patterns and psychohistory modeling

**NER10 Enhancement**: Extracts psychological entities from text to populate Level 4-6

---

## Usage

**For NER10 Training**:
1. Use cognitive bias annotations for bias detection
2. Use personality frameworks for individual profiling
3. Use psychohistory demographics for population modeling
4. Use sector data for domain-specific entity recognition

**Training Pipeline**: See `../01_ARCHITECTURE/04_NER10_TRAINING_SPECIFICATION_v3.0_2025-11-19.md`

**Vision Fulfillment**: 100% - Training data perfectly aligned with McKenney psychohistory vision
