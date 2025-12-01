

# **Cyber Threat Landscape and Risk Analysis for the Queensland Train Manufacturing Program**

## **Executive Summary**

This report provides a comprehensive analysis of the cyber threat landscape facing the Queensland Train Manufacturing Program (QTMP), a critical national infrastructure endeavor. The program's strategic importance, coupled with its complex, multi-layered international supply chain and the deep integration of Information Technology (IT) and Operational Technology (OT), creates a significant and attractive attack surface for a wide spectrum of malicious actors. The analysis synthesizes threat intelligence from global sources such as the European Union Agency for Cybersecurity (ENISA), national bodies including the Australian Cyber Security Centre (ACSC), and industry-specific guidance from the Rail Industry Safety and Standards Board (RISSB).

Key findings indicate that the QTMP is positioned at the nexus of the world's most targeted sectors: manufacturing, transportation, and critical infrastructure. The primary threats are not singular but convergent, with state-sponsored actors adopting disruptive tactics, financially motivated criminals targeting critical operations for maximum leverage, and hacktivists seeking to cause reputational damage. A dominant theme emerging from the analysis is the acute risk posed by the project's extensive supply chain, where a compromise at a smaller partner can serve as a pivot point into core systems. Adversary tactics are evolving, with a marked shift towards the use of stolen credentials and "living-off-the-land" techniques that are difficult to detect with traditional security tools.

To contextualize these findings, this report formulates six detailed and plausible cyber threat scenarios. These scenarios are designed for use in strategic planning, threat modeling workshops, and resilience testing. A high-level summary of these scenarios is presented below.

**Cyber Threat Scenario Matrix for the Queensland Train Manufacturing Program**

| Scenario Title | Threat Actor Profile | Primary Target(s) | Key MITRE Tactic(s) (ICS) | Potential Impact |
| :---- | :---- | :---- | :---- | :---- |
| 1\. State-Sponsored Sabotage via IT/OT Convergence | Nation-State APT (e.g., Volt Typhoon/Vanguard Panda) | Train Control & Signaling Systems (TCMS, CBTC), SCADA | T0886: Impair Process Control, T0855: Valid Accounts | Catastrophic service disruption, potential safety incidents, national economic impact. |
| 2\. Ransomware Attack via Third-Party Supply Chain Compromise | Financially Motivated Group (e.g., LockBit affiliate) | Downer's Corporate Network, Project Management Systems (Autodesk, Azure) | T0885: Inhibit Response Function, T0813: Data Destruction | Major project delays, significant financial loss, data extortion, reputational damage. |
| 3\. Insider Threat Exploiting Physical and Digital Access | Disgruntled Contractor/Employee (Malicious or Unwitting) | Physical access to OT assets (PLCs, HMIs), internal network credentials | T0836: Modify Parameter, T0845: Steal Application Key | Sabotage of manufacturing processes, theft of sensitive project data, safety system bypass. |
| 4\. Disruption of Signaling Systems via Wireless Exploitation | Sophisticated Cybercriminal/Hacktivist | Communications-Based Train Control (CBTC) wireless links (WLAN) | T0822: Impair Process Control, T0830: Adversary-in-the-Middle | Train delays, service stoppages, potential for low-speed collisions, loss of public trust. |
| 5\. Industrial Espionage via Compromised Engineering Platforms | Competitor/State-Sponsored Actor (e.g., China-nexus group) | John Holland's Autodesk Cloud, Hyundai Rotem's design data, Digital Twin models | T0861: Point and Tag Identification, T0815: Data from Information Repositories | Theft of intellectual property (train designs, manufacturing processes), loss of competitive advantage. |
| 6\. Hacktivist Disruption of Passenger Services | Ideologically Motivated Group (e.g., NoName057(16)) | TMR Public-Facing Websites, Passenger Information Systems (PIS) | T0814: Denial of Service, T0880: Theft of Operational Information | Reputational damage, public confusion, minor operational disruption, erosion of public confidence. |

Strategic recommendations are provided to mitigate these threats, focusing on the principles of the RISSB Australian Rail Network Cyber Security Strategy and the IEC 62443 standard. These include the urgent implementation of a comprehensive supply chain risk management program, the enforcement of robust identity and access controls with phishing-resistant multi-factor authentication, the architectural implementation of a defense-in-depth strategy with strict IT/OT segmentation, and the development and regular testing of an OT-specific incident response plan.

## **1.0 Introduction**

### **1.1 The Queensland Train Manufacturing Program (QTMP): A Critical National Endeavor**

The Queensland Train Manufacturing Program (QTMP) represents a state-shaping investment in Australia's critical infrastructure, designed to meet the escalating demand for rail transport in South East Queensland over the next decade.1 The program's primary objective is the delivery of 65 new six-car passenger trains, which will be manufactured at a purpose-built, state-of-the-art facility in Torbanlea (TMF) and subsequently maintained at a new rail facility in Ormeau.1 Valued at $9.5 billion, the QTMP is a cornerstone of regional economic development and is integral to supporting major state projects, including the Cross River Rail and preparations for the Brisbane 2032 Olympic and Paralympic Games.2 The strategic importance of the QTMP elevates it beyond a standard infrastructure project, positioning it as a high-value target whose disruption could have significant economic and social consequences for the state and the nation.

### **1.2 Mapping the Ecosystem: Key Entities and the Supply Chain Attack Surface**

The delivery of the QTMP is managed through a complex, multi-tiered consortium of international and domestic partners, creating a vast and interconnected digital ecosystem. Understanding this structure is fundamental to appreciating the project's attack surface.

The key entities involved include:

* **Client/Asset Owner:** The Queensland Department of Transport and Main Roads (TMR) is the procuring agency and ultimate owner of the infrastructure and rolling stock.4  
* **Primary Contractor (Design, Build, Maintain \- DBM):** Downer Group was awarded the $4.6 billion DBM contract, making it the central entity responsible for overall project delivery, including train design, manufacturing, and the first 15 years of maintenance.2  
* **Train Manufacturer Partner:** Hyundai Rotem Corporation (HRC), a major South Korean rolling stock manufacturer, is partnered with Downer for the design and manufacturing of the trains. HRC is also establishing a separate facility in Maryborough for sub-component production.3  
* **Construction Contractors:** The construction of the physical facilities is subcontracted to John Holland, which is responsible for the Torbanlea Manufacturing Facility, and DT Infrastructure (a subsidiary of the global firm Gamuda), which is responsible for the Ormeau Maintenance and Stabling Facility.3  
* **Advisory and Management:** Turner & Townsend serves as the Program Management Office (PMO) provider, overseeing project controls and management, while WSP provides critical design services for the civil, structural, and rail systems of the greenfield facilities.3  
* **Technology & Service Providers:** The project's digital backbone is comprised of a diverse technology stack. Downer Group utilizes Microsoft Azure for cloud services and AI-powered safety systems, in addition to enterprise applications like SAP S/4 HANA.11 John Holland has a strategic partnership with Autodesk, leveraging its cloud-based construction platforms (ACC Build, BIM 360\) and also partners with Microsoft.13 Hyundai Rotem employs proprietary Train Control Management Systems (TCMS) and signaling technologies in its rolling stock.15

This intricate web of partnerships, while assembled for operational excellence, constitutes the project's most significant cyber vulnerability. Recent global threat reports consistently identify third-party and supply chain compromises as a leading and rapidly growing initial access vector for cyberattacks.19 The 2025 ENISA Threat Landscape report specifically highlights the increasing "abuse of cyber dependencies," where attackers compromise one entity to pivot to another.21 An adversary targeting the QTMP does not need to breach the hardened perimeter of a primary contractor like Downer directly. A more effective and lower-effort approach would be to compromise a smaller, potentially less-resourced partner in the supply chain to steal credentials or gain access to shared project platforms, such as a cloud-based design repository. This allows the attacker to bypass perimeter defenses and enter the ecosystem with a level of implied trust, demonstrating a classic supply chain attack pattern.

### **1.3 Foundational Cybersecurity Frameworks for Rail**

The analysis within this report is grounded in two globally recognized, complementary cybersecurity frameworks that are essential for securing modern industrial environments.

#### **1.3.1 MITRE ATT\&CK for Industrial Control Systems (ICS)**

The MITRE ATT\&CK for ICS framework is a comprehensive, publicly accessible knowledge base of adversarial tactics, techniques, and procedures (TTPs). It is curated from observations of real-world cyberattacks targeting industrial control systems and operational technology.23 The framework's primary purpose is to provide a common lexicon for describing and analyzing adversary behavior. By cataloging the methods attackers use to achieve their objectives—from gaining initial access to causing a physical impact—it enables defenders to model threats, inform threat intelligence programs, and focus detection and response strategies on known adversary actions. It provides the critical "how" of an attack, allowing organizations to think from the adversary's perspective.

#### **1.3.2 IEC 62443**

The IEC 62443 is a series of international standards that provides a comprehensive framework for the cybersecurity of Industrial Automation and Control Systems (IACS).25 Unlike ATT\&CK, which focuses on adversary behavior, IEC 62443 provides a structured, risk-based methodology for designing, implementing, and managing secure OT environments. Its core principles include the segmentation of networks into "zones" (groupings of assets with common security requirements) and "conduits" (secure communication channels between zones), and the assignment of Security Levels (SLs) to define the required resilience of each zone against attack.27 This standard provides the prescriptive "what" and "where" of defense, guiding organizations in building a defensible and resilient architecture.

#### **1.3.3 Synergistic Application**

The true strength of these frameworks lies in their synergistic application.25 The MITRE ATT\&CK for ICS framework describes the adversary's playbook, while the IEC 62443 standard provides the blueprint for building a robust defense against those plays. By mapping the TTPs identified in ATT\&CK to the specific security controls and architectural principles mandated by IEC 62443, an organization can transition from a reactive, compliance-based security posture to a proactive, threat-informed defense. This integrated approach ensures that security investments are directly targeted at mitigating the most relevant and likely threats, building systems that are resilient by design against known adversary behaviors.

## **2.0 The Global and National Threat Context for Rail Infrastructure**

### **2.1 The European Threat Landscape (ENISA)**

The ENISA Threat Landscape 2025 report, which analyzes nearly 4,900 incidents between July 2024 and June 2025, provides critical insights into the global threat environment relevant to the QTMP.21 Ransomware is identified as the most impactful threat, characterized by aggressive double- and triple-extortion tactics and the professionalization of the cybercrime ecosystem.30 While ransomware causes the most damage, Distributed Denial-of-Service (DDoS) attacks, primarily perpetrated by hacktivist groups, are the most frequent incident type, accounting for 77% of all reports.32

Critically for the QTMP, the transport sector is the second most targeted sector in the EU, accounting for 7.5% of incidents, while manufacturing also ranks in the top five.33 The report highlights that state-aligned threat groups have intensified their long-term cyberespionage campaigns against the telecommunications, logistics, and manufacturing sectors.21 The primary initial intrusion vector remains phishing (60% of cases), with a concerning trend of AI-powered campaigns that are used to craft more convincing lures and automate social engineering.21 A key strategic trend identified is the convergence of threat actor motivations and tools, where the lines between cybercrime, espionage, and hacktivism are increasingly blurred.30

