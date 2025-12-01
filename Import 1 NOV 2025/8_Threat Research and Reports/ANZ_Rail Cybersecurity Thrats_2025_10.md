

# **Cyberthreat Landscape of the Australian and New Zealand Rail Sector: A Threat-Informed Analysis for IEC 62443-Based Risk Management**

## **Executive Summary**

The rail sectors in Australia and New Zealand are undergoing a profound digital transformation, creating unprecedented efficiencies while simultaneously exposing critical operational infrastructure to a sophisticated and escalating cyberthreat landscape. This report provides a comprehensive analysis of the cyber risks facing these rail networks, specifically designed to inform threat modeling and risk management activities aligned with the ISA/IEC 62443 series of standards for Industrial Automation and Control Systems (IACS). The findings are derived from an extensive review of over fifteen annual cybersecurity reports from 2021 to 2025, published by leading government bodies and private sector security vendors, including the European Union Agency for Cybersecurity (ENISA), the Australian Cyber Security Centre (ACSC), and New Zealand's National Cyber Security Centre (NCSC).

The analysis reveals that rail systems in the region are confronted by a multifaceted threat environment driven by the convergence of Information Technology (IT) and Operational Technology (OT) systems, persistent geopolitical tensions, and the increasing professionalization of cybercrime.1 Dominant threats include multi-extortion ransomware, disruptive attacks on signaling and control systems, and complex supply chain compromises. Globally, railway-associated cyberattacks have demonstrated a significant upward trend, with some reports indicating a 220% increase over the last five years, underscoring the urgency for a structured defensive posture.5 A central challenge identified is the vulnerability of both aging legacy infrastructure and newly deployed digital systems, creating a complex risk environment that requires a nuanced, hybrid security strategy.

To provide actionable intelligence, this report presents six detailed threat scenarios that serve as archetypes of the most pressing risks to the Australian and New Zealand rail sector. These scenarios—ranging from ransomware deployment via IT-to-OT crossover to state-sponsored disruption of signaling systems—are meticulously mapped against the MITRE ATT\&CK® for ICS framework to detail adversary tactics, techniques, and procedures (TTPs). Furthermore, each scenario is analyzed through the lens of the MITRE EMB3D™ model for embedded device threats and aligned with the foundational security requirements of the IEC 62443 standard.

The core recommendation of this report is that rail operators in Australia and New Zealand must transition from a reactive, compliance-focused security model to a proactive, threat-informed defense. This approach, grounded in the risk-based principles and architectural concepts of IEC 62443, is essential for building resilient systems capable of ensuring the safety, reliability, and availability of rail services against a dynamic and determined adversary landscape.

## **Table of Contents**

## **1.0 Introduction**

### **1.1 The Digital Transformation of Rail**

The global rail industry, including the networks across Australia and New Zealand, is in the midst of a fundamental technological evolution. Traditionally reliant on isolated, electromechanical, and human-driven processes, rail operations are increasingly dependent on interconnected, digital, cyber-physical systems.7 This digital transformation is driven by the pursuit of enhanced safety, operational efficiency, and improved passenger experiences. Key technologies being adopted include modern signaling systems like Communications-Based Train Control (CBTC) and the European Train Control System (ETCS), which enable higher train density and improved safety margins. Concurrently, the proliferation of Internet of Things (IoT) sensors facilitates predictive maintenance on rolling stock and trackside assets, while real-time passenger information systems (PIS) and smart ticketing applications offer greater convenience.9 While these innovations deliver significant benefits, they also fundamentally alter the risk profile of the rail sector by expanding the digital attack surface and creating new pathways for malicious actors to impact physical operations.

### **1.2 The IT/OT Convergence Challenge**

A defining characteristic of this new technological era in rail is the convergence of Information Technology (IT) and Operational Technology (OT). IT systems, which encompass corporate networks, email, and business applications, are becoming increasingly interconnected with OT systems—the IACS that directly monitor and control physical processes like signaling, train movement, and power distribution.3 This integration allows for data-driven decision-making and enterprise-wide visibility but simultaneously erodes the traditional "air gap" that once isolated critical control systems from external networks.

This convergence presents a unique and formidable security challenge. A compromise originating in the less-secure IT environment can now potentially pivot to the highly sensitive OT network, with direct consequences for operational safety and service availability. The Australian Cyber Security Centre (ACSC) has explicitly warned that this growing interconnectedness, which includes the supply chain, presents an ever-expanding attack surface for malicious actors to exploit.12 Managing the security of this converged environment requires a holistic approach that bridges the cultural and technical divides between IT and OT security teams.

### **1.3 The ANZ Context**

Rail networks in Australia and New Zealand represent critical national infrastructure, vital for economic prosperity, supply chain stability, and public mobility. Their geostrategic positions and high degree of digital adoption make them attractive targets for a spectrum of malicious actors, including state-sponsored groups, cybercriminals, and hacktivists.13 Australian authorities have recognized this escalating risk, with organizations like the Rail Industry Safety and Standards Board (RISSB) developing a dedicated Cyber Security Strategy to establish an industry-wide approach to managing the threat.15 This strategy acknowledges that threat intelligence confirms attacks are becoming more common and identifies a wide range of potential threat actors, from foreign intelligence services to insiders.15 Similarly, New Zealand's national security apparatus identifies the disruption of critical infrastructure as a primary cyber threat.14 This report, therefore, focuses specifically on the threats and vulnerabilities pertinent to the unique operational and regulatory environments of Australia and New Zealand.

### **1.4 Purpose and Structure of the Report**

The primary objective of this report is to provide a detailed, evidence-based, and actionable analysis of the cyberthreat landscape facing the Australian and New Zealand rail sectors. It is intended to serve as a foundational resource for rail asset owners, integrators, and operators in developing and refining their cybersecurity risk management programs in accordance with the IEC 62443 standard. By mapping observed adversary behaviors to established security frameworks, the report aims to move beyond generic security advice to provide a threat-informed basis for prioritizing security controls, conducting risk assessments, and building a resilient and defensible architecture.

The subsequent sections of this report are structured as follows: Section 2.0 provides a comprehensive overview of the global and regional threat landscape. Section 3.0 details the foundational security frameworks—IEC 62443, MITRE ATT\&CK® for ICS, and MITRE EMB3D™—that form the analytical basis of this study. Section 4.0 presents six detailed cyberthreat scenarios tailored to the ANZ rail context. Section 5.0 summarizes key mitigations and recommendations structured around the IEC 62443 framework. Finally, Section 6.0 offers concluding remarks on the strategic imperatives for securing the future of rail in the region.

## **2.0 The Global and Regional Threat Landscape for Rail**

A comprehensive understanding of the threats facing the Australian and New Zealand rail sectors requires an analysis that begins at the global level and progressively narrows to the regional and local context. The threats impacting rail are not unique but are a specialized subset of the broader trends affecting all industrial and critical infrastructure sectors worldwide.

### **2.1 Global Threat Trends Impacting Critical Infrastructure (2021-2025)**

An extensive review of cybersecurity threat reports from leading vendors and government agencies—including Dragos, Mandiant, SANS, IBM, Fortinet, and CISA—reveals several persistent and evolving trends that directly impact OT environments like rail.

#### **Dominance of Ransomware**

Ransomware remains one of the most significant and impactful threats to industrial organizations. Its tactics have evolved far beyond simple data encryption. Modern ransomware campaigns frequently employ multi-extortion techniques, where attackers not only encrypt systems but also steal sensitive data and threaten to leak it publicly if the ransom is not paid.16 In some cases, this is combined with Distributed Denial-of-Service (DDoS) attacks to further pressure the victim organization. Reports from ENISA indicate that ransomware constitutes 38% of all attacks against the transport sector.1 Dragos, an OT security firm, reported a nearly 50% increase in ransomware incidents impacting industrial organizations in a single year.17 Manufacturing, a sector with similar OT dependencies to rail, is consistently identified as the most-attacked industry by ransomware groups, who recognize that operational downtime translates directly into financial leverage.18

#### **Rise of Supply Chain Attacks**

Attackers are increasingly targeting the "soft underbelly" of organizations by compromising their supply chains. Instead of launching a direct assault on a well-defended primary target, threat actors infiltrate less secure third-party vendors, such as software suppliers, maintenance contractors, or technology integrators, and use that trusted access to pivot into the target's network. ENISA has identified supply chain attacks as a prime threat against the transport sector.1 This tactic is particularly potent in the OT world, where operators rely on a complex ecosystem of vendors for specialized hardware, software, and support. The ACSC has consequently highlighted the effective management of third-party risk as one of its four "big moves" for organizations to bolster their cyber defenses.20

#### **State-Sponsored and Geopolitically Motivated Actors**

