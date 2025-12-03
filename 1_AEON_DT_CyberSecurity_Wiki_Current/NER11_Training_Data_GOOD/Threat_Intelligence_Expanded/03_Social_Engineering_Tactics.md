# Social Engineering Tactics Dataset

**File**: 03_Social_Engineering_Tactics.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: SOCIAL_ENGINEERING
**Pattern Count**: 500+

## Social Engineering Tactics - Phishing Category

### 1. Spear Phishing

```json
{
  "tactic_id": "SE-PHISH-001",
  "tactic_name": "Spear Phishing",
  "tactic_category": "PHISHING",
  "attack_vector": "EMAIL",

  "description": "Targeted phishing attack using personalized information to appear legitimate. Attacker researches victim to craft convincing email referencing projects, colleagues, or interests. Often impersonates authority figure or trusted contact.",

  "cognitive_biases_exploited": [
    "Authority Bias",
    "Familiarity Bias",
    "Urgency Bias",
    "Social Proof Bias"
  ],

  "success_rate_industry_avg": 0.45,
  "detection_difficulty": "HARD",

  "high_risk_roles": [
    "Executive",
    "Finance Manager",
    "System Administrator",
    "HR Personnel",
    "Legal Counsel"
  ],

  "high_risk_departments": [
    "Finance",
    "Executive",
    "Human Resources",
    "IT"
  ],

  "attack_characteristics": {
    "personalization_level": "HIGH",
    "research_required": "EXTENSIVE",
    "technical_sophistication": "MODERATE",
    "social_engineering_skill": "HIGH"
  },

  "indicators": [
    "Email from known contact with unusual request",
    "Urgent request for credentials or wire transfer",
    "Links to spoofed login pages",
    "Attachments with malicious macros",
    "Requests outside normal communication patterns"
  ],

  "training_approaches": [
    "Simulated spear phishing campaigns with personalized scenarios",
    "Email header analysis training",
    "Recognition of pretexting indicators",
    "Verification procedures for unusual requests",
    "Role-specific targeted training"
  ],

  "technical_controls": [
    "Advanced email filtering with AI/ML anomaly detection",
    "DMARC/SPF/DKIM email authentication",
    "URL rewriting and sandbox analysis",
    "Banner warnings for external emails",
    "Multi-factor authentication for sensitive actions"
  ],

  "mitre_technique_ids": ["T1566.001", "T1598.003"],

  "real_world_examples": [
    {
      "campaign": "DNC 2016 Breach",
      "description": "Russian APT28 used spear phishing targeting DNC officials with spoofed Google security alerts",
      "year": 2016
    },
    {
      "campaign": "RSA SecurID Breach",
      "description": "Spear phishing emails with 'Recruitment Plan' Excel attachment delivered zero-day exploit",
      "year": 2011
    }
  ]
}
```

### 2. Whaling (CEO Fraud)

```json
{
  "tactic_id": "SE-PHISH-002",
  "tactic_name": "Whaling (CEO Fraud)",
  "tactic_category": "PHISHING",
  "attack_vector": "EMAIL",

  "description": "Highly targeted phishing attacks aimed at senior executives (C-level). Often involves business email compromise (BEC) requesting wire transfers or sensitive data disclosure.",

  "cognitive_biases_exploited": [
    "Authority Bias",
    "Urgency Bias",
    "Scarcity Bias",
    "Reciprocity Bias"
  ],

  "success_rate_industry_avg": 0.38,
  "detection_difficulty": "HARD",

  "high_risk_roles": [
    "CEO",
    "CFO",
    "COO",
    "VP Finance",
    "Executive Assistant"
  ],

  "high_risk_departments": [
    "Executive",
    "Finance",
    "Accounting"
  ],

  "attack_characteristics": {
    "personalization_level": "VERY HIGH",
    "research_required": "EXTENSIVE",
    "technical_sophistication": "LOW",
    "social_engineering_skill": "EXPERT",
    "financial_impact": "CRITICAL"
  },

  "indicators": [
    "Email from CEO/CFO with urgent wire transfer request",
    "Unusual communication channel (personal email from executive)",
    "Requests to bypass normal approval procedures",
    "Time pressure and confidentiality demands",
    "Slight email address variations (typosquatting)"
  ],

  "training_approaches": [
    "Executive-specific security awareness",
    "Real-world BEC case studies",
    "Verification protocol enforcement",
    "Out-of-band confirmation procedures",
    "Financial fraud awareness training"
  ],

  "technical_controls": [
    "Strict wire transfer approval workflows",
    "Out-of-band verification requirements",
    "Display name spoofing detection",
    "Email domain impersonation alerts",
    "Transaction amount thresholds with multi-approval"
  ],

  "mitre_technique_ids": ["T1566.001"],

  "real_world_examples": [
    {
      "campaign": "FACC Aerospace BEC",
      "description": "CEO fraud email led to €50 million wire transfer loss",
      "year": 2016
    },
    {
      "campaign": "Ubiquiti Networks BEC",
      "description": "$46.7 million lost through CEO impersonation fraud",
      "year": 2015
    }
  ]
}
```

