<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Comprehensive Research Report: Ontology Frameworks for Neo4j Knowledge Graph Optimization

## Executive Overview

Building a comprehensive ontological formal schema to optimize Neo4j knowledge graphs for digital twins of organizations and critical infrastructure facilities requires a strategic combination of standard, domain-specific, and industry ontologies. This report provides detailed descriptions, applications, use cases, and implementation guidance for 23+ ontology frameworks spanning cybersecurity, industrial control systems, engineering disciplines, critical infrastructure, business operations, IT/cloud environments, psychological concepts, and digital twin architectures.

## Standard and Foundational Ontologies

### Basic Formal Ontology (BFO)

**Description:** BFO is an ISO/IEC 21838-2 international standard top-level ontology designed for interoperability across diverse domains. It provides a foundational framework based on a distinction between **continuants** (entities that persist through time, such as objects and spatial regions) and **occurrents** (processes that unfold over time). BFO has been adopted by over 450 ontology projects worldwide and serves as the basis for domain-specific ontologies in biomedicine, defense, intelligence, and manufacturing.[^1][^2][^3][^4]

**Key Features:**

- Realist perspectivalism philosophical approach avoiding both constructionism and pure logical formalism[^2]
- Minimal axiomatization allowing flexible domain extensions
- Standard compliance ensuring long-term stability and interoperability

**Use Cases:**

- **Manufacturing Digital Twins:** BFO provides the foundational structure for the Industrial Ontologies Foundry (IOF), enabling standardized representation of manufacturing processes, equipment, and operations across supply chains[^5]
- **Healthcare Data Integration:** The Ontology for Biomedical Investigations (OBI) extends BFO to integrate clinical trial data, laboratory results, and patient records[^1]
- **Defense and Intelligence:** Adopted by DOD and Intelligence Community as baseline standard for all formal ontology work, ensuring data interoperability across agencies[^4][^6]

**Implementation for Neo4j:**
BFO classes map naturally to Neo4j node labels (e.g., `Continuant`, `Process`, `MaterialEntity`), while BFO relations become relationship types. Use BFO as the top-level structure, then extend with domain ontologies for specific knowledge graph applications.[^7][^1]

### DOLCE (Descriptive Ontology for Linguistic and Cognitive Engineering)

**Description:** DOLCE is an ISO standard foundational ontology inspired by cognitive and linguistic considerations, modeling a commonsense view of reality used in everyday human activities. It focuses on how humans conceptualize the world rather than strict metaphysical realism, making it particularly suitable for socio-technical systems, cultural heritage, and human-centered applications.[^8][^9][^10][^11]

**Key Features:**

- Cognitive grounding based on linguistic evidence and human categorization
- Rich axiomatization in first-order logic with proven consistency[^10]
- OntoClean methodology ensuring ontological rigor[^11]

**Use Cases:**

- **Cultural Heritage Management:** DOLCE has been used to develop and improve CIDOC CRM, the standard for museum and cultural heritage documentation[^11]
- **Manufacturing and Product Design:** Applied in engineering technical specifications and product lifecycle management[^12]
- **Semantic Web Integration:** Used to improve DBpedia and WordNet semantic resources[^11]

**Implementation for Neo4j:**
DOLCE's emphasis on natural language semantics makes it ideal for knowledge graphs requiring human-interpretable relationships. Its modular architecture (basic module, n-ary relations module, concepts/descriptions module) allows selective implementation based on use case complexity.[^12]

***

## Cybersecurity Ontologies

### Unified Cybersecurity Ontology (UCO)

**Description:** UCO is a community-developed ontology providing standardized information representation across the entire cybersecurity ecosystem. It integrates heterogeneous schemas from different security tools and incorporates commonly used standards including STIX, TAXII, MISP, CAPEC, CVE, and CWE. UCO is designed to support information integration, cyber situational awareness, and automated reasoning for threat intelligence, incident response, malware analysis, and vulnerability research.[^13][^14][^15]

**Key Features:**

- Unified representation eliminating need for point-to-point mappings between security tools
- Mappings to Linked Open Data cloud enabling integration with general world knowledge[^14]
- Support for temporal reasoning and event correlation[^14]

**Use Cases:**

- **Threat Intelligence Sharing:** Organizations use UCO to automatically exchange indicators of compromise (IoCs), threat actor profiles, and attack patterns across different security platforms without manual translation[^13]
- **Incident Response Automation:** Security operations centers leverage UCO to correlate alerts from SIEM, EDR, and network monitoring tools, automatically identifying attack campaigns and affected assets[^13][^14]
- **Vulnerability Management:** Linking CVE entries with asset inventories, exploit databases (CAPEC), and patch management systems through UCO enables prioritized remediation based on actual organizational risk[^14]