### **2.2 The Australian Threat Landscape (ACSC)**

The Australian Cyber Security Centre's (ACSC) Annual Cyber Threat Report 2024-25 corroborates global trends and provides a specific national context.34 The report details a significant increase in malicious activity, with an 11% rise in responded-to incidents and a striking 111% increase in notifications of potential malicious activity sent to critical infrastructure (CI) entities.34

CI entities, such as those involved in the QTMP, are identified as highly attractive targets for both state-sponsored actors and cybercriminals due to their sensitive data holdings and the potential for widespread societal disruption.34 The ACSC specifically warns of state-sponsored actors targeting CI to pre-position for potential disruptive attacks and highlights a Russian campaign targeting Western logistics businesses.34 For incidents affecting Australian CI, the most common initial attack vectors were phishing (23%) and the exploitation of public-facing applications (21%).36 The Australian Government's 2023-2030 Cyber Security Strategy reinforces this focus, establishing "Protected critical infrastructure" as one of its six core "cyber shields" to defend the nation.37

### **2.3 The Australian Rail Industry Context (RISSB)**

The Rail Industry Safety and Standards Board's (RISSB) Australian Rail Network Cyber Security Strategy provides the foundational approach for the domestic rail sector.38 The strategy's central premise is the recognition that the increasing convergence of IT and OT systems in modern rail operations has significantly expanded the digital attack surface, making previously isolated control systems vulnerable to remote threats.38

The strategy is built upon three key directions: leveraging existing frameworks, taking organizational responsibility for cyber risk, and fostering collaborative information sharing across the industry.38 It outlines a practical, four-stage activity cycle for managing cyber risk: UNDERSTAND the risks, PROTECT the assets, DETECT anomalous behavior, and RESPOND to incidents to limit damage.38 This framework provides a clear, industry-endorsed pathway for QTMP stakeholders to build and mature their cybersecurity capabilities.

The QTMP project exists at the intersection of the most heavily targeted sectors identified in these global and national threat reports. The Torbanlea facility is a *manufacturing* plant, producing *transportation* assets that form a key part of Australia's *critical infrastructure*. This places it squarely in the crosshairs of a diverse range of threat actors. Furthermore, the threat is not from distinct, isolated groups but from a convergent ecosystem where motivations and TTPs overlap. State-sponsored actors are increasingly using ransomware-style disruptive tools, while the disruption caused by a financially motivated ransomware group against a critical rail project could align perfectly with a hostile nation-state's geopolitical objectives. This blended threat profile necessitates a defense strategy that is resilient against a wide range of TTPs, rather than one tailored to a single threat type.

## **3.0 Summary of Cyber Threat Scenarios**

This section provides a one-page summary for each of the six detailed cyber threat scenarios developed from the synthesized intelligence. These summaries are designed for use in workshops and strategic threat modeling sessions, offering a concise overview of each plausible attack before the in-depth analysis that follows.

### **3.1 Scenario 1 Summary: State-Sponsored Sabotage via IT/OT Convergence**

* **Threat Actor:** A highly sophisticated and persistent nation-state Advanced Persistent Threat (APT) group (e.g., China-nexus Volt Typhoon/Vanguard Panda) with a strategic motivation to pre-position on Western critical infrastructure for future disruptive operations.  
* **Attack Path:** The actor gains initial access to the corporate IT network of a primary contractor by exploiting a vulnerability in an internet-facing edge device. Using stealthy "living-off-the-land" techniques, they move laterally, harvest credentials, and pivot across the IT/OT boundary using a legitimate engineering jump-host. After a prolonged period of dormant reconnaissance within the OT network, they execute an attack during a time of heightened geopolitical tension.  
* **Targeted Systems:** The attack targets the core of the manufacturing and testing process, including the Supervisory Control and Data Acquisition (SCADA) systems controlling manufacturing robotics and the Communications-Based Train Control (CBTC) or interlocking systems on the facility's commissioning track.  
* **Impact:** The primary impact is physical sabotage and long-term disruption. Malicious commands cause damage to expensive manufacturing equipment and render the train testing infrastructure inoperable, leading to a complete halt in production and significant delays to the entire QTMP. The attack is designed for maximum strategic effect, not financial gain.

### **3.2 Scenario 2 Summary: Ransomware Attack via Third-Party Supply Chain Compromise**

* **Threat Actor:** A financially motivated cybercrime group, likely an affiliate of a prominent Ransomware-as-a-Service (RaaS) operation (e.g., LockBit, Akira), known for targeting manufacturing and critical infrastructure.  
* **Attack Path:** The attack originates not with a primary contractor, but with a smaller, less secure third-party supplier in the extensive QTMP supply chain (e.g., a provider of building management systems). The actor compromises this supplier and steals legitimate VPN credentials used to access the main construction network. From this trusted position, they pivot to shared cloud-based project management platforms (e.g., Autodesk Construction Cloud), exfiltrate sensitive project plans and financial data, and then deploy ransomware across the on-premises network of a major construction partner.  
* **Targeted Systems:** The initial target is a third-party supplier. The primary targets are the corporate IT network of a construction contractor (e.g., John Holland), their file servers, workstations, and cloud-hosted project data.  
* **Impact:** The attack is a double-extortion campaign. Encryption of key systems halts construction and project management activities, causing immediate and costly delays. The threat of leaking stolen proprietary data (project timelines, costs, designs) is used as leverage to force a multi-million-dollar ransom payment, leading to severe financial and reputational damage.

### **3.3 Scenario 3 Summary: Insider Threat Exploiting Physical and Digital Access**

* **Threat Actor:** A disgruntled or coerced contractor, or a negligent employee, with authorized physical and logical access to the Torbanlea Manufacturing Facility.  
* **Attack Path:** The insider uses their legitimate access badge to enter a restricted OT area. They connect a malicious USB device or personal laptop directly to the Human-Machine Interface (HMI) of a Programmable Logic Controller (PLC) on the production line. They then modify control logic parameters, causing a critical piece of machinery (e.g., a robotic welder) to operate outside of its specifications, leading to physical damage and production defects. In parallel, they may use saved credentials on a shared engineering workstation to access and exfiltrate sensitive quality control data or intellectual property.  
* **Targeted Systems:** Physical access controls, PLCs and HMIs on the manufacturing floor, and internal IT assets like shared workstations and file servers.  
* **Impact:** The primary impact is direct sabotage of the manufacturing process, resulting in damaged equipment, defective train components, and production halts. The theft of sensitive data represents a secondary impact, potentially for financial gain or to leak to competitors. The attack undermines trust in both physical and digital security controls.

### **3.4 Scenario 4 Summary: Disruption of Signaling Systems via Wireless Exploitation**

* **Threat Actor:** A technically proficient cybercriminal, hacktivist, or security researcher aiming to demonstrate capability or cause disruption.  
* **Attack Path:** The actor targets the wireless communications that underpin the modern signaling systems, such as Communications-Based Train Control (CBTC), used on the facility's internal test track and planned for the final rolling stock. By positioning themselves within radio range, they exploit known vulnerabilities in the WLAN protocol (e.g., weak encryption, lack of robust authentication) to conduct a man-in-the-middle (MITM) or denial-of-service (DoS) attack.  
* **Targeted Systems:** The primary target is the train-to-wayside wireless communication link of the CBTC system. This includes onboard radios, wayside access points, and the underlying communication protocols.  
* **Impact:** The attack disrupts the flow of critical control data between the train and the control center. A DoS attack could cause the train's safety system to engage emergency brakes, halting all testing operations. A more sophisticated MITM attack could potentially inject false data, though modern systems have safeguards against this. The primary impacts are operational disruption, delays to the train commissioning schedule, and an erosion of confidence in the safety and security of the new fleet's core technology.

### **3.5 Scenario 5 Summary: Industrial Espionage via Compromised Engineering Platforms**

* **Threat Actor:** A state-sponsored espionage group or a commercially motivated actor working for a competitor, focused on acquiring valuable intellectual property (IP). China-nexus groups are noted for targeting these sectors.  
* **Attack Path:** The actor launches a highly targeted spear-phishing campaign against engineers at a key design or construction partner (e.g., WSP, John Holland). The email contains a lure relevant to the project, tricking an employee into revealing their credentials for a cloud-based engineering platform like Autodesk Construction Cloud. Using these legitimate credentials, the actor gains access to the central repository for all project designs.  
* **Targeted Systems:** The primary target is the cloud-hosted Common Data Environment (CDE) containing all project-related intellectual property. This includes detailed 3D models (BIM/VDC), blueprints, proprietary manufacturing process documents from Hyundai Rotem, and technical specifications for the new trains.  
* **Impact:** The impact is not disruptive but strategic. The actor stealthily exfiltrates terabytes of sensitive design and manufacturing data over a prolonged period. This results in a catastrophic loss of intellectual property, eroding the competitive advantage of the contractors and providing a foreign competitor with a complete blueprint for Australia's next-generation passenger trains. The breach may go undetected for months or years.

### **3.6 Scenario 6 Summary: Large-Scale Service Disruption via Hacktivist DDoS Campaign**

* **Threat Actor:** An ideologically motivated hacktivist collective (e.g., a pro-Russian group like NoName057(16) or an environmental protest group) seeking to make a political statement and cause high-visibility disruption.  
* **Attack Path:** The group uses a globally distributed botnet, potentially comprised of volunteer-run devices, to launch a massive Distributed Denial-of-Service (DDoS) attack. The attack targets the public-facing digital infrastructure of the Queensland Department of Transport and Main Roads (TMR) and the broader South East Queensland rail network.  
* **Targeted Systems:** The attack focuses on publicly accessible websites (tmr.qld.gov.au), journey planners, mobile applications, and potentially the Application Programming Interfaces (APIs) that feed data to real-time Passenger Information Systems (PIS) at stations.  
* **Impact:** The attack does not directly impact the OT systems of the TMF or the operational rail network. However, it successfully cripples public-facing communication channels, preventing passengers from accessing timetables, buying tickets, or receiving service updates. This causes widespread public confusion, frustration, and a loss of confidence in the transport authority. The incident generates negative media attention and forces the TMR security team to divert critical resources to mitigate the DDoS attack, potentially leaving other systems less monitored.

## **4.0 In-Depth Threat Scenario Analysis**

### **4.1 Scenario 1: State-Sponsored Sabotage via IT/OT Convergence**

#### **Attack Narrative**

A state-sponsored Advanced Persistent Threat (APT) group, operating with the strategic objectives and tradecraft of an actor like **Volt Typhoon (also known as Vanguard Panda)**, initiates a campaign against the QTMP. This is not for immediate financial gain but as part of a broader, long-term effort to pre-position on Western critical infrastructure. The attack begins with the compromise of an internet-facing edge device, such as a VPN concentrator or firewall, at a regional office of either Downer Group or the Department of Transport and Main Roads (TMR). The actor exploits a known but unpatched vulnerability to gain an initial foothold.