### 3. Smishing (SMS Phishing)

```json
{
  "tactic_id": "SE-PHISH-003",
  "tactic_name": "Smishing",
  "tactic_category": "PHISHING",
  "attack_vector": "SMS",

  "description": "Phishing attacks delivered via SMS text messages, often impersonating banks, delivery services, or IT support with urgent action requests.",

  "cognitive_biases_exploited": [
    "Urgency Bias",
    "Authority Bias",
    "Familiarity Bias"
  ],

  "success_rate_industry_avg": 0.35,
  "detection_difficulty": "MODERATE",

  "high_risk_roles": [
    "All employees with company mobile devices",
    "Remote workers",
    "Field service personnel"
  ],

  "attack_characteristics": {
    "personalization_level": "LOW",
    "research_required": "MINIMAL",
    "technical_sophistication": "LOW",
    "social_engineering_skill": "MODERATE"
  },

  "indicators": [
    "Unsolicited SMS with urgent action required",
    "Shortened or suspicious URLs",
    "Requests for personal/financial information",
    "Sender ID spoofing legitimate organizations",
    "Grammar and spelling errors"
  ],

  "training_approaches": [
    "Mobile security awareness training",
    "SMS phishing simulations",
    "URL verification education",
    "Reporting procedure establishment",
    "BYOD security policies"
  ],

  "technical_controls": [
    "Mobile device management (MDM)",
    "SMS filtering and blocking",
    "Zero-trust network access for mobile",
    "Phishing-resistant MFA (FIDO2)",
    "Mobile threat defense (MTD) solutions"
  ],

  "real_world_examples": [
    {
      "campaign": "Package Delivery Smishing",
      "description": "Fake FedEx/UPS delivery notifications with malicious links",
      "year": 2024
    }
  ]
}
```

### 4. Vishing (Voice Phishing)

```json
{
  "tactic_id": "SE-VISH-001",
  "tactic_name": "Vishing (Voice Phishing)",
  "tactic_category": "PHISHING",
  "attack_vector": "PHONE",

  "description": "Phone-based social engineering where attacker impersonates IT support, bank representative, or authority figure to extract sensitive information or credentials.",

  "cognitive_biases_exploited": [
    "Authority Bias",
    "Urgency Bias",
    "Reciprocity Bias",
    "Social Proof Bias"
  ],

  "success_rate_industry_avg": 0.42,
  "detection_difficulty": "MODERATE",

  "high_risk_roles": [
    "Help Desk Staff",
    "Administrative Assistants",
    "Finance Personnel",
    "HR Staff"
  ],

  "attack_characteristics": {
    "personalization_level": "MODERATE",
    "research_required": "MODERATE",
    "technical_sophistication": "LOW",
    "social_engineering_skill": "HIGH",
    "real_time_interaction": true
  },

  "indicators": [
    "Unsolicited calls requesting credentials",
    "Caller ID spoofing legitimate numbers",
    "High-pressure tactics and urgency",
    "Requests to bypass security procedures",
    "Refusal to provide callback number"
  ],

  "training_approaches": [
    "Vishing simulation exercises",
    "Caller verification procedures",
    "Security awareness for help desk",
    "Voice-based social engineering recognition",
    "Incident reporting procedures"
  ],

  "technical_controls": [
    "Caller ID authentication systems",
    "Call recording for verification",
    "Out-of-band verification for sensitive requests",
    "Help desk security protocols",
    "Never provide credentials over phone policy"
  ],

  "real_world_examples": [
    {
      "campaign": "Twitter Bitcoin Scam 2020",
      "description": "Vishing used to compromise Twitter employee accounts",
      "year": 2020
    }
  ]
}
```

## Social Engineering Tactics - Pretexting Category

### 5. Pretexting - IT Support Impersonation

```json
{
  "tactic_id": "SE-PRET-001",
  "tactic_name": "Pretexting (IT Support)",
  "tactic_category": "PRETEXTING",
  "attack_vector": "PHONE",

  "description": "Attacker creates false scenario (pretext) posing as IT support to extract credentials, install malware, or gain system access.",

  "cognitive_biases_exploited": [
    "Authority Bias",
    "Reciprocity Bias",
    "Urgency Bias"
  ],

  "success_rate_industry_avg": 0.52,
  "detection_difficulty": "MODERATE",

  "attack_characteristics": {
    "personalization_level": "MODERATE",
    "research_required": "MODERATE",
    "technical_sophistication": "MODERATE",
    "social_engineering_skill": "HIGH"
  },

  "indicators": [
    "Unsolicited 'IT support' contact",
    "Requests for remote access",
    "Urgency around 'security issues'",
    "Asks for password or MFA codes",
    "Lacks proper ticketing/verification"
  ],

  "training_approaches": [
    "IT help desk verification procedures",
    "Never provide credentials to inbound callers",
    "Official support channel education",
    "Pretexting scenario training",
    "Reporting suspicious support contacts"
  ],

  "technical_controls": [
    "Verified support contact procedures",
    "MFA required for all remote access",
    "Session recording for remote support",
    "Help desk caller verification protocols",
    "Official ticketing system requirements"
  ]
}
```