**Implementation for Neo4j:**
UCO's focus on relationships between cyber entities (threats, vulnerabilities, assets, events) aligns perfectly with graph database structures. Implement UCO classes as node labels (`ThreatActor`, `Vulnerability`, `Asset`) and properties as node attributes, with UCO relationships as Neo4j edges enabling graph-based threat hunting queries.[^13]

***

## Industrial Control Systems and Critical Infrastructure

### ICS-SEC Knowledge Graph Ontology

**Description:** The ICS-SEC ontology provides formal OWL-DL representation of industrial control system components, operations, and cybersecurity threats. It covers the Purdue Enterprise Reference Architecture levels (0-4), modeling PLCs, RTUs, SCADA systems, HMIs, DCS, sensors, actuators, and their interconnections. The ontology integrates ICS-specific cybersecurity information from standards like IEC 62443, NIST SP 800-82, and MITRE ATT\&CK for ICS.[^16][^17]

**Key Features:**

- Multi-level architecture representation from field devices to enterprise networks
- Integration of operational technology (OT) and information technology (IT) security concepts
- Support for attack pattern modeling and vulnerability analysis specific to ICS environments[^16]

**Use Cases:**

- **ICS Asset Inventory and Dependency Mapping:** Manufacturing facilities use ICS-SEC to create comprehensive digital inventories of all control system components, mapping dependencies between PLCs, HMIs, and controlled processes to assess cascade failure risks[^16]
- **Threat Modeling for Critical Infrastructure:** Power utilities leverage the ontology to model attack scenarios against SCADA systems, simulating threat actor tactics (e.g., manipulating setpoints, disrupting communications) and evaluating defensive controls[^18][^19]
- **Compliance and Risk Assessment:** Oil and gas operators use ICS-SEC to map security controls to regulatory requirements (NERC CIP, ISA/IEC 62443), automatically identifying gaps and prioritizing remediation[^16]

**Implementation for Neo4j:**
Model ICS hierarchies as node hierarchies with levels as properties. Use relationship types like `CONTROLS`, `MONITORS`, `DEPENDS_ON` to capture operational dependencies. Integrate with UCO for cybersecurity threat modeling.[^17][^16]

### Critical Infrastructure System Ontology

**Description:** A multi-sectoral ontology modeling critical infrastructure across energy, water, transportation, telecommunications, and other sectors. It represents assets, functions, services, dependencies, and disruption scenarios for infrastructure protection and resilience planning.[^20][^21][^22]

**Key Features:**

- Cross-sector dependency modeling
- Disruption scenario generation and cascading failure analysis
- Integration with geographic and temporal information[^20]

**Use Cases:**

- **Interdependency Analysis:** Emergency management agencies model how power grid failures cascade to water treatment, telecommunications, and healthcare facilities, enabling coordinated response planning[^20]
- **Resilience Planning:** Transportation authorities use the ontology to simulate infrastructure disruptions (natural disasters, cyber attacks) and evaluate alternative routing and backup systems[^22]
- **Investment Prioritization:** Government agencies analyze which infrastructure upgrades provide maximum risk reduction across multiple sectors using graph-based criticality scoring[^20]

***

## Engineering and Manufacturing Ontologies

### Engineering Application Ontology

**Description:** Comprehensive ontology spanning mechanical, electrical, civil, software, chemical, biomedical, and aerospace engineering disciplines. It models engineering systems, subsystems, components, their properties, relationships, and design constraints for multi-disciplinary engineering projects.[^23][^24]

**Key Features:**

- Cross-disciplinary terminology harmonization
- Component-based system modeling with interfaces and interactions
- Integration of engineering processes and lifecycle stages[^24]

**Use Cases:**

- **Aerospace Systems Engineering:** Aircraft manufacturers use the ontology to integrate mechanical (airframe), electrical (avionics), and software (flight control) subsystems, ensuring consistent terminology across engineering teams and supply chain partners[^23]
- **Infrastructure Project Management:** Civil engineering firms leverage the ontology for large projects (bridges, buildings, tunnels) to coordinate structural, mechanical, and electrical engineering disciplines, tracking design decisions and change impacts[^23]
- **Product Lifecycle Management:** Consumer electronics companies use engineering ontologies to link design specifications, manufacturing processes, and maintenance procedures in digital twin environments[^23]