Once inside the corporate IT network, the actor exclusively employs "living-off-the-land" (LOTL) techniques to evade detection. They use native Windows tools like PowerShell, Windows Management Instrumentation (WMI), and netsh to conduct reconnaissance, blending their activity with legitimate administrative traffic.40 Their first objective is to achieve domain dominance. They use tools like vssadmin to access and exfiltrate the Active Directory database (NTDS.dit), which is then taken offline to crack password hashes.41

With high-privilege credentials, the actor maps the network, identifying the critical jump-host or bastion server that engineers use to access the OT environment at the Torbanlea Manufacturing Facility. Using these stolen, valid credentials, they traverse the IT/OT boundary, bypassing security controls that may not enforce multi-factor authentication for what appears to be a legitimate connection. Once inside the OT network, the actor enters a long-term dormant phase, lasting for months. During this time, they passively collect information, identifying the SCADA systems that control the facility's manufacturing robotics and the interlocking systems governing the internal commissioning and test track.

At a time of heightened geopolitical tension between Australia and the actor's home nation, the group receives its activation order. They use their established access to issue malicious control commands directly to the Programmable Logic Controllers (PLCs) on the factory floor and the signaling network. These commands override safety interlocks, causing robotic arms to collide, damaging both themselves and train car bodies. Simultaneously, they manipulate the test track's signaling, creating a hazardous state that makes train commissioning impossible. The attack results in immediate physical damage and an indefinite halt to all production and testing activities.

#### **Threat Actor Profile: Nation-State APT (Volt Typhoon / Vanguard Panda)**

* **Attribution:** This profile models a People's Republic of China (PRC) state-sponsored actor.40 This is consistent with intelligence from security vendors like CrowdStrike, which reported a 150% increase in China-nexus intrusions in 2024, with a specific focus on the industrials, engineering, and transportation sectors.43  
* **Motivation:** The primary motivation is strategic pre-positioning, not espionage or financial gain. The goal is to establish persistent access to critical infrastructure to enable disruptive or destructive effects at a future time of the actor's choosing.41 This aligns with observed targeting of logistical networks, maritime operations, and air transportation, which are vital for military mobilization and economic stability.43  
* **TTPs:** Stealth and long-term persistence are the actor's hallmarks. They achieve this by heavily relying on **Living-off-the-Land (LOTL)** techniques, which use legitimate, built-in system tools to avoid detection by EDR and antivirus solutions.40 Initial access is gained by exploiting vulnerabilities in public-facing applications and edge devices. They use valid, stolen accounts for lateral movement and persistence. To further obscure their operations, they often route command-and-control (C2) traffic through a network of compromised small office/home office (SOHO) routers.42

#### **Targeted Technologies & Vulnerabilities**

* **Initial Access:** Known vulnerabilities in edge network devices such as VPNs and firewalls from major vendors like Fortinet, Cisco, and Palo Alto. The ACSC has highlighted the exploitation of public-facing applications as a top vector for CI incidents in Australia.34  
* **Internal IT Systems:** Microsoft Active Directory for credential harvesting. Native Windows tools including PowerShell, WMI, certutil, and netsh for execution and discovery.  
* **Operational Technology (OT) Systems:** The primary targets for impact are the industrial control systems within the TMF, including SCADA systems controlling the manufacturing process, Hyundai Rotem's proprietary Train Control Management System (TCMS), and the facility's interlocking and signaling systems.16 The attack would exploit vulnerabilities in unpatched PLCs, insecure proprietary protocols, or weak access controls between OT systems.

#### **Mapping to MITRE ATT\&CK for ICS**

| Tactic | Technique ID | Technique Name | Description |
| :---- | :---- | :---- | :---- |
| Initial Access | T0866 | Exploitation of Remote Services | The actor exploits a vulnerability in an internet-facing VPN to gain entry into the IT network. |
| Execution | T0853 | Scripting | PowerShell is used extensively for reconnaissance, lateral movement, and execution of commands. |
| Persistence | T0855 | Valid Accounts | Stolen administrator credentials are used to maintain access to both IT and OT networks. |
| Privilege Escalation | T0855 | Valid Accounts | The actor uses cracked domain administrator hashes to escalate privileges within the IT environment. |
| Discovery | T0861 | Point & Tag Identification | Once in the OT network, the actor identifies critical control system points and tags related to robotics and signaling. |
| Lateral Movement | T0867 | Remote Services | The actor moves from the IT network to the OT network through a legitimate remote access service (jump-host). |
| Impair Process Control | T0822 | Impair Process Control | The actor sends malicious commands to PLCs to disrupt the physical manufacturing and train testing processes. |
| Impact | T0810 | Damage to Property | The attack causes physical damage to robotic equipment and train components. |
| Impact | T0828 | Loss of Productivity and Revenue | The halt in production leads to massive financial losses and project delays. |

#### **Potential Impact Analysis**

* **Safety:** While the attack does not target an active passenger line, there is a high risk to the safety of employees within the TMF due to the unpredictable and malicious behavior of heavy industrial robotics. There is also a risk of a low-speed derailment or collision on the internal test track.  
* **Operations:** The impact is catastrophic, resulting in a complete and prolonged shutdown of all train manufacturing and commissioning activities. This would cause severe delays to the entire QTMP, jeopardizing its ability to support the Cross River Rail project and the 2032 Olympics timeline.  
* **Financial:** The financial costs would be exceptionally high, likely running into hundreds of millions of dollars. This includes the cost of repairing or replacing damaged robotic and signaling equipment, the costs associated with project delays and contractual penalties, and the expense of a full-scale incident response and network rebuild.

#### **Alignment with IEC 62443**

This attack scenario demonstrates a cascading failure to meet several of the Foundational Requirements (FRs) of the IEC 62443 standard:

* **FR 5 (Restricted Data Flow):** The most significant failure is the actor's ability to move laterally from the IT zone to the high-consequence OT zone. This indicates a failure to properly implement a secure "conduit" with adequate traffic filtering and monitoring between these two distinct security zones, a core principle of the standard.27  
* **FR 1 (Identification and Authentication Control) & FR 2 (Use Control):** The actor's use of valid, albeit stolen, credentials to access the OT network highlights weaknesses in authentication and authorization. A robust implementation would require separate, non-propagated credentials for the OT environment and mandatory multi-factor authentication for any access crossing the IT/OT boundary.  
* **FR 3 (System Integrity):** The final stage of the attack, where the actor modifies the behavior of the PLCs and control systems, is a direct violation of system integrity.  
* **FR 7 (Timed Event Response):** The actor's ability to remain undetected for months demonstrates a failure in timely detection and response capabilities, which this requirement is designed to ensure.

### **4.2 Scenario 2: Ransomware Attack via Third-Party Supply Chain Compromise**

#### **Attack Narrative**

A financially motivated cybercrime group, acting as an affiliate for a major Ransomware-as-a-Service (RaaS) platform like Akira or Play, identifies a small-to-medium-sized subcontractor as its initial target. This subcontractor provides a specialized service for the TMF, such as the Building Management System (BMS) or HVAC controls, and has been granted VPN access into the primary construction network managed by John Holland to monitor its systems.

The attackers gain access to the subcontractor's network, either through a phishing campaign that harvests credentials or by purchasing credentials from an initial access broker on the dark web. They discover the stored credentials for the VPN connection to the John Holland network and use this trusted channel to gain their initial foothold. Once inside the main construction network, they begin reconnaissance. They find that project teams have stored access credentials for shared cloud platforms, such as Autodesk Construction Cloud, in insecure locations like configuration files or internal wikis.

The attackers use these credentials to pivot to the cloud environment, where they begin exfiltrating terabytes of sensitive data, including detailed project plans, financial projections, employee data, and intellectual property related to the train designs. With the data secured, they pivot back to the on-premises John Holland network and deploy their ransomware payload. The ransomware spreads rapidly, encrypting critical project management servers, engineering workstations, and file shares.

The attack brings all construction and design work to an immediate halt. John Holland and Downer Group receive a ransom note demanding a multi-million-dollar payment in cryptocurrency. The note is accompanied by a sample of the exfiltrated data and a threat to publicly release the entire dataset if the ransom is not paid, creating a double-extortion crisis.

#### **Threat Actor Profile: Financially Motivated Cybercrime Group**

* **Attribution:** An affiliate of a professional RaaS operation. Groups like Akira, Play, and RansomHub have been identified as highly active against the transportation and manufacturing sectors.32 The RaaS model lowers the barrier to entry, allowing less sophisticated actors to leverage powerful malware and infrastructure.21  
* **Motivation:** The sole motivation is financial profit. The attack is structured around a double-extortion model: demanding payment for decryption keys to restore operations and a second payment to prevent the public leakage of stolen sensitive data.30 These groups are known to exploit regulatory compliance fears and the high cost of downtime to pressure victims into paying.21  
* **TTPs:** Initial access is often opportunistic and indirect. The 2025 Verizon DBIR highlights that breaches involving third parties doubled year-over-year, now accounting for 30% of all cases.19 Attackers frequently gain access via stolen credentials obtained through phishing or infostealer malware.19 Once inside, they are increasingly using "hands-on-keyboard" techniques, which are malware-free in the initial stages, to conduct reconnaissance and lateral movement before deploying the final ransomware payload.43

#### **Targeted Technologies & Vulnerabilities**

* **Initial Access:** Weak credential management, lack of MFA, or an unpatched VPN appliance at a third-party supplier.  
* **Internal Systems:** Shared network drives, internal collaboration sites (e.g., SharePoint), and cloud-based construction management platforms like Autodesk Construction Cloud.13 Corporate email and financial systems are also targets for data exfiltration.  
* **OT Systems:** While not the primary target for encryption, the Building Management System (BMS) could be compromised as part of the lateral movement, potentially impacting physical conditions at the facility. The main impact on OT is indirect, caused by the disruption of the IT systems needed to manage construction and engineering.

#### **Mapping to MITRE ATT\&CK for ICS**

| Tactic | Technique ID | Technique Name | Description |
| :---- | :---- | :---- | :---- |
| Initial Access | T0862 | Supply Chain Compromise | The actor gains access by compromising a trusted third-party supplier with legitimate network access. |
| Credential Access | T0855 | Valid Accounts | Stolen VPN and cloud platform credentials are used for initial access and lateral movement. |
| Collection | T0815 | Data from Information Repositories | The actor exfiltrates sensitive project files from on-premises servers and cloud storage. |
| Exfiltration | T0882 | Exfiltration Over C2 Channel | Large volumes of stolen data are transferred to actor-controlled infrastructure prior to encryption. |
| Impact | T0813 | Data Destruction | Ransomware encrypts files on servers and workstations, rendering them unusable. |
| Impact | T0885 | Inhibit Response Function | The ransomware may target and encrypt network-based backups to prevent easy recovery. |
| Impact | T0880 | Theft of Operational Information | The exfiltration of project plans, schedules, and designs constitutes theft of operational information. |