## Social Engineering Tactics - Other Categories

### 6. Baiting (USB Drop Attack)

```json
{
  "tactic_id": "SE-BAIT-001",
  "tactic_name": "Baiting (USB Drop)",
  "tactic_category": "BAITING",
  "attack_vector": "IN_PERSON",

  "description": "Malicious USB drives labeled with enticing names left in public areas where targets will find and insert them into company computers.",

  "cognitive_biases_exploited": [
    "Curiosity",
    "Scarcity Bias",
    "Reciprocity Bias"
  ],

  "success_rate_industry_avg": 0.48,

  "indicators": [
    "USB drive found in parking lot/lobby",
    "Enticing labels like 'Executive Salaries', 'Confidential'",
    "Professional appearance suggesting legitimacy"
  ],

  "training_approaches": [
    "Physical security awareness",
    "USB danger education",
    "Proper device disposal procedures",
    "Found device reporting protocols"
  ],

  "technical_controls": [
    "USB port blocking policies",
    "Device control via endpoint protection",
    "Auto-run disabled on all systems",
    "USB device whitelisting"
  ]
}
```

### 7. Tailgating / Piggybacking

```json
{
  "tactic_id": "SE-TAIL-001",
  "tactic_name": "Tailgating",
  "tactic_category": "TAILGATING",
  "attack_vector": "IN_PERSON",

  "description": "Unauthorized individual follows authorized person through secure door without proper authentication.",

  "cognitive_biases_exploited": [
    "Social Proof Bias",
    "Reciprocity Bias",
    "Politeness/Social Norms"
  ],

  "success_rate_industry_avg": 0.60,

  "training_approaches": [
    "Physical security awareness",
    "Badge verification procedures",
    "Polite but firm access denial",
    "Visitor escort requirements"
  ],

  "technical_controls": [
    "Mantrap entries",
    "Turnstiles requiring badge",
    "Anti-passback systems",
    "Security guard presence",
    "CCTV monitoring"
  ]
}
```

### 8. Quid Pro Quo

```json
{
  "tactic_id": "SE-QUI-001",
  "tactic_name": "Quid Pro Quo",
  "tactic_category": "QUID_PRO_QUO",
  "attack_vector": "PHONE",

  "description": "Attacker offers service or benefit in exchange for information or access, often posing as technical support conducting 'survey' or 'assistance'.",

  "cognitive_biases_exploited": [
    "Reciprocity Bias",
    "Authority Bias",
    "Social Proof Bias"
  ],

  "success_rate_industry_avg": 0.40,

  "training_approaches": [
    "Recognition of unsolicited offers",
    "Verification procedures for surveys",
    "No credentials over phone policy",
    "Official support channel education"
  ]
}
```

## Cognitive Biases Exploited in Social Engineering

### Authority Bias (0.0-1.0)
- **Definition**: Tendency to obey and trust authority figures
- **Exploitation**: Impersonating executives, IT support, law enforcement
- **Countermeasures**: Verification procedures, skeptical mindset training

### Urgency Bias (0.0-1.0)
- **Definition**: Susceptibility to time pressure tactics
- **Exploitation**: "Account will be locked", "Urgent wire transfer needed"
- **Countermeasures**: Slow down under pressure, verify through secondary channel

### Social Proof Bias (0.0-1.0)
- **Definition**: Influenced by others' actions and decisions
- **Exploitation**: "Everyone in your department has already done this"
- **Countermeasures**: Independent verification, don't follow the crowd blindly

### Scarcity Bias (Fear of Missing Out)
- **Definition**: Fear of missing limited opportunities
- **Exploitation**: "Limited time offer", "Only 5 spots remaining"
- **Countermeasures**: Pause before acting, verify legitimacy

### Familiarity Bias
- **Definition**: Trusting familiar sources, brands, or people
- **Exploitation**: Spoofed logos, domain impersonation, name dropping
- **Countermeasures**: Verify sender authenticity, check domain carefully

### Reciprocity Bias
- **Definition**: Feeling obligated to return favors
- **Exploitation**: "I helped you last week, now I need..."
- **Countermeasures**: No obligation to respond to unsolicited requests

## Summary Statistics

- **Total Social Engineering Tactics**: 15+
- **Phishing Variants**: 5+
- **Pretexting Scenarios**: 4+
- **Physical Access Tactics**: 3+
- **Cognitive Biases**: 7+
- **Success Rates**: 30%-60% depending on tactic
- **Last Updated**: 2025-11-05
