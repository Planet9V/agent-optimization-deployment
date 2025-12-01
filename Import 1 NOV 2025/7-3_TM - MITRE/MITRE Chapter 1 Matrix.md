---
title: "Chapter 1 - MITRE ATT&CK Matrix"
source: "https://www.devo.com/threat-hunting-guide/mitre-attack-matrix/"
author:
  - "[[Devo.com]]"
published: 2024-03-26
created: 2025-03-16
description: "Learn how information is organized in the MITRE ATT&CK Matrix and how this can be used to plan your security procedures."
tags:
  - "clippings"
---
MITRE is a non-profit organization, renowned in the field of cybersecurity. Founded in 1958, MITRE Corporation is based in Bedford, Massachusetts, and McLean, Virginia, and is funded by the U.S. government. It conducts cybersecurity analysis and research for the federal government.

With the ATT&CK framework, the MITRE organization provides the security community with an extensive, empirical and varied knowledge-base of known attack techniques. Unlike similar projects, the focus does not concentrate on specific tools or malware, but on the actions of the attacker.

This unique approach has the following advantages:

- Freely accessible on the Internet via the MITRE website
- Focused on actions performed by an attacker against a system, and not on exploitation tools or malware
- Relatively comprehensive, with over 250 listed attack ‘tactics, techniques and procedures’ (TTPs)
- Representative of attacks observed in the real world
- Updated regularly with several updates per year

While the framework can appear overwhelming due to its size and complexity, particularly for newcomers, it is nonetheless a powerful tool when used correctly to identify a threat actor’s possible behavior within a compromised environment and support organizational risk assessment and cyber-defense. Furthermore, it can be invaluable for the definition of effective and comprehensive business SOC strategies and in the selection of appropriate security technology.

This article will serve as an introduction to the MITRE framework and is aimed at both new and existing security professionals. With this in mind we will begin with a brief executive summary to set the tone, before covering the MITRE ATT&CK matrix and its architecture in more depth. We will then provide a practical example of where the framework works well, followed by an example of where it requires a little help. We will then conclude with our final thoughts and provide some advice.

## **Executive Summary**

- The MITRE ATT&CK matrix is a comprehensive, current and down-to-earth framework detailing the potential behavior of an adversary to reach information assets
- The MITRE ATT&CK matrix can be used as an effective training aid allowing SOC and blue teams to prepare for common types of cyber-attack, as well as red and purple team for their intrusion scenarios.
- The MITRE ATT&CK matrix should be used as a support tool and not, as we will later demonstrate, the sole focus of an Information Security supervision strategy
- A risk-based approach helping to define threat scenarios, such as a risk management framework, should be coupled with the use of the MITRE matrix

