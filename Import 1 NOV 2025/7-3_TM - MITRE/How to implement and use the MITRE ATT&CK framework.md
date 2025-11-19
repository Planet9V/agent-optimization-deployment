---
title: "How to implement and use the MITRE ATT&CK framework"
source: "https://www.csoonline.com/article/567265/how-to-implement-and-use-the-mitre-attandck-framework.html"
author:
  - "[[abraham_kang]]"
published: 2019-05-21
created: 2025-03-16
description: "The MITRE ATT&CK framework is a popular template for building detection and response programs. Here's what you'll find in its knowledgebase and how you can apply it to your environment."
tags:
  - "clippings"
---
## The MITRE ATT&CK framework is a popular template for building detection and response programs. Here's what you'll find in its knowledgebase and how you can apply it to your environment.

Mitigating security vulnerabilities is difficult. Attackers need to exploit just one vulnerability to breach your network, but defenders have to secure everything. That’s why security programs have been shifting resources toward detection and response: detecting when the bad guys are in your network and then responding to their actions efficiently to gather evidence and mitigate the risk.

How can you build a program around detection and response? [MITRE’s ATT&CK framework](https://www.csoonline.com/article/565030/mitre-att-and-ck-framework-understanding-attack-methods.html) is one answer. ATT&CK can serve as a unifying taxonomy for different groups within an organization to share information, work together and build the necessary detection and response procedures.

MITRE’s ATT&CK framework has been gaining steady adoption from the security community because it organizes the steps attackers take to infiltrate your network, compromise hosts, escalate privileges, move laterally without detection, and exfiltrate data. Using a common taxonomy of attacker behavior in MITRE ATT&CK will help security teams — cyber incident response teams (CIRT), security operations centers (SOC), red and blue teams, threat hunters, IT — better test, develop, and prioritize their detection and response mechanisms to be relevant to their companies’ business, industry and intellectual property.

MITRE ATT&CK’s taxonomy is daunting and a bit overwhelming. There is so much information that it is easy to get stuck in analysis paralysis. These tips and guidance will help you quickly get your ATT&CK program up and running.

## How to understand the MITRE ATT&CK content

The tactics, techniques and procedures are documented in a tabular format as the [MITRE ATT&CK Enterprise Matrix.](https://attack.mitre.org/groups/) The [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/enterprise/) on GitHub provides more options for exploring the matrix.

- “Tactics” are the column header names and are generalized categories for why attackers use specific techniques.
- “Techniques” appear in each box under the tactics column headers and show what attackers do to accomplish a tactic. The ATT&CK matrix assigns a number to each technique such as T1500 or T1191.
- “Procedures” are accessible via links in the techniques boxes. They show how attackers execute a technique. Procedures provide more detailed instructions on how a specific technique has been implemented by attackers (even by attacking group) in the wild.

What makes MITRE ATT&CK great is that all the tactics, techniques and procedures (TTP) are based on what has been [observed by actual attacking groups in the real world](https://attack.mitre.org/groups/). Many of these groups use the same techniques. It is almost as if the hacking groups have their own playbook when attacking systems and they use this playbook to get new members productive quickly.

If you have read the [Pyramid of Pain](https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html), then you understand that many of the indicators of compromise (IOC) and indicators of attack (IOA) under TTP are similar to signature-based methods. By working at any of the levels below TTP, you are fighting their tools. So, the attackers might need to change a config file or recompile their tools to get around any of the lower Pyramid of Pain indicators below TTP (tools, network/host artifacts, domain names, IP addresses, and hashed values of file).

When targeting an attacker’s TTP, you are targeting their behaviors. This is much harder to change as understanding and detecting how an attacker would, for example, escalate privileges is different than looking for a file that hashes to a value known for the [Mimikatz](https://www.csoonline.com/article/566987/what-is-mimikatz-and-how-to-defend-against-this-password-stealing-tool.html) credential-in-memory dumping tool. In the latter case, an attacker just needs to recompile the tool with some random comments to change the hash of the tool and evade a signature-based detection tool.

However, finding an account that becomes administrator is much harder for the attacker to avoid and hide. It forces the attacker to change their behavior. It’s hard for junior hackers using a hacking playbook to change behavior; they are not skilled enough to create another way of escalating privileges on the fly. So, attackers try the hacking playbook elsewhere when detection methods target their behaviors.

This is the foundational premise of MITRE ATT&CK. Study and analyze the TTP used by past attackers at all stages of attack:

> initial access–>execution–>persistence–>privilege escalation–>defense evasion–>credential access–>discovery–>lateral movement–>collection –>exfiltration–>command and control

Drill down into each of the techniques’ procedures to better understand how different attack groups are executing the technique. Then use this knowledge to build detections that monitor for active attackers within your network based on their behaviors.

## How to implement MITRE ATT&CK

It sounds simple, but there are 291 techniques in the MITRE ATT&CK framework and it will only expand as new technologies roll out and artificial intelligence and machine learning systems are deployed. Where do you start and how do you prioritize, build and manage the detections that are developed? The first step in many security programs is to know yourself.

> “If you know the enemy and know yourself, you need not fear the result of a hundred battles. If you know yourself but not the enemy, for every victory gained you will also suffer a defeat. If you know neither the enemy nor yourself, you will succumb in every battle.” –Sun Tzu, The Art of War

### Know yourself (threat modeling)

You must first understand your company’s business drivers, how the business operates, where the revenue streams flow from, assets (prioritized by importance), intellectual property (IP), as well as the internal systems that drive the business and enterprise forward. Understand the impact on the business if any of these business assets, data, IP or systems were compromised. Also, ask yourself what external attackers would want if they were given magical keys to the enterprise kingdom. What would they target and why?

Now that you know what is important and would be targeted by an attacker, you can target the techniques that an attacker would use to get your most highly prized assets.

### Pick techniques for which you write detections

Many of the 291 techniques might apply to your high-value assets, systems and IP. How do you pick which techniques to start writing detections for?

Looking at the MITRE ATT&CK Matrix, you will notice an organizational structure from left to right that is chronologically tied to the sequence of steps an attacker would go through to eventually exfiltrate data or command and control (C2) servers. At the far left is initial access and this represents the beginning of an attacker’s journey through your network.

As you move to the right in the matrix the attacker is making progress and using those techniques on the right as needed. You can’t just start building detections on the far left and move rightward because you may already have threat actors in your network. Alternatively, you can’t just roll the dice and pick any random technique.

So, identify the techniques that are most relevant to your company’s sensitive data, systems and assets.

### Look at difficulty of attack

It is good that you narrowed the field down from 291 to those that apply to your company, but how do you further narrow down the field of techniques?

Due to the increasing popularity of MITRE ATT&CK and willingness of implementers to share information, many open-source and public resources are available to help you. For example, Travis Smith of Tripwire gave an excellent presentation at ATT&CKCon called [“ATT&CK as a Teacher”](https://www.youtube.com/watch?v=4s3pZirFCPk&list=PLkTApXQou_8JrhtrFDfAskvMqk97Yu2S2&index=13&t=0s) where he organized the ATT&CK Matrix by difficulty of exploitation. The color-coded legend is based on the chart below showing increasing levels of difficulty going top to bottom.

![kang mitre 1](https://images.idgesg.net/images/article/2019/05/kang-mitre-1-100796766-large.jpg?auto=webp&quality=85,70)

Color codes showing difficulty of attack

This is what the ATT&CK Navigator looks like after they applied the difficulty color codes:

![kang mitre 2](https://images.idgesg.net/images/article/2019/05/kang-mitre-2-100796768-large.jpg?auto=webp&quality=85,70)

Color codes applied to ATT&CK Navigator

Now you further narrowed your list down depending on skillset of the team members you have to build detections. You can do more to pare down your list. The remaining detection candidates have certain data source requirements to build detections on top of. If your organization does not have an associated data source to a targeted technique, then writing a detection for that technique will not be straightforward.

### Look at data sources

Every technique’s procedure has data sources associated with it. Let’s look at T1214:

![kang mitre 3](https://images.idgesg.net/images/article/2019/05/kang-mitre-3-100796767-large.jpg?auto=webp&quality=85,70)

Data sources for T1214

When you are finalizing which techniques to implement as detections, make sure you have the appropriate data sources to implement the detection for that technique. This is where things get a bit nebulous. For the Credentials in Registry example above, you are given “Windows Registry”, “0rocess command-line parameters”, and “process monitoring”.

The following slides are from a presentation by Roberto and Jose Rodriguez, “[Hunters ATT&CKing with the Data](https://www.youtube.com/watch?v=QCDBjFJ_C3g&list=PLkTApXQou_8JrhtrFDfAskvMqk97Yu2S2&index=21&t=0s).” According to the Rodriguez brothers, you can prioritize the technique-based detections that you want to implement by looking at the common data sources across different ATT&CK techniques in your environment.

![kang mitre 4](https://images.idgesg.net/images/article/2019/05/kang-mitre-4-100796769-large.jpg?auto=webp&quality=85,70)

If you can integrate the above three data sources into your ATT&CK implementation, then you can maximize the number of detections that you could create. Also, to give you a better overall picture of data sources required to implement different ATT&CK techniques, the Rodriguez brothers provide the following two slides that highlight the data source requirements for them.

![kang mitre 5](https://images.idgesg.net/images/article/2019/05/kang-mitre-5-100796770-large.jpg?auto=webp&quality=85,70)

![kang mitre 6](https://images.idgesg.net/images/article/2019/05/kang-mitre-6-100796771-large.jpg?auto=webp&quality=85,70)

Another important point they stress is that almost every high-level data source named in the ATT&CK procedures consists of subdata sources (different forms of that data source). It is important to understand which of those data sources you have access to and what those subdata sources provide. It is not enough to find one of the subdata sources. You need to understand what you are missing to identify gaps in your detection capabilities.

When implementing different related technique detections (overpass-the-hash via Mimikatz or Rubeus), you may be able to reduce the number of subdata sources you need to detect specific techniques by analyzing which techniques are more relevant to your organization. For example, the file and process monitoring data sources are needed for 66 different techniques.

![kang mitre 7](https://images.idgesg.net/images/article/2019/05/kang-mitre-7-100796772-large.jpg?auto=webp&quality=85,70)

However, your techniques of interest may only require a subset of the subdata sources.

![kang mitre 8](https://images.idgesg.net/images/article/2019/05/kang-mitre-8-100796761-large.jpg?auto=webp&quality=85,70)

Other examples of this depend on the variations of how attackers go about executing techniques. The Rodriguez brother’s presentation shows one technique (overpass-the-hash) can be executed and detected using two different methods (Mimikatz and Rubeus).

![kang mitre 9](https://images.idgesg.net/images/article/2019/05/kang-mitre-9-100796764-large.jpg?auto=webp&quality=85,70)

![kang mitre 10](https://images.idgesg.net/images/article/2019/05/kang-mitre-10-100796763-large.jpg?auto=webp&quality=85,70)

The point of showing the subset of the subdata sources was that you may want to focus on one version over the other if your threat intel says that one is more relevant for your company’s environment. This will allow you to get detections out more efficiently.

How do you hook into the data sources and where is that information provided? If you are new to MITRE ATT&CK, read the References section, but you usually have to tease this information out of the references. Lucky for you there is [The Open Source Security Events Metadata (OSSEM).](https://github.com/Cyb3rWard0g/OSSEM)

Created by Roberto and Jose Rodriguez, OSSEM provides you with four different categories of information related to data sources: ATT&CK data sources, detection data models, common information models and data dictionaries.

ATT&CK data sources are a mapping from an ATT&CK technique’s data sources to the actual system events or analytics that produce the data for that technique’s detection mechanism. The following graphic illustrates what the mapping is trying to store.

![kang mitre 11](https://images.idgesg.net/images/article/2019/05/kang-mitre-11-100796762-large.jpg?auto=webp&quality=85,70)

Mapping ATT&CK data sources to system events or analytics

This ATT&CK data source mapping is for T1214 (Credentials in Registry). T1214 points to the data sources (Windows Registry, process monitoring and process command-line parameters) identified in the ATT&CK Matrix for Credentials in Registry above. The picture above describes the subprocesses for the process monitoring data source as well as the event log sources for the information. [This spreadsheet](https://docs.google.com/spreadsheets/d/1ow7YRDEDJs67kcKMZZ66_5z1ipJry9QrsDQkjQvizJM/edit#gid=0) shows more of the ATT&CK data sources defined as well as their subcomponents. This information is useful when evaluating MITRE ATT&CK tools vendors to see how deep their actual support of a particular MITRE ATT&CK data source goes.

### Bring your data together

After understanding where your data sources are physically sourced as well as the events’ relationships to those physical data sources, you need a repository of this information and a way to query it. You could use a graph database and implement something similar to the following based on the information in the data dictionary and common information model:

![kang mitre 12](https://images.idgesg.net/images/article/2019/05/kang-mitre-12-100796765-large.jpg?auto=webp&quality=85,70)

One model for an information repository

However, this is a lot of work. If don’t want to create everything from scratch, you have two options: open source tools — such as [Osquery](https://osquery.io/), Filippo Mottini’s [Osquery with reference detection implementations](https://github.com/teoseller/osquery-attck), the [Kolide](https://github.com/olafhartong/kolide) agentless Osquery web interface and remote API server by Olaf Hartong — or commercial endpoint security platforms.

Facebook developed OSquery to manage its server infrastructure. It is well implemented and supported by the community. It gathers information across hosts in your environment and aggregates the data into tables. You use SQL like queries to access the data in the tables and to write detections, so the learning curve is not as steep for people who have exposure to relational databases.

OSquery can create collections of queries that map to targeted TTP in ATT&CK for threat hunting. Hunters can create and execute ad hoc queries on the fly and those queries that identify attackers on the network can be integrated with your [security information and event management (SIEM)](https://www.csoonline.com/article/524286/what-is-siem-security-information-and-event-management-explained.html) system. In addition, smart people like Filippo Mottini and Olaf Hartong have already created reference detection implementations with OSquery that you can build upon.

[Evaluated commercial tools](https://attackevals.mitre.org/evaluations.html) that support MITRE ATT&CK fall under the general category of endpoint security platforms. There are several things to consider when purchasing a tool:

- What data sources does it support?
- To what degree and which subdata source does the tool support a particular data source?
- Which techniques are covered and to what extent?

### Understand the capabilities and limitations of different tools

Make sure that the tool supports the specific data sources in your environment to detect different MITRE ATT&CK techniques. If the tool you are considering integrates with directories and you have LDAP, make sure that the tool’s vendor doesn’t assume that you have Active Directory.

Also, understand what level of subdata source support the tool provides. If the tool advertises support for Windows Registry, does it support the creation, deletion, modification and access of registry keys? Verify, vet or test the assumptions and features that you will rely on from the tool’s vendor.

Look at whether the tool integrates with your SIEM and security orchestration, automation and response (SOAR) infrastructure. You may be able to push data to or get data from your SIEM and SOAR infrastructure to provide richer findings with fewer false positives.

Finally when reviewing the products make sure you understand the differences in warning types. For example, tools provide different levels of information related to detections. Some tools provide informational type events while other tools provide specific references to MITRE ATT&CK techniques and deeper explanation about the events. The richer the information provided the less guess work your blue team has to do to triage the event. For the purpose of describing the levels of event description richness in the MITRE ATT&CK tools evaluations, they go from:

None (lowest) →

Telemetry (info) →

IOC (signature-based identification of problem) →

Enrichment (telemetry + ATT&CK correlated information) →

General behavior (alert “finding” but without specific details) →

Specific behavior (alert “finding” with specific details explaining how the finding is malicious can be tied to ATT&CK technique related information)

## Maintain the ATT&CK detection lifecycle

Building detections requires thinking about how attackers will implement the different ATT&CK techniques with their own procedures, understanding how those procedures work and ultimately how to detect the procedures. Once you have this, then you can build, test, deploy, fine tune, disable and periodically verify the detections. The process encompasses the detection life cycle (DLC) described below:

### Detection ideation

You will need a system to keep track of detections as they move from inception to each phase of the DLC. People get ideas on how they can tackle implementing detections for specific important techniques. Sometimes only bits and pieces of a solutions materialize, but there needs to be a central store for this information so different people can see the detections status and build on each other’s knowledge while learning about different detection methods.

### Detection creation

Once the detection’s status has moved from ideation to ready for implementation, it can be claimed for development. The blue team can look at the description of the detection and implement it. Once finished and tested locally, the code needs to be checked in and referenced in the DLC management system. Then the status for the detection needs to be modified to “ready for testing”.

### Detection testing

Once a detection is ready for testing. It needs to be deployed to an integration test environment that provides output to use to anticipate the number of events generated by the new detection before the security analysts have to review them. This is to gauge how well the detection works in an environment similar to production.

The number of events generated per time period are gathered as well as the actual events themselves for review by the detection developer. Once the testing period has completed, the detection is put in “ready for review”. The detection developer and a more senior detection developer needs to review the results and both need to approve the detection before it is placed into production. If the detection produces too many false positives, the detection logic can be changed and status marked “ready for testing”.

### Detection deployment

Once the detection has been approved by two members of the detections development team, it moves to “ready for production”. At this point team members installing detections into the production environment deploy the detection into the production environment. Initially, full logging is turned on and all data is gathered for a two-week break-in period to account for deployment during prolonged corporate holidays. At this point security analysts need to be apprised of the new detection so they know how to evaluate events generated from the detection and are given an opportunity to ask questions related to the new event.

### Detection break-in period

After the two-week break-in period (or sooner if there are problems), the Detection developer reviews the logs, events and any other pertinent information related to the detection. In addition, the testing team should have validated that the detection is working in the production environment by manually creating events that the new detection should identify.

### Detection enhancement

The detection developer analyzes the information and makes adjustments to the detection to address identified problems. If there are problems, the detection is set to “ready for testing”. If there are no problems, then the detection’s status is changed to “finalized for production”. This triggers the production deployment teams to open the events to the security analysts for triage.

### Detection tracking

Full logging is turned down but metrics related to the detection are still collected for tracking and validation.

### Periodic validation

All detections need to be periodically assessed for proper functioning and relevancy. In addition, detections need to be changed to account for new tools and techniques used by adversaries (threat intelligence).

## Threat hunting with ATT&CK

Building detections and running them through the DLC takes time. While your detections are being built you can actively pursue threat actors in your network with MITRE ATT&CK.

Because MITRE’s ATT&CK represents a taxonomy of behavioral TTP attackers use to compromise corporate networks, it can also be used to direct efforts and find active actors in your network by focusing on non-implemented detection use cases. You need to understand what the critical assets of the corporation are and what attackers would likely target and why. Then use the MITRE ATT&CK taxonomy to focus on manually detecting techniques used to compromise the critical assets.

If you can focus your hunting efforts around techniques that have not been covered by implemented detections, you can use the information gained going through the hunt to help develop associated detections. Finally, the Hunt should focus on techniques that are difficult to implement as detections.

## Gamifying ATT&CK

Going through the MITRE ATT&CK process may become robotic and monotonous. To keep the process from becoming an assembly line, use gamification to make the process fun.

Have groups try to bypass the detections and detecting techniques continually and one-up each other. Continually reward both sides. It is not about one side beating the other. It is about both sides continually improving. For example, if the red team finds a way around a detection, celebrate with both the red and blue teams. When the blue team proactively learns about the bypass and anticipates the modification of a technique used previously to bypass a detection, celebrate again with both teams.

## Keeping up with the Joneses

Attackers and red-teamers are constantly upping their game. Attackers have the same access to MITRE’s ATT&CK framework as you do so they know what data sources you are using and how you may be trying to detect them. You need to be aware of the techniques that attackers use to bypass evasion and account for them.

William Burgess gave a phenomenal presentation called [Red teaming in the EDR age](https://www.youtube.com/watch?v=l8nkXCOYQC4) that highlighted the techniques that advanced red teamers use to avoid attack detection:

- Misdirection: Create false and misleading information that makes endpoint detection and response solutions useless. For example, create an initially suspended process that is legitimate and logged but then modify its runtime commands and parameters and resume the process, causing the attacker-provided command execute and not be logged. Then rewrite the command back to its legitimate version so runtime analysis (Process Explorer) is fooled,

- Minimization: Avoid creation of processes from traditional parent processes or use a legitimate process in combination with injecting a reflected DLL into the legitimate process to execute the desired commands.

- Memory evasion: Hide tell-tale signs of memory exploitation via reflective loading, process hollowing, process scheduling and hiding malicious processes in read-only segments.

All the above techniques need to be accounted for.

*Special thanks to Filippo Mottini, Roberto and Jose Rodriguez for reviewing this article.*