**Implementation for Neo4j:**
Create hierarchical component structures with `HAS_PART` relationships. Model engineering disciplines as node types with cross-disciplinary relationships (`INTERFACES_WITH`, `REQUIRES`, `SUPPLIES`). Link to BIM/CAD systems through external identifiers.[^23]

### ISO 15926 / Industrial Data Ontology (IDO)

**Description:** ISO standard for lifecycle integration of process plant data, particularly in oil, gas, and chemical industries. IDO provides upper-level ontology for industrial automation, equipment specifications, and engineering data exchange across the asset lifecycle.[^25][^26][^27]

**Key Features:**

- Lifecycle coverage from design through operations to decommissioning
- Integration with IEC 81346 for asset identification and classification
- OWL DL reasoning capabilities with engineer-accessible language[^25]

**Use Cases:**

- **Plant Engineering Data Integration:** Oil refineries integrate P\&IDs, 3D models, equipment specifications, and maintenance records using ISO 15926, enabling queries across previously siloed engineering systems[^27][^25]
- **Digital Handover:** EPC contractors deliver completed facilities to operators with ISO 15926-structured data, ensuring operators receive complete, standardized information for operation and maintenance[^27]
- **Asset Information Management:** Chemical plants maintain "golden records" of all equipment linked to design documentation, operational data, and maintenance history throughout multi-decade lifecycles[^25]

***

## Business and Enterprise Architecture Ontologies

### Business Ontology (LEADing Practice)

**Description:** The LEADing Practice Business Ontology provides standardized representation of business concepts including value creation, business models, operating models, organizational capabilities, governance, and strategic positioning. Developed by Global University Alliance, it has been applied successfully in organizational transformation projects.[^28][^29][^30]

**Key Features:**

- Comprehensive business terminology standardization
- Integration with enterprise architecture frameworks
- Support for business model innovation and transformation[^29][^28]

**Use Cases:**

- **Mergers and Acquisitions Integration:** Companies use the Business Ontology to map and harmonize business processes, capabilities, and information flows between merging organizations, accelerating post-merger integration[^28]
- **Business Model Innovation:** Organizations leverage the ontology to explore new value propositions, revenue models, and operating structures by systematically analyzing current-state architectures and designing future states[^28]
- **Regulatory Compliance Mapping:** Financial institutions map regulatory requirements to business capabilities and processes using standardized terminology, ensuring comprehensive compliance coverage and efficient audit trails[^30][^28]


### ArchiMate Ontology

**Description:** ArchiMate is an Open Group standard for enterprise architecture modeling, providing integrated representation of business, application, and technology layers. The ArchiMate ontology (ArchiMEO) extends the conceptual model with semantic richness, enabling reasoning and integration across enterprise architecture tools.[^31][^32][^33]

**Key Features:**

- Multi-layer architecture (business, application, technology, physical)
- Rich relationship types (composition, aggregation, realization, serving)
- Integration with TOGAF and other EA frameworks[^34][^31]

**Use Cases:**

- **Enterprise Transformation Planning:** Large organizations use ArchiMate to model current and target architectures, performing gap analysis and generating transformation roadmaps that coordinate business process changes with IT system implementations[^34]
- **Portfolio Management:** IT departments leverage ArchiMate to visualize which applications support which business capabilities, enabling rationalization decisions and cloud migration prioritization[^34]
- **Impact Analysis:** When planning system changes or retirements, architects use ArchiMate graphs to trace dependencies across business processes, applications, and infrastructure components, identifying all affected stakeholders[^32][^33]

***

## IT, Cloud, and Networking Ontologies

### ICT Infrastructure High-Level Ontology Network

**Description:** A suite of nine interconnected ontologies representing IT infrastructure configuration items including data centers, servers, networks, software, databases, hardware, and security components. Designed for Configuration Management Databases (CMDB) and IT Service Management (ITSM) systems.[^35][^36][^37]

**Key Features:**

- Modular architecture with core ontology and domain-specific modules
- Integration with TMForum Open APIs and industry standards
- Support for cloud, hybrid, and on-premises infrastructure[^36][^35]

**Use Cases:**

- **Disaster Recovery Planning:** Cloud service providers use the ICT ontology to model primary and backup infrastructure, automatically generating failover scenarios and validating recovery time objectives (RTOs)[^35]
- **Service Impact Analysis:** When performance degradation occurs, IT operations teams trace from affected products/services through supporting infrastructure (applications, servers, networks, databases) to identify root causes[^37][^36]
- **Multi-Cloud Management:** Enterprises managing resources across AWS, Azure, and on-premises data centers use the ontology to create unified infrastructure views, optimizing workload placement and cost[^36]


