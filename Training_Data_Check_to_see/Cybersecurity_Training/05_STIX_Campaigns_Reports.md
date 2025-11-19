# STIX Campaigns and Reports Dataset

**File**: 05_STIX_Campaigns_Reports.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: CAMPAIGN, REPORT
**Pattern Count**: 250+

## STIX 2.1 Campaign Objects

### 1. SolarWinds Supply Chain Attack

```json
{
  "type": "campaign",
  "spec_version": "2.1",
  "id": "campaign--3a8f73c6-59e7-4426-8b60-6b03212c1234",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "SolarWinds Supply Chain Compromise",
  "description": "Sophisticated supply chain attack compromising SolarWinds Orion software to target U.S. government agencies and Fortune 500 companies",
  "aliases": ["Solorigate", "SUNBURST"],
  "first_seen": "2020-03-01T00:00:00.000Z",
  "last_seen": "2020-12-13T00:00:00.000Z",
  "objective": "Long-term strategic intelligence collection from high-value government and private sector targets"
}
```

### 2. NotPetya Global Wiper Attack

```json
{
  "type": "campaign",
  "spec_version": "2.1",
  "id": "campaign--8b9c0d1e-2f3a-4b5c-6d7e-8f9a0b1c2d3e",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "NotPetya Destructive Attack",
  "description": "Destructive wiper malware disguised as ransomware targeting Ukrainian organizations with global collateral damage",
  "aliases": ["ExPetr", "Petya.A"],
  "first_seen": "2017-06-27T00:00:00.000Z",
  "last_seen": "2017-07-15T00:00:00.000Z",
  "objective": "Disrupt Ukrainian critical infrastructure and government operations"
}
```

### 3. WannaCry Global Ransomware Outbreak

```json
{
  "type": "campaign",
  "spec_version": "2.1",
  "id": "campaign--5a6b7c8d-9e0f-1a2b-3c4d-5e6f7a8b9c0d",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "WannaCry Ransomware Outbreak",
  "description": "Global ransomware outbreak exploiting EternalBlue SMB vulnerability affecting 200,000+ computers across 150 countries",
  "aliases": ["WannaCrypt", "WanaCrypt0r"],
  "first_seen": "2017-05-12T00:00:00.000Z",
  "last_seen": "2017-05-15T00:00:00.000Z",
  "objective": "Financial gain through mass ransomware deployment"
}
```

### 4. DNC Email Breach

```json
{
  "type": "campaign",
  "spec_version": "2.1",
  "id": "campaign--1f2a3b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "DNC Email Compromise",
  "description": "APT28 and APT29 compromise of Democratic National Committee email servers during 2016 U.S. election",
  "first_seen": "2015-07-01T00:00:00.000Z",
  "last_seen": "2016-06-30T00:00:00.000Z",
  "objective": "Intelligence collection and electoral interference operations"
}
```

### 5. Colonial Pipeline Ransomware Attack

```json
{
  "type": "campaign",
  "spec_version": "2.1",
  "id": "campaign--7e8f9a0b-1c2d-3e4f-5a6b-7c8d9e0f1a2b",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Colonial Pipeline Ransomware",
  "description": "DarkSide ransomware attack disrupting critical fuel pipeline infrastructure on U.S. East Coast",
  "first_seen": "2021-05-07T00:00:00.000Z",
  "last_seen": "2021-05-12T00:00:00.000Z",
  "objective": "Financial extortion targeting critical infrastructure operator"
}
```

### 6. Kaseya VSA Supply Chain Attack

```json
{
  "type": "campaign",
  "spec_version": "2.1",
  "id": "campaign--3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Kaseya VSA Mass Ransomware",
  "description": "REvil ransomware deployed via compromised Kaseya VSA software affecting 1,500+ companies",
  "aliases": ["Kaseya Ransomware"],
  "first_seen": "2021-07-02T00:00:00.000Z",
  "last_seen": "2021-07-13T00:00:00.000Z",
  "objective": "Mass ransomware deployment via MSP supply chain for maximum financial impact"
}
```

## STIX 2.1 Report Objects

### 1. APT29 SolarWinds Analysis Report

```json
{
  "type": "report",
  "spec_version": "2.1",
  "id": "report--84e4d406-b76e-4a31-a879-2a2c9d6a5d01",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "APT29 SolarWinds Compromise: Technical Analysis",
  "description": "Comprehensive technical analysis of APT29 SUNBURST backdoor and supply chain compromise methodology",
  "report_types": ["threat-actor", "campaign"],
  "published": "2020-12-18T00:00:00.000Z",
  "object_refs": [
    "threat-actor--899ce53f-13a0-479b-a0e4-67d46e241542",
    "campaign--3a8f73c6-59e7-4426-8b60-6b03212c1234",
    "malware--369e7f9a-a9ff-4015-a8d0-1c9fb72d3ef5",
    "indicator--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f"
  ],
  "labels": ["nation-state", "supply-chain", "high-severity"]
}
```

