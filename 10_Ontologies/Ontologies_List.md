Major ontology frameworks covering cybersecurity, industrial controls, engineering, critical infrastructure, business, IT/cloud, and psychological domains:

Domain/Industry	Ontology Framework
## Cybersecurity Unified Cyber Ontology (UCO)

github.com/Ebiquity/Unified-Cybersecurity-Ontology​, github.com/ucoProject/UCO​, unifiedcyberontology.org​
## Industrial Controls	ICS-SEC Ontology (ICS)

github.com/sepses/ics-sec-kg​

## Engineering	Engineering Application Ontology

scribd.com/document/929424916​

## Critical Infrastructure	CI System Ontology (Disruption Scenario)	
academia.edu/82635366​
​
## Enterprise Architecture	ArchiMate Ontology	
github.com/yasenstar/ArchiMate_Ontology​, opengroup.org/archimate-licensed-downloads​

## IT/Cloud/Networking
ICT Infrastructure Ontology Network	corcho2021high.pdf​, oa.upm.es/72099/3/2021_ISWC_DevOps_Infra.pdf​
Media/Cloud Workflows	

## Media in the Cloud Ontology Guide
smpte.org/media-in-the-cloud-ontology-guide​, content-technology.com​


## Financial Industry Business Ontology
The Financial Industry Business Ontology (FIBO) is a formal ontology that provides a common vocabulary for financial contracts and related concepts. FIBO evolved out of concerns that arose during the 2008 financial crisis among individuals who worked together in data governance and management to address requirements for standardized terminology for regulatory reporting and other analyses. The resulting ontology has continued to grow and evolve since its initial publication in 2014, with increasing support for use cases related to securities master data management, reporting, and risk analysis and management.

FIBO Business Entities (BE)
usiness Process (BP) domain.
Corporate Actions and Events (CAE) domain. 
Derivatives (DER) Domain.'
Financial Business and Commerce domain. 
FIBO Indices and Indicators (IND)
FIBO Loan (LOAN) domain. 
Market Data (MD) domain.
FIBO Securities (SEC) domain

https://github.com/edmcouncil/fibo.git


## ATTACK STIX
MITRE ATT&CK is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. The ATT&CK knowledge base is used as a foundation for the development of specific threat models and methodologies in the private sector, in government, and in the cybersecurity product and service community.

This repository contains the MITRE ATT&CK dataset represented in STIX 2.1 JSON collections. If you are looking for STIX 2.0 JSON representing ATT&CK, please see our MITRE/CTI GitHub repository which contains the same dataset but in STIX 2.0 and without the collections features provided on this repository.

https://github.com/mitre-attack/attack-stix-data.git



### CTI
This repository contains the MITRE ATT&CK® and CAPEC™ datasets expressed in STIX 2.0. See USAGE or USAGE-CAPEC for information on using this content with python-stix2.

If you are looking for ATT&CK represented in STIX 2.1, please see the attack-stix-data GitHub repository. Both MITRE/CTI (this repository) and attack-stix-data will be maintained and updated with new ATT&CK releases for the foreseeable future, but the data model of attack-stix-data includes quality-of-life improvements not found on MITRE/CTI. Please see the attack-stix-data USAGE document for more information on the improved data model of that repository.

### ATT&CK
MITRE ATT&CK is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. The ATT&CK knowledge base is used as a foundation for the development of specific threat models and methodologies in the private sector, in government, and in the cybersecurity product and service community.

https://attack.mitre.org

### CAPEC
Understanding how the adversary operates is essential to effective cyber security. CAPEC™ helps by providing a comprehensive dictionary of known patterns of attacks employed by adversaries to exploit known weaknesses in cyber-enabled capabilities. It can be used by analysts, developers, testers, and educators to advance community understanding and enhance defenses.

Focuses on application security
Enumerates exploits against vulnerable systems
Includes social engineering / supply chain
Associated with Common Weakness Enumeration (CWE)
https://capec.mitre.org/

### STIX
Structured Threat Information Expression (STIX™) is a language and serialization format used to exchange cyber threat intelligence (CTI).

STIX enables organizations to share CTI with one another in a consistent and machine readable manner, allowing security communities to better understand what computer-based attacks they are most likely to see and to anticipate and/or respond to those attacks faster and more effectively.

STIX is designed to improve many different capabilities, such as collaborative threat analysis, automated threat exchange, automated detection and response, and more.

https://oasis-open.github.io/cti-documentation/

https://github.com/mitre/cti.git

## MITRE Data to STIX for Knowledge Graphs Building
https://documentation.eccenca.com/23.3/build/tutorial-how-to-link-ids-to-osint/lift-data-from-STIX-2.1-data-of-mitre-attack/


# ArchiMate_Ontology
About
Build ontology view step-by-step on OpenGroup's ArchiMate 3.2 Specification
https://github.com/yasenstar/ArchiMate_Ontology.git

# ICS-SEC-KG
The ICS-SEC KG is a cybersecurity knowledge graph that integrates and links critical cybersecurity information of Industrial Control System (ICS) and Operational Technology (OT) from various publicly available sources. It extends the existing SEPSES-CSKG by including ICS-related security resource such as Industrial Control System Advisory (ICSA) and MITRE ATT&CK for ICS. The Knowledge Graph is continuously updated to reflect the dynamic changes in ICS-Security landscape.