#### **Potential Impact Analysis**

* **Safety:** The direct safety impact is low. However, an encrypted BMS could lead to unsafe environmental conditions within the facility. The unavailability of safety documentation or procedures stored on encrypted servers could also pose a secondary risk.  
* **Operations:** The attack would cause a complete halt to all construction, engineering, and project management activities. This would lead to significant project delays, impacting the entire QTMP timeline.  
* **Financial:** The financial impact would be severe. It includes the potential cost of the ransom payment, the massive cost of business interruption and project downtime, regulatory fines for data breaches, and the expense of a large-scale incident response and recovery effort. IBM reports the average cost of a data breach in the transport sector is $4.18 million, a figure that would be dwarfed by the scale of this project disruption.47

#### **Alignment with IEC 62443**

This scenario exposes significant gaps in the implementation of a mature security program as defined by the IEC 62443 standard, particularly concerning the management of the wider ecosystem.

* **IEC 62443-2-1 (Security Program Requirements for Asset Owners):** The scenario highlights a failure to effectively manage the cybersecurity of the supply chain. A mature program would involve assessing the security posture of all third parties and enforcing baseline security requirements as a condition of network access.  
* **FR 1 (Identification and Authentication Control):** The use of stolen credentials indicates a weakness in authentication, particularly the lack of MFA on the third-party VPN connection.  
* **FR 5 (Restricted Data Flow):** The actor's ability to pivot from the on-premises construction network to a cloud platform and back indicates poor segmentation and a lack of effective data flow restrictions between different environments. The connection from the third-party supplier should have been a highly restricted conduit, allowing access only to the specific systems required for their function.

### **4.3 Scenario 3: Insider Threat Exploiting Physical and Digital Access**

#### **Attack Narrative**

A contractor working at the Torbanlea Manufacturing Facility becomes disgruntled due to a contract dispute or is coerced by an external party. Possessing an authorized access badge, the insider enters a restricted area on the manufacturing floor during a period of low supervision. They connect a personal laptop, loaded with PLC programming software and malicious logic, directly to the maintenance port of a PLC that controls a critical robotic welding station.

The insider modifies the control logic, subtly altering the welding parameters to be just outside of the acceptable tolerance. The change is not significant enough to trigger an immediate process alarm but is sufficient to create microscopic weaknesses in the welds. This act of sabotage is intended to cause latent defects that will only be discovered much later, potentially after the trains are in service, maximizing the reputational damage.

In a separate action, the insider uses a shared, kiosk-style engineering workstation on the factory floor. They find that a previous user had saved their domain credentials in the browser. Using these credentials, the insider logs into the corporate network, accesses a repository of quality control reports and proprietary manufacturing process documents, and exfiltrates them to a personal cloud storage account via a web browser. The goal is to leak this information to a competitor or a journalist to further damage the project's reputation.

#### **Threat Actor Profile: Malicious or Unwitting Insider**

* **Attribution:** A current or former employee or contractor with authorized access to the facility and its systems. The motivation could be personal grievance (e.g., termination, dispute), financial gain (coerced or paid by an external entity), or ideology.  
* **Motivation:** The primary motivation is sabotage and/or data theft. The goal is to cause direct harm to the project's operations, quality, and reputation. Unwitting insiders could also be manipulated through social engineering to unknowingly facilitate an attack.  
* **TTPs:** The key advantage of an insider is the bypass of external perimeter defenses. Their TTPs revolve around the abuse of legitimate access. This includes using their physical access privileges to reach sensitive OT equipment, exploiting weak digital access controls like shared credentials, and using common tools (USB drives, personal laptops, web browsers) for their attack, making their actions difficult to distinguish from normal activity.

#### **Targeted Technologies & Vulnerabilities**

* **Physical Security:** Exploitation of gaps in supervision or procedural controls that allow unauthorized connection of devices in secure areas.  
* **OT Systems:** Direct access to PLCs and HMIs on the manufacturing floor. The vulnerability is the unprotected physical maintenance port on the PLC.  
* **IT Systems:** Shared engineering workstations with weak credential hygiene (e.g., saved passwords). The vulnerability is a lack of strict use control and session management on shared assets.  
* **Data Repositories:** Internal file servers or SharePoint sites containing sensitive quality control and process documentation.

#### **Mapping to MITRE ATT\&CK for ICS**

| Tactic | Technique ID | Technique Name | Description |
| :---- | :---- | :---- | :---- |
| Initial Access | T0839 | Physical Access | The actor uses their authorized badge to physically access the OT environment and connect to a PLC. |
| Credential Access | T0855 | Valid Accounts | The actor uses credentials saved on a shared workstation to access the IT network. |
| Evasion | T0820 | Hide Artifacts | The actor may attempt to clear logs on the workstation or PLC to hide their activity. |
| Collection | T0807 | Data from Device | The actor exfiltrates quality control documents from an internal file server. |
| Inhibit Response Function | T0836 | Modify Parameter | The actor subtly alters welding parameters in the PLC logic to introduce latent defects. |
| Impact | T0848 | Spurious/Intermittent Operation | The modified parameters cause the robotic welder to operate incorrectly, impacting product quality. |
| Impact | T0880 | Theft of Operational Information | The exfiltration of proprietary process documents constitutes theft of critical operational information. |

#### **Potential Impact Analysis**

* **Safety:** High latent safety risk. The introduction of structural defects in the train car bodies could lead to catastrophic failures years later when the trains are in passenger service. This represents one of the most severe potential safety impacts.  
* **Operations:** The immediate operational impact may be low if the sabotage is not detected. However, if discovered, it would trigger a massive and costly quality control investigation, requiring the inspection of all potentially affected components and a halt in production.  
* **Financial:** Extremely high potential cost, especially if the defects are discovered after delivery, necessitating a fleet-wide recall and retrofitting. The theft and leak of IP would also cause significant commercial and reputational damage.

#### **Alignment with IEC 62443**

This scenario demonstrates the importance of applying security controls not just to external threats but also to internal risks.

* **FR 1 (Identification and Authentication Control) & FR 2 (Use Control):** The scenario highlights a failure in both. A shared workstation should not have saved credentials, and user sessions should be strictly controlled and logged. Physical port security on PLCs (e.g., locking maintenance ports) is a key aspect of Use Control.  
* **FR 3 (System Integrity):** The unauthorized modification of the PLC's logic is a direct breach of system integrity. File integrity monitoring and regular logic validation checks are required controls to mitigate this.  
* **IEC 62443-2-1 (Security Program):** A mature security program must include policies and procedures for managing insider risk, including background checks, security awareness training focused on insider threats, and robust offboarding processes that immediately revoke all physical and logical access.

### **4.4 Scenario 4: Disruption of Signaling Systems via Wireless Exploitation**

#### **Attack Narrative**

A technically skilled attacker, motivated by hacktivism or simply the challenge, targets the modern signaling systems of the QTMP trains. They focus on the Communications-Based Train Control (CBTC) system, which relies on continuous wireless communication between the train and wayside equipment to determine its precise location and enforce safe operating speeds.

The attacker positions themselves near the Torbanlea facility's outdoor test track. Using readily available hardware (like a software-defined radio) and open-source software, they begin to analyze the WLAN traffic used by the CBTC system. They discover that the system, while functional, uses an older Wi-Fi protocol with known vulnerabilities, such as weak encryption or insufficient authentication for management frames.48

The attacker launches a denial-of-service (DoS) attack by flooding the wireless spectrum with deauthentication frames. This attack spoofs the identity of the test train, repeatedly telling the wayside access point to disconnect it.48 The constant disconnections interrupt the flow of vital location and speed data to the train control center. The CBTC system's fail-safe mechanism correctly interprets this loss of communication as a hazardous condition and automatically applies the emergency brakes on the test train, bringing it to a sudden halt. The attacker can repeat this process at will, making it impossible for TMR and Downer to conduct any commissioning tests on the track, causing significant delays in the validation schedule for the new rolling stock.

#### **Threat Actor Profile: Sophisticated Cybercriminal / Hacktivist**

* **Attribution:** This could be an individual or small group with specialized knowledge of radio frequency (RF) and network protocols. Their motivation may not be financial but rather to cause disruption, expose vulnerabilities, or make a political statement.  
* **Motivation:** To demonstrate technical capability, disrupt a high-profile project, or protest the project on ideological grounds. The goal is to impact operations and generate publicity.  
* **TTPs:** The attack relies on technical exploitation of wireless protocols rather than compromising user credentials or networks. The actor uses specialized hardware and software to analyze and interfere with RF communications. Key TTPs include RF scanning, packet sniffing, and packet injection to execute attacks like jamming, deauthentication floods, or man-in-the-middle attacks.48

#### **Targeted Technologies & Vulnerabilities**

* **Primary Target:** The train-to-ground wireless communication link of the CBTC system. This is one of the most critical components of modern, high-capacity rail operations.50  
* **Technology:** Wireless Local Area Network (WLAN), often based on IEEE 802.11 standards, used for data transmission between the train and wayside equipment.  
* **Vulnerabilities:**  
  * Use of outdated or weakly implemented Wi-Fi security protocols (e.g., WEP, WPA) susceptible to cracking.  
  * Lack of authentication for management frames in older 802.11 standards, allowing for deauthentication/disassociation attacks.48  
  * Proprietary vendor protocols layered on top of standard wireless that may lack robust, built-in security measures.49  
  * Susceptibility to RF jamming, which can also cause a denial of service.

#### **Mapping to MITRE ATT\&CK for ICS**

| Tactic | Technique ID | Technique Name | Description |
| :---- | :---- | :---- | :---- |
| Initial Access | T0871 | Wireless Compromise | The actor gains access to the control system's communication channel by exploiting vulnerabilities in the wireless protocol. |
| Impair Process Control | T0822 | Impair Process Control | By disrupting communications, the actor prevents the control system from managing the train's movement, forcing a fail-safe stop. |
| Inhibit Response Function | T0859 | Wireless Jamming | While the narrative focuses on a protocol-level attack, RF jamming could achieve a similar disruptive effect on the wireless link. |
| Impact | T0826 | Loss of Availability | The signaling system becomes unavailable, halting all train operations on the affected track segment. |
| Impact | T0828 | Loss of Productivity and Revenue | The inability to test and commission new trains leads to project delays and associated costs. |

#### **Potential Impact Analysis**

* **Safety:** The direct safety impact is low in this specific scenario because the CBTC system is designed to fail-safe (i.e., stop the train) upon loss of communication. However, repeated, unexpected emergency braking could pose a risk to onboard personnel, and a more sophisticated attack that successfully injects malicious data could have severe safety consequences.  
* **Operations:** The attack causes a complete halt to all train testing and commissioning activities. This creates significant delays in the project schedule, as the new rolling stock cannot be validated for service.  
* **Financial:** The primary financial impact stems from project delays. There would also be costs associated with diagnosing the wireless issue, conducting a forensic investigation, and potentially retrofitting the entire fleet with more secure wireless hardware and protocols.