The MITRE “Adversarial Tactics, Techniques, and Common Knowledge” (ATT&CK) knowledge base is rapidly becoming one of the most established and frequently referenced security resources for cyber-security professionals. Whether for SOC, CERT, CTI or intrusion testing, MITRE can be found cited in several specialized cyber-threat publications, including articles from the likes of FireEye and Microsoft. Most recently, it has been featured in the [Verizon Data Breach Report](https://www.verizon.com/business/resources/reports/dbir/).

One key benefit of the framework is that it allows cyber professionals from different backgrounds to communicate using a common language, built around a repository of evolving TTPs, which are updated on a regular basis.

“Tactics” are the most important component of the ATT&CK framework and represent the reasoning or technical goal behind an ATT&CK technique. They are the tactical objective of the threat actor: the reason he launches a specific offensive action. Tactics gather the different methods used by attackers, such as “persist,” “discover,” “move laterally,” “execute files” or “exfiltrate data.” The MITRE ATT&CK framework consists of 14 different tactics, illustrated in the image below.

![MITRE ATT&CK Techniques](https://www.devo.com/wp-content/uploads/2024/02/MITRE-Techniques.png)

*MITRE ATT&CK framework’s Techniques (mitre.org)*

MITRE ATT&CK techniques (which are categorized by tactic) are a set of specific technical actions that attackers can utilize to achieve their goal and what they can get out of it.

The ATT&CK framework allows analysts to better understand the specifics of an attack via official definitions and terminology, which enhances communication between team members. This in turn accelerates and improves threat detection and response time.

Effectively, by understanding the behavior of a potential adversary, the organization can better identify which controls might be operational in case of a cyber incident, and which might present gaps and limitations. This helps the organization gain a better view over its coverage in terms of controls and detection capabilities. It also shows which patterns within the environment would prove to be the most interesting for a threat actor and hence helps the organization focus its resources on specific areas.

The ATT&CK framework can also be used by departments not strictly associated with cyber-security. Due to MITRE’s ability to paint a picture of general incidents and assist in the creation of reports and dashboards, auditors and CISOs can utilize this information more generally.

## **MITRE ATT&CK Strengths**

It is likely that MITRE ATT&CK has become the leading cyber-security industry standard, at least as far as the documentation of offensive processes is concerned, on both the vendor and service company sides.

To date, the ATT&CK matrix includes 14 tactics, over 250 techniques and 350 sub-techniques, which indicates that the framework is rich and evolving. Combined with increasing adoption and direct support from the NSA, MITRE is a credible framework with a strong future.

The MITRE ATT&CK matrix can help blue teams in 3 key areas:

- Threat Intelligence: ATT&CK allows security analysts to standardize the way they share knowledge about potential threats, by engaging many partner companies with panels of security experts from a wide range of organizations in different industries.
- Attack simulation: This greatly facilitates exchanges between blue teams and red teams by defining a common structure during an attack simulation. Many tools are suggested in the ATT&CK framework that simulate and test different attack scenarios, including CALDERA Python scripts.
- Defense level assessment: The matrix allows SOC teams to have a precise representation of attack techniques covered by their current security tools.

![MITRE ATT&CK Framework](https://www.devo.com/wp-content/uploads/2024/02/Framework-1024x434.png)

*A partial view of the MITRE ATT&CK framework (*[*source*](https://attack.mitre.org/matrices/enterprise/#)*)*

During a SOC training session (referred to as “purple teaming”), the offensive team usually expects to receive a list of TTPs that are theoretically detectable by the SOC. At the end of the “purple teaming”, both the SOC team (“blue”) and the offensive team (“red”) can confirm, TTP by TTP, which were detected and which were not. This allows the SOC team to improve by utilizing feedback gathered from failed detections, and by verifying the presence of compromise indicators during successful detections. This also highlights the current depth of coverage provided by the SOC and indicates areas for improvement.

In addition, MITRE formalizes the processes used by active attackers, maps TTPs they use to a common framework, allowing for a common language when communication across groups within the security apparatus of the organization, thus leading to the formulation of trends, which can subsequently be used to direct the efforts of security teams, the SOC or CSIRT.

## **Challenges**

The total utilization of any security framework by a SOC is, in reality, neither realistic nor relevant in an organizational context. The key question is: where should the focus of improving SOC threat detection capabilities be placed? Specifically, how does one choose which techniques, sub-techniques or even tactics to concentrate on, in the short, medium, and long term? The vastness of the ATT&CK framework means that this is a non-trivial task.

Let’s examine a hypothetical scenario. The use of scripts by attackers is one of the most common TTPs at the moment, and corresponds to the “Execution” tactic in the ATT&CK matrix. This TTP is often used by attackers to extort money via ransomware (and to exfiltrate sensitive data). This can represent a major security issue for any organization.

However, if the same organization also considers phishing to be a major security threat, then the TTPs of the “Command and Scripting Interpreter” technique (referenced T1059) will not necessarily be the most relevant in terms of detection.  Instead, the TTPs of the “Phishing” technique (referenced T1566) are much more relevant.

The problem here is that the sensors needed for the detection of T1566 are quite different from those required for T1059. Specifically, for the Command and Scripting Interpreter (T1059), the ATT&CK framework lists sensors as:

- *Command Execution*
- *Module Load*
- *Process Creation*
- *Script Execution*

Whereas, for the “Phishing” technique (T1566), the framework indicates these sensors:

- *Application Log Content*
- *Network Traffic Content*
- *Network Traffic Flow*
- *File Creation*

We can see that these two lists have nothing in common. As a result, the  workload placed on the SOC could dramatically increase and require the completion of multiple tasks, including: defining logging policies, retention strategies, conducting SIEM data integration, and designing detection and response strategies. 

Without automation to apply appropriate security policy changes, the additional burden placed onto the SOC could result in burnout.  How then, do we correctly prioritize the actions of the SOC in light of so many options? Which sensors should we acquire and deploy in order to meet the desired detection capacity?

If security needs were determined via specific, scenario-based risk analysis, for example, “solicitation by email of a user, in order to lead him to perform fraudulent actions on an application (integrity and confidentiality impacts)”, then the efforts of the SOC could be more efficiently concentrated and directed. Some readers may have recognized here a scenario similar to the “Fake President Fraud”, and clearly, the “Phishing” TTP seems more relevant. As a result, detection efforts will likely be placed onto messaging systems,  including anti-spam utilities and application log monitoring.

This is where the ATT&CK database shows its limitations when used alone, because there is no concept of allowing for specific security needs within the ATT&CK database.

Crucially, one should also remember that the MITRE ATT&CK framework does not include any notion of “cyber risk”, but only the operational scenarios that lead to a cyber incident. It would therefore be appropriate to consider the additional use of a risk management framework, such as ISO 27005, COSO or the NIST ERM framework, that helps define and mitigate the risks described by the MITRE ATT&CK framework.

## **Conclusion**

The MITRE ATT&CK framework is a useful asset to any SOC team. It provides a well-referenced and comprehensive repository of attack tactics and is supported by a growing community of experienced experts and security enthusiasts. It is gradually being adopted and promoted by security vendors as a guarantee of quality in the field of cybersecurity. After all, it is only with a thorough understanding of offensive techniques that it becomes possible to counter them. We strongly encourage cybersecurity professionals to give this framework the attention it deserves, but with the caveat that it should be paired with a suitable risk management framework.