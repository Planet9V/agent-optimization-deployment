# M&A-Focused SBOM/SCA Due Diligence Questionnaire

This document is designed to gather the necessary information to accurately scope an SBOM and SCA assessment in the context of a Mergers and Acquisitions (M&A) transaction. The acquiring company will use this assessment to evaluate the software supply chain risks associated with the target company.

## 1. Introduction

This questionnaire is designed to gather the necessary information to accurately scope an SBOM and SCA assessment in the context of a Mergers and Acquisitions (M&A) transaction. Your responses will enable us to understand the specific needs of the acquiring company, define project requirements, and develop a tailored proposal for due diligence.

## 2. Project Information

Provide general information about the project.

|     |                        |                 |
| --- | ---------------------- | --------------- |
|     | **Field**              | **Description** |
|     | Acquiring Company Name |                 |
|     | Target Company Name    |                 |
|     | Date                   |                 |
|     | Prepared By            |                 |

## 3. Project Overview

Provide a high-level description of the M&A transaction and its objectives.

- Brief description of the M&A transaction and its objectives:
    
- Identify the business drivers for this assessment (e.g., identify potential risks associated with the acquisition):
    
- Define the overall scope, including all in-scope and out-of-scope systems, applications, and environments at the Target Company:
    

## 4. Target Company Product/System Inventory

Provide an inventory of the products, software stacks, or devices of the Target Company that are in scope for this assessment. Repeat the table as needed.

|                      |                                    |                 |
| -------------------- | ---------------------------------- | --------------- |
| **Product/System #** | **Product/System Name/Identifier** | **Description** |
| 1                    |                                    |                 |
| 2                    |                                    |                 |
| 3                    |                                    |                 |
| 4                    |                                    |                 |
| 5                    |                                    |                 |
| 6                    |                                    |                 |
| 7                    |                                    |                 |
| 8                    |                                    |                 |

## 5. Target Company Architecture Assessment

This section provides a structured approach to documenting the architecture of each system, product, or device in scope. Repeat this section for _each_ Product/System listed in Section 4. Clearly indicate which Product/System # this assessment pertains to.

### Product/System #: (Reference # from Section 4)

### 5.1 Product/System Name/Identifier:

Provide a unique identifier for the system, product, or device. (Redundant, but included for clarity in this section)

### 5.2 Product/System Description:

Describe the system, product, or device, including its purpose, function, and key features.

### 5.3 Architecture Overview:

Provide a high-level architectural diagram or description, including:

- Hardware components and their relationships
    
- Software components, libraries, and dependencies
    
- Network topology and connections
    
- Data flow and storage
    

Identify any hierarchical structures or dependencies between subsystems.

### 5.4 Technologies Used:

List all programming languages, frameworks, operating systems, and technologies used in the system. Specify versions where applicable.

|   |   |   |   |
|---|---|---|---|
||**Technology**|**Description**|**Version**|
||Programming Language(s)|||
||Framework(s)|||
||Operating System(s)|||
||Other Technologies|||

### 5.5 Deployment Environment:

Describe the deployment environment (e.g., cloud, on-premises, embedded, mobile). Identify any relevant infrastructure components (e.g., servers, containers, virtual machines).

## 6. SBOM Requirements

This section details the requirements for Software Bill of Materials (SBOM) generation for each system or product. Repeat this section for _each_ Product/System listed in Section 4. Clearly indicate which Product/System # this assessment pertains to.

### Product/System: (Reference # from Section 4)

### 6.1 SBOM Generation:

Describe the requirements for SBOM generation, including the types of software components to be included and any Hardware Bill of Materials (HBOM) requirements.

- What types of software components need to be included in the SBOM (e.g., open-source, third-party, custom)?
    
- Are there any specific requirements for HBOM generation? If so, please describe:
    
- What methods or tools are currently used (if any) for SBOM/HBOM generation at the Target Company?
    
- **Artifacts Provided:** Please specify the types and state of software artifacts that will be provided for analysis (e.g., source code, binaries, executables, container images, build files). For example:
    
    - Source code repositories (Git, SVN, etc.)
        
    - Build scripts (e.g., Maven, Gradle, Makefiles)
        
    - Compiled binaries (e.g., ELF, PE)
        
    - Container images (e.g., Docker)
        
    - Installation packages (e.g., RPM, DEB)
        
    - Firmware images
        
    - Hardware schematics
        
- **Platform/Language**: Please specify the platforms and codebases.
    
    - e.g., Linux, Windows, IoT, Node.js, .NET, MacOS, Java, Elixir, C#
        

### 6.2 SBOM Formats:

Specify the required SBOM formats and versions.

|   |   |   |   |
|---|---|---|---|
||**SBOM Format**|**Required**|**Version**|
||SPDX|||
||CycloneDX|||
||Other|||

### 6.3 SBOM Data Fields:

Describe the required level of detail and any specific data fields.

- What level of detail is required for the SBOM data? (e.g., NTIA minimum elements, additional fields)
    
- Are there any specific data fields that are critical for this project? (e.g., license, vulnerability, provenance)
    

### 6.4 SBOM Hierarchy:

Describe how the system's hierarchical structure should be represented in the SBOM.

### 6.5 SBOM Output:

Specify the desired output format and any reporting requirements.

|   |   |   |
|---|---|---|
||**Output Format**|**Description**|
||JSON||
||XML||
||Other||

## 7. SCA Requirements

This section outlines the requirements for Software Composition Analysis (SCA) for each system or product. Repeat this section for _each_ Product/System listed in Section 4. Clearly indicate which Product/System # this assessment pertains to.

### Product/System #:_ (Reference # from Section 4)

### 7.1 SCA Scope:

Describe the scope of the SCA, including the types of analysis required, programming languages, and frameworks.

- What types of analysis are required (e.g., vulnerability detection, license compliance)?
    
- What programming languages, frameworks, and package managers are used?
    
- Are there any specific dependencies or components that require extra attention?
    
- **Platforms/Languages**:
    
    - What platforms and languages are used (e.g., Linux, Windows, IoT, Node.js, .NET, MacOS, Java, Elixir, C#)
        

### 7.2 Vulnerability Detection:

Specify the vulnerability databases to be used and the acceptable threshold for vulnerability severity.

|   |   |   |   |
|---|---|---|---|
||**Vulnerability Database**|**Used**|**Severity Threshold**|
||NVD|||
||CVE|||
||Other|||

### 7.3 License Compliance:

Describe the license compliance requirements and any prohibited or special-handling licenses.

- What are the license compliance requirements and policies?
    
- Are there any specific licenses that are prohibited or require special handling?
    

### 7.4 SCA Reporting:

Specify the desired output format and any reporting requirements for SCA reports.

|   |   |   |
|---|---|---|
||**Report Format**|**Description**|
||JSON||
||XML||
||SARIF||
||Other||

### 7.5 SCA Integration:

Describe how SCA results should be delivered and integrated into existing systems or workflows.

## 8. M&A Due Diligence Focus

This section highlights key areas relevant to M&A due diligence, focusing on software supply chain risks.

### 8.1 Target Company/System:

Identify the target company or system being evaluated.

### 8.2 Codebase Analysis:

Describe the size, complexity, and history of the codebase.

- What is the size and complexity of the codebase?
    
- What is the history of the codebase (e.g., age, number of contributors, commit frequency)? Are there any indications of unusual code contributions or rapid development cycles that could introduce risk?
    

### 8.3 Software Composition Analysis (SCA):

Perform a comprehensive SCA to identify:

- Open-source software (OSS) components and their versions: What is the target company's reliance on OSS, and are the versions up-to-date and patched?
    
- Third-party libraries and dependencies: What is the target company's process for vetting and managing third-party dependencies?
    
- Known vulnerabilities in OSS and third-party components: What is the severity and exploitability of known vulnerabilities? (Cross-reference with VEX data - see section 13)
    
- License compliance issues and potential legal risks: Are there any OSS licenses that could create obligations for the acquiring company (e.g., copyleft licenses)?
    

Assess the target's SCA practices and tools: What tools and processes does the target company have in place for performing SCA? How mature are their practices?

### 8.4 Static Application Security Testing (SAST):

Perform SAST to identify potential security vulnerabilities in the source code.

- Common coding flaws (e.g., buffer overflows, SQL injection): Are there any patterns of insecure coding practices?
    
- Security misconfigurations: Are there any insecure default settings or misconfigurations?
    
- Hardcoded credentials or secrets: Has the target company implemented adequate controls to prevent hardcoded credentials?
    

Assess the target's SAST practices and tools: What tools and processes does the target company have in place for performing SAST? How frequently is SAST performed?

### 8.5 Intellectual Property (IP) Review:

Conduct an IP review to identify potential risks.

- Ownership of the codebase and its components: Does the target company have clear ownership of its software assets? Are there any disputes or potential claims?
    
- Infringement of third-party patents or copyrights: Has the target company conducted any IP clearance or freedom-to-operate analysis?
    
- Compliance with open-source licenses: Are there any inconsistencies between the claimed licenses and the actual usage of OSS components?
    

Assess the target's IP management practices: What processes does the target company have in place for managing and protecting its IP?

### 8.6 Provenance Analysis:

Analyze the provenance of software components to determine their origin and supply chain.

- Identifying the original sources of OSS components: Can the target company trace the origin of all OSS components used in their products?
    
- Tracing the history of code modifications and contributions: Are there clear records of who has modified the code and why?
    
- Assessing the risk of supply chain attacks: What is the likelihood that the target company's software has been compromised by a supply chain attack?
    

Evaluate the target's practices for ensuring code provenance: What controls does the target company have in place to ensure the integrity of their software supply chain?

### 8.7 Supply Chain Risk Assessment:

Evaluate the target's overall supply chain risk, considering factors such as:

- Number and criticality of third-party suppliers: How reliant is the target company on external suppliers for critical software components?
    
- Geographic distribution of suppliers: Are there any geopolitical risks associated with the location of the target company's suppliers?
    
- Supplier security practices and certifications: Do the target company's suppliers have adequate security practices and certifications (e.g., ISO 27001, SOC 2)?
    
- Reliance on high-risk or vulnerable suppliers: Does the target company rely on any suppliers with a history of security breaches or vulnerabilities?
    
- How does the target company assess the risk of its suppliers?
    

### 8.8 Executive Order 14028 and Industry Standards Compliance:

Assess the target's compliance with relevant standards and regulations, including:

- SBOM generation and maintenance practices: Does the target company generate and maintain SBOMs for their software products? Are their practices mature and well-documented?
    
- Vulnerability disclosure and remediation processes: How does the target company disclose and remediate vulnerabilities in their software? Do they have a clear process and track record?
    
- Secure software development practices: What secure software development practices (e.g., secure coding guidelines, threat modeling, penetration testing) does the target company follow?
    
- Compliance with U.S. Executive Order 14028: Is the target company compliant with the requirements of EO 14028, if applicable?
    
- Compliance with industry standards (e.g., IEC 62443, OWASP): Does the target company adhere to relevant industry standards for security? What Security Level (SL) is claimed or required for IEC 62443?
    

### 8.9 Sovereign Data and Code/Device Restrictions:

- Are there any sovereign data restrictions that would impact the acquiring company's ability to use or modify the target company's code or devices?
    
- Are there any restrictions on the transfer of code or devices across international borders?
    

### 8.10 Backdoor and Malware Assessment

- What processes does the target company have in place to prevent the introduction of backdoors or malware into their software or hardware?
    
- Has the target company conducted any independent security audits or penetration testing to detect potential backdoors or malware?
    
- What is the target company's incident response plan for dealing with a potential security breach involving backdoors or malware?