#### **Alignment with IEC 62443**

This scenario directly targets the communication channels that form the "conduits" in the IEC 62443 model.

* **FR 5 (Restricted Data Flow) & FR 6 (Timely Response to Events):** The attack demonstrates a failure to secure the conduit itself. A secure conduit requires not only encryption but also integrity checks and resilience against denial-of-service conditions. The inability to prevent or quickly mitigate the DoS attack shows a gap in these requirements.  
* **FR 3 (System Integrity):** While the logic of the train control system itself is not modified, the integrity of the data it relies upon is compromised (or made unavailable), leading to a failure state.  
* **IEC 62443-3-3 (System Security Requirements):** This part of the standard specifies detailed requirements for securing communications, including protecting against DoS attacks (SR 5.3) and ensuring communication integrity (SR 5.1). This attack would represent a failure to meet these specific system-level requirements.

### **4.5 Scenario 5: Industrial Espionage via Compromised Engineering Platforms**

#### **Attack Narrative**

An espionage-focused APT group, sponsored by a rival nation-state or a competing rolling stock manufacturer, targets the vast repository of intellectual property (IP) generated by the QTMP. The actor's goal is to steal the complete design and manufacturing blueprints for Australia's next-generation passenger trains.

The campaign begins with a highly targeted spear-phishing attack directed at a small number of senior engineers at John Holland and WSP, key partners in the design and construction of the facilities. The phishing emails are meticulously crafted, referencing specific, non-public details about the QTMP (gleaned from prior reconnaissance) to appear legitimate. The email contains a link to a malicious clone of a project-related portal, which harvests the engineers' corporate credentials, including their credentials for the Autodesk Construction Cloud platform.

Using the stolen, valid credentials, the actor logs into the project's central Common Data Environment (CDE). Because the access is authenticated and originates from a seemingly legitimate source, it does not trigger immediate alarms. Once inside, the actor has access to the project's "single source of truth," containing everything from initial architectural designs to detailed Building Information Models (BIM), Virtual Design and Construction (VDC) data, and, most critically, the proprietary train design specifications and manufacturing process documents from Hyundai Rotem and Downer.

Over several months, the actor engages in low-and-slow data exfiltration. They download gigabytes of sensitive data in small chunks during off-peak hours to avoid detection thresholds. The theft is not discovered until long after the data has been successfully exfiltrated and analyzed by the foreign competitor or intelligence agency.

#### **Threat Actor Profile: State-Sponsored or Corporate Espionage Group**

* **Attribution:** A sophisticated actor focused on intelligence gathering and IP theft. This could be a China-nexus APT, given their documented focus on targeting industrials, engineering, and technology sectors for economic advantage, as noted in the CrowdStrike 2025 Global Threat Report.43  
* **Motivation:** Economic and strategic advantage. By stealing the complete design and manufacturing IP, the actor's sponsor can replicate the technology, undercut the market, and gain insight into the capabilities and potential vulnerabilities of Australia's critical transport infrastructure.  
* **TTPs:** The attack is characterized by stealth, patience, and precision. Key TTPs include targeted spear-phishing for initial credential harvesting, use of valid accounts to bypass perimeter defenses, and slow, methodical exfiltration to remain below the radar of security monitoring tools. The focus is on avoiding detection entirely, rather than causing disruption.

#### **Targeted Technologies & Vulnerabilities**

* **Primary Target:** Cloud-hosted Software-as-a-Service (SaaS) platforms used for project management and digital engineering, such as Autodesk Construction Cloud.13 These platforms are a treasure trove of consolidated project IP.  
* **Initial Vector:** The human element is the primary vulnerability, exploited via a sophisticated spear-phishing campaign.  
* **Technology:** User credentials, single sign-on (SSO) systems, and the data repositories within the cloud platform itself. A lack of mandatory, phishing-resistant MFA for accessing these critical platforms is the key technical vulnerability.

#### **Mapping to MITRE ATT\&CK for ICS**

While the primary target is the IT and cloud environment containing engineering data, this data is fundamental to the OT process, making it a relevant scenario.

| Tactic | Technique ID | Technique Name | Description |
| :---- | :---- | :---- | :---- |
| Initial Access | T0865 | Spearphishing | The actor uses targeted emails to trick engineers into revealing their credentials. |
| Credential Access | T0855 | Valid Accounts | Stolen cloud platform credentials are used to gain access to the project's central data repository. |
| Discovery | T0816 | Data from Information Repositories | The actor explores the file structure of the cloud platform to identify the most valuable design and process documents. |
| Collection | T0807 | Data from Device | The actor stages and compresses large volumes of data for exfiltration. |
| Exfiltration | T0882 | Exfiltration Over C2 Channel | The actor slowly exfiltrates the stolen IP over an encrypted channel to their own infrastructure. |
| Impact | T0880 | Theft of Operational Information | The core of the attack is the theft of proprietary designs and manufacturing processes, which are critical operational information. |

#### **Potential Impact Analysis**

* **Safety & Operations:** There is no immediate impact on safety or physical operations. The attack is designed to be entirely passive and undetectable in the short term.  
* **Financial & Strategic:** The long-term impact is catastrophic. The loss of years of research, development, and design work represents a massive financial loss. It erodes the competitive advantage of Downer, Hyundai Rotem, and their partners. A foreign competitor gaining this IP could replicate the technology at a fraction of the cost, impacting future international sales. Furthermore, a foreign intelligence agency possessing these detailed schematics would have an invaluable resource for planning future cyber or physical attacks against the fleet.

#### **Alignment with IEC 62443**

This scenario primarily concerns the security of the IT and enterprise systems that support the OT environment, which falls under the scope of a holistic security program as defined in IEC 62443\.

* **FR 4 (Data Confidentiality):** The exfiltration of sensitive, proprietary data is a fundamental breach of confidentiality. Controls such as data loss prevention (DLP), encryption at rest and in transit, and robust access monitoring are required to meet this requirement.  
* **FR 1 (Identification and Authentication Control):** The success of the phishing attack underscores a weakness in authentication. Implementing phishing-resistant MFA would be a critical mitigating control, preventing the stolen credentials from being used successfully.  
* **IEC 62443-2-1 (Security Program):** This standard requires asset owners to establish a program that includes security awareness training. The failure of an employee to recognize a spear-phishing attempt points to a gap in the effectiveness of such training.

### **4.6 Scenario 6: Large-Scale Service Disruption via Hacktivist DDoS Campaign**

#### **Attack Narrative**

A pro-Russian hacktivist collective, such as **NoName057(16)**, decides to target Australian critical infrastructure as a protest against the Australian government's support for Ukraine. They identify the Queensland public transport network as a high-visibility target. Their goal is not to compromise systems or steal data, but to cause widespread, public-facing disruption to generate media attention and spread their political message.

Using their established "DDoSia" platform, which relies on a network of volunteer-run devices, the group launches a multi-vector Distributed Denial-of-Service (DDoS) attack.52 The attack simultaneously targets the main public websites of the Department of Transport and Main Roads (TMR), the TransLink journey planner, and the APIs that provide real-time data to mobile applications and Passenger Information Systems (PIS) at train stations across South East Queensland.

The volumetric attack overwhelms the network infrastructure of TMR's web hosting provider, rendering the websites and mobile apps inaccessible. Passengers are unable to check train schedules, plan their journeys, or receive updates on service status. The attack on the APIs causes the PIS displays at stations to freeze or show incorrect information, leading to confusion and frustration among commuters.

While the core operational rail network and the TMF itself remain completely unaffected, the public perception is one of chaos. The attack succeeds in its objective: it causes significant disruption to the public, erodes trust in the transport authority, and generates widespread media coverage, which the hacktivist group proudly publicizes on its Telegram channel.

#### **Threat Actor Profile: Ideologically Motivated Hacktivist Group (NoName057(16))**

* **Attribution:** A loosely organized, pro-Russian hacktivist collective known for conducting DDoS attacks against countries that support Ukraine.52  
* **Motivation:** Purely ideological and political. The group's stated goal is to disrupt the websites of nations they deem hostile to Russia's interests.52 The attacks are a form of digital protest and information warfare, designed to cause disruption and gain publicity for their cause.  
* **TTPs:** Their primary and almost exclusive TTP is the DDoS attack. They do not typically engage in network intrusion, data theft, or destructive attacks. They leverage a custom toolset (DDoSia) and a network of volunteers and sympathizers to generate the attack traffic. They are highly public about their activities, claiming responsibility for successful attacks on their Telegram channel.52

#### **Targeted Technologies & Vulnerabilities**

* **Primary Targets:** Public-facing web infrastructure, including web servers, Domain Name System (DNS) servers, and the APIs that serve real-time data to customer-facing applications.  
* **Technology:** Standard web protocols (HTTP/HTTPS), DNS, and the network infrastructure (routers, load balancers) of the hosting provider.  
* **Vulnerabilities:** Insufficient bandwidth or capacity to absorb large-scale volumetric attacks. Lack of a robust, cloud-based DDoS mitigation service. Application-layer vulnerabilities that can be exploited by more sophisticated Layer 7 DDoS attacks.

#### **Mapping to MITRE ATT\&CK for ICS**

This attack does not directly target the ICS/OT environment, but it impacts the broader operational ecosystem and is a recognized threat to the transport sector.

| Tactic | Technique ID | Technique Name | Description |
| :---- | :---- | :---- | :---- |
| Impact | T0814 | Denial of Service | The actor overwhelms public-facing web servers and APIs with a high volume of traffic, making them unavailable to legitimate users. |
| Impact | T0826 | Loss of Availability | Key passenger information services become unavailable, disrupting the customer experience. |
| Impact | T0880 | Theft of Operational Information | While not theft in the traditional sense, the disruption prevents the dissemination of real-time operational information to the public. |

#### **Potential Impact Analysis**

* **Safety & OT Operations:** There is no direct impact on the safety of train operations or the manufacturing processes at the TMF. The core control systems are isolated from the public internet and are not targeted.  
* **Public-Facing Operations:** The impact is high, causing a complete breakdown of public information channels. This leads to significant passenger inconvenience, confusion, and a severe loss of public trust and confidence in the transport authority.  
* **Financial:** The direct financial impact is relatively low, primarily consisting of the costs of engaging a DDoS mitigation service and the resources required for incident response. There is no data loss or system destruction to remediate. The primary damage is reputational.

#### **Alignment with IEC 62443**

While IEC 62443 is focused on the security of IACS, its principles of zoning can be applied to the broader enterprise. The public-facing web services should be located in a low-security zone, completely segregated from any corporate or operational networks.