### SAREF (Smart Applications REFerence Ontology)

**Description:** ETSI European standard ontology for IoT and smart applications enabling semantic interoperability across vertical domains. SAREF core models devices, functions, states, and services, with extensions for energy (SAREF4ENER), buildings (SAREF4BLDG), industry/manufacturing (SAREF4INMA), agriculture (SAREF4AGRI), cities (SAREF4CITY), and more.[^38][^39][^40]

**Key Features:**

- Lightweight, extensible core with domain-specific modules
- Mappings to oneM2M IoT framework and major IoT platforms
- Support for device capabilities, measurements, and actuations[^41][^38]

**Use Cases:**

- **Smart Building Management:** Facility managers integrate HVAC, lighting, security, and energy management systems using SAREF4BLDG, enabling coordinated optimization (e.g., adjusting lighting and HVAC based on occupancy sensors)[^38][^41]
- **Industrial IoT Integration:** Manufacturing plants use SAREF4INMA to integrate PLCs, robots, sensors, and MES systems, creating unified digital twins of production lines for real-time monitoring and predictive maintenance[^41]
- **Smart City Platforms:** Cities deploy SAREF4CITY to integrate traffic management, waste collection, environmental monitoring, and public services, enabling data-driven urban planning and citizen services[^42][^38]


### SOSA/SSN (Sensor, Observation, Sample, Actuator / Semantic Sensor Network)

**Description:** W3C/OGC standard lightweight ontology for modeling sensors, observations, actuators, sampling, and IoT systems. SOSA provides the minimal core, while SSN adds richer axiomatization for advanced reasoning.[^43][^44][^45]

**Key Features:**

- Minimal dependencies enabling broad adoption
- Support for sensor networks, satellite systems, and citizen science
- Alignment with other ontologies (PROV, DUL, OGC O\&M)[^46][^43]

**Use Cases:**

- **Environmental Monitoring Networks:** Research institutions deploy SOSA to integrate weather stations, water quality sensors, and air quality monitors, creating queryable knowledge graphs of environmental conditions over time[^44][^45]
- **Industrial Asset Monitoring:** Oil and gas facilities use SSN to model sensor networks monitoring pressure, temperature, flow, and vibration across distributed infrastructure, enabling predictive maintenance and safety monitoring[^44]
- **Smart Agriculture:** Precision agriculture systems leverage SOSA/SSN to integrate soil moisture, weather, and crop health sensors, optimizing irrigation and fertilization based on real-time observations[^46]

***

## Digital Twin Ontologies

### Digital Twin Ontology Framework (Manufacturing)

**Description:** Three-layer knowledge graph architecture for digital twins consisting of: (1) Concept Layer providing domain ontologies and rules, (2) Model Layer instantiating physical-virtual parameter mappings, and (3) Decision Layer leveraging real-time data for optimization and predictive analytics. Validated in aerospace manufacturing with proven quality improvements.[^47][^48]

**Key Features:**

- Multi-layer separation of concerns (concepts, models, decisions)
- Real-time bidirectional synchronization between physical and virtual entities
- Integration of multi-source heterogeneous data (IoT, ERP, MES, quality systems)[^47]

**Use Cases:**

- **Aerospace Blade Manufacturing:** Aero-engine manufacturers implement the framework to create digital twins of blade production, integrating machining process models with real-time sensor data. Over 5 months, precision improved from 0.073mm to 0.062mm and qualification rate increased from 81.3% to 85.2%[^47]
- **Process Optimization:** Discrete manufacturers use the decision layer to continuously optimize process parameters (feed rates, temperatures, pressures) based on real-time quality measurements and predictive models[^47]
- **Anomaly Detection and Root Cause Analysis:** The integrated knowledge graph enables automated detection of process deviations and tracing through material properties, equipment status, and environmental conditions to identify root causes[^47]


### Building Digital Twin Ontology Network (SPHERE)

**Description:** Network of open reference ontologies for building lifecycle management integrating Industry Foundation Classes (IFC), SAREF, Building Information Modeling (BIM), and circular economy concepts. Supports distributed energy resources, smart grids, lifecycle assessment (LCA), and material passports.[^49]

**Key Features:**

- Unified network approach avoiding one-size-fits-all monolithic ontologies
- Use case-based extensions (smart energy, circular economy)
- Open Digital Twin API for ecosystem interoperability[^49]

**Use Cases:**

- **Building Lifecycle Management:** Property owners maintain digital twins from design through construction to operations and eventual demolition, integrating architectural models (IFC), IoT sensor data (SAREF), and maintenance records for optimized facility management[^49]
- **Energy Performance Optimization:** Building managers use SPHERE to integrate building automation systems with smart grid connections, optimizing energy consumption based on occupancy patterns, weather forecasts, and electricity pricing[^49]
- **Circular Economy and Material Passports:** Architects and developers create material passports documenting all building materials' environmental impacts, recyclability, and reusability, supporting deconstruction planning and circular material flows[^49]

***

## Financial Services Ontology

### FIBO (Financial Industry Business Ontology)

**Description:** EDM Council/OMG standard formal ontology for financial services covering securities, derivatives, loans, indices, market data, business entities, contracts, and regulatory reporting. Developed through consensus of financial industry experts and standardized in OWL with extensive human-readable documentation.[^50][^51][^52]

**Key Features:**

- Comprehensive coverage of financial instruments, parties, transactions, and regulations
- Quarterly updates reflecting evolving market practices
- Alignment with industry standards (ISO 20022, FpML, ACTUS)[^53][^52]

**Use Cases:**

- **Securities Master Data Management:** Investment banks use FIBO to create unified views of securities across trading, risk, and operations systems, resolving conflicts in instrument identifiers, corporate actions, and reference data[^52][^54]
- **Regulatory Reporting Automation:** Financial institutions map regulatory reporting requirements (MiFID II, Dodd-Frank, Basel III) to FIBO concepts, automating report generation and ensuring consistency across jurisdictions[^54][^53]
- **Risk Analysis and Stress Testing:** Banks leverage FIBO to integrate positions, market data, and counterparty relationships into knowledge graphs supporting risk calculations, scenario analysis, and stress testing[^53][^52]

***

## E-Commerce and Structured Data Ontologies

### GoodRelations (integrated into Schema.org)

**Description:** Lightweight ontology for e-commerce describing products, offers, prices, business entities, opening hours, payment options, delivery terms, and warranties. Originally independent, GoodRelations was integrated into Schema.org in 2012, becoming the standard e-commerce data model.[^55][^56][^57]

**Key Features:**

- Comprehensive commercial relationship modeling
- Support for complex pricing (quantity discounts, bundles, B2B terms)
- Integration with product classification systems (eClassOWL, UNSPSC)[^57]

**Use Cases:**

- **E-Commerce SEO:** Online retailers markup product pages with GoodRelations/Schema.org, enabling rich snippets in Google search results showing prices, availability, and ratings, significantly increasing click-through rates[^58][^55]
- **Price Comparison Services:** Shopping aggregators consume GoodRelations data from multiple retailers, creating unified product catalogs with real-time pricing and availability comparisons[^56][^59]
- **B2B Marketplaces:** Industrial suppliers use GoodRelations to publish complex offers with quantity discounts, delivery terms, and technical specifications, enabling automated procurement systems[^57]


### Schema.org

**Description:** Collaborative standard vocabulary for structured data on web pages, developed by Google, Microsoft, Yahoo, and Yandex. Provides hierarchical type system with 803 types and 1461 properties covering products, people, events, organizations, and more.[^60][^61][^62]

**Key Features:**

- Major search engine support for rich results
- Multiple serialization formats (JSON-LD, Microdata, RDFa)
- Active community development with domain extensions[^62][^60]

**Use Cases:**

- **Content Discovery and SEO:** Publishers markup articles, videos, and recipes with Schema.org, enabling Google to display rich results (headlines, images, ratings) that drive traffic[^63][^60]
- **Voice Assistant Integration:** E-commerce sites use Schema.org to structure product information, enabling voice assistants (Alexa, Google Assistant) to answer product queries and facilitate voice shopping[^60]
- **Knowledge Graph Population:** Search engines use Schema.org markup to extract structured data from web pages, populating knowledge graphs that power direct answers and entity cards in search results[^61][^64]

***

## Integration and Implementation Strategies

### Cross-Domain Ontology Integration

**Best Practices:**

1. **Start with Foundational Ontologies:** Implement BFO or DOLCE as top-level structure, ensuring consistency across domain ontologies[^8][^1]
2. **Use Modular Architecture:** Adopt SAREF's modular approach with core concepts and domain-specific extensions[^39][^40]
3. **Leverage Existing Alignments:** Many ontologies provide mappings (e.g., SOSA to DOLCE, SAREF to SSN, GoodRelations to Schema.org), enabling interoperability[^43][^55]
4. **Implement Governance:** Establish ontology working groups similar to DOD/IC DIOWG to maintain consistency and coordinate updates[^65][^6]

### Neo4j Implementation Patterns

**Ontology-to-Graph Mapping:**

- **Classes → Node Labels:** OWL/RDFS classes become Neo4j node labels
- **Properties → Node Properties:** Data properties become node attributes
- **Object Properties → Relationships:** Object properties become typed relationships
- **Class Hierarchies → Label Hierarchies:** Use multiple labels for subclass relationships

**Example Neo4j Cypher for UCO Threat Modeling:**

```cypher
// Create threat actor
CREATE (ta:ThreatActor:Agent {
  name: "APT29",
  sophistication: "Advanced",
  motivation: "Espionage"
})

// Create vulnerability
CREATE (vuln:Vulnerability {
  cve_id: "CVE-2024-1234",
  severity: "Critical",
  cvss_score: 9.8
})

// Create asset
CREATE (asset:Asset:InformationSystem {
  name: "Email Server",
  criticality: "High"
})

// Create relationships
CREATE (ta)-[:EXPLOITS]->(vuln)
CREATE (vuln)-[:AFFECTS]->(asset)
```


### Digital Twin Knowledge Graph Architecture

**Recommended Stack:**

1. **Foundational Layer:** BFO for core entity types and relationships
2. **Domain Layer:**
    - ICS-SEC for industrial equipment
    - Engineering Application Ontology for system components
    - Critical Infrastructure Ontology for dependencies
3. **Operational Layer:**
    - SOSA/SSN for sensor observations
    - SAREF extensions for device capabilities
    - UCO for cybersecurity monitoring
4. **Business Layer:**
    - Business Ontology for processes and capabilities
    - ArchiMate for enterprise architecture
5. **Integration Layer:** Custom mappings and transformations

This multi-layer approach enables comprehensive digital twins that integrate physical assets, operations, cybersecurity, and business processes in a unified knowledge graph optimized for Neo4j querying and reasoning.[^48][^49][^47]

***

## Conclusion

The 23 ontology frameworks detailed in this report provide comprehensive coverage for building knowledge graph schemas optimized for Neo4j-based digital twins of organizations and critical infrastructure facilities. By combining foundational ontologies (BFO, DOLCE) with domain-specific frameworks (UCO, ICS-SEC, Engineering Application Ontology, SAREF, FIBO) and integration standards (Schema.org, SOSA/SSN), organizations can create interoperable, semantically rich knowledge graphs supporting real-time monitoring, predictive analytics, and intelligent decision-making across cyber-physical systems.[^15][^66][^67][^68][^50][^36][^1][^8][^43][^13][^49][^47]
<span style="display:none">[^100][^101][^102][^103][^104][^105][^106][^107][^108][^109][^110][^111][^69][^70][^71][^72][^73][^74][^75][^76][^77][^78][^79][^80][^81][^82][^83][^84][^85][^86][^87][^88][^89][^90][^91][^92][^93][^94][^95][^96][^97][^98][^99]</span>

<div align="center">⁂</div>

[^1]: https://en.wikipedia.org/wiki/Basic_Formal_Ontology

[^2]: https://www.sciencedirect.com/topics/computer-science/basic-formal-ontology

[^3]: https://www.buffalo.edu/cas/philosophy/news/latestnews/global-ontology.html

[^4]: https://www.buffalo.edu/news/releases/2024/02/department-of-defense-ontology.html

[^5]: https://www.research.autodesk.com/publications/a-first-order-logic-formalization-of-the-industrial-ontologies-foundry-signature-using-basic-formal-ontology/

[^6]: https://www.buffalo.edu/cas/philosophy/news/latestnews/smith-top-level-ontologies.html

[^7]: https://basic-formal-ontology.org

[^8]: https://arxiv.org/abs/2308.01597

[^9]: https://ontolearner.readthedocs.io/benchmarking/upper_ontology/dolce.html

[^10]: http://www.loa.istc.cnr.it/dolce/overview.html

[^11]: https://www.danieleporello.net/papers/BorgoEtAlAO2022.pdf

[^12]: https://www.utwente.nl/en/eemcs/fois2024/resources/papers/porello-et-al-dolce-in-owl.pdf

[^13]: https://www.unifiedcyberontology.org/ontology/start.html

[^14]: https://ebiquity.umbc.edu/_file_directory_/papers/781.pdf

[^15]: https://github.com/Ebiquity/Unified-Cybersecurity-Ontology

[^16]: https://publications.sba-research.org/publications/ISWC24_ICS-SEC__Andreas%20Ekelhart.pdf

[^17]: https://github.com/sepses/ics-sec-kg

[^18]: https://scholarworks.boisestate.edu/cgi/viewcontent.cgi?article=3118\&context=td

[^19]: https://par.nsf.gov/servlets/purl/10327905

[^20]: https://re.public.polimi.it/retrieve/e0c31c0f-0b70-4599-e053-1705fe0aef77/PSAM12_Paper%20365_final.pdf

[^21]: https://www.sciencedirect.com/science/article/abs/pii/S1874548223000471

[^22]: https://www.academia.edu/82635366/Ontology_based_approach_to_disruption_scenario_generation_for_critical_infrastructure_systems

[^23]: https://www.scribd.com/document/929424916/Engineering-Application-Ontology

[^24]: https://ris.utwente.nl/ws/portalfiles/portal/6642675/Borst97engineering.pdf

[^25]: https://rds.posccaesar.org/WD_IDO.pdf

[^26]: https://www.sciencedirect.com/science/article/pii/S1570794605800999

[^27]: https://readi-jip.org/wp-content/uploads/2020/10/ISO_15926-14_2020-09-READI-Deliverable.pdf

[^28]: https://www.leadingpractice.com/wp-content/uploads/2020/03/Using-the-LEAD-Ontology-to-Transform-three-leading-organizations-Connectwise.pdf

[^29]: https://www.leadingpractice.com/enterprise-standards/enterprise-engineering/enterprise-ontology/

[^30]: https://www.globaluniversityalliance.org/wp-content/uploads/2017/10/The-Business-Ontology-Research-Analysis.pdf

[^31]: https://www.scitepress.org/Papers/2020/90002/90002.pdf

[^32]: https://www.linkedin.com/pulse/bridging-enterprise-modeling-ontologies-toward-fair-knowledge-figay-bi89e

[^33]: https://ieeexplore.ieee.org/document/6690082/

[^34]: https://blog.opengroup.org/2018/01/25/real-case-application-of-archimate-an-open-group-standard/

[^35]: https://oa.upm.es/72099/3/2021_ISWC_DevOps_Infra.pdf

[^36]: https://davidchavesfraga.com/outcomes/papers/2021/corcho2021high.pdf

[^37]: https://www.semantic-web-journal.net/content/noria-o-ontology-anomaly-detection-and-incident-management-ict-systems

[^38]: https://www.embedded.com/an-iot-ontology-for-cross-domain-smart-applications/

[^39]: https://saref.etsi.org/core/

[^40]: https://saref.etsi.org

[^41]: https://digital-strategy.ec.europa.eu/en/library/workshop-explores-role-saref-enhancing-iot-semantic-interoperability-digital-twins

[^42]: https://2020.standict.eu/saref-etsi

[^43]: https://w3c.github.io/sdw-sosa-ssn/ssn/

[^44]: https://www.semantic-web-journal.net/system/files/swj1804.pdf

[^45]: https://www.w3.org/TR/vocab-ssn/

[^46]: https://data.ontocommons.linkeddata.es/vocabulary/Sensor,Observation,Sample,AndActuator(sosa)Ontology

[^47]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11997226/

[^48]: https://www.itcon.org/papers/2025_14-ITcon-Ghorbani.pdf

[^49]: https://buildingdigitaltwin.org/wp-content/uploads/2022/11/Sphere_Digital_Twins_White_Paper-3-.pdf

[^50]: https://edmcouncil.org/frameworks/industry-models/fibo/

[^51]: https://spec.edmcouncil.org/fibo/

[^52]: https://github.com/edmcouncil/fibo

[^53]: https://www.ontotext.com/blog/fibo-in-context/

[^54]: https://globalfintechseries.com/featured/financial-information-business-ontology-fibo-architecture-use-cases-and-implementation-challenges/

[^55]: https://www.w3.org/wiki/GoodRelations

[^56]: https://en.wikipedia.org/wiki/GoodRelations

[^57]: http://www.heppnetz.de/projects/goodrelations/primer/

[^58]: https://blog.mynarz.net/2011/04/data-driven-e-commerce-with.html

[^59]: https://www.heppnetz.de/projects/goodrelations/

[^60]: https://www.seozoom.com/schema-org/

[^61]: https://schema.org/docs/datamodel.html

[^62]: https://schema.org

[^63]: https://www.conductor.com/academy/schema/

[^64]: https://en.wikipedia.org/wiki/Schema.org

[^65]: https://www.cubrc.org/data-science-information-fusion/specialized-data-ontology-development/

[^66]: https://neo4j.com/apoc/5/nlp/build-knowledge-graph-nlp-ontologies/

[^67]: https://neo4j.com/blog/knowledge-graph/ontologies-in-neo4j-semantics-and-knowledge-graphs/

[^68]: https://deepsense.ai/resource/ontology-driven-knowledge-graph-for-graphrag/

[^69]: https://www.darktrace.com/cyber-ai-glossary/industrial-control-system-security

[^70]: https://www.kuppingercole.com/blog/ashford/navigator-securing-industrial-control-systems-ics

[^71]: https://www.fortinet.com/resources/cyberglossary/ics-security

[^72]: https://www.sciencedirect.com/science/article/abs/pii/S0306437915000745

[^73]: https://www.caseontology.org/resources/case_design_document.html

[^74]: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=956387

[^75]: https://www.paloaltonetworks.com/cyberpedia/what-is-ics-security

[^76]: https://www.semanticscholar.org/paper/UCO:-A-Unified-Cybersecurity-Ontology-Syed-Padia/67b3c0893013cbdcc9f35ec9359fa4466df7360e

[^77]: https://gca.isa.org/blog/industrial-control-system-ics-security-and-segmentation

[^78]: https://caminao.blog/knowledge-architecture/ontologies-ea/

[^79]: https://www.utwente.nl/en/eemcs/fois2024/resources/papers/dawood-marengwa-ontology-driven-cybersecurity-learning-factory-a-use-case-for-securing-electricity-utilities.pdf

[^80]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10932805/

[^81]: https://opendl.ifip-tc6.org/db/conf/cnsm/cnsm2024/1571066299.pdf

[^82]: https://ontology.buffalo.edu/smith/articles/ICBO2012/MFO_Hastings.pdf

[^83]: https://scibite.com/wp-content/uploads/2024/10/SciBite-Use-Case_Democratised-Ontology-Management_UC016v2.pdf

[^84]: https://github.com/jannahastings/mental-functioning-ontology

[^85]: https://graphwise.ai/blog/the-power-of-ontologies-and-knowledge-graphs-practical-examples-from-the-financial-industry/

[^86]: https://pubmed.ncbi.nlm.nih.gov/37702040/

[^87]: https://www.reddit.com/r/semanticweb/comments/1fqec66/best_ontology_development_environment_tool/

[^88]: https://atlarge-research.com/pdfs/2024-graphsys-ontology.pdf

[^89]: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.673586/full

[^90]: https://enterprise-knowledge.com/keys-to-successful-ontology-design/

[^91]: https://asset-group.github.io/papers/SCOPES_ontology.pdf

[^92]: http://obofoundry.org/ontology/mf.html

[^93]: https://www.sciencedirect.com/science/article/abs/pii/S0169023X1500110X

[^94]: https://www.sciencedirect.com/science/article/abs/pii/S0926580517308907

[^95]: https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2011.00017/full

[^96]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3167196/

[^97]: https://www.sciencedirect.com/science/article/pii/S0167739X23004739

[^98]: https://processgenius.eu/articles/what-is-digital-twin-ontology/

[^99]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4701616/

[^100]: https://learn.microsoft.com/en-us/azure/digital-twins/concepts-ontologies-adopt

[^101]: https://www.sciencedirect.com/science/article/pii/S0926580525001517

[^102]: https://www.cognitiveatlas.org

[^103]: https://dl.acm.org/doi/10.1145/3652620.3688261

[^104]: https://www.cogitatiopress.com/urbanplanning/article/download/10109/4602

[^105]: https://cogat-python.readthedocs.io

[^106]: https://bentleyjoakes.github.io/assets/publications/Oakes2024-Towards_Ontological_Service-Driven_Engineering_of_Digital_Twins.pdf

[^107]: https://iowngf.org/wp-content/uploads/2025/02/Digital_Twin_Framework_Analysis_Report.pdf

[^108]: https://bioportal.bioontology.org/ontologies/COGAT

[^109]: https://www.youtube.com/watch?v=fX6zNzpH4rY

[^110]: https://www.nist.gov/publications/towards-ontologizing-digital-twin-framework-manufacturing

[^111]: https://www.nature.com/articles/npre.2010.4532.1.pdf