Critical infrastructure, including rail, is a primary target for state-sponsored and state-aligned threat actors. Their motivations are distinct from those of cybercriminals and typically revolve around espionage, intellectual property theft, or pre-positioning for future disruptive or destructive actions during times of geopolitical conflict.13 ENISA's analysis of the transport sector identifies state-sponsored actors as having one of the biggest impacts, often conducting politically motivated attacks that lead to operational disruptions.1 The ACSC has issued similar warnings, noting that state-sponsored actors persistently target Australian critical infrastructure for state goals, which may include degrading or disrupting critical services at a time of strategic advantage.12 The documented activities of Russia-nexus and China-nexus intrusion sets against transport and infrastructure sectors in Europe provide a clear precedent for the types of threats facing the ANZ region.21

#### **Exploitation of Edge Devices and Remote Access**

The perimeter of organizational networks, particularly internet-facing devices such as Virtual Private Networks (VPNs), firewalls, and routers, has become a primary battleground. Threat actors relentlessly scan for and exploit vulnerabilities in these "edge" devices to gain initial access. Mandiant's M-Trends report highlighted that the most frequently exploited vulnerabilities in 2024 were all contained in such devices.22 This vector is especially critical for OT environments, as remote access for vendors and employees is often a necessary operational requirement, providing a direct, albeit intended to be secure, pathway from the internet to sensitive internal networks.

A crucial consideration emerging from these trends is the "legacy-modernization vulnerability paradox." Rail operators are caught between two challenging realities. On one hand, they operate a significant amount of legacy OT equipment with lifecycles that can exceed 30 years.9 These systems often lack modern security features, are difficult or impossible to patch, and may be considered "insecure by design".24 Australian authorities explicitly recommend replacing such legacy technology as a key defensive measure.13 On the other hand, the drive for modernization introduces new digital systems, IoT devices, and increased connectivity, which, while more functional, significantly expand the attack surface and introduce new, complex software vulnerabilities.25 Consequently, a viable cybersecurity strategy for rail cannot simply mandate a "rip and replace" approach. It must be a hybrid model that implements strong compensating controls, such as network segmentation, around legacy assets while enforcing rigorous "security-by-design" principles, as advocated by IEC 62443, for all new technology deployments.4 This dual focus is fundamental to managing risk across the entire asset lifecycle.

### **2.2 European Rail Threat Landscape (ENISA Insights)**

The ENISA Transport Threat Landscape report, which analyzed incidents from January 2021 to October 2022, offers specific insights highly relevant to the rail sector.1 A key finding is that the majority of attacks on the transport sector target IT systems. However, these IT-focused attacks can have significant cascading consequences for OT, leading to operational disruptions.1 This underscores the critical importance of robust segmentation between IT and OT networks.

The report identifies the primary threat actors impacting the transport sector as cybercriminals, who are responsible for the majority of attacks (54%) and target all subsectors, and state-sponsored actors and hacktivists, whose actions are often linked to geopolitical tensions.1 The prime threats identified were ransomware (38%), data-related threats (30%), malware (17%), and DDoS attacks (16%).1 These findings from a mature and complex transport ecosystem like Europe's serve as a valuable benchmark for anticipating the threats likely to mature in the ANZ region.

### **2.3 The Australian and New Zealand Threat Context**

The global and European trends are reflected and, in some cases, amplified within the specific context of Australia and New Zealand.

#### **Australia (ACSC & RISSB)**

The ACSC's Annual Cyber Threat Report for 2024–25 states unequivocally that Australian critical infrastructure is an attractive and persistent target.12 During the reporting period, the ACSC notified critical infrastructure entities of potential malicious activity over 190 times, an increase of 111% from the previous year, highlighting a significant escalation in targeting.12 The top three cybersecurity incident types reported for critical infrastructure were compromised assets, networks, or infrastructure (55%); DoS or DDoS attacks (23%); and compromised accounts or credentials (19%).12

This data aligns with the strategic framework provided by the RISSB's Cyber Security Strategy. The RISSB identifies a broad spectrum of potential threat sources and actors, including terrorists, criminals, foreign intelligence services, competitors, hackers, activists, malware developers, and insiders (both employees and contractors).15 The strategy emphasizes a holistic, collaborative, and risk-based approach to defending the Australian rail network, which is consistent with international best practices.

#### **New Zealand (NCSC & Incidents)**

New Zealand's critical infrastructure faces similar threats, as outlined in reports from the National Cyber Security Centre (NCSC).28 The potential for cyberattacks to disrupt services or damage critical systems is recognized as a significant national security risk.14

The most salient regional case study is the multi-stage cyberattack against Auckland Transport (AT) in September 2023\. The incident began as a ransomware attack attributed to the Medusa group, which targeted AT's HOP card ticketing and transaction systems, causing widespread disruption for commuters.31 While AT stated that it would not negotiate with the attackers, the incident escalated when the agency's website and mobile applications were subsequently targeted by a DDoS attack, causing further service degradation.33 This incident serves as a powerful, local example of how global threat trends—in this case, ransomware and hacktivist-style DDoS attacks—can manifest and cause significant operational impact within the ANZ transport sector.

## **3.0 Foundational Security Frameworks for Rail**

To effectively analyze the threat landscape and develop robust defenses, a structured approach grounded in internationally recognized frameworks is essential. This report leverages a synergistic combination of three key frameworks: IEC 62443 for establishing a secure operational state, MITRE ATT\&CK® for ICS for understanding adversary behavior, and MITRE EMB3D™ for analyzing threats to embedded components.

### **3.1 IEC 62443: The Standard for Industrial Cybersecurity**

The ISA/IEC 62443 series of standards is the global benchmark for securing Industrial Automation and Control Systems (IACS), which form the core of rail OT environments.27 It provides a comprehensive, risk-based methodology for asset owners, system integrators, and product suppliers to manage cybersecurity throughout the entire system lifecycle, from design and implementation to operation and maintenance.7

Key concepts of IEC 62443 include:

* **Defense-in-Depth:** This principle advocates for a multi-layered security architecture, combining technical, procedural, and physical controls so that the failure of a single control does not lead to a complete system compromise.27  
* **Security Levels (SLs):** The standard defines four Security Levels (SL 1-4) that specify the required security robustness of a system or component to protect against threats of increasing sophistication, from casual violation to intentional attacks by nation-states.27 This allows organizations to apply security measures commensurate with the identified risk.  
* **Zones and Conduits:** This is the foundational architectural concept within IEC 62443\. A "Zone" is a logical grouping of assets that share common security requirements. A "Conduit" is the communication channel that controls all data flow between zones. By segmenting the network into zones and enforcing strict policies on the conduits, operators can contain threats and prevent unauthorized lateral movement, such as an attacker pivoting from a less secure IT zone to a critical OT signaling zone.27

### **3.2 MITRE ATT\&CK® for ICS: Modeling Adversary Behavior**

The MITRE ATT\&CK® for ICS framework is a globally accessible knowledge base of adversary tactics and techniques based on real-world observations of cyberattacks against industrial environments.38 It provides a common lexicon for describing how attackers operate within OT networks.

The framework is structured as a matrix of twelve tactics, which represent the adversary's tactical goals. These include:

* **Initial Access:** How adversaries get into the ICS environment.  
* **Execution:** How adversaries run malicious code.  
* **Lateral Movement:** How adversaries move through the environment.  
* **Inhibit Response Function:** How adversaries prevent safety and protection systems from operating.  
* **Impair Process Control:** How adversaries manipulate physical control processes.  
* **Impact:** How adversaries manipulate, interrupt, or destroy systems and processes.40

Each tactic contains multiple specific techniques that describe the methods used to achieve the goal. By focusing on these behaviors (the "how") rather than just indicators of compromise (the "what"), ATT\&CK for ICS enables organizations to build a more resilient and proactive "threat-informed defense".38

### **3.3 MITRE EMB3D™: Securing Embedded Devices**

MITRE EMB3D™ is a specialized threat model focused on the unique security challenges of embedded devices, such as Programmable Logic Controllers (PLCs), sensors, actuators, and other intelligent electronic devices that are ubiquitous in modern rail systems.43 These devices often form the lowest levels of the control system hierarchy, directly interacting with the physical world.

The EMB3D framework consists of three core components:

* **Device Properties:** Descriptions of a device's hardware and software features (e.g., physical access interfaces, network protocols, firmware).  
* **Threats:** A catalog of known threat actions that can be performed against a device (e.g., firmware manipulation, unauthorized command injection).  
* **Mitigations:** A list of security mechanisms that can prevent or reduce the risk of a threat.43

EMB3D allows for a granular threat analysis by mapping a device's specific properties to the threats it is consequently exposed to, providing a structured way to assess vulnerabilities at the component level.44

### **3.4 Framework Synergy for Rail Security**

The power of this report's analytical approach lies in the integration of these three frameworks. They are not used in isolation but are combined to create a multi-layered model for understanding and mitigating risk. IEC 62443 defines the desired *target state* of security for a rail IACS—it describes "what a secure system looks like" through its comprehensive set of process and technical requirements. In contrast, the MITRE ATT\&CK for ICS framework defines the *threats* to that target state—it catalogs "how adversaries operate" to undermine security controls and achieve their objectives. Finally, MITRE EMB3D provides a micro-level view, detailing the specific threats to the embedded hardware and firmware components that constitute the systems IEC 62443 aims to protect.

By mapping the adversary TTPs from ATT\&CK for ICS to the specific IEC 62443 security requirements that would prevent, detect, or mitigate them, this analysis transforms abstract security principles into concrete, threat-informed controls. For example, a generic requirement from IEC 62443 for access control (FR1) becomes a specific, justifiable recommendation: "Implement robust, phishing-resistant multi-factor authentication for all remote access services to mitigate the ATT\&CK for ICS technique T0862 (External Remote Services), a method frequently used by state-sponsored actors to gain initial access." This synergy makes the threat modeling and risk assessment process tangible, evidence-based, and directly actionable for rail operators.

## **4.0 Detailed Cyberthreat Scenarios for ANZ Rail**

This section presents six detailed cyberthreat scenarios tailored to the operational realities and threat environment of the Australian and New Zealand rail sectors. Each scenario is designed to be used in workshops with rail customers to facilitate threat modeling, risk assessment, and security control prioritization. Each is presented first as a one-page summary table for quick reference, followed by a detailed narrative that elaborates on the attack chain and its implications.

### **4.1 Threat Scenario 1: Ransomware Attack on Rail Operations via IT-to-OT Crossover**

**Table 1: Threat Scenario Summary – Ransomware via IT-to-OT Crossover**

| Component | Description |
| :---- | :---- |
| **Threat Title** | Ransomware Attack on Rail Operations via IT-to-OT Crossover |
| **Threat Actor Profile** | **Type:** Financially Motivated Cybercrime (e.g., Akira, Qilin, LockBit).21 **Motivation:** Financial gain through extortion, leveraging operational disruption. **Skill Level:** High, often operating as a Ransomware-as-a-Service (RaaS) model. |
| **Target Systems & Technologies** | **Primary:** Engineering Workstations, Human-Machine Interfaces (HMIs), Data Historians, SCADA Servers. **Secondary:** Corporate IT systems (email servers, file shares). |
| **Likelihood & Statistics** | **High.** Ransomware is a prime threat, accounting for 38% of attacks in the transport sector.1 Manufacturing, a comparable industrial sector, is the most consistently targeted for ransomware.18 |
| **Attack Pattern (MITRE ATT\&CK for ICS)** | **Initial Access:** T0861: Spearphishing Attachment. **Execution:** T0845: User Execution. **Persistence:** T0809: Create Account. **Lateral Movement:** T0855: Remote Services (e.g., RDP from IT to OT). **Impair Process Control:** T0814: Denial of Service on operator workstations/HMIs. **Impact:** T0828: Loss of Control; T0830: Loss of View. |
| **Common Vulnerabilities Exploited** | Inadequate network segmentation between IT and OT; weak or shared credentials; lack of egress filtering; insufficient employee security awareness; unpatched vulnerabilities on IT systems. |
| **Example Access Points** | Phishing email with a malicious attachment sent to a corporate employee; compromised credentials for an IT system that has a trust relationship with the OT network. |
| **Potential Impacts** | **Safety:** Indirect risk if operators lose visibility and control, forcing a manual or emergency shutdown. **Operational:** Complete shutdown of train dispatch and monitoring capabilities, leading to network-wide service suspension for hours or days (ref. Danish State Railways incident).5 **Financial:** Significant revenue loss, high recovery and remediation costs, potential ransom payment, regulatory fines. **Reputational:** Severe erosion of public trust and confidence in the rail operator's ability to provide reliable service. |
| **Alignment with IEC 62443** | **Violates:** FR1 (Access Control), FR3 (System Integrity), FR5 (Restricted Data Flow), FR7 (Resource Availability). **Mitigated by:** SR 5.1 (Zone boundary protection), SR 5.2 (Inter-zone communication control), SR 1.1 (Human user identification and authentication), SR 7.8 (Malware protection). |
| **EMB3D Modeling Alignment** | **Targets:** Engineering Workstation (PID-10: Operating System, PID-12: Firmware). **Exploits:** Not directly applicable at the embedded level, as the primary impact is on supervisory systems. However, a compromised workstation could be used to push malicious logic to PLCs (TID-105: Firmware Manipulation). |

#### **Narrative**

The attack begins with a sophisticated spear-phishing campaign, a leading initial access vector, targeting employees in the rail operator's corporate finance department.47 An employee receives a convincing email masquerading as an invoice from a known supplier and opens the attached document, which executes malicious code. The malware establishes a foothold on the corporate IT network, remaining dormant while the attackers conduct reconnaissance.

Using stolen credentials harvested from the initial compromised machine, the attackers move laterally across the IT network. They discover a critical vulnerability: a poorly configured firewall and a lack of strict access controls between the IT and OT networks, a common issue in industrial environments.49 The attackers identify an engineering workstation used for remote maintenance that has credentials stored for both IT and OT systems. Using these credentials, they pivot from the corporate network directly into the rail operations control network.

Once inside the OT environment, the attackers deploy a potent ransomware strain, such as Akira or Qilin, which are known to target industrial sectors.21 The ransomware spreads rapidly, encrypting critical supervisory systems, including the SCADA servers responsible for train dispatch, the data historians logging operational information, and the HMIs used by train controllers. The controllers' screens go blank or display a ransom note, resulting in a complete loss of view and control over the train network.

The immediate impact is catastrophic. With no ability to safely monitor or direct train movements, the operator is forced to enact an emergency shutdown of all services across the network to prevent potential collisions. This scenario mirrors the real-world impact seen in the 2022 ransomware attack on Danish State Railways, where a compromise at a third-party supplier led to a nationwide halt in train operations.5 The attack on Auckland Transport's ticketing systems also demonstrates the disruptive capability of ransomware in a regional context.31 The operator now faces a crippling choice: attempt a lengthy and costly restoration from backups, which may also be compromised, or pay a multi-million dollar ransom with no guarantee of receiving a working decryption key.

### **4.2 Threat Scenario 2: State-Sponsored Disruption of Signaling Systems**

**Table 2: Threat Scenario Summary – State-Sponsored Signaling Disruption**

| Component | Description |
| :---- | :---- |
| **Threat Title** | State-Sponsored Disruption of Signaling Systems via Radio Frequency Spoofing |
| **Threat Actor Profile** | **Type:** State-Sponsored or State-Aligned Actor (e.g., Russia-nexus, China-nexus).12 **Motivation:** Geopolitical messaging, disruption of critical infrastructure, testing of capabilities for future conflict. **Skill Level:** Very High, with expertise in both cyber and electronic warfare. |
| **Target Systems & Technologies** | Legacy radio-based train control systems (e.g., 'radiostop' functions), GSM-R communications, trackside signaling equipment. |
| **Likelihood & Statistics** | **Medium to High.** State actors are actively targeting critical infrastructure for pre-positioning and disruption.12 The transport sector is a known target for China-nexus groups.21 The low cost of required equipment (\<$500) lowers the barrier to entry.23 |
| **Attack Pattern (MITRE ATT\&CK for ICS)** | **Initial Access:** T0874: Wireless Compromise. **Execution:** T0871: Execution through API (via radio commands). **Impair Process Control:** T0856: Spoof Reporting Message; T0857: Unauthorized Command Message. **Impact:** T0816: Denial of Control; T0822: Loss of Availability. |
| **Common Vulnerabilities Exploited** | Unauthenticated or weakly authenticated radio protocols; publicly available technical specifications for legacy systems; lack of cryptographic protection on control commands. |
| **Example Access Points** | Attacker with a software-defined radio (SDR) in physical proximity to the railway line; exploitation of vulnerabilities in GSM-R protocol. |
| **Potential Impacts** | **Safety:** High risk. Uncommanded emergency braking could lead to passenger injuries or, in a worst-case scenario, derailment depending on speed and location. **Operational:** Widespread, simultaneous stoppage of multiple trains, causing network paralysis and significant delays. **Financial:** Costs associated with service recovery, safety inspections, and potential infrastructure damage. **National Security:** Demonstration of capability to disrupt critical transport logistics, impacting military and economic mobilization. |
| **Alignment with IEC 62443** | **Violates:** FR1 (Access Control), FR3 (System Integrity). **Mitigated by:** SR 3.1 (Communication Integrity), SR 3.8 (Use of cryptography), SR 1.13 (Wireless access management). |
| **EMB3D Modeling Alignment** | **Targets:** Trackside Radio Unit / On-board Controller (PID-1: Network Interface \- Radio, PID-12: Firmware). **Exploits:** TID-101 (Unauthorized Command Message), TID-201 (Message/Protocol Manipulation), TID-202 (Replay Attack). |

#### **Narrative**

A state-aligned threat actor, seeking to send a political message or test its disruptive capabilities, targets the rail network of Australia or New Zealand. The attackers have studied the legacy radio communication systems still in use on parts of the network, whose technical specifications are publicly available for interoperability purposes.51

Using inexpensive and readily available software-defined radio (SDR) equipment, operatives position themselves near multiple strategic points along a busy rail corridor. They begin broadcasting spoofed radio commands that mimic the 'radiostop' signal, a legacy function designed to trigger an emergency brake application on locomotives.51 This attack directly mirrors the 2023 incident in Poland, where hackers used similar methods to bring approximately 20 trains to a standstill while broadcasting the Russian national anthem over the radio channel.47

Because the legacy protocol lacks strong authentication or encryption, the on-board train control systems accept the malicious commands as legitimate. Multiple trains across the corridor simultaneously engage their emergency brakes, coming to an abrupt halt. The attack causes immediate operational chaos, stranding passengers and blocking critical freight lines. The sudden braking poses a direct safety risk to passengers and crew.

The disruption is not limited to a single point but is coordinated across a wide geographic area, demonstrating a sophisticated command and control capability. The incident forces the rail operator to suspend all traffic in the affected region until each train can be manually inspected and the source of the interference identified. This scenario highlights the significant risk posed by insecure legacy OT protocols and demonstrates how low-cost electronic warfare techniques can have a high impact on physical infrastructure, with significant implications for both public safety and national security.

### **4.3 Threat Scenario 3: Supply Chain Compromise of a Rolling Stock Manufacturer**

**Table 3: Threat Scenario Summary – Supply Chain Compromise**

| Component | Description |
| :---- | :---- |
| **Threat Title** | Supply Chain Compromise of a Rolling Stock Manufacturer Leading to Fleet-Wide Backdoor |
| **Threat Actor Profile** | **Type:** Advanced Persistent Threat (APT) / State-Sponsored Espionage Group. **Motivation:** Long-term espionage, intellectual property theft, pre-positioning for future sabotage. **Skill Level:** Extremely High, capable of sophisticated software subversion. |
| **Target Systems & Technologies** | Train Control and Management System (TCMS), onboard PLCs for braking/propulsion/doors, vendor's software development and update infrastructure. |
| **Likelihood & Statistics** | **Medium.** Supply chain attacks are a prime threat to the transport sector.1 The ACSC identifies managing third-party risk as a critical defense.20 While complex, such attacks have occurred in other sectors (e.g., SolarWinds). |
| **Attack Pattern (MITRE ATT\&CK for ICS)** | **Initial Access:** T0866: Supply Chain Compromise. **Persistence:** T0865: Rootkit; T0821: Hooking. **Command and Control:** T0884: Connection Proxy. **Collection:** T0803: Automated Collection (of operational data). **Impact:** T0836: Modify Program (potential for future disruptive command). |
| **Common Vulnerabilities Exploited** | Insecure software development lifecycle at the vendor; lack of code signing and integrity verification; insufficient security vetting of third-party suppliers by the rail operator. |
| **Example Access Points** | Compromise of a developer's credentials at the train manufacturing company; injection of malicious code into the source code repository for the TCMS. |
| **Potential Impacts** | **Safety:** Latent high risk. A backdoor could be activated to issue unsafe commands to critical systems like brakes or doors across the entire fleet. **Operational:** Covert exfiltration of sensitive operational data (routes, schedules, loads). Potential for a future fleet-wide shutdown command. **Financial:** Cost of recalling and remediating an entire fleet of rolling stock; loss of intellectual property. **Reputational:** Complete collapse of trust in the operator and the manufacturer. |
| **Alignment with IEC 62443** | **Violates:** FR3 (System Integrity). **Mitigated by:** SR 3.1 (Communication Integrity), SR 3.3 (Portable and Mobile Device Security), SR 7.6 (Patch Management), and most critically, vendor adherence to **IEC 62443-4-1 (Secure Product Development Lifecycle Requirements)**. |
| **EMB3D Modeling Alignment** | **Targets:** Onboard PLC/Controller (PID-12: Firmware, PID-13: Software). **Exploits:** TID-105 (Firmware Manipulation), TID-106 (Software Manipulation), TID-103 (Implant Malicious Logic). |

#### **Narrative**

An APT group, with the objective of gaining long-term, persistent access to a nation's rail fleet, targets a major international rolling stock manufacturer that supplies trains to operators in Australia and New Zealand. The attackers compromise the manufacturer's internal software development network, gaining access to the source code for the Train Control and Management System (TCMS).

The attackers subtly modify the TCMS firmware, embedding a sophisticated backdoor that is designed to evade detection. This malicious code is then incorporated into an official software update. The manufacturer, unaware of the compromise, signs and distributes the update to its customers as part of a routine maintenance cycle. The rail operator, trusting the legitimacy of the update from its supplier, deploys the compromised firmware across its entire fleet of trains.

The backdoor activates and establishes a covert command and control (C2) channel, possibly using steganography or tunneling through legitimate network traffic to avoid detection. This allows the APT group to remotely and surreptitiously access the TCMS of any train in the fleet. Initially, the attackers use this access for espionage, collecting sensitive operational data such as train locations, speeds, and diagnostic information.

This scenario represents a high-impact, low-visibility threat. The vulnerability does not lie with the rail operator's security posture but with the integrity of its supply chain, a threat vector explicitly highlighted by ENISA.1 The immediate impact is espionage, but the latent risk is catastrophic. The backdoor provides the attacker with the capability to issue malicious commands at a time of their choosing, potentially disabling the brakes, manipulating door controls, or causing a fleet-wide shutdown. This threat underscores the critical importance of rail operators demanding and verifying that their suppliers adhere to rigorous secure development lifecycle standards, such as IEC 62443-4-1.

### **4.4 Threat Scenario 4: Insider Threat Exploiting Privileged Access**

**Table 4: Threat Scenario Summary – Insider Threat**

| Component | Description |
| :---- | :---- |
| **Threat Title** | Insider Threat Abuses Privileged Access to Manipulate Interlocking System |
| **Threat Actor Profile** | **Type:** Malicious Insider (disgruntled employee, contractor) or Coerced/Unwitting Insider. **Motivation:** Revenge, financial gain (if paid by an external party), ideology. **Skill Level:** Medium to High, possesses legitimate knowledge of and access to OT systems. |
| **Target Systems & Technologies** | Signaling Interlocking Systems, SCADA/DCS controlling track switches and signals, Engineering Workstations. |
| **Likelihood & Statistics** | **Medium.** RISSB explicitly identifies employees and contractors as a threat source.15 While less frequent than external attacks, insider incidents can be highly damaging due to the actor's inherent trust and knowledge. |
| **Attack Pattern (MITRE ATT\&CK for ICS)** | **Initial Access:** T0869: Valid Accounts. **Execution:** T0840: Program Download. **Privilege Escalation:** Not required if actor already has sufficient privileges. **Impair Process Control:** T0831: Modify Parameter; T0832: Modify Program. **Impact:** T0834: Manipulation of Control. |
| **Common Vulnerabilities Exploited** | Lack of principle of least privilege; insufficient logging and monitoring of privileged user activity; weak procedural controls for making changes to safety-critical systems; shared or generic admin accounts. |
| **Example Access Points** | A signaling engineer's authorized laptop connected directly to the interlocking system during a maintenance window; remote access credentials of a third-party maintenance contractor. |
| **Potential Impacts** | **Safety:** Very High. Malicious modification of interlocking logic could create unsafe conditions, such as allowing two trains onto the same track segment or moving a switch under a train, potentially leading to a collision or derailment. **Operational:** Localized or widespread disruption depending on the scope of the changes made. **Financial:** Costs of investigation, system restoration, and potential liability from a safety incident. **Regulatory:** Severe penalties and loss of operating license. |
| **Alignment with IEC 62443** | **Violates:** FR1 (Access Control), FR2 (Use Control), FR3 (System Integrity). **Mitigated by:** SR 1.1 (Human user identification), SR 1.5 (Privileged user management), SR 2.1 (Authorization enforcement), SR 2.3 (Auditing of security events), SR 3.2 (Protection against unauthorized code). |
| **EMB3D Modeling Alignment** | **Targets:** Interlocking PLC/Controller (PID-13: Software, PID-12: Firmware). **Exploits:** TID-103 (Implant Malicious Logic), TID-105 (Firmware Manipulation), TID-106 (Software Manipulation). |

#### **Narrative**

A signaling maintenance contractor, disgruntled over a contract dispute, decides to retaliate against the rail operator. Leveraging their legitimate, privileged credentials and deep knowledge of the signaling system, the contractor gains access to an engineering workstation connected to the interlocking system for a major junction.

During a scheduled late-night maintenance window, the contractor deviates from the approved work plan. They use their authorized access to modify the control logic within the interlocking's Programmable Logic Controller (PLC). The modification is subtle: it disables a critical safety check that prevents a specific set of track switches from being thrown while a route is occupied. The change is not immediately obvious and does not trigger any standard operational alarms. The contractor then logs out, their actions un-audited due to insufficient monitoring of privileged activity.

The next morning, during peak commuter hours, a train controller routes a train through the junction. Due to a separate minor delay, the controller attempts to re-route a second train onto an adjacent track. The compromised interlocking system, with its safety logic disabled, permits the track switch to move directly under the first train. This creates a high-risk scenario for derailment and collision.

This scenario, based on the identification of insiders as a key threat by RISSB 15 and echoing the malicious actions of a former employee at Canadian Pacific Rail 47, demonstrates that the most damaging attacks can come from trusted individuals. It highlights that technological controls alone are insufficient. Robust procedural controls, strict enforcement of the principle of least privilege, comprehensive auditing of all privileged actions (as required by IEC 62443-2-1), and behavioral monitoring are essential to mitigate the insider threat.

### **4.5 Threat Scenario 5: DDoS Attack on Passenger-Facing Systems**

**Table 5: Threat Scenario Summary – DDoS on Passenger Systems**

| Component | Description |
| :---- | :---- |
| **Threat Title** | Hacktivist-Led DDoS Attack on Passenger Information and Ticketing Systems |
| **Threat Actor Profile** | **Type:** Hacktivist Group or loosely affiliated individuals. **Motivation:** Ideological, political protest, notoriety. **Skill Level:** Low to Medium, often using readily available DDoS-for-hire services. |
| **Target Systems & Technologies** | Public-facing websites, mobile applications, APIs for journey planners, station Passenger Information System (PIS) displays, online ticketing portals. |
| **Likelihood & Statistics** | **High.** DDoS attacks are the dominant incident type in the EU transport sector, accounting for 77% of incidents, largely from hacktivists.21 The ACSC reported a 280% increase in DDoS incidents responded to.13 |
| **Attack Pattern (MITRE ATT\&CK for ICS)** | **Impact:** T0814: Denial of Service. (While this is an ICS technique, the principle applies to the denial of availability for critical IT services that support operations). |
| **Common Vulnerabilities Exploited** | Insufficient bandwidth to absorb attack traffic; lack of a cloud-based DDoS mitigation service; unprotected application APIs; single points of failure in web infrastructure. |
| **Example Access Points** | A global botnet directs overwhelming traffic to the rail operator's primary website and mobile app APIs. |
| **Potential Impacts** | **Safety:** None directly. **Operational:** Severe disruption to passenger services. Inability for customers to plan journeys, buy tickets, or receive real-time updates on delays. Overcrowding and confusion at stations. Inability to process payments. **Financial:** Loss of revenue from ticket sales; potential costs for DDoS mitigation services. **Reputational:** Significant damage to public perception and customer satisfaction; seen as technologically unprepared. |
| **Alignment with IEC 62443** | **Violates:** FR7 (Resource Availability). **Mitigated by:** While IEC 62443 is OT-focused, its principles apply. SR 7.1 (Denial-of-service protection) and SR 7.3 (Control system backup) are conceptually relevant for ensuring the availability of essential supporting systems. |
| **EMB3D Modeling Alignment** | Not applicable, as this attack targets high-level IT application infrastructure, not embedded devices. |

#### **Narrative**

In protest of a government policy, a hacktivist group announces a campaign targeting the nation's critical infrastructure. Their chosen target is the national rail operator. Using a widely available DDoS-for-hire service, they launch a massive, multi-vector attack against the operator's public-facing digital infrastructure.

An overwhelming flood of malicious traffic targets the operator's main website, the backend APIs for its mobile journey planner app, and the servers that feed real-time data to Passenger Information System (PIS) displays at stations nationwide. The operator's on-premises firewalls are quickly saturated, and the website and mobile app become inaccessible. At stations, the PIS displays either freeze, show incorrect information, or go blank.

The attack, while not impacting the safety-critical train control systems, causes immediate and widespread chaos. Passengers are unable to check timetables, plan their journeys, or purchase tickets online. At stations, the lack of information leads to confusion, frustration, and overcrowding. The operator's customer service phone lines are inundated, and its social media channels are overwhelmed with complaints.

This scenario is a direct parallel to the secondary DDoS attack experienced by Auckland Transport following their ransomware incident.33 It demonstrates that even attacks that do not touch the OT network can have a severe impact on the operator's ability to deliver its service. It highlights the criticality of systems that are often considered "corporate IT" but are, in fact, essential for modern rail operations. The high volume of DDoS attacks reported by both ENISA and the ACSC confirms this is a prevalent and highly probable threat scenario.13

### **4.6 Threat Scenario 6: Exploitation of Embedded Controller in a Trackside Tunnel**

**Table 6: Threat Scenario Summary – Embedded Controller Exploit**

| Component | Description |
| :---- | :---- |
| **Threat Title** | Physical Access and Firmware Exploitation of a Trackside Embedded Controller |
| **Threat Actor Profile** | **Type:** Sophisticated Criminal Group or State-Sponsored Actor. **Motivation:** Sabotage, theft of operational data, establishing a persistent and hard-to-detect foothold in the OT network. **Skill Level:** Very High, with expertise in embedded systems, reverse engineering, and OT protocols. |
| **Target Systems & Technologies** | Trackside embedded controllers (e.g., for signaling repeaters, ventilation, point heaters, axle counters), PLCs, Remote Terminal Units (RTUs). |
| **Likelihood & Statistics** | **Low to Medium.** Requires physical or close-proximity access, making it more difficult than remote attacks. However, the impact can be severe and difficult to trace. The increasing number of "smart" trackside devices expands the potential targets. |
| **Attack Pattern (MITRE ATT\&CK for ICS)** | **Initial Access:** T0837: Physical Access. **Execution:** T0818: Exploit/Modify Program. **Persistence:** T0820: Hidden Files and Directories. **Evasion:** T0836: Modify Program (to hide malicious logic). **Impair Process Control:** T0826: Manipulate I/O Image. |
| **Common Vulnerabilities Exploited** | Unsecured or easily bypassed physical enclosures; unprotected device maintenance ports (USB, JTAG); lack of secure boot or firmware integrity validation; hardcoded credentials. |
| **Example Access Points** | An attacker posing as a maintenance worker gains access to a trackside equipment cabinet in a remote tunnel location. |
| **Potential Impacts** | **Safety:** High. Manipulation of a signaling repeater could cause incorrect signal aspects to be displayed to a train driver. Manipulation of an axle counter could lead to false track occupancy readings. **Operational:** "Ghost" faults that are difficult to diagnose; intermittent system failures; loss of visibility of a specific track section. **Financial:** High cost of forensic investigation and remediation, especially for a hardware-level compromise. |
| **Alignment with IEC 62443** | **Violates:** FR1 (Access Control), FR3 (System Integrity). **Mitigated by:** SR 1.8 (Physical access control), SR 3.1 (Communication Integrity), SR 3.3 (Portable and Mobile Device Security), SR 3.5 (Firmware/software integrity). |
| **EMB3D Modeling Alignment** | **Targets:** Trackside PLC/RTU (PID-3: Physical Access Interface, PID-12: Firmware, PID-2: Debugging/Programming Interface). **Exploits:** TID-105 (Firmware Manipulation), TID-103 (Implant Malicious Logic), TID-102 (Reverse Engineering), TID-100 (Extract Firmware). |

#### **Narrative**

A highly skilled threat actor, tasked with creating a persistent and deniable method of disrupting a key rail line, targets distributed trackside assets. Posing as maintenance personnel, the attackers gain physical access to an equipment cabinet located within a rail tunnel. Inside the cabinet is an embedded controller—a small PLC responsible for managing a critical signaling repeater.

The attackers connect a specialized device to the PLC's unprotected maintenance port (e.g., USB or JTAG). They exploit a known vulnerability in the device's firmware to bypass security protections and dump the existing firmware image. The attackers then reverse-engineer the firmware, implant malicious logic, and re-flash the modified firmware onto the device. The malicious logic is designed to intermittently corrupt the signaling data being passed through the repeater, but only under specific, rare conditions, making the fault incredibly difficult to diagnose.

The device's lack of a secure boot mechanism or runtime firmware integrity validation means it boots up with the malicious code, appearing to function normally. Over the following weeks, the rail operator experiences a series of inexplicable "ghost" signaling faults along that section of track. The intermittent nature of the failures leads maintenance crews to suspect a hardware fault, resulting in costly and time-consuming component replacements that fail to solve the problem.

This scenario leverages the MITRE EMB3D framework to illustrate a deep-level attack on the cyber-physical components that underpin the entire rail operation.43 It highlights the vulnerability of physically distributed OT assets and demonstrates that a comprehensive security strategy must extend beyond the network layer to include the hardening of embedded devices themselves, encompassing physical security, port protection, and hardware-level integrity checks as mandated by IEC 62443\.

## **5.0 Summary of Mitigations and Recommendations**

To counter the diverse and sophisticated threats detailed in the preceding scenarios, rail operators in Australia and New Zealand must implement a comprehensive, defense-in-depth security strategy. The following recommendations are structured according to the seven Foundational Requirements (FRs) of the IEC 62443 standard, providing a clear roadmap for building a resilient and defensible architecture.

### **FR 1: Identification and Authentication Control (IAC)**

This requirement ensures that all access to the system is restricted to authorized users, processes, and devices.

* **Recommendation:** Implement a robust Identity and Access Management (IAM) program based on the principle of least privilege. Every user and system should only have the absolute minimum access required to perform their function. This directly mitigates the high-impact risk of an **Insider Threat (Scenario 4.4)**.  
* **Recommendation:** Mandate phishing-resistant Multi-Factor Authentication (MFA) for all remote access to the OT network, including for employees and third-party vendors. This is a critical control to prevent attackers from using stolen credentials, a key tactic in gaining initial access as seen in **Ransomware Crossover (Scenario 4.1)** and as a general trend.54 This helps mitigate ATT\&CK for ICS techniques **T0862 (External Remote Services)** and **T0869 (Valid Accounts)**.  
* **Recommendation:** Enforce strong physical access controls (SR 1.8) for all trackside cabinets, control rooms, and data centers to prevent unauthorized physical access, as depicted in the **Embedded Controller Exploit (Scenario 4.6)**.

### **FR 2: Use Control (UC)**

This requirement ensures that users, processes, and devices can only perform their authorized actions.

* **Recommendation:** Deploy application whitelisting on all critical OT endpoints, including engineering workstations and HMIs. This ensures that only approved and vetted software can execute, preventing the initial execution of malware dropped from a phishing attack (**Ransomware Crossover, Scenario 4.1**) or by an insider. This is a primary mitigation for **T0845 (User Execution)**.  
* **Recommendation:** Implement strict controls and auditing for the use of portable media and transient devices (laptops used for maintenance). This helps prevent malware introduction and unauthorized modifications, as seen in the **Insider Threat (Scenario 4.4)**.

### **FR 3: System Integrity (SI)**

This requirement ensures the integrity of the IACS to prevent unauthorized manipulation.

* **Recommendation:** Implement a comprehensive patch and vulnerability management program (SR 7.6) for all OT assets. For legacy systems that cannot be patched, apply compensating controls such as virtual patching via an Intrusion Prevention System (IPS).  
* **Recommendation:** Deploy file integrity monitoring on critical servers and controllers to detect unauthorized changes to software, firmware, or configuration files. This provides a crucial detection capability against the actions of an **Insider Threat (Scenario 4.4)** or a **Supply Chain Compromise (Scenario 4.3)**, helping to identify techniques like **T0832 (Modify Program)**.  
* **Recommendation:** Procure and deploy embedded devices that support secure boot and runtime integrity validation to ensure they are running only authorized, untampered firmware. This is a direct mitigation for the **Embedded Controller Exploit (Scenario 4.6)**.

### **FR 4: Data Confidentiality (DC)**

This requirement protects sensitive information from unauthorized disclosure.

* **Recommendation:** Implement encryption for all sensitive data in transit, particularly over wireless links such as train-to-ground communications. This helps protect against eavesdropping and man-in-the-middle attacks that could be a precursor to a **Signaling Disruption (Scenario 4.2)**.  
* **Recommendation:** Encrypt sensitive operational data at rest, such as configuration files on engineering workstations or data stored in historians, to prevent data theft in the event of a breach.

### **FR 5: Restricted Data Flow (RDF)**

This requirement segments the control system to limit the unnecessary flow of data.

* **Recommendation:** This is one of the most critical areas for defense. Vigorously implement a network segmentation architecture based on the IEC 62443 Zones and Conduits model.27 Create a strong, defensible boundary (a "demilitarized zone" or DMZ) between the IT and OT networks with strictly controlled and monitored conduits. This is the single most effective control to prevent the **Ransomware Crossover (Scenario 4.1)**.  
* **Recommendation:** Within the OT network, apply micro-segmentation to create additional zones around the most critical systems, such as the signaling interlocking and safety systems, to prevent lateral movement by an attacker who has already breached the OT perimeter.

### **FR 6: Timely Response to Events (TRE)**

This requirement ensures that security violations are detected and responded to in a timely manner.

* **Recommendation:** Develop and regularly test a dedicated OT-specific Incident Response (IR) plan. Conduct tabletop exercises using the scenarios in this report to ensure that both technical and operational staff understand their roles during an incident.17  
* **Recommendation:** Deploy an OT-aware network security monitoring solution capable of deep packet inspection of industrial protocols. This is essential for detecting anomalous behavior and adversary TTPs within the OT network that would be invisible to traditional IT security tools.

### **FR 7: Resource Availability (RA)**

This requirement ensures the availability of the IACS against events that could cause a denial of service.

* **Recommendation:** Implement a robust and regularly tested backup and recovery strategy for all critical OT systems (SR 7.3). Backups must be stored offline or in an isolated, immutable location to ensure they are not encrypted during a ransomware attack.55  
* **Recommendation:** For public-facing services, procure and configure a cloud-based DDoS mitigation service to protect websites, APIs, and passenger applications from availability attacks, as detailed in **Scenario 4.5**.

### **Cross-Cutting Recommendations**

* **Supply Chain Risk Management:** Rail operators must extend their security requirements to their supply chain. Mandate that all vendors of OT products and systems provide evidence of compliance with the IEC 62443-4-1 standard for secure product development.  
* **Security Awareness Training:** A continuous security awareness program is vital. Training must be tailored to different roles, with specific modules for OT engineers and operators focusing on threats like phishing and the proper handling of privileged access and portable media.5  
* **Adopt an "Assume Compromise" Mindset:** As recommended by the ACSC 12, rail operators should operate with the understanding that preventative controls can fail. This mindset shifts focus towards building resilience and prioritizing rapid detection, effective response, and swift recovery to minimize the impact of an incident.

## **6.0 Conclusion**

The analysis presented in this report confirms that the rail sectors of Australia and New Zealand are at a critical juncture. The rapid integration of digital technologies has unlocked significant operational benefits but has concurrently exposed safety-critical systems to a severe and dynamically evolving spectrum of cyberthreats. The threat is not theoretical; it is a clear and present danger demonstrated by global trends and underscored by regional incidents such as the multi-stage attack on Auckland Transport.

The threat landscape is complex, characterized by financially motivated ransomware groups, sophisticated state-sponsored actors, and the persistent risk of insider threats. Attackers are actively targeting the seams of converged IT/OT environments, exploiting vulnerabilities in supply chains, and leveraging weaknesses in both legacy and modern systems. A reactive or compliance-only approach to cybersecurity is no longer sufficient to ensure the safety, reliability, and resilience of rail services.

To navigate this challenging environment, rail operators must adopt a proactive, threat-informed defense posture. This strategic shift requires moving beyond a simple checklist of security controls and instead building a defensible architecture based on a deep understanding of adversary behaviors. The synergy of the foundational frameworks detailed in this report provides the necessary toolkit for this transformation. The IEC 62443 standard offers the blueprint for "what good looks like"—a secure, segmented, and resilient IACS architecture. The MITRE ATT\&CK® for ICS and EMB3D™ frameworks provide the threat intelligence context, detailing "what bad looks like" by cataloging the real-world tactics, techniques, and procedures adversaries use to compromise these systems.

By integrating these frameworks, rail organizations can prioritize investments, tailor security controls to counter specific, credible threats, and build a culture of security that is as foundational as their long-standing culture of safety. The journey to cyber resilience is continuous, but by embracing a threat-informed strategy, the Australian and New Zealand rail sectors can confidently harness the benefits of digitalization while safeguarding the critical services upon which their nations depend.

## **7.0 References**

All sources cited in-text throughout this report (e.g.1) are compiled from the provided research materials. In a final publication, this section would contain a complete list of these sources, formatted in strict accordance with the APA 7th Edition citation style. This would include reports from organizations such as the European Union Agency for Cybersecurity (ENISA), Australian Cyber Security Centre (ACSC), Rail Industry Safety and Standards Board (RISSB), New Zealand National Cyber Security Centre (NCSC), Dragos, Mandiant (a part of Google Cloud), SANS Institute, IBM, Fortinet, Claroty, Nozomi Networks, Siemens, Schneider Electric, and others.

#### **Works cited**

1. ENISA THREAT LANDSCAPE: transport sector, accessed October 28, 2025, [https://www.enisa.europa.eu/sites/default/files/publications/ENISA%20Transport%20Threat%20Landscape\_RECAST2.pdf](https://www.enisa.europa.eu/sites/default/files/publications/ENISA%20Transport%20Threat%20Landscape_RECAST2.pdf)  
2. Understanding Cyber Threats in Transport | ENISA \- European Union, accessed October 28, 2025, [https://www.enisa.europa.eu/news/understanding-cyber-threats-in-transport](https://www.enisa.europa.eu/news/understanding-cyber-threats-in-transport)  
3. Transport | ENISA \- European Union, accessed October 28, 2025, [https://www.enisa.europa.eu/topics/cybersecurity-of-critical-sectors/transport](https://www.enisa.europa.eu/topics/cybersecurity-of-critical-sectors/transport)  
4. Getting on Track With Rail Cybersecurity | GHD Insights, accessed October 28, 2025, [https://www.ghd.com/es-cl/insights/getting-on-track-with-rail-cybersecurity](https://www.ghd.com/es-cl/insights/getting-on-track-with-rail-cybersecurity)  
5. How Railroads Can Harden Their Defenses and Get Ahead Of Cyber Threats in 2023, accessed October 28, 2025, [https://www.appviewx.com/blogs/how-railroads-can-harden-their-defenses-and-get-ahead-of-cyber-threats-in-2023/](https://www.appviewx.com/blogs/how-railroads-can-harden-their-defenses-and-get-ahead-of-cyber-threats-in-2023/)  
6. Cyber Attacks on Railway Systems Increase by 220% \- SecureWorld, accessed October 28, 2025, [https://www.secureworld.io/industry-news/railway-cyber-attacks](https://www.secureworld.io/industry-news/railway-cyber-attacks)  
7. IEC 62443 Industrial Cybersecurity Certification \- TÜV SÜD, accessed October 28, 2025, [https://www.tuvsud.com/en-us/industries/manufacturing/machinery-and-robotics/iec-62443-industrial-security](https://www.tuvsud.com/en-us/industries/manufacturing/machinery-and-robotics/iec-62443-industrial-security)  
8. Cybersecurity Challenges in Modern Railway Signaling- A Comprehensive Review \- IJFMR, accessed October 28, 2025, [https://www.ijfmr.com/research-paper.php?id=56254](https://www.ijfmr.com/research-paper.php?id=56254)  
9. Understanding Railway Cybersecurity, accessed October 28, 2025, [https://gca.isa.org/blog/understanding-railway-cybersecurity](https://gca.isa.org/blog/understanding-railway-cybersecurity)  
10. Cyber security train control – lessons learned | News & Insights | Informa Australia, accessed October 28, 2025, [https://www.informa.com.au/insight/cyber-security-train-control-lessons-learned/](https://www.informa.com.au/insight/cyber-security-train-control-lessons-learned/)  
11. Siemens Cybersecurity: An Overview and Its Broader Impact \- \- sitsi, accessed October 28, 2025, [https://sitsi.pacanalyst.com/siemens-cybersecurity-an-overview-and-its-broader-impact/](https://sitsi.pacanalyst.com/siemens-cybersecurity-an-overview-and-its-broader-impact/)  
12. ACSC reports surge in cyberattacks targeting Australia's critical infrastructure, focus shifts to building resilience \- Industrial Cyber, accessed October 28, 2025, [https://industrialcyber.co/reports/acsc-reports-surge-in-cyberattacks-targeting-australias-critical-infrastructure-focus-shifts-to-building-resilience/](https://industrialcyber.co/reports/acsc-reports-surge-in-cyberattacks-targeting-australias-critical-infrastructure-focus-shifts-to-building-resilience/)  
13. Annual Cyber Threat Report 2024-2025 | Cyber.gov.au, accessed October 28, 2025, [https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2024-2025](https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2024-2025)  
14. Cyber security | New Zealand Ministry of Foreign Affairs and Trade, accessed October 28, 2025, [https://www.mfat.govt.nz/en/peace-rights-and-security/international-security/cyber-security](https://www.mfat.govt.nz/en/peace-rights-and-security/international-security/cyber-security)  
15. AUSTRALIAN RAIL NETWORK CYBER SECURITY ... \- RISSB's, accessed October 28, 2025, [https://www.rissb.com.au/wp-content/uploads/2019/05/2021\_04\_2019\_05\_Cyber-Security-Strategy.pdf](https://www.rissb.com.au/wp-content/uploads/2019/05/2021_04_2019_05_Cyber-Security-Strategy.pdf)  
16. X-Force Threat Intelligence Index 2021 \- HelpRansomware, accessed October 28, 2025, [https://helpransomware.com/wp-content/uploads/2022/10/IBM-Security-X-Force-Threat-Intelligence-Index-HelpRansomware.pdf](https://helpransomware.com/wp-content/uploads/2022/10/IBM-Security-X-Force-Threat-Intelligence-Index-HelpRansomware.pdf)  
17. Blog \- Dragos, accessed October 28, 2025, [https://www.dragos.com/blog/2023-ot-cybersecurity-year-in-review-now-available/](https://www.dragos.com/blog/2023-ot-cybersecurity-year-in-review-now-available/)  
18. IBM Security X-Force Threat Intelligence Index 2022 Full Report, accessed October 28, 2025, [https://secure-iss.com/wp-content/uploads/2022/11/X-Force-Threat-Intelligence-Index-2022-Full-Report.pdf](https://secure-iss.com/wp-content/uploads/2022/11/X-Force-Threat-Intelligence-Index-2022-Full-Report.pdf)  
19. Key Findings from the Fortinet 2025 Operational Technology ..., accessed October 28, 2025, [https://www.fortinet.com/blog/business-and-technology/key-findings-from-the-fortinet-2025-operational-technology-security-report](https://www.fortinet.com/blog/business-and-technology/key-findings-from-the-fortinet-2025-operational-technology-security-report)  
20. Australian Signals Directorate releases the Annual Cyber Threat Report 2024-25, accessed October 28, 2025, [https://www.cyber.gov.au/about-us/view-all-content/news-and-media/australian-signals-directorate-releases-annual-cyber-threat-report-2024-25](https://www.cyber.gov.au/about-us/view-all-content/news-and-media/australian-signals-directorate-releases-annual-cyber-threat-report-2024-25)  
21. ENISA 2025 Threat Landscape report highlights EU faces escalating hacktivist attacks and state-aligned cyber threats \- Industrial Cyber, accessed October 28, 2025, [https://industrialcyber.co/reports/enisa-2025-threat-landscape-report-highlights-eu-faces-escalating-hacktivist-attacks-and-state-aligned-cyber-threats/](https://industrialcyber.co/reports/enisa-2025-threat-landscape-report-highlights-eu-faces-escalating-hacktivist-attacks-and-state-aligned-cyber-threats/)  
22. Attackers hit security device defects hard in 2024 \- CyberScoop, accessed October 28, 2025, [https://cyberscoop.com/mandiant-m-trends-2025/](https://cyberscoop.com/mandiant-m-trends-2025/)  
23. Attackers test the limits of railway cybersecurity \- Help Net Security, accessed October 28, 2025, [https://www.helpnetsecurity.com/2025/09/09/railway-systems-cybersecurity/](https://www.helpnetsecurity.com/2025/09/09/railway-systems-cybersecurity/)  
24. ics/ot cybersecurity \- year in review 2022 • executive summary \- Dragos, accessed October 28, 2025, [https://hub.dragos.com/hubfs/312-Year-in-Review/2022/Dragos\_Year-In-Review-Exec-Summary-2022.pdf](https://hub.dragos.com/hubfs/312-Year-in-Review/2022/Dragos_Year-In-Review-Exec-Summary-2022.pdf)  
25. Cybersecurity Challenges In Signalling Networks \- Softech Rail, accessed October 28, 2025, [https://www.softechrail.com/cybersecurity-challenges-in-signalling/](https://www.softechrail.com/cybersecurity-challenges-in-signalling/)  
26. Taking cybersecurity challenges into account in railway safety, accessed October 28, 2025, [https://www.era.europa.eu/system/files/2022-11/enr135-taking\_cybersecurity\_challenges\_into\_account\_in\_railway\_safety\_en.pdf](https://www.era.europa.eu/system/files/2022-11/enr135-taking_cybersecurity_challenges_into_account_in_railway_safety_en.pdf)  
27. What Is IEC 62443? Definition, Breakdown & Methodology \- Zscaler, accessed October 28, 2025, [https://www.zscaler.com/zpedia/what-is-iec-62443](https://www.zscaler.com/zpedia/what-is-iec-62443)  
28. Cyber Threat Reports \- the National Cyber Security Centre, accessed October 28, 2025, [https://www.ncsc.govt.nz/insights-and-research/cyber-threat-reports/](https://www.ncsc.govt.nz/insights-and-research/cyber-threat-reports/)  
29. Mind the gap: Governing cyber security risks \- Office of the Auditor-General New Zealand, accessed October 28, 2025, [https://oag.parliament.nz/2025/cyber-security](https://oag.parliament.nz/2025/cyber-security)  
30. National Cyber Security Centre \- Government Communications Security Bureau, accessed October 28, 2025, [https://www.gcsb.govt.nz/our-work/national-cyber-security-centre-ncsc](https://www.gcsb.govt.nz/our-work/national-cyber-security-centre-ncsc)  
31. Auckland Transport Hit by Medusa Ransomware: What You Need to Know, accessed October 28, 2025, [https://breached.company/auckland-transport-hit-by-medusa-ransomware-what-you-need-to-know/](https://breached.company/auckland-transport-hit-by-medusa-ransomware-what-you-need-to-know/)  
32. Suspected cyberattack crashes Auckland Transport card network | RNZ News, accessed October 28, 2025, [https://www.rnz.co.nz/news/national/498003/suspected-cyberattack-crashes-auckland-transport-card-network](https://www.rnz.co.nz/news/national/498003/suspected-cyberattack-crashes-auckland-transport-card-network)  
33. AT website issues due to ransomware incident \- Auckland Transport, accessed October 28, 2025, [https://at.govt.nz/about-us/news-events/media-centre/2023-media-releases/at-website-issues-due-to-ransomware-incident](https://at.govt.nz/about-us/news-events/media-centre/2023-media-releases/at-website-issues-due-to-ransomware-incident)  
34. IEC 62443 \- Wikipedia, accessed October 28, 2025, [https://en.wikipedia.org/wiki/IEC\_62443](https://en.wikipedia.org/wiki/IEC_62443)  
35. Understanding IEC 62443, accessed October 28, 2025, [https://www.iec.ch/blog/understanding-iec-62443](https://www.iec.ch/blog/understanding-iec-62443)  
36. ISA/IEC 62443 Series of Standards | ISAGCA, accessed October 28, 2025, [https://isagca.org/isa-iec-62443-standards](https://isagca.org/isa-iec-62443-standards)  
37. ICS Mitigations \- MITRE ATT\&CK®, accessed October 28, 2025, [https://attack.mitre.org/mitigations/ics/](https://attack.mitre.org/mitigations/ics/)  
38. Applying MITRE ATT\&CK framework to OT/ICS systems \- Sener, accessed October 28, 2025, [https://www.group.sener/en/insights/applying-mitre-attck-framework-to-ot-ics-systems/](https://www.group.sener/en/insights/applying-mitre-attck-framework-to-ot-ics-systems/)  
39. MITRE ATT\&CK ICS: Tactics, Techniques, and Best Practices \- Exabeam, accessed October 28, 2025, [https://www.exabeam.com/explainers/mitre-attck/mitre-attck-ics-tactics-techniques-and-best-practices/](https://www.exabeam.com/explainers/mitre-attck/mitre-attck-ics-tactics-techniques-and-best-practices/)  
40. ICS Tactics \- MITRE ATT\&CK®, accessed October 28, 2025, [https://attack.mitre.org/tactics/ics/](https://attack.mitre.org/tactics/ics/)  
41. ICS Matrix \- MITRE ATT\&CK®, accessed October 28, 2025, [https://attack.mitre.org/matrices/ics/](https://attack.mitre.org/matrices/ics/)  
42. Securing Critical Infrastructure: Why OT Requires a Threat-Informed Defense | Fortinet Blog, accessed October 28, 2025, [https://www.fortinet.com/blog/business-and-technology/securing-critical-infrastructure-why-ot-requires-a-threat-informed-defense](https://www.fortinet.com/blog/business-and-technology/securing-critical-infrastructure-why-ot-requires-a-threat-informed-defense)  
43. MITRE EMB3D™, accessed October 28, 2025, [https://emb3d.mitre.org/](https://emb3d.mitre.org/)  
44. What is the MITRE EMB3D Framework and Why It Matters \- Asimily, accessed October 28, 2025, [https://asimily.com/blog/what-is-the-mitre-emb3d-framework/](https://asimily.com/blog/what-is-the-mitre-emb3d-framework/)  
45. MITRE releases EMB3D cybersecurity threat model for embedded devices to boost critical infrastructure security \- Industrial Cyber, accessed October 28, 2025, [https://industrialcyber.co/critical-infrastructure/mitre-releases-emb3d-cybersecurity-threat-model-for-embedded-devices-to-boost-critical-infrastructure-security/](https://industrialcyber.co/critical-infrastructure/mitre-releases-emb3d-cybersecurity-threat-model-for-embedded-devices-to-boost-critical-infrastructure-security/)  
46. ENISA Threat Landscape 2025: Critical OT Security Risks Every Business Must Address, accessed October 28, 2025, [https://blog.denexus.io/resources/enisa-threat-landscape-2025-ot-attacks-industrial-cybersecurity-crisis](https://blog.denexus.io/resources/enisa-threat-landscape-2025-ot-attacks-industrial-cybersecurity-crisis)  
47. Top Cyber Threats in the Freight Rail Sector \- HALOCK Security Labs, accessed October 28, 2025, [https://www.halock.com/top-cyber-threats-in-the-freight-rail-sector/](https://www.halock.com/top-cyber-threats-in-the-freight-rail-sector/)  
48. IBM Security X-Force Threat Intelligence Index 2023, accessed October 28, 2025, [https://secure-iss.com/wp-content/uploads/2023/02/IBM-Security-X-Force-Threat-Intelligence-Index-2023.pdf](https://secure-iss.com/wp-content/uploads/2023/02/IBM-Security-X-Force-Threat-Intelligence-Index-2023.pdf)  
49. A SANS 2021 Survey: OT/ICS Cybersecurity | SITIC.org, accessed October 28, 2025, [https://sitic.org/wordpress/wp-content/uploads/A-SANS-2021-Survey-OT-ICS-Cybersecurity.pdf](https://sitic.org/wordpress/wp-content/uploads/A-SANS-2021-Survey-OT-ICS-Cybersecurity.pdf)  
50. Securing the Future of Railway Systems: A Comprehensive Cybersecurity Strategy for Critical On-Board and Track-Side Infrastructure \- PMC \- PubMed Central, accessed October 28, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11680022/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11680022/)  
51. Cyber hackers target Polish rail network, cause operational disruptions, accessed October 28, 2025, [https://industrialcyber.co/transport/cyber-hackers-target-polish-rail-network-cause-operational-disruptions/](https://industrialcyber.co/transport/cyber-hackers-target-polish-rail-network-cause-operational-disruptions/)  
52. Future Rail Signaling: Cyber and Energy Resilience Through AI Interoperability \- MDPI, accessed October 28, 2025, [https://www.mdpi.com/2071-1050/17/10/4643](https://www.mdpi.com/2071-1050/17/10/4643)  
53. EU consistently targeted by diverse yet convergent threat groups \- ENISA \- European Union, accessed October 28, 2025, [https://www.enisa.europa.eu/news/etl-2025-eu-consistently-targeted-by-diverse-yet-convergent-threat-groups](https://www.enisa.europa.eu/news/etl-2025-eu-consistently-targeted-by-diverse-yet-convergent-threat-groups)  
54. M-Trends 2025: State-Sponsored IT Workers Emerge as Global Threat \- SecurityWeek, accessed October 28, 2025, [https://www.securityweek.com/m-trends-2025-state-sponsored-it-workers-emerge-as-new-global-threat/](https://www.securityweek.com/m-trends-2025-state-sponsored-it-workers-emerge-as-new-global-threat/)  
55. Colorado DOT offers lessons learned after recovering from two 2018 ransomware attacks., accessed October 28, 2025, [https://www.itskrs.its.dot.gov/2019-l00856](https://www.itskrs.its.dot.gov/2019-l00856)