* **FR 5 (Restricted Data Flow):** The success of this scenario relies on the assumption that these public systems are properly isolated. If the DDoS attack were to have a cascading effect on internal systems due to a poorly configured network architecture (e.g., shared resources between public and internal zones), it would represent a major failure of this foundational requirement.  
* **FR 7 (Timed Event Response):** This requirement focuses on maintaining essential functions during an attack. While the core essential function (running trains safely) is maintained, the essential function of communicating with the public is lost. A resilient architecture would include redundant communication channels and a pre-provisioned DDoS mitigation service to ensure this function can be restored in a timely manner.

## **5.0 Strategic Recommendations and Mitigation Pathways**

To address the multifaceted threats identified in this report, a strategic, defense-in-depth approach is required. The following recommendations are structured around the RISSB's cybersecurity activity cycle (UNDERSTAND, PROTECT, DETECT, RESPOND) and are grounded in the principles of the IEC 62443 standard.

### **5.1 UNDERSTAND: Enhance Threat Intelligence and Risk Management**

* **Implement a Comprehensive Supply Chain Risk Management Program:** The QTMP's most significant vulnerability is its complex, multi-tiered supply chain. TMR and Downer must establish a formal risk management program based on the principles of IEC 62443-2-4 (Requirements for IACS solution suppliers). This program should mandate that all partners and subcontractors—from major players like Hyundai Rotem and John Holland down to smaller suppliers—demonstrate compliance with a defined baseline of cybersecurity controls as a contractual obligation. Regular security assessments and audits of partners should be conducted to validate compliance.  
* **Establish a Continuous Threat Intelligence Function:** Proactively monitor for threats specific to the QTMP ecosystem. This should include continuous Open-Source Intelligence (OSINT) gathering and dark web monitoring for leaked credentials, mentions of project entities, or chatter indicating planned attacks. This intelligence should be used to inform risk assessments and prioritize defensive efforts.

### **5.2 PROTECT: Implement a Resilient, Defense-in-Depth Architecture**

* **Enforce Strict IT/OT Network Segmentation:** A foundational control is the logical and physical separation of the IT and OT networks, as prescribed by the IEC 62443 zones and conduits model.27 All data flows across this boundary must pass through a secure conduit (demilitarized zone or DMZ) with robust filtering, inspection, and monitoring. This control is the primary defense against scenarios like the state-sponsored sabotage attack (Scenario 1), preventing lateral movement from a compromised IT environment into the critical OT domain.  
* **Mandate Phishing-Resistant Multi-Factor Authentication (MFA):** Stolen credentials are a primary vector in multiple scenarios. Phishing-resistant MFA must be enforced for all remote access, all access to cloud services (especially engineering platforms like Autodesk), and critically, for any user or system traversing the IT/OT boundary. The SANS 2024 survey identified MFA for remote access as a key maturity indicator, now used by 75% of respondents.55  
* **Implement a Risk-Based OT Vulnerability Management Program:** Patching in OT environments is challenging due to operational constraints and certification requirements. A risk-based approach, as recommended by security firms like Dragos, should be adopted.57 Instead of relying solely on CVSS scores, vulnerabilities should be prioritized based on their exploitability within the TMF environment, their potential impact on safety and operations, and the availability of compensating controls.

### **5.3 DETECT: Achieve Visibility Across the Converged Environment**

* **Deploy OT-Specific Network Monitoring:** Traditional IT security tools are often blind to OT protocols and behaviors. An OT-native network monitoring solution should be deployed within the TMF's control network. This solution must be capable of deep packet inspection for rail-specific protocols (e.g., TCMS, signaling) and behavioral anomaly detection. This is the most effective way to identify the subtle "living-off-the-land" techniques used by advanced actors, as highlighted in Scenario 1\. The SANS 2024 survey shows a direct correlation between ICS network monitoring capabilities and faster incident detection times.55  
* **Unify Security Operations and Log Correlation:** Logs from all critical sources—IT networks, cloud platforms, OT systems, and physical access control systems—should be centralized in a Security Information and Event Management (SIEM) platform. A Security Operations Center (SOC) with specific training in OT incident analysis should monitor these correlated logs to detect patterns of activity, such as lateral movement across the IT/OT boundary or anomalous access by an insider.

### **5.4 RESPOND: Develop and Test an OT-Specific Incident Response Plan**

* **Develop a Dedicated OT Incident Response Plan (IRP):** An IT-centric IRP is insufficient for an OT incident. A dedicated OT IRP must be developed, as highlighted by the SANS 2024 survey, which found that only 56% of organizations have one.55 This plan must prioritize safety and the continuity of physical operations. It must define clear roles and responsibilities that include not just cybersecurity staff but also plant engineers, operations managers, and safety officers. Containment and eradication procedures must be carefully designed to avoid causing further disruption to sensitive control processes.  
* **Conduct Regular, Scenario-Based Tabletop Exercises:** The IRP must be tested regularly. Tabletop exercises should be conducted with all key stakeholders from across the QTMP consortium (TMR, Downer, John Holland, etc.). These exercises should be based on the plausible, detailed scenarios outlined in this report to test communication channels, decision-making processes, and technical response capabilities against realistic threats. This builds the "muscle memory" required to respond effectively during a real crisis.

## **6.0 Bibliography**

Australasian Railway Association. (n.d.). *Cyber Security*. ARA. Retrieved from [https://ara.net.au/org-category/cyber-security/](https://ara.net.au/org-category/cyber-security/)

Australian Government. (2023). *2023-2030 Australian Cyber Security Strategy*. Department of Home Affairs. Retrieved from [https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/strategy/2023-2030-australian-cyber-security-strategy](https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/strategy/2023-2030-australian-cyber-security-strategy)

Australian Signals Directorate. (n.d.). *Cyber security*. ASD. Retrieved from [https://www.asd.gov.au/about/what-we-do/cyber-security](https://www.asd.gov.au/about/what-we-do/cyber-security)

Australian Signals Directorate's Australian Cyber Security Centre. (2024). *Annual Cyber Threat Report 2023-2024*. ACSC. Retrieved from [https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2023-2024](https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2023-2024)

Australian Signals Directorate's Australian Cyber Security Centre. (2025). *Annual Cyber Threat Report 2024-2025*. ACSC. Retrieved from [https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2024-2025](https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2024-2025)

Bleeping Computer. (2023). *Auckland Transport authority hit by suspected ransomware attack*. Retrieved from [https://www.bleepingcomputer.com/news/security/auckland-transport-authority-hit-by-suspected-ransomware-attack/](https://www.bleepingcomputer.com/news/security/auckland-transport-authority-hit-by-suspected-ransomware-attack/)

Claroty. (2023). *The Global State of Industrial Cybersecurity 2023*. Retrieved from [https://claroty.com/resources/reports/the-global-state-of-industrial-cybersecurity-2023](https://claroty.com/resources/reports/the-global-state-of-industrial-cybersecurity-2023)

Claroty. (2025). *State of CPS Security: OT Exposures 2025*. Retrieved from [https://claroty.com/resources/reports/state-of-cps-security-ot-exposures-2025](https://claroty.com/resources/reports/state-of-cps-security-ot-exposures-2025)

CrowdStrike. (2025). *CrowdStrike 2025 Global Threat Report: Executive Summary*. Retrieved from [https://www.crowdstrike.com/en-us/resources/reports/global-threat-report-executive-summary-2025/](https://www.crowdstrike.com/en-us/resources/reports/global-threat-report-executive-summary-2025/)

Cyber Peace Institute. (n.d.). *Transportation*. Cyber Conflicts. Retrieved from [https://cyberconflicts.cyberpeaceinstitute.org/impact/sectors/transportation](https://cyberconflicts.cyberpeaceinstitute.org/impact/sectors/transportation)

Cybersecurity Dive. (2025). *Major railroad-signaling vulnerability could lead to train disruptions*. Retrieved from [https://www.cybersecuritydive.com/news/railroad-train-vulnerability-derail-brake-cisa-advisory/752940/](https://www.cybersecuritydive.com/news/railroad-train-vulnerability-derail-brake-cisa-advisory/752940/)

Cylus. (2022). *Rail Cybersecurity 2022: a Year in Review*. Retrieved from [https://www.cylus.com/resources/2022-rail-cybersecurity-at-a-glance](https://www.cylus.com/resources/2022-rail-cybersecurity-at-a-glance)

Department of Transport and Main Roads, Queensland Government. (n.d.). *Torbanlea train manufacturing facility*. Retrieved from [https://www.tmr.qld.gov.au/projects/torbanlea-manufacturing-facility](https://www.tmr.qld.gov.au/projects/torbanlea-manufacturing-facility)

Downer Group. (n.d.). *Queensland Train Manufacturing Program*. Retrieved from [https://www.downergroup.com/queensland-train-manufacturing-program](https://www.downergroup.com/queensland-train-manufacturing-program)

Dragos. (2025). *2025 OT Security Financial Risk Report*. Retrieved from [https://www.dragos.com/2025-ot-security-financial-risk-report](https://www.dragos.com/2025-ot-security-financial-risk-report)

Dragos. (n.d.). *The 2025 Dragos OT Cybersecurity Year in Review is coming soon*. Retrieved from [https://www.dragos.com/blog/the-2025-dragos-ot-cybersecurity-year-in-review-is-coming-soon](https://www.dragos.com/blog/the-2025-dragos-ot-cybersecurity-year-in-review-is-coming-soon)

DT Infrastructure. (n.d.). *Queensland Train Manufacturing Program*. Retrieved from [https://dtinfrastructure.com.au/queensland-train-manufacturing-program/](https://dtinfrastructure.com.au/queensland-train-manufacturing-program/)

ENISA. (2025). *ENISA Threat Landscape 2025*. Retrieved from [https://www.enisa.europa.eu/publications/enisa-threat-landscape-2025](https://www.enisa.europa.eu/publications/enisa-threat-landscape-2025)

GHD. (n.d.). *Getting on track with rail cybersecurity*. Retrieved from [https://www.ghd.com/en/insights/getting-on-track-with-rail-cybersecurity](https://www.ghd.com/en/insights/getting-on-track-with-rail-cybersecurity)

Help Net Security. (2025). *Attackers test the limits of railway cybersecurity*. Retrieved from [https://www.helpnetsecurity.com/2025/09/09/railway-systems-cybersecurity/](https://www.helpnetsecurity.com/2025/09/09/railway-systems-cybersecurity/)

IBM. (2025). *IBM X-Force 2025 Threat Intelligence Index*. Retrieved from [https://www.ibm.com/thought-leadership/institute-business-value/en-us/report/2025-threat-intelligence-index](https://www.ibm.com/thought-leadership/institute-business-value/en-us/report/2025-threat-intelligence-index)

Industrial Cyber. (2025). *ENISA 2025 Threat Landscape report highlights EU faces escalating hacktivist attacks and state-aligned cyber threats*. Retrieved from [https://industrialcyber.co/reports/enisa-2025-threat-landscape-report-highlights-eu-faces-escalating-hacktivist-attacks-and-state-aligned-cyber-threats/](https://industrialcyber.co/reports/enisa-2025-threat-landscape-report-highlights-eu-faces-escalating-hacktivist-attacks-and-state-aligned-cyber-threats/)

Industrial Cyber. (2024). *SANS Institute 2024 survey reveals progress and gaps in ICS/OT cybersecurity for critical infrastructure*. Retrieved from [https://industrialcyber.co/threats-attacks/sans-institute-2024-survey-reveals-progress-and-gaps-in-ics-ot-cybersecurity-for-critical-infrastructure/](https://industrialcyber.co/threats-attacks/sans-institute-2024-survey-reveals-progress-and-gaps-in-ics-ot-cybersecurity-for-critical-infrastructure/)

Infrastructure Pipeline. (n.d.). *Queensland Train Manufacturing Program*. Retrieved from [https://infrastructurepipeline.org/project/queensland-rollingstock-expansion-program](https://infrastructurepipeline.org/project/queensland-rollingstock-expansion-program)

Kaspersky ICS CERT. (n.d.). *Reports*. Retrieved from [https://ics-cert.kaspersky.com/publications/reports/](https://ics-cert.kaspersky.com/publications/reports/)

Mandiant. (2025). *M-Trends 2025 Report*. Retrieved from [https://services.google.com/fh/files/misc/m-trends-2025-en.pdf](https://services.google.com/fh/files/misc/m-trends-2025-en.pdf)

MITRE. (n.d.). *Mitigations for ICS*. MITRE ATT\&CK®. Retrieved from [https://attack.mitre.org/mitigations/ics/](https://attack.mitre.org/mitigations/ics/)

Nozomi Networks. (n.d.). *Securing Critical Rail Networks*. Retrieved from [https://www.nozominetworks.com/blog/securing-critical-rail-networks](https://www.nozominetworks.com/blog/securing-critical-rail-networks)

Queensland Government. (2023). *Major construction starts on new train manufacturing facility*. Retrieved from [https://statements.qld.gov.au/statements/99209](https://statements.qld.gov.au/statements/99209)

Rail Industry Safety and Standards Board. (2019). *Australian Rail Network Cyber Security Strategy*. RISSB. Retrieved from [https://www.rissb.com.au/wp-content/uploads/2019/05/2021\_04\_2019\_05\_Cyber-Security-Strategy.pdf](https://www.rissb.com.au/wp-content/uploads/2019/05/2021_04_2019_05_Cyber-Security-Strategy.pdf)

RNZ. (2023). *AT cyber attacks pose no risk for development of NZ-wide ticketing system \- authorities*. Retrieved from [https://www.rnz.co.nz/news/national/500248/at-cyber-attacks-pose-no-risk-for-development-of-nz-wide-ticketing-system-authorities](https://www.rnz.co.nz/news/national/500248/at-cyber-attacks-pose-no-risk-for-development-of-nz-wide-ticketing-system-authorities)

Security Affairs. (2025). *Reading the ENISA Threat Landscape 2025 report*. Retrieved from [https://securityaffairs.com/182978/security/reading-the-enisa-threat-landscape-2025-report.html](https://securityaffairs.com/182978/security/reading-the-enisa-threat-landscape-2025-report.html)

TakePoint. (n.d.). *Top Industrial Cyber-Attacks Mapped to MITRE ATT\&CK Techniques & IEC 62443 Controls*. Retrieved from [https://takepoint.co/research/top-industrial-cyber-attacks-mapped-to-mitre-attck-techniques-iec-62443-controls/](https://takepoint.co/research/top-industrial-cyber-attacks-mapped-to-mitre-attck-techniques-iec-62443-controls/)

Turner & Townsend. (n.d.). *Queensland Train Manufacturing Program, Australia*. Retrieved from [https://www.turnerandtownsend.com/outcomes/queensland-train-manufacturing-program-australia/](https://www.turnerandtownsend.com/outcomes/queensland-train-manufacturing-program-australia/)

TXOne Networks. (n.d.). *Railway Cybersecurity: A Look at Potential Threats*. Retrieved from [https://www.txone.com/blog/potential-threats-to-railway-industry/](https://www.txone.com/blog/potential-threats-to-railway-industry/)

Verizon. (2025). *2025 Data Breach Investigations Report*. Retrieved from multiple sources.

WSP. (n.d.). *Queensland Train Manufacturing Program*. Retrieved from [https://www.wsp.com/en-au/projects/queensland-train-manufacturing-program](https://www.wsp.com/en-au/projects/queensland-train-manufacturing-program)

#### **Works cited**

1. Torbanlea manufacturing facility | Department of Transport and Main ..., accessed October 28, 2025, [https://www.tmr.qld.gov.au/projects/torbanlea-manufacturing-facility](https://www.tmr.qld.gov.au/projects/torbanlea-manufacturing-facility)  
2. Queensland Train Manufacturing Program \- Downer Group, accessed October 28, 2025, [https://www.downergroup.com/queensland-train-manufacturing-program](https://www.downergroup.com/queensland-train-manufacturing-program)  
3. Queensland Train Manufacturing Program \- WSP, accessed October 28, 2025, [https://www.wsp.com/en-au/projects/queensland-train-manufacturing-program](https://www.wsp.com/en-au/projects/queensland-train-manufacturing-program)  
4. Queensland Train Manufacturing Program Fact Sheet, accessed October 28, 2025, [https://www.msq.qld.gov.au/tmr\_site\_msqinternet/\_/media/projects/q/queensland-train-manufacturing-program/queensland-train-manufacturing-program-factsheet.pdf](https://www.msq.qld.gov.au/tmr_site_msqinternet/_/media/projects/q/queensland-train-manufacturing-program/queensland-train-manufacturing-program-factsheet.pdf)  
5. Queensland Train Manufacturing Program \- DT Infrastructure, accessed October 28, 2025, [https://dtinfrastructure.com.au/queensland-train-manufacturing-program/](https://dtinfrastructure.com.au/queensland-train-manufacturing-program/)  
6. Qld drives rail expansion with $9.5B Train Manufacturing Program, accessed October 28, 2025, [https://www.australianmanufacturing.com.au/qld-drives-rail-expansion-with-9-5b-train-manufacturing-program/](https://www.australianmanufacturing.com.au/qld-drives-rail-expansion-with-9-5b-train-manufacturing-program/)  
7. Queensland Train Manufacturing Program, Australia | Turner & Townsend, accessed October 28, 2025, [https://www.turnerandtownsend.com/outcomes/queensland-train-manufacturing-program-australia/](https://www.turnerandtownsend.com/outcomes/queensland-train-manufacturing-program-australia/)  
8. Queensland Train Manufacturing Program \- AWS, accessed October 28, 2025, [https://hdp-au-prod-app-qldtmr-yoursay-files.s3.ap-southeast-2.amazonaws.com/9817/4365/7924/QTMP\_Fact-Sheet\_April\_2025\_Approved.pdf](https://hdp-au-prod-app-qldtmr-yoursay-files.s3.ap-southeast-2.amazonaws.com/9817/4365/7924/QTMP_Fact-Sheet_April_2025_Approved.pdf)  
9. Queensland Train Manufacturing Program brings more investment to Maryborough \- Ministerial Media Statements, accessed October 28, 2025, [https://statements.qld.gov.au/statements/99209](https://statements.qld.gov.au/statements/99209)  
10. Queensland Train Manufacturing Program \- Infrastructure Pipeline, accessed October 28, 2025, [https://infrastructurepipeline.org/project/queensland-rollingstock-expansion-program](https://infrastructurepipeline.org/project/queensland-rollingstock-expansion-program)  
11. Downer Group case study \- Crayon, accessed October 28, 2025, [https://www.crayon.com/resources/case-studies/downer-group/](https://www.crayon.com/resources/case-studies/downer-group/)  
12. Downer Group Software Purchases and Digital Transformation Initiatives, accessed October 28, 2025, [https://www.appsruntheworld.com/customers-database/customers/view/downer-group-australia](https://www.appsruntheworld.com/customers-database/customers/view/downer-group-australia)  
13. John Holland Group Partners with Autodesk for Digital Innovation, accessed October 28, 2025, [https://www.autodesk.com/customer-stories/john-holland-group-and-autodesk-digital-innovation-story](https://www.autodesk.com/customer-stories/john-holland-group-and-autodesk-digital-innovation-story)  
14. How generative AI is accelerating digital transformation in Australia's construction, engineering and legal industries \- Microsoft News, accessed October 28, 2025, [https://news.microsoft.com/en-au/features/how-generative-ai-is-accelerating-digital-transformation-in-australias-construction-engineering-and-legal-industries/](https://news.microsoft.com/en-au/features/how-generative-ai-is-accelerating-digital-transformation-in-australias-construction-engineering-and-legal-industries/)  
15. Hyundai Rotem Company Overview, Contact Details & Competitors | LeadIQ, accessed October 28, 2025, [https://leadiq.com/c/hyundai-rotem/5f9fe46d4133a8a89a272338](https://leadiq.com/c/hyundai-rotem/5f9fe46d4133a8a89a272338)  
16. Hyundai Rotem's In-House Developed Total Signaling System ..., accessed October 28, 2025, [https://tech.hyundai-rotem.com/en/hyundai-rotems-in-house-developed-total-signaling-system-solution-drives-k-rails-global-expansion/](https://tech.hyundai-rotem.com/en/hyundai-rotems-in-house-developed-total-signaling-system-solution-drives-k-rails-global-expansion/)  
17. EMU900 series \- Wikipedia, accessed October 28, 2025, [https://en.wikipedia.org/wiki/EMU900\_series](https://en.wikipedia.org/wiki/EMU900_series)  
18. Digital transformation of trains using IoT and ICT technologies \- Hyundai Rotem TECH, accessed October 28, 2025, [https://tech.hyundai-rotem.com/en/digital-transformation-of-trains-using-iot-and-ict-technologies/](https://tech.hyundai-rotem.com/en/digital-transformation-of-trains-using-iot-and-ict-technologies/)  
19. 2025 Verizon Data Breach Investigations Report \- Keepnet Labs, accessed October 28, 2025, [https://keepnetlabs.com/blog/2025-verizon-data-breach-investigations-report](https://keepnetlabs.com/blog/2025-verizon-data-breach-investigations-report)  
20. Breaking Down the 2025 Verizon Data Breach Investigations Report \- SpyCloud, accessed October 28, 2025, [https://spycloud.com/blog/verizon-2025-data-breach-report-insights/](https://spycloud.com/blog/verizon-2025-data-breach-report-insights/)  
21. ENISA THREAT LANDSCAPE 2025 \- European Union, accessed October 28, 2025, [https://www.enisa.europa.eu/sites/default/files/2025-10/ENISA%20Threat%20Landscape%202025.pdf](https://www.enisa.europa.eu/sites/default/files/2025-10/ENISA%20Threat%20Landscape%202025.pdf)  
22. ENISA THREAT LANDSCAPE 2025 \- European Union, accessed October 28, 2025, [https://www.enisa.europa.eu/sites/default/files/2025-10/ENISA%20Threat%20Landscape%202025\_0.pdf](https://www.enisa.europa.eu/sites/default/files/2025-10/ENISA%20Threat%20Landscape%202025_0.pdf)  
23. MITRE ATT\&CK Applications in Cybersecurity and The Way Forward \- arXiv, accessed October 28, 2025, [https://arxiv.org/html/2502.10825v1](https://arxiv.org/html/2502.10825v1)  
24. Threat-based Security Controls to Protect Industrial Control Systems \- arXiv, accessed October 28, 2025, [https://arxiv.org/html/2501.13268v1](https://arxiv.org/html/2501.13268v1)  
25. Top Industrial Cyber-Attacks Mapped to MITRE ATT\&CK Techniques ..., accessed October 28, 2025, [https://takepoint.co/research/top-industrial-cyber-attacks-mapped-to-mitre-attck-techniques-iec-62443-controls/](https://takepoint.co/research/top-industrial-cyber-attacks-mapped-to-mitre-attck-techniques-iec-62443-controls/)  
26. Securing Rail Networks: Cyber Risk Scenarios & Defense Strategies, accessed October 28, 2025, [https://www.nozominetworks.com/blog/securing-critical-rail-networks](https://www.nozominetworks.com/blog/securing-critical-rail-networks)  
27. ICS Mitigations \- MITRE ATT\&CK®, accessed October 28, 2025, [https://attack.mitre.org/mitigations/ics/](https://attack.mitre.org/mitigations/ics/)  
28. How does the MITRE ATT\&CK framework align with Cyber PHA? \- YouTube, accessed October 28, 2025, [https://www.youtube.com/watch?v=qgaFeM3QfbM](https://www.youtube.com/watch?v=qgaFeM3QfbM)  
29. ENISA Threat Landscape 2025 | ENISA, accessed October 28, 2025, [https://www.enisa.europa.eu/publications/enisa-threat-landscape-2025](https://www.enisa.europa.eu/publications/enisa-threat-landscape-2025)  
30. Reading the ENISA Threat Landscape 2025 report \- Security Affairs, accessed October 28, 2025, [https://securityaffairs.com/182978/security/reading-the-enisa-threat-landscape-2025-report.html](https://securityaffairs.com/182978/security/reading-the-enisa-threat-landscape-2025-report.html)  
31. Threat Landscape | ENISA \- European Union, accessed October 28, 2025, [https://www.enisa.europa.eu/topics/cyber-threats/threat-landscape](https://www.enisa.europa.eu/topics/cyber-threats/threat-landscape)  
32. ENISA 2025 Threat Landscape report highlights EU faces escalating hacktivist attacks and state-aligned cyber threats \- Industrial Cyber, accessed October 28, 2025, [https://industrialcyber.co/reports/enisa-2025-threat-landscape-report-highlights-eu-faces-escalating-hacktivist-attacks-and-state-aligned-cyber-threats/](https://industrialcyber.co/reports/enisa-2025-threat-landscape-report-highlights-eu-faces-escalating-hacktivist-attacks-and-state-aligned-cyber-threats/)  
33. EU consistently targeted by diverse yet convergent threat groups \- ENISA \- European Union, accessed October 28, 2025, [https://www.enisa.europa.eu/news/etl-2025-eu-consistently-targeted-by-diverse-yet-convergent-threat-groups](https://www.enisa.europa.eu/news/etl-2025-eu-consistently-targeted-by-diverse-yet-convergent-threat-groups)  
34. Annual Cyber Threat Report 2024-2025 | Cyber.gov.au, accessed October 28, 2025, [https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2024-2025](https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2024-2025)  
35. ACSC reports surge in cyberattacks targeting Australia's critical infrastructure, focus shifts to building resilience \- Industrial Cyber, accessed October 28, 2025, [https://industrialcyber.co/reports/acsc-reports-surge-in-cyberattacks-targeting-australias-critical-infrastructure-focus-shifts-to-building-resilience/](https://industrialcyber.co/reports/acsc-reports-surge-in-cyberattacks-targeting-australias-critical-infrastructure-focus-shifts-to-building-resilience/)  
36. Annual Cyber Threat Report 2023-2024 | Cyber.gov.au, accessed October 28, 2025, [https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2023-2024](https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2023-2024)  
37. 2023-2030 Australian Cyber Security Strategy \- Department of Home Affairs, accessed October 28, 2025, [https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/strategy/2023-2030-australian-cyber-security-strategy](https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/strategy/2023-2030-australian-cyber-security-strategy)  
38. AUSTRALIAN RAIL NETWORK CYBER SECURITY ... \- RISSB's, accessed October 28, 2025, [https://www.rissb.com.au/wp-content/uploads/2019/05/2021\_04\_2019\_05\_Cyber-Security-Strategy.pdf](https://www.rissb.com.au/wp-content/uploads/2019/05/2021_04_2019_05_Cyber-Security-Strategy.pdf)  
39. Securing a digital railway: Cyber security in the era of digital rail \- Rail Express, accessed October 28, 2025, [https://www.railexpress.com.au/securing-digital-railway-cyber-security-era-of-digital-rail/](https://www.railexpress.com.au/securing-digital-railway-cyber-security-era-of-digital-rail/)  
40. Volt Typhoon Explained: Living Off the Land Tactics for Cyber Espionage \- Picus Security, accessed October 28, 2025, [https://www.picussecurity.com/resource/blog/volt-typhoon-living-off-the-land-cyber-espionage](https://www.picussecurity.com/resource/blog/volt-typhoon-living-off-the-land-cyber-espionage)  
41. PRC State-Sponsored Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure | CISA, accessed October 28, 2025, [https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a](https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a)  
42. People's Republic of China State-Sponsored Cyber Actor Living off the Land to Evade Detection | CISA, accessed October 28, 2025, [https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-144a](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-144a)  
43. Five Big Takeaways From CrowdStrike's 2025 Threat Report \- CRN, accessed October 28, 2025, [https://www.crn.com/news/security/2025/five-big-takeaways-from-crowdstrike-s-2025-threat-report](https://www.crn.com/news/security/2025/five-big-takeaways-from-crowdstrike-s-2025-threat-report)  
44. Dark Reading: Security Tech That Can Make a Difference During an Attack | MITRE, accessed October 28, 2025, [https://www.mitre.org/news-insights/media-coverage/dark-reading-security-tech-can-make-difference-during-attack](https://www.mitre.org/news-insights/media-coverage/dark-reading-security-tech-can-make-difference-during-attack)  
45. Railway Cybersecurity: a Look at Potential Threats | TXOne Networks, accessed October 28, 2025, [https://www.txone.com/blog/potential-threats-to-railway-industry/](https://www.txone.com/blog/potential-threats-to-railway-industry/)  
46. Global Logistics & Transportation Threat Landscape Report 2025 ..., accessed October 28, 2025, [https://socradar.io/resources/industry-reports/global-logistics-transportation-threat-landscape-report-2025/](https://socradar.io/resources/industry-reports/global-logistics-transportation-threat-landscape-report-2025/)  
47. Cybersecurity in transportation and logistics: inside the sector's risks \- Eye Security, accessed October 28, 2025, [https://www.eye.security/blog/cybersecurity-in-transportation-and-logistics-inside-the-sectors-risks](https://www.eye.security/blog/cybersecurity-in-transportation-and-logistics-inside-the-sectors-risks)  
48. CBTC: Vulnerabilities of Communication-Based Train Control Architecture, accessed October 28, 2025, [https://www.txone.com/blog/communication-based-train-control-architecture-and-its-attack-aspects/](https://www.txone.com/blog/communication-based-train-control-architecture-and-its-attack-aspects/)  
49. 7 Reasons Why CBTC Systems Need Cybersecurity Solutions \- Cylus, accessed October 28, 2025, [https://www.cylus.com/post/7-reasons-why-cbtc-systems-need-cybersecurity-solutions](https://www.cylus.com/post/7-reasons-why-cbtc-systems-need-cybersecurity-solutions)  
50. CBTC-Based Signaling System: Challenges, Solutions, Expectations \- psa.inc, accessed October 28, 2025, [https://www.psa.inc/company/news/cbtc-based-signaling-system-challenges-solutions-expectations-/](https://www.psa.inc/company/news/cbtc-based-signaling-system-challenges-solutions-expectations-/)  
51. Securing Communication-Based Train Control (CBTC) \- Cylus, accessed October 28, 2025, [https://www.cylus.com/cbtc](https://www.cylus.com/cbtc)  
52. NetSecurity Threat Report: NoName057(16) Pro-Russian Hacktivist Group, accessed October 28, 2025, [https://www.netsecurity.com/netsecurity-threat-report-noname05716-pro-russian-hacktivist-group/](https://www.netsecurity.com/netsecurity-threat-report-noname05716-pro-russian-hacktivist-group/)  
53. Global operation targets NoName057(16) pro-Russian cybercrime network \- The offenders targeted Ukraine and supporting countries, including many EU Member States | Europol, accessed October 28, 2025, [https://www.europol.europa.eu/media-press/newsroom/news/global-operation-targets-noname05716-pro-russian-cybercrime-network](https://www.europol.europa.eu/media-press/newsroom/news/global-operation-targets-noname05716-pro-russian-cybercrime-network)  
54. Noname057(16) \- Wikipedia, accessed October 28, 2025, [https://en.wikipedia.org/wiki/Noname057(16)](https://en.wikipedia.org/wiki/Noname057\(16\))  
55. The 2024 State of ICS/OT Cybersecurity: Our Past and Our Future | SANS Institute, accessed October 28, 2025, [https://www.sans.org/blog/the-2024-state-of-ics-ot-cybersecurity-our-past-and-our-future](https://www.sans.org/blog/the-2024-state-of-ics-ot-cybersecurity-our-past-and-our-future)  
56. SANS 2024 State of ICS/OT Cybersecurity, accessed October 28, 2025, [https://www.aftana.ir/images/docs/files/000022/nf00022599-1.pdf](https://www.aftana.ir/images/docs/files/000022/nf00022599-1.pdf)  
57. The 2025 Dragos OT Cybersecurity Year in Review is Coming Soon, accessed October 28, 2025, [https://www.dragos.com/blog/the-2025-dragos-ot-cybersecurity-year-in-review-is-coming-soon](https://www.dragos.com/blog/the-2025-dragos-ot-cybersecurity-year-in-review-is-coming-soon)  
58. SANS Institute 2024 survey reveals progress and gaps in ICS/OT ..., accessed October 28, 2025, [https://industrialcyber.co/threats-attacks/sans-institute-2024-survey-reveals-progress-and-gaps-in-ics-ot-cybersecurity-for-critical-infrastructure/](https://industrialcyber.co/threats-attacks/sans-institute-2024-survey-reveals-progress-and-gaps-in-ics-ot-cybersecurity-for-critical-infrastructure/)  
59. 4 Findings from SANS ICS Cyber Report | ICS Rapid Response \#1 \- YouTube, accessed October 28, 2025, [https://www.youtube.com/shorts/USVXjOalBpg](https://www.youtube.com/shorts/USVXjOalBpg)