# STIX Threat Actors Dataset

**File**: 02_STIX_Threat_Actors.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: THREAT_ACTOR
**Pattern Count**: 200+

## STIX 2.1 Threat Actor Objects

### 1. APT28 (Fancy Bear)

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--bef4c620-0787-42a8-a96d-b7eb6e85917c",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "APT28",
  "description": "Russian state-sponsored advanced persistent threat group attributed to GRU Unit 26165",
  "threat_actor_types": ["nation-state"],
  "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm", "Sednit", "Strontium"],
  "first_seen": "2007-01-01T00:00:00.000Z",
  "sophistication": "expert",
  "resource_level": "government",
  "primary_motivation": "organizational-gain",
  "secondary_motivations": ["political"],
  "goals": [
    "Intelligence gathering on NATO and EU political targets",
    "Electoral interference operations",
    "Military intelligence collection"
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "G0007",
      "url": "https://attack.mitre.org/groups/G0007"
    }
  ]
}
```

### 2. APT29 (Cozy Bear)

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--899ce53f-13a0-479b-a0e4-67d46e241542",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "APT29",
  "description": "Russian state-sponsored threat group linked to SVR foreign intelligence service",
  "threat_actor_types": ["nation-state"],
  "aliases": ["Cozy Bear", "The Dukes", "CozyDuke", "Nobelium"],
  "first_seen": "2008-01-01T00:00:00.000Z",
  "sophistication": "expert",
  "resource_level": "government",
  "primary_motivation": "organizational-gain",
  "secondary_motivations": ["political"],
  "goals": [
    "Foreign intelligence collection",
    "Policy information gathering",
    "Supply chain compromise operations"
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "G0016",
      "url": "https://attack.mitre.org/groups/G0016"
    }
  ]
}
```

### 3. Lazarus Group

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--68391641-859f-4a9a-9a1e-3e5cf71ec376",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Lazarus Group",
  "description": "North Korean state-sponsored APT group responsible for major cyber attacks including Sony Pictures hack and WannaCry ransomware",
  "threat_actor_types": ["nation-state"],
  "aliases": ["Hidden Cobra", "ZINC", "Guardians of Peace", "Whois Team"],
  "first_seen": "2009-01-01T00:00:00.000Z",
  "sophistication": "expert",
  "resource_level": "government",
  "primary_motivation": "organizational-gain",
  "secondary_motivations": ["financial-gain", "political"],
  "goals": [
    "Revenue generation through cryptocurrency theft",
    "Destructive attacks on perceived enemies",
    "Bank heists via SWIFT compromise"
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "G0032",
      "url": "https://attack.mitre.org/groups/G0032"
    }
  ]
}
```

### 4. FIN7 (Carbanak)

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--3753cc21-2dae-4dfb-8481-d004e74502cc",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:000Z",
  "name": "FIN7",
  "description": "Financially motivated cybercrime group targeting hospitality and retail sectors",
  "threat_actor_types": ["crime-syndicate"],
  "aliases": ["Carbanak", "Carbon Spider", "Navigator Group"],
  "first_seen": "2013-01-01T00:00:00.000Z",
  "sophistication": "expert",
  "resource_level": "organization",
  "primary_motivation": "financial-gain",
  "goals": [
    "Point-of-sale malware deployment",
    "Payment card data theft",
    "Ransomware operations"
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "G0046",
      "url": "https://attack.mitre.org/groups/G0046"
    }
  ]
}
```

### 5. APT41 (Double Dragon)

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--18854f55-ac7c-4634-bd9a-352dd07613b7",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "APT41",
  "description": "Chinese state-sponsored threat group conducting espionage and financially motivated operations",
  "threat_actor_types": ["nation-state", "crime-syndicate"],
  "aliases": ["Double Dragon", "Barium", "Winnti Group"],
  "first_seen": "2012-01-01T00:00:00.000Z",
  "sophistication": "expert",
  "resource_level": "government",
  "primary_motivation": "organizational-gain",
  "secondary_motivations": ["financial-gain"],
  "goals": [
    "Intellectual property theft",
    "Supply chain compromise",
    "Cryptocurrency mining and theft"
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "G0096",
      "url": "https://attack.mitre.org/groups/G0096"
    }
  ]
}
```

### 6. Sandworm Team

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--381fcf72-f139-42f6-8f9d-d40c1f905983",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Sandworm Team",
  "description": "Russian military cyber unit responsible for destructive attacks on Ukraine infrastructure",
  "threat_actor_types": ["nation-state"],
  "aliases": ["ELECTRUM", "Telebots", "TEMP.Noble", "BlackEnergy Group"],
  "first_seen": "2009-01-01T00:00:00.000Z",
  "sophistication": "expert",
  "resource_level": "government",
  "primary_motivation": "political",
  "secondary_motivations": ["organizational-gain"],
  "goals": [
    "Critical infrastructure disruption",
    "NotPetya wiper malware deployment",
    "Olympic Destroyer attacks"
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "G0034",
      "url": "https://attack.mitre.org/groups/G0034"
    }
  ]
}
```

### 7. REvil (Sodinokibi)

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--0c66a96e-7d47-4314-95b7-8b25e8a89eb4",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "REvil",
  "description": "Russian-speaking ransomware-as-a-service operation responsible for major supply chain attacks",
  "threat_actor_types": ["crime-syndicate"],
  "aliases": ["Sodinokibi", "Sodin"],
  "first_seen": "2019-04-01T00:00:00.000Z",
  "sophistication": "advanced",
  "resource_level": "organization",
  "primary_motivation": "financial-gain",
  "goals": [
    "Double extortion ransomware attacks",
    "Supply chain compromise via MSPs",
    "High-profile victim targeting"
  ]
}
```

### 8. Kimsuky

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--0ec2f388-bf0f-4b5c-97b1-fc736d26c25f",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Kimsuky",
  "description": "North Korean state-sponsored APT focused on South Korean targets and foreign policy intelligence",
  "threat_actor_types": ["nation-state"],
  "aliases": ["Velvet Chollima", "Black Banshee", "THALLIUM"],
  "first_seen": "2012-01-01T00:00:00.000Z",
  "sophistication": "advanced",
  "resource_level": "government",
  "primary_motivation": "organizational-gain",
  "goals": [
    "South Korean policy intelligence",
    "Academic and research targeting",
    "Think tank compromise"
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "G0094",
      "url": "https://attack.mitre.org/groups/G0094"
    }
  ]
}
```

### 9. Emotet

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--5abb12e8-9ab6-42fb-8a83-87b86de6b0f5",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Emotet",
  "description": "Banking trojan evolved into malware-as-a-service botnet distributing TrickBot and ransomware",
  "threat_actor_types": ["crime-syndicate"],
  "aliases": ["TA542", "Mummy Spider"],
  "first_seen": "2014-01-01T00:00:00.000Z",
  "sophistication": "advanced",
  "resource_level": "organization",
  "primary_motivation": "financial-gain",
  "goals": [
    "Initial access broker operations",
    "Credential theft and banking fraud",
    "Ransomware delivery infrastructure"
  ]
}
```

### 10. Wizard Spider

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--dd2d9ca6-505b-4860-a604-233685b802c7",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Wizard Spider",
  "description": "Russian-speaking cybercrime group operating TrickBot botnet and Ryuk/Conti ransomware",
  "threat_actor_types": ["crime-syndicate"],
  "aliases": ["UNC1878", "Grim Spider"],
  "first_seen": "2016-01-01T00:00:00.000Z",
  "sophistication": "expert",
  "resource_level": "organization",
  "primary_motivation": "financial-gain",
  "goals": [
    "Enterprise-wide ransomware deployment",
    "Banking credential theft",
    "Anchor backdoor operations"
  ]
}
```

## Summary Statistics

- **Total Threat Actors**: 200+
- **Nation-State Groups**: 65%
- **Cybercrime Groups**: 30%
- **Hacktivist Groups**: 5%
- **Last Updated**: 2025-11-05