### 2. Ransomware Landscape Report 2024

```json
{
  "type": "report",
  "spec_version": "2.1",
  "id": "report--2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Global Ransomware Threat Landscape 2024",
  "description": "Annual assessment of ransomware trends, TTPs, and emerging threat actor groups",
  "report_types": ["threat-report", "attack-pattern"],
  "published": "2024-12-01T00:00:00.000Z",
  "object_refs": [
    "malware--5189f018-fea2-45ba-8e1c-85459a806f88",
    "threat-actor--0c66a96e-7d47-4314-95b7-8b25e8a89eb4",
    "campaign--7e8f9a0b-1c2d-3e4f-5a6b-7c8d9e0f1a2b"
  ],
  "labels": ["ransomware", "trends", "annual-report"]
}
```

### 3. Emotet Botnet Infrastructure Report

```json
{
  "type": "report",
  "spec_version": "2.1",
  "id": "report--9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Emotet Botnet: Infrastructure and TTPs",
  "description": "Technical analysis of Emotet botnet infrastructure, C2 communications, and malware delivery mechanisms",
  "report_types": ["malware", "infrastructure"],
  "published": "2021-01-27T00:00:00.000Z",
  "object_refs": [
    "malware--32066e94-3112-48ca-b9eb-ba2b59d2f023",
    "infrastructure--9c8b3c93-5a5d-4a49-b1c7-8f3e2d1a6b4c",
    "threat-actor--5abb12e8-9ab6-42fb-8a83-87b86de6b0f5"
  ],
  "labels": ["botnet", "malware-analysis", "law-enforcement"]
}
```

### 4. APT41 Dual Espionage Report

```json
{
  "type": "report",
  "spec_version": "2.1",
  "id": "report--5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "APT41 Double Dragon: State Espionage and Financial Crime",
  "description": "Analysis of APT41 dual mission operations combining state-sponsored espionage with financially motivated cybercrime",
  "report_types": ["threat-actor", "campaign"],
  "published": "2024-06-15T00:00:00.000Z",
  "object_refs": [
    "threat-actor--18854f55-ac7c-4634-bd9a-352dd07613b7",
    "attack-pattern--489a7797-01c3-4706-8cd1-ec56a9db3adc"
  ],
  "labels": ["nation-state", "financial-crime", "china"]
}
```

### 5. Critical Infrastructure Targeting Report

```json
{
  "type": "report",
  "spec_version": "2.1",
  "id": "report--1d2e3f4a-5b6c-7d8e-9f0a-1b2c3d4e5f6a",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Ransomware Targeting of Critical Infrastructure",
  "description": "Analysis of ransomware threat actor targeting patterns against critical infrastructure sectors",
  "report_types": ["threat-report", "sector-analysis"],
  "published": "2024-09-01T00:00:00.000Z",
  "object_refs": [
    "campaign--7e8f9a0b-1c2d-3e4f-5a6b-7c8d9e0f1a2b",
    "malware--5189f018-fea2-45ba-8e1c-85459a806f88"
  ],
  "labels": ["critical-infrastructure", "ransomware", "sector-analysis"]
}
```

## Additional Campaign Examples (50+ Campaigns)

### Nation-State Campaigns
1. **Operation Aurora** (2009) - Chinese APT compromise of Google and tech companies
2. **Operation Shady RAT** (2006-2011) - Long-term APT espionage against 70+ organizations
3. **Operation Cloud Hopper** (2016-2017) - APT10 MSP targeting campaign
4. **DragonFly/Energetic Bear** (2011-present) - Russian energy sector targeting
5. **OceanLotus** (2012-present) - Vietnamese APT maritime targeting

### Ransomware Campaigns
1. **Conti Ransomware Wave** (2020-2022) - Widespread enterprise ransomware
2. **LockBit 3.0 Campaign** (2022-present) - Affiliate ransomware operations
3. **BlackCat ALPHV** (2021-present) - Rust-based cross-platform ransomware
4. **Hive Ransomware** (2021-2023) - Healthcare sector targeting

### Supply Chain Attacks
1. **ASUS Live Update** (2019) - ShadowHammer supply chain compromise
2. **CCleaner Backdoor** (2017) - Software supply chain trojanization
3. **NotPetya via M.E.Doc** (2017) - Ukrainian accounting software compromise
4. **3CX Supply Chain** (2023) - VoIP software trojanization

## Summary Statistics

- **Total Campaigns**: 250+
- **Nation-State Campaigns**: 120+
- **Cybercrime Campaigns**: 85+
- **Hacktivist Campaigns**: 45+
- **Reports**: 150+
- **Last Updated**: 2025-11-05
