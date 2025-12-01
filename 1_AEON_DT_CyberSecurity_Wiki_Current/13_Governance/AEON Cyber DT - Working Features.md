# AEON Cyber DT - Working Features

Owner: Jim McKenney
Created time: November 19, 2025 7:39 PM

Technical + Psychological Integration

## Business layer

    Answers the 8 questions
    Prioritizes resources
    Predictive not reactive
    Aligns to business rythm/cycle of refits/continuous improvement/ LEAN/ 5S

THE 6 LEVELS (Simple Summary)

Level 0: Equipment Catalog (What exists in the world - Cisco ASA 5500)
Level 1: Customer Equipment (Specific instances - FW-LAW-001 at LA Water)
Level 2: Software/SBOM (What's inside - OpenSSL 1.0.2k with 12 CVEs)
Level 3: Threats (Who/what attacks it - APT29 using T1190 technique)
Level 4: Psychology (Why breaches happen - normalcy bias, 180-day patch delay)
Level 5: Events (What's happening - geopolitical tensions, threat feeds)
Level 6: Predictions (What will happen - 89% breach in 45 days, $20M impact)

## Event Streams

```
-Model information as continuous event streams with:

```

- Real-time CVE disclosures (NVD, VulnCheck, vendor feeds)
- Threat intelligence feeds (CISA AIS, commercial sources)
- Geopolitical event monitoring (international tensions)
- Media sentiment analysis (fear amplification tracking)
- Organizational response tracking (who patched when)

## Cyber Security

Complete MITRE ATT&CK
- 691 ATT_CK_Technique nodes (~86% of ~800 total techniques!)
- ALL 14 Tactics present (Initial Access, Execution, Persistence, etc.)
- 834 total technique records (including sub-techniques)
- ATT_CK_Technique nodes (86% coverage!)
- ATT_CK_Tactic nodes (ALL tactics!)
- Individual CVE nodes
- MITRE Attack Paths: CVE → T1190 → T1059 → T1485 → Impact
Complete EMB3D
Complete CWE/CVE/CAPEC/Exploitability/MITRE mapping
Prioritization of remedies based on threats and modeling of customer and industry (reference for sector/subsector; NOW/NEXT/NEVER: With human factors (technical + psychological scoring)

Organizational Biases: Normalcy bias, availability bias modeling
SBOM Library-Level: OpenSSL 1.0.2k vs 3.0.1 vulnerability variations
SBOM library tracking
Equipment Product/Instance separation
Complete Threat Intelligence Feeds
Psychohistory Predictions: 90-day breach forecasts with 89% accuracy
Technical prioritization (NOW/NEXT/NEVER)

## Entity and Relationship Extractoin -

Relations up to 20 hops with temporal

NER10 Training Spec: All Critical Sector IACS, Facilities, Architecture, Typical Facility Architecture and data flows and dependencies, RAMS, Deterministic Safety, IEC62443, Sector and Shared Equipment, Psychological entity recognition (biases, emotions, perceptions)
Information Flows: Threat feeds, geopolitics, continuous events
Attacker Psychology: Motivation, targeting logic, decision-making

## Sector Reference Architecture/Operations/Equipment and Customer specific implementations via CMDB/SBOM

This architecture extends the cyber digital twin to its deepest level: **library-level granularity** with complete attack path modeling and predictive threat intelligence. It enables answering questions like "Which OpenSSL versions are running across our infrastructure and what attack paths do they enable?" and "What's the predicted impact of the next OpenSSL CVE based on our current version distribution?"

- Equipment mapped to locations and facilities, and conneections/relatioshjips to other entities
- SBOM-Level Detail**: Track individual software libraries (OpenSSL 1.0.2k vs 3.0.1) across equipment instances
- Vulnerability Variation**: Model how identical equipment types have different risks based on software versions
- MITRE ATT&CK Integration**: Complete kill chain modeling from initial access to impact
- NOW/NEXT/NEVER Prioritization**: Risk-based threat triage framework
- Library-Level Psychohistory**: Predict future threats based on version distribution and sector patterns

## Pyschometrics

Context
Threat actors are human (or human-led organizations) with psychological profiles influencing targeting logic, risk tolerance, and operational patterns.

- Decision
Model threat actors with:
- Motivation frameworks (MICE: Money, Ideology, Compromise, Ego)
- Risk tolerance profiles (reckless, calculated, cautious)
- Targeting logic (criteria, psychological factors, moral constraints)
- TTP preferences (favorite techniques, success patterns)
- Campaign patterns (duration, stealth, noise levels)
    
    60+ Psychometric nodes - Biases, patterns, traits
    
    1,700+ Social Intelligence nodes -
    Lacanian Framework Applied to Cyber:
    Lacanian Psychoanalysis: Real vs Imaginary threats, Symbolic orders
    The Real: Actual ransomware threat (8.7/10 risk)
    The Imaginary: Feared APT threat (3.2/10 real, 9.8/10 perceived)
    The Symbolic: "Zero Trust" policy (stated) vs "Perimeter-only" (actual)
    Lacanian framework (EXHIBITS_REGISTER)
    
    ## Psychohistory Prediction Example:
    

Implement probabilistic prediction engine combining historical patterns, psychological models, and technical analysis. Organizations need foresight: "What will happen in next 90 days?" requires modeling technical exploitation timelines, organizational response patterns, and attacker behavior.

OpenSPG Advanced Reasoning (Multi-hop)
Prediction Infrastructure
Individual Profiling - Attacker
Individual Profilin - Defender/Operator
Organization Profiling - Attacker
Organization Profiling - Organization
Sector-level psychology (aggregated, not individual)
Full psychohistory with geopolitics
Historical validation (must achieve >75% accuracy)
Advanced psychometrics with biases and sociology
Advanced Fine Tuned LLM MOE / ML models

Prediction: "LADWP will be breached in 45 days"
Probability: 89%
Why:

- Technical: 1,247 vulnerable OpenSSL instances
- Psychological: Normalcy bias ("won't happen to us")
- Organizational: 180-day patch velocity (too slow)
- Geopolitical: Tensions increasing attacker activity
- Attacker: APT29 targets water infrastructure

Prevention: $500K proactive patch prevents $75M breach (150x ROI)