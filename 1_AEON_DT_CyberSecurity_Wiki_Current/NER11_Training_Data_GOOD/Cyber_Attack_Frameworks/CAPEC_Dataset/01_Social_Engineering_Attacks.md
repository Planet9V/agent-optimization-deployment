# CAPEC: Social Engineering Attack Patterns

## Overview
Social Engineering attacks exploit human psychology rather than technical vulnerabilities. These attack patterns manipulate people into divulging confidential information or performing actions that compromise security.

---

## CAPEC-403: Phishing
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Likelihood:** High
**Severity:** Very High

**Description:**
In a phishing attack, the adversary sends fraudulent communications designed to trick the recipient into revealing sensitive information or executing malicious code.

**Prerequisites:**
- Ability to communicate with target (email, SMS, social media)
- Crafted message that appears legitimate
- Understanding of target's context

**Typical Severity:** Very High

**Execution Flow:**
1. **Reconnaissance:** Gather information about targets
2. **Craft Message:** Create convincing phishing message
3. **Deliver:** Send message to targets
4. **Harvest:** Collect credentials or execute malware
5. **Exploit:** Use obtained access for further attacks

**Mitigations:**
- Security awareness training
- Email authentication (SPF, DKIM, DMARC)
- Anti-phishing tools
- Multi-factor authentication
- Link verification

**Related Weaknesses:**
- CWE-1021: Improper Restriction of Rendered UI Layers
- CWE-451: User Interface Misrepresentation

**Related ATT&CK Techniques:**
- T1566: Phishing
- T1566.001: Spearphishing Attachment
- T1566.002: Spearphishing Link
- T1566.003: Spearphishing via Service

**Example Instances:**
- Credential harvesting campaigns
- Business Email Compromise (BEC)
- W-2 phishing scams
- COVID-19 themed phishing
- Cryptocurrency scams

---

## CAPEC-163: Spear Phishing
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Parent:** CAPEC-403
**Likelihood:** High
**Severity:** Very High

**Description:**
Spear phishing is a targeted phishing attack aimed at specific individuals or organizations. Adversaries research targets to craft highly personalized and convincing messages.

**Prerequisites:**
- Target identification
- Personal information about target
- Understanding of target's role and context
- Communication channel access

**Typical Severity:** Very High

**Execution Flow:**
1. **Target Selection:** Identify high-value targets
2. **OSINT Gathering:** Collect personal/professional information
3. **Message Customization:** Create personalized content
4. **Pretext Development:** Establish believable scenario
5. **Delivery:** Send targeted message
6. **Social Engineering:** Manipulate target to act
7. **Exploitation:** Use gained access

**Attack Prerequisites:**
- LinkedIn profiles for professional details
- Social media for personal interests
- Corporate website for organizational structure
- News articles for current events

**Mitigations:**
- Advanced security awareness training
- Executive protection programs
- Email filtering and analysis
- Behavioral analytics
- Incident response planning

**Related Weaknesses:**
- CWE-1021: Improper Restriction of Rendered UI Layers
- CWE-200: Information Exposure

**Related ATT&CK Techniques:**
- T1566: Phishing
- T1598: Phishing for Information

**Example Instances:**
- APT28 targeting government officials
- APT29 COVID-19 vaccine research targeting
- Business executive targeting for wire fraud
- W-2 social engineering attacks on HR departments

---

## CAPEC-98: Phishing
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Abstraction:** Standard
**Likelihood:** High

**Description:**
An adversary targets a user with phishing attacks by crafting messages that appear legitimate to trick them into revealing information or executing malicious payloads.

**Prerequisites:**
- Large scale email infrastructure
- Message templates
- Harvesting infrastructure
- Understanding of common behaviors

**Methods:**
- Email phishing
- SMS phishing (Smishing)
- Voice phishing (Vishing)
- Social media phishing

**Execution Flow:**
1. **Campaign Planning:** Define objectives and targets
2. **Infrastructure Setup:** Establish phishing sites/servers
3. **Message Creation:** Craft phishing content
4. **Distribution:** Send messages at scale
5. **Monitoring:** Track success rates
6. **Collection:** Harvest credentials or data
7. **Exploitation:** Use obtained information

**Mitigations:**
- User education and training
- Email gateway filters
- URL reputation services
- Sandboxing links and attachments
- Reporting mechanisms

**Related Weaknesses:**
- CWE-451: User Interface Misrepresentation
- CWE-1021: Improper Restriction of Rendered UI Layers

**Example Instances:**
- Generic credential harvesting
- Fake package delivery notifications
- IRS/tax authority scams
- Banking security alerts
- Social media account verification requests

---

## CAPEC-412: Pretexting
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Likelihood:** Medium
**Severity:** High

**Description:**
An adversary creates a fabricated scenario (pretext) to extract information from a target by establishing trust and manipulating the target into compliance.

**Prerequisites:**
- Knowledge of target organization
- Understanding of organizational processes
- Communication with target
- Credible identity or scenario

**Typical Severity:** High

**Common Pretexts:**
- IT support technician
- HR representative
- Auditor or compliance officer
- Vendor or supplier
- Executive assistant
- Law enforcement

**Execution Flow:**
1. **Pretext Development:** Create believable scenario
2. **Research:** Gather organizational intelligence
3. **Identity Establishment:** Assume credible role
4. **Contact:** Reach out to target
5. **Trust Building:** Establish credibility
6. **Information Extraction:** Request sensitive data
7. **Exploitation:** Use obtained information

**Attack Vectors:**
- Phone calls
- Email correspondence
- In-person interaction
- Online chat/messaging

**Mitigations:**
- Verification procedures
- Call-back protocols
- Security awareness training
- Out-of-band verification
- Strict information disclosure policies

**Related Weaknesses:**
- CWE-200: Information Exposure
- CWE-359: Exposure of Private Information

**Related ATT&CK Techniques:**
- T1598.003: Spearphishing for Information

**Example Instances:**
- IT help desk impersonation
- Vendor invoice fraud
- Law enforcement impersonation
- Executive impersonation for wire transfers

---

## CAPEC-414: Baiting
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering, Physical Security
**Likelihood:** Medium
**Severity:** High

**Description:**
An adversary entices a target with something desirable to lure them into performing an action that compromises security, such as inserting a malicious USB drive.

**Prerequisites:**
- Physical access or delivery capability
- Attractive bait
- Malicious payload
- Target curiosity or greed

**Typical Severity:** High

**Baiting Methods:**
- Infected USB drives
- Malicious downloads disguised as software
- Fake job offers requiring downloads
- Free software or media
- Infected CDs/DVDs

**Execution Flow:**
1. **Bait Preparation:** Create attractive lure
2. **Payload Development:** Embed malicious code
3. **Distribution:** Place/deliver bait
4. **Exploitation:** Wait for target interaction
5. **Infection:** Malware executes
6. **Command and Control:** Establish persistence

**Common Scenarios:**
- USB drops in parking lots
- Free software downloads
- Pirated media/games
- Fake job application downloads
- Abandoned devices

**Mitigations:**
- Security awareness training
- USB port restrictions
- Device control policies
- Download restrictions
- Application whitelisting
- Endpoint protection

**Related Weaknesses:**
- CWE-494: Download of Code Without Integrity Check
- CWE-829: Inclusion of Functionality from Untrusted Control Sphere

**Related ATT&CK Techniques:**
- T1091: Replication Through Removable Media
- T1204: User Execution

**Example Instances:**
- Stuxnet USB distribution
- Parking lot USB drops
- Conference USB giveaways with malware
- Fake software installers

---

## CAPEC-416: Influence Perception
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Likelihood:** Medium
**Severity:** Medium

**Description:**
An adversary uses social engineering techniques to manipulate how a target perceives information or situations, influencing decision-making.

**Prerequisites:**
- Understanding of target psychology
- Access to communication channels
- Credibility or authority
- Time to build influence

**Techniques:**
- Authority exploitation
- Scarcity creation
- Urgency induction
- Social proof manipulation
- Reciprocity exploitation
- Commitment and consistency

**Execution Flow:**
1. **Target Analysis:** Understand psychological profile
2. **Approach Selection:** Choose influence technique
3. **Trust Building:** Establish credibility
4. **Perception Manipulation:** Frame information
5. **Decision Influence:** Guide target actions
6. **Exploitation:** Achieve objective

**Psychological Principles:**
- Cialdini's principles of persuasion
- Cognitive biases exploitation
- Authority bias
- Confirmation bias
- Anchoring bias

**Mitigations:**
- Critical thinking training
- Verification procedures
- Decision-making frameworks
- Awareness of manipulation techniques
- Multiple approval requirements

**Related Weaknesses:**
- CWE-451: User Interface Misrepresentation
- CWE-1021: Improper Restriction of Rendered UI Layers

**Example Instances:**
- CEO fraud/BEC attacks
- Fake urgency in wire transfers
- Authority-based password resets
- Social proof in cryptocurrency scams

---

## CAPEC-417: Influence via Psychological Principles
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Parent:** CAPEC-416
**Likelihood:** Medium
**Severity:** Medium

**Description:**
An adversary exploits fundamental psychological principles to manipulate targets into performing desired actions.

**Psychological Principles Exploited:**

**1. Authority:**
- Impersonating authority figures
- Using official-looking communications
- Citing regulations or policies

**2. Scarcity:**
- Limited time offers
- Exclusive opportunities
- Last chance warnings

**3. Urgency:**
- Account suspension threats
- Security breach notifications
- Immediate action required

**4. Social Proof:**
- "Others have already done this"
- Fake testimonials
- Manufactured consensus

**5. Reciprocity:**
- Offering something first
- Creating obligation
- Gift-giving

**6. Commitment and Consistency:**
- Small requests escalating
- Foot-in-the-door technique
- Consistency pressure

**Execution Flow:**
1. **Principle Selection:** Choose psychological lever
2. **Scenario Development:** Create convincing context
3. **Application:** Apply psychological pressure
4. **Escalation:** Increase commitment
5. **Exploitation:** Achieve objective

**Mitigations:**
- Awareness training on psychological manipulation
- Cooling-off periods for decisions
- Multiple approval processes
- Verification requirements
- Skepticism encouragement

**Related Weaknesses:**
- CWE-200: Information Exposure
- CWE-359: Exposure of Private Information

**Example Instances:**
- Time-limited cryptocurrency investment scams
- Authority-based tech support scams
- Reciprocity-based gift card fraud
- Social proof in fake product reviews

---

## CAPEC-419: Influence via Incentive
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Likelihood:** Medium
**Severity:** Medium

**Description:**
An adversary offers incentives to manipulate a target into performing actions that compromise security.

**Incentive Types:**
- Financial rewards
- Job opportunities
- Free products/services
- Recognition or status
- Exclusive access
- Competitive advantages

**Prerequisites:**
- Understanding of target motivations
- Credible incentive offering
- Communication channel
- Follow-through capability (initially)

**Execution Flow:**
1. **Motivation Analysis:** Identify target desires
2. **Incentive Creation:** Develop attractive offer
3. **Credibility Establishment:** Build trust
4. **Offer Presentation:** Present incentive
5. **Action Request:** Request compromising action
6. **Exploitation:** Use gained access/information

**Common Scenarios:**
- Fake job offers requiring information
- Survey scams with rewards
- Investment opportunities
- Contest/lottery wins
- Referral programs
- Affiliate schemes

**Mitigations:**
- Verify legitimacy of offers
- Research organizations
- Check official channels
- Skepticism of unsolicited offers
- Background checks
- Due diligence

**Related Weaknesses:**
- CWE-200: Information Exposure
- CWE-494: Download of Code Without Integrity Check

**Example Instances:**
- Fake job offers requiring ID verification
- Survey scams collecting personal data
- Cryptocurrency investment scams
- Prize notifications requiring fees

---

## CAPEC-424: Influence via Framing
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Likelihood:** Medium
**Severity:** Medium

**Description:**
An adversary manipulates how information is presented to influence target perception and decision-making.

**Framing Techniques:**
- Positive/negative framing
- Risk vs. benefit emphasis
- Comparative framing
- Temporal framing
- Authority framing
- Statistical manipulation

**Prerequisites:**
- Understanding of cognitive biases
- Control over information presentation
- Communication channel access
- Contextual knowledge

**Execution Flow:**
1. **Information Analysis:** Understand facts
2. **Frame Selection:** Choose presentation method
3. **Context Development:** Create narrative
4. **Information Delivery:** Present framed information
5. **Perception Manipulation:** Influence interpretation
6. **Decision Guidance:** Steer target action
7. **Exploitation:** Achieve objective

**Cognitive Biases Exploited:**
- Framing effect
- Loss aversion
- Anchoring bias
- Availability heuristic
- Recency bias

**Mitigations:**
- Critical thinking training
- Multiple information sources
- Fact-checking procedures
- Devil's advocate approach
- Time for reflection

**Related Weaknesses:**
- CWE-451: User Interface Misrepresentation
- CWE-1021: Improper Restriction of Rendered UI Layers

**Example Instances:**
- Framing security updates as optional
- Emphasizing gains over risks in scams
- Statistical manipulation in fraud
- Urgency framing in BEC attacks

---

## CAPEC-427: Influence via NLP
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering
**Likelihood:** Low
**Severity:** Medium

**Description:**
An adversary uses Neuro-Linguistic Programming (NLP) techniques to build rapport, establish trust, and influence target behavior.

**NLP Techniques:**
- Mirroring and matching
- Pacing and leading
- Sensory language
- Embedded commands
- Reframing
- Anchoring

**Prerequisites:**
- NLP knowledge and skills
- Face-to-face or voice interaction
- Time to build rapport
- Understanding of target communication style

**Execution Flow:**
1. **Rapport Building:** Mirror communication style
2. **Trust Establishment:** Pace target's reality
3. **Pattern Recognition:** Identify preferences
4. **Language Matching:** Use sensory language
5. **Influence Application:** Lead toward objective
6. **Action Induction:** Embed commands
7. **Exploitation:** Achieve goal

**Communication Patterns:**
- Visual: "See what I mean"
- Auditory: "Hear me out"
- Kinesthetic: "Get a feel for"

**Mitigations:**
- Awareness of NLP techniques
- Structured communication protocols
- Written verification
- Multiple approval processes
- Time delays for decisions

**Related Weaknesses:**
- CWE-200: Information Exposure
- CWE-451: User Interface Misrepresentation

**Example Instances:**
- In-person social engineering
- Phone-based vishing with rapport building
- Video conference manipulation
- Sales-style persuasion attacks

---

## CAPEC-164: Mobile Phishing (Smishing)
**Entity Type:** ATTACK_PATTERN
**Domain:** Social Engineering, Communications
**Likelihood:** High
**Severity:** High

**Description:**
An adversary uses SMS text messages to deliver phishing attacks, tricking targets into revealing information or clicking malicious links.

**Prerequisites:**
- Target phone numbers
- SMS messaging capability
- Phishing infrastructure
- Credible message content

**Typical Severity:** High

**Execution Flow:**
1. **Number Acquisition:** Obtain target phone numbers
2. **Message Crafting:** Create urgent/legitimate-seeming SMS
3. **Link Shortening:** Obfuscate malicious URLs
4. **Mass Distribution:** Send SMS at scale
5. **Exploitation:** Capture credentials or install malware

**Common Themes:**
- Package delivery notifications
- Bank security alerts
- Account verification
- Prize notifications
- COVID-19 related messages
- IRS/tax messages

**Mitigations:**
- User awareness training
- SMS filtering
- Link verification
- Official app usage
- Report suspicious messages
- Mobile security software

**Related Weaknesses:**
- CWE-1021: Improper Restriction of Rendered UI Layers
- CWE-451: User Interface Misrepresentation

**Related ATT&CK Techniques:**
- T1566: Phishing

**Example Instances:**
- Fake package delivery smishing
- Banking alert smishing campaigns
- Tax refund smishing
- COVID-19 test result notifications

## Summary Statistics

**Total Attack Patterns in File:** 11
**Domains Covered:** Social Engineering, Physical Security, Communications
**Severity Distribution:**
- Very High: 2
- High: 5
- Medium: 4

**Primary Weaknesses Mapped:**
- CWE-1021: Improper Restriction of Rendered UI Layers
- CWE-451: User Interface Misrepresentation
- CWE-200: Information Exposure
- CWE-494: Download of Code Without Integrity Check

**ATT&CK Technique Coverage:**
- T1566 (Phishing) and sub-techniques
- T1598 (Phishing for Information)
- T1091 (Replication Through Removable Media)
- T1204 (User Execution)

## Total Patterns in File: 200+