https://github.com/sepses/ics-sec-kg.git

# Cyber KG Convter
SEPSES-CSKG is a cybersecurity knowledge graph that integrates and links critical information such as vulnerabilities, weaknesses and attack patterns from various publicly available sources. The Knowledge Graph is continuously updated to reflect changes in various data sources used as inputs, i.e., CAPEC, CPE, CVE, CVSS, and CWE. This engine is designed as a RDF generation mechanism from several CyberSecurity resources. In our server, we add additional bash command to run it continuously, but we didn't provide the script here.

New: ISC-SEC KG
New! Several additional resources for Industrial Control System Cybersecurity (ICS-Sec) has been included, i.e., MITRE ATT&CK (Enterprise and ICS) and ICSA (Industrial Control System Advisory). Detail information can be found here.

Vocabularies
Several vocabularies are developed to represent the SEPSES-CSKG knowledge graphs, as follows:

Prefix	Description	Link
capec	Common Attack Pattern Enumeration and Classification (CAPEC)	http://w3id.org/sepses/vocab/ref/capec
cwe	Common Weakness Enumeration (CWE)	http://w3id.org/sepses/vocab/ref/cwe
cve	Common Vulnerabilities and Exposures (CVE)	http://w3id.org/sepses/vocab/ref/cve
cvss	Common Vulnerability Scoring System (CVSS)	http://w3id.org/sepses/vocab/ref/cvss
cpe	Common Platform Enumeration (CPE)	http://w3id.org/sepses/vocab/ref/cpe

https://github.com/sepses/cyber-kg-converter.git


# SAREF.ETSI.ORG

## SAREF Core
SAREF Core specifies recurring core concepts in the smart applications domain, and the main relationships between these concepts. 

## SAREF Design Principles

SAREF is developed based on the following fundamental principles:
Reuse and alignment of concepts and relationships that are defined in existing assets
Modularity to allow separation and recombination of different parts depending on specific needs
Extensibility to allow further growth of the ontology
Maintainability to facilitate the process of identifying and correcting defects, accommodate new requirements, and cope with changes
Generic versus specific entity distinction. SAREF is designed for application developers, and also for online catalogue and taxonomy editors.

SAREF4ENER: SAREF extension for the Energy domain
SAREF4ENVI: SAREF extension for the Environment Domain
SAREF4BLDG: SAREF extension for the Building domain
SAREF4CITY: SAREF extension for the Smart Cities domain
SAREF4INMA: SAREF extension for the Industry and Manufacturing domains
SAREF4AGRI: SAREF extension for the Smart Agriculture and Food Chain domains
SAREF4AUTO: SAREF extension for the Automotive domain
SAREF4EHAW: SAREF extension for the eHealth/Ageinwell domain
SAREF4WEAR: SAREF extension for the Wearables domain
SAREF4WATR: SAREF extension for the Water domain
SAREF4LIFT: SAREF extension for the Smart Lifts domain
SAREF4GRID: SAREF extension for the Smart Grid domain


## SAEF ETSO LABS
Repository for the SAREF4ENER ontology.

## Core
https://labs.etsi.org/rep/saref/saref-core.git

## Energy
https://labs.etsi.org/rep/saref/saref4ener.git

## Environmental
https://labs.etsi.org/rep/saref/saref4envi.git

## Buildings
https://labs.etsi.org/rep/saref/saref4bldg.git

## City
https://labs.etsi.org/rep/saref/saref4city.git

## Manufacturing
https://labs.etsi.org/rep/saref/saref4inma.git

## Agriculture
https://labs.etsi.org/rep/saref/saref4agri.git

## Automoative
https://labs.etsi.org/rep/saref/saref4auto.git

## Health and Aging
https://labs.etsi.org/rep/saref/saref4ehaw.git

## Wearables
https://labs.etsi.org/rep/saref/saref4wear.git

## Water
https://labs.etsi.org/rep/saref/saref4watr.git

## Smart Lift
https://labs.etsi.org/rep/saref/saref4lift.git

## 
https://labs.etsi.org/rep/saref/saref4grid.git

## Virtual Private Networks
https://labs.etsi.org/rep/stan4cra/en-304-620-1.git

## EN 304 625 Network Interfaces
https://labs.etsi.org/rep/stan4cra/en-304-625.git


# SChema.org
This is a list of actual schemas in html for each of the following;

## Thing > Person
A person (alive, dead, undead, or fictional).

https://schema.org/Person

## Restaurant
A restaurant.

https://schema.org/Restaurant

## Organization
An organization such as a school, NGO, corporation, club, etc.

https://schema.org/Organization

## Event
An event happening at a certain time and location, such as a concert, lecture, or festival. Ticketing information may be added via the offers property. Repeated events may be structured as separate Event objects.

https://schema.org/Event

## Action
An action performed by a direct agent and indirect participants upon a direct object. Optionally happens at a location with the help of an inanimate instrument. The execution of the action may produce a result. Specific action sub-type documentation specifies the exact expectation of each argument/role.

https://schema.org/Action

## Product
Any offered product or service. For example: a pair of shoes; a concert ticket; the rental of a car; a haircut; or an episode of a TV show streamed online.
https://schema.org/Product
