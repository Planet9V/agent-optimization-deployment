# NCC-OTCE-EAB-025: Kimsuky DMARC Exploitation Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-025
**Date:** 2024-11-28
**Version:** 1.0
**Campaign Period:** May 2024 - November 2024

---

## EXECUTIVE SUMMARY

Kimsuky, a North Korean state-sponsored APT group, has exploited weak DMARC email security policies to impersonate trusted entities and conduct sophisticated phishing campaigns targeting government agencies, think tanks, and high-profile organizations with interests in North Korean affairs.

**Threat Level:** HIGH
**Primary Motivation:** Intelligence Collection / Cyber Espionage
**Attribution:** North Korea - Reconnaissance General Bureau (RGB)
**Also Known As:** Thallium, Black Banshee, Velvet Chollima

---

## THREAT ACTOR PROFILE

### Attribution
- **Nation-State:** Democratic People's Republic of Korea
- **Military Unit:** Reconnaissance General Bureau (RGB)
- **Primary Mission:** Geopolitical intelligence collection
- **Focus Areas:** North Korean policy, East Asian affairs

### Target Profile
- Government agencies
- Think tanks
- Academic institutions
- Media organizations
- Non-governmental organizations (NGOs)
- High-profile individuals in East Asian policy

---

## CAMPAIGN ANALYSIS (May-Nov 2024)

### Exploitation of DMARC Weaknesses
**Vulnerability:** Improperly configured DNS DMARC record policies
**Impact:** Ability to send spoofed emails appearing from legitimate domains
**Advisory Date:** May 2, 2024 (FBI, NSA, US State Department)

### Target Selection
- Experts in East Asian affairs
- North Korean policy analysts
- Academic researchers
- Journalists covering DPRK
- Government officials

---

## TACTICS, TECHNIQUES, AND PROCEDURES (TTPs)

### Reconnaissance (T1589)
- Extensive open-source intelligence (OSINT) gathering
- Target identification and profiling
- Research on North Korean policy circles
- Identification of trusted professional relationships

### Initial Access (T1566.001)
**Spearphishing with Spoofed Emails:**
- Impersonation of legitimate journalists
- Posing as academics or policy experts
- Creating credible online personas
- Leveraging DMARC misconfigurations

### Credential Access (T1056)
- Keylogging malware deployment
- Credential harvesting
- Session token theft

### Collection (T1114)
- Email collection
- Private document theft
- Research material exfiltration
- Communications monitoring

---

## MITRE ATT&CK MAPPING

| Tactic | Technique | Description |
|--------|-----------|-------------|
| Reconnaissance | T1589 | Gather Victim Identity Information |
| Initial Access | T1566.001 | Phishing: Spearphishing Attachment |
| Execution | T1204.002 | User Execution: Malicious File |
| Persistence | T1547.001 | Boot or Logon Autostart Execution |
| Credential Access | T1056.001 | Input Capture: Keylogging |
| Collection | T1114 | Email Collection |
| Exfiltration | T1041 | Exfiltration Over C2 Channel |

---

## TECHNICAL DETAILS

### DMARC Exploitation
**Vulnerability:**
- Organizations with DMARC policy set to "p=none"
- Lack of SPF/DKIM enforcement
- Absence of email authentication verification

**Attack Chain:**
1. Identify organizations with weak DMARC policies
2. Craft spoofed emails appearing from trusted domains
3. Impersonate trusted individuals
4. Deliver malicious content or harvest credentials

### Social Engineering Tactics
- Tailored content related to North Korean affairs
- Use of current events and policy discussions
- Building rapport through extended correspondence
- Leveraging professional networks and trust relationships

---

## INDICATORS OF COMPROMISE

### Email Indicators
- Emails from trusted domains with unexpected content
- Requests for sensitive information
- Unusual attachment types
- Links to credential harvesting pages
- Urgency or unusual meeting requests

### Technical Indicators
- DMARC policy showing "p=none"
- Missing SPF records
- Lack of DKIM signatures
- Email headers showing unusual routing

---

## DETECTION STRATEGIES

### Email Security
1. **DMARC Monitoring**
   - Implement DMARC with "quarantine" or "reject" policy
   - Monitor DMARC reports
   - Enforce SPF and DKIM

2. **Behavioral Analysis**
   - Baseline normal email patterns
   - Detect unusual sender behavior
   - Flag spoofing attempts

3. **User Training**
   - Recognize social engineering
   - Verify sender identity through alternate channels
   - Report suspicious communications

---

## MITIGATION RECOMMENDATIONS

### Immediate Actions
1. **DMARC Configuration**
   - Set DMARC policy to "quarantine" or "reject"
   - Implement SPF records
   - Enable DKIM signing
   - Monitor DMARC reports

2. **Email Security Controls**
   - Deploy advanced email filtering
   - Implement sandboxing for attachments
   - Enable link protection
   - Block executable attachments from external sources

3. **User Awareness**
   - Train on Kimsuky tactics
   - Verify identity before sharing information
   - Report suspicious emails
   - Use out-of-band verification

### Strategic Mitigations
1. **Email Authentication**
   - Full DMARC/SPF/DKIM implementation
   - Regular policy audits
   - Third-party sending validation

2. **Security Culture**
   - Ongoing security awareness training
   - Simulated phishing exercises
   - Incident reporting procedures

3. **Technical Controls**
   - Multi-factor authentication (MFA)
   - Privileged access management
   - Data loss prevention (DLP)
   - Email encryption

---

## INTELLIGENCE COLLECTION OBJECTIVES

Kimsuky seeks to collect intelligence on:
- Geopolitical events affecting North Korea
- Adversary foreign policy strategies
- Information affecting North Korean interests
- Private documents and research on DPRK
- Communications between policy experts

---

## REFERENCES

1. [FBI/NSA/State Department Advisory - May 2, 2024](https://www.ic3.gov/Media/News/2024/240502.pdf)
2. [Dark Reading - DPRK's Kimsuky APT Abuses Weak DMARC Policies](https://www.darkreading.com/cloud-security/dprks-kimsuky-apt-abuses-weak-dmarc-policies-feds-warn)
3. [The Record - Email Security Loopholes for North Korean Social Engineering](https://therecord.media/north-korea-kimsuky-hackers-dmarc-emails)
4. [Barracuda - How North Korean APT Groups Exploit DMARC Misconfigurations](https://blog.barracuda.com/2024/10/02/north-korean-apt-groups-dmarc-misconfigurations)

---

**Distribution:** TLP:CLEAR
**Contact:** otce-research@ncc.example.com

---
*End of Report*
