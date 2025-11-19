---
title: "MITRE ATT&CK: The Complete Guide | Splunk"
source: "https://www.splunk.com/en_us/blog/learn/mitre-attack.html"
author:
  - "[[Splunk]]"
published:
created: 2025-03-16
description: "Threat actions are always one step ahead. Get ahead of them with the great information in MITRE ATT&CK, a go-to for all security pros. Get the full story here."
tags:
  - "clippings"
---
Our cyber adversaries are always staying one step ahead. Threat actors love nothing more than trying out new tactics and techniques to attack targets, achieving their malicious objectives.

Today, anyone is susceptible to cyber threats at practically any moment. MITRE ATT&CK is a framework that serves as a guiding light— it helps you assess your existing security measures and enhance device and endpoint security mechanisms against these evolving cyber threats.

This article explains the definition and history of MITRE ATT&CK while providing an overview of its matrices and details the components of each matrix. We’ll also, of course, peek at the various use cases of the ATT&CK framework.

## What is MITRE ATT&CK?

MITRE ATT&CK is a free, comprehensive collection of [tactics, techniques and procedures](https://www.splunk.com/en_us/blog/learn/ttp-tactics-techniques-procedures.html) (TTPs) that attackers use in the real world. This information is not theoretical: instead, it is based on TTPs that threat actors have actually used in attacks.

![](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2023/09/mitre-attack1.png)This framework is maintained by [The MITRE Corporation](https://www.mitre.org/who-we-are/our-story), a non-profit organization with decades of history that today supports industries, governments and academia. The name “MITRE ATT&CK” is a mix of the organization’s name and the shorthand for Adversarial Tactics, Techniques and Common Knowledge.

MITRE ATT&CK aims to help [craft distinct threat models](https://www.splunk.com/en_us/blog/learn/threat-modeling.html). It approaches various sectors, including businesses, government, and cybersecurity services. MITRE advises attack techniques for adversaries' tactics and provides techniques to detect and eliminate them. The matrices, tactics, and techniques described by the  MITRE ATT&CK knowledge base are relevant to mobile, enterprise, and Industrial Control Systems (ICS).

### History of MITRE ATT&CK

The MITRE Corporation initiated the ATT&CK project in 2013 to capture adversarial behavior [after you’ve been compromised](https://www.splunk.com/en_us/blog/learn/ioc-indicators-of-compromise.html). In 2015, MITRE made the ATT&CK matrix publicly available with tactics and techniques for enterprise systems, especially Windows. 

Over the next few years, the project expanded to cover macOS, Linux, and cloud environments. In 2019, the collection was expanded to include tactics and techniques metrics for Industrial Control Systems (ICS). MITRE also introduced ATT&CK for Mobile, covering iOS and Android operating systems.

Today, the MITRE ATT&CK framework continues to evolve with new techniques and updates to existing ones — all based on the latest research and intelligence. 

## The ATT&CK Framework Matrices

The MITRE ATT&CK framework is currently comprised of three ATT&CK matrices:

- Enterprise
- Mobile
- Industrial Control Systems (ICS)

Each matrix is organized into columns, consisting of tactics [used by adversaries](https://www.splunk.com/en_us/blog/learn/threat-actors.html). The matrix rows under each tactic provide a set of related techniques with sub-techniques depending on their nature. The result is that each matrix does not look like a real matrix. Rather, it looks like an organizational chart with sub-levels or hierarchies of different elements.

On the website, [you can see a concise version](https://attack.mitre.org/) of each matrix and expand it to reveal the sub-techniques of each technique.  Here’s a snapshot of how the ATT&CK Matrix for Enterprise looks:

![](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2023/09/mitre-attack2.png)

## Components of the ATT&CK matrix

Each matrix has three major components: tactics, techniques, and sub-techniques. The collection is organized so that every tactic, technique, and sub-technique has a unique id. 

### Tactics

A tactic is the reason behind the techniques or sub-techniques that an attacker chooses. In other words, why will the attacker use a particular technique on the compromised system?  Here’s a couple examples:

- In the **defense evasion tactic**, the goal of the attacker is to somehow hide from being detected.
- In the **credential access tactic**, the adversaries’ goal is to steal credential information like usernames and passwords to gain access to systems.

The enterprise and mobile matrices are comprised of 14 tactics, while the ICS matrix describes 12. Many tactics are common to all three environments — the initial access, execution, lateral movement, and impact techniques are common across all three matrices.

Visually, the framework displays the number of techniques under each tactic, while each technique displays the number of associated sub-techniques. As of this writing, there are 14 total tactics in the Enterprise matrix:

1. Reconnaissance: TA0043 (10 techniques)
2. Resource Development: TA0042 (8 techniques)
3. Initial Access: TA0001 (9 techniques)
4. Execution: TA0002 (14 techniques)
5. Persistence: TA0003 (19 techniques)
6. Privilege Escalation: TA0004 (13 techniques)
7. Defense Evasion: TA0005 (42 techniques)
8. Credential Access: TA0006 (17 techniques)
9. Discovery: TA0007 (31 techniques)
10. Lateral Movement: TA0008 (9 techniques)
11. Collection: TA0009 (17 techniques)
12. Command & Control: TA0011 (16 techniques)
13. Exfiltration: TA0010 (9 techniques)
14. Impact: TA0040 (13 techniques)

*([See how ATT&CK compares to the cyber kill chain](https://www.splunk.com/en_us/blog/learn/cyber-kill-chains.html).)*

### Techniques

Techniques are the methods adversaries use to achieve their tactic or goal. So, we can define techniques as *how* the adversary is going to achieve the tactic.

For instance, consider **the reconnaissance tactic**. Here, the adversaries’ goal is to collect the required information about a particular target in order to plan future attacks. To achieve this recon tactic, they use techniques like active scanning, scanning vulnerability IP blocks and [vulnerability scanning](https://www.splunk.com/en_us/blog/learn/vulnerability-scanning.html).

The MITRE ATT&CK framework provides an overview or definition for each technique. From there, it provides examples of relevant procedures and real-world implementations of the techniques. For each procedure example, they provide useful information like…

- A description of the procedure
- Techniques used
- Groups who use that software
- Campaigns

Additionally, each technique provides lists of mitigation and detection techniques the users can use with their data components for detection. You can see additional details, like which platforms are vulnerable to the technique and who has contributed to the knowledge. 

### Sub-Techniques

Some techniques can have several sub-techniques, while some do not have any.  For example, [phishing techniques](https://www.splunk.com/en_us/blog/learn/phishing-scams-attacks.html) used by adversaries can be further divided into three types of phishing attacks: [spear phishing](https://www.splunk.com/en_us/blog/learn/spear-phishing.html) attachment, link, and service.

Like major techniques, each sub-technique page describes procedure examples, mitigation, and detection techniques. 

By referring to specific tactics, the user can gain a comprehensive understanding of different techniques and sub-techniques used, as well as the mitigation and prevention methods. 

## More useful info from MITRE ATT&CK

In addition to the above three components of the matrices, the MITRE ATT&CK also provides separate documentation to the community on a variety of information.

### Data sources

Data sources describe what information you can gather from [sensors or logs](https://www.splunk.com/en_us/blog/learn/log-data.html). The [Data Sources document](https://attack.mitre.org/datasources/) briefly describes data components or what can be monitored, collected, and detected for each data source.

For example, enterprises can use [mailbox audit logs](https://www.splunk.com/en_us/blog/learn/audit-logs.html) from application logs data sources to detect folder modifications and identify areas that have been compromised. 

### Groups

[Groups is a collection of common names](https://attack.mitre.org/groups/) for which experts might use different terms, like threat or activity groups.  Sometimes, different experts give different names to the same group — they're displaying the same behaviors, even if the names vary.

MITRE ATT&CK team tracks overlaps between those names. For each group, documentation provides information such as a short description, techniques used, and software.  

### Software

[Software is the listings](https://attack.mitre.org/software/) showing a subset of techniques that are either publicly known to be used or that the software *could* use. If a group is known to use a particular software, then they're linked or "mapped" to it. It describes different types of software available for threat actors and the defending party, as well as the malware attackers. 

### Campaigns

[The Campaigns page](https://attack.mitre.org/campaigns/) lists online activities with a shared goal for specific targets. The team will provide a unique label if there is no specific name for these activities. When there are different names for different people or reports, the team names them "Associated Campaigns" on the page, hoping that researchers might connect the dots. 

They will also link those campaigns to specific groups or software if public reports have made those connections. They also describe any known techniques used in a campaign and how they obtained this information. 

## Use cases for the MITRE ATT&CK framework

There are ways for your organization to harness the information in the MITRE ATT&CK framework. Let’s take a look at what you can do.

### Identify security loopholes

You can absolutely use this framework to evaluate the effectiveness of your existing security mechanisms for known tactics and techniques. That assessment will reveal the gaps and vulnerabilities in your existing structure, highlighting areas where you need to improve security.

These, of course, are items your organization must prioritize based on your own industry, business, [risk appetite and risk tolerance](https://www.splunk.com/en_us/blog/learn/risk-tolerance-vs-risk-appetite.html).

### Gather threat intelligence

Next up, use the framework to [gain threat intel](https://www.splunk.com/en_us/blog/learn/cyber-threat-intelligence-cti.html) — that is, information on specific threat groups and [related malware families](https://www.splunk.com/en_us/blog/learn/ransomware-families.html). Organizations can maintain up-to-date information on adversaries by mapping the behaviors of specific threat groups to the ATT&CK matrix.

Additionally, you have a built-in and standardized way to describe and categorize attack behaviors. No more inventing your own lingo for various TTPs.

### Hunt for threats

Because MITRE ATT&CK is a comprehensive knowledge base of known adversary TTPs, [threat hunting](https://www.splunk.com/en_us/blog/learn/threat-hunting.html) is an obvious use case. Any ATT&CK matrix is a guiding document that threat hunters can use to build their processes, such as developing a hypothesis, prioritization, data collection, and documentation. 

*([Explore the PEAK Threat Hunting Model](https://www.splunk.com/en_us/blog/security/peak-threat-hunting-framework.html) or [learn how to hunt with Splunk](https://www.splunk.com/en_us/blog/security/hunting-with-splunk-the-basics.html).)*

![](https://www.splunk.com/content/dam/splunk2/images/data-insider/mitre-att-ck-framework/mitre-att-and-ck-diagram.svg)

### Research

For security researchers, the framework provides a standard way to name, describe and categorize adversary behaviors. Furthermore, researchers can identify gaps or areas requiring more thorough investigation by exploring and studying the ATT&CK matrix, opening up new avenues to consider and explore.

### Red team

Red teams test the security posture of an organization by simulating adversary behaviors. They can select the profile of a specific threat actor from the framework and emulate their behavior during operations. This ensures that any simulated attack closely resembles real-world scenarios.

Organizations using the MITRE ATT&CK framework in red team simulation exercises can better understand their security strengths and weaknesses.

*(Colors matter: know the difference between [red teams, blue teams](https://www.splunk.com/en_us/blog/learn/red-team-vs-blue-team.html) and [even purple teams](https://www.splunk.com/en_us/blog/learn/purple-team.html).)*

### Provide security training

Smart organizations know that MITRE ATT&CK is the perfect reference [for security teams](https://www.splunk.com/en_us/blog/learn/cybersecurity-jobs-skills-responsibilities.html) to gain comprehensive knowledge and training about various attack techniques and tactics. 

## ATT&CKing for good

MITRE ATT&CK provides comprehensive guidance on understanding and defending against sophisticated cyber threats. Since adversaries refine their tactics daily, this tool is indispensable in [practicing proactive defense](https://www.splunk.com/en_us/blog/learn/cci-cyber-counterintelligence.html). It provides informed threat intelligence that helps you [build resilience](https://www.splunk.com/en_us/blog/learn/digital-resilience.html) against new and emerging adversaries.