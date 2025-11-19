# Part 3 of 4: Analysis & Automation

**Series**: Taranis AI
**Navigation**: [← Part 2](./02_Intelligence_Collection.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Deployment_Integration.md)

---

- Designed based on user stories from national authorities and CERTs
- Used by multiple European CSIRT teams (specific deployments not publicly disclosed for security reasons)

**Benefits:**
- Reduced time to threat detection
- Comprehensive visibility across disparate sources
- Automated correlation of related threat indicators
- Improved incident response preparedness

### 9.2 National Authority Cyber Situational Awareness

**Primary Use Case:** NIS (Network and Information Security) Authorities

**Application:**
- National-level monitoring of cyber threat landscape
- Identification of threats to critical infrastructure
- Support for cyber defense policy and strategy
- Coordination of cross-sector threat intelligence

**European Defence Fund Integration:**
- **AWAKE Project:** Assessment for advanced intelligence analysis
- **NEWSROOM Project:** Mission-oriented cyber situational awareness from clear and dark web
- **EUCINF Project:** European member state cyber threat detection and countermeasures

**Benefits:**
- Strategic cyber threat visibility
- Early detection of nation-state threats
- Support for critical infrastructure protection
- Evidence-based policy development

### 9.3 Defense and Military Intelligence

**Primary Use Case:** European Defence Organizations

**Application:**
- Monitoring of cyber threats to military systems and operations
- Tracking of disinformation campaigns
- Geopolitical cyber threat intelligence
- Support for cyber warfare capabilities

**EUCINF Project (Airbus Coordination):**
- Develop technological infrastructure for threat detection
- Deliver countermeasures to secure confidential data
- Equip EU member states with resources to counter cyber threats
- Address disinformation as part of information warfare

**Benefits:**
- Military-grade cyber threat intelligence
- Disinformation campaign detection and tracking
- Strategic advantage through advanced OSINT
- Secure collaborative intelligence sharing

### 9.4 Critical Infrastructure Protection

**Application:**
- Monitor threats to energy, transportation, communications, healthcare sectors
- Track vulnerability disclosures affecting industrial control systems
- Identify targeted campaigns against critical infrastructure
- Support for sector-specific threat intelligence

**Capabilities:**
- Entity extraction identifies affected products and sectors
- Story clustering reveals coordinated campaigns
- Timely alerting for critical vulnerabilities
- Cross-sector threat correlation

### 9.5 Threat Hunting and Proactive Defense

**Application:**
- Proactive identification of threat actor TTPs
- Hypothesis-driven threat hunting based on intelligence
- Tracking of malware families and campaigns
- Attribution support through APT profiling

**Intelligence Lifecycle:**
1. Continuous monitoring of threat actor communications
2. Entity extraction identifies IoCs and TTPs
3. Story clustering reveals campaign evolution
4. Analyst investigation produces actionable intelligence
5. Defensive measures implemented based on intelligence

### 9.6 Security Vendor and Researcher Applications

**Potential Use Cases (based on capabilities):**
- Threat research and analysis
- Vulnerability intelligence aggregation
- Malware campaign tracking
- Threat actor profiling and attribution
- Competitive threat intelligence

### 9.7 Case Study: European Cyber Situational Awareness

**Context:** Multiple European Union projects leverage Taranis AI for enhanced cyber defense.

**Deployment:**
- AWAKE (CEF Project): Initial proof-of-concept and validation
- NEWSROOM (EDF): Production deployment for mission-oriented intelligence
- EUCINF (EDF): Large-scale deployment coordinated by Airbus Defence and Space

**Objectives:**
- Improve cyber situational awareness at national and EU levels
- Detect and counter cyber threats and disinformation
- Provide technological infrastructure for threat detection
- Deliver countermeasures to secure confidential information

**Results:**
- Successfully demonstrated NLP-enhanced OSINT analysis
- Published academic research in ERCIM News (January 2024)
- Continued funding and expansion through EDF projects
- Growing adoption across European CSIRT and defense communities

**Key Success Factors:**
- Open-source model enables cross-organizational collaboration
- Modular architecture supports customization for different use cases
- AI enhancement reduces analyst workload while improving quality
- MISP integration enables collaborative threat intelligence

---

## 10. Comparison with Traditional OSINT Tools

### 10.1 Traditional OSINT Tool Landscape

**Common Traditional Tools:**
- **Maltego:** Visual link analysis and data mining
- **Shodan:** Internet of Things and infrastructure search engine
- **SpiderFoot:** Automated reconnaissance and OSINT collection
- **TheHarvester:** Email, subdomain, and name harvesting
- **Recon-ng:** Web reconnaissance framework

**Traditional Tool Characteristics:**
- Manual data collection workflows
- Visualization-focused (graph databases, link analysis)
- Single-source or specialized collection (e.g., Shodan for IoT)
- Limited to no automated analysis or enrichment
- Analyst-driven investigation and correlation

### 10.2 Taranis AI Differentiators

**Automated Intelligence Lifecycle**
- **Traditional:** Manual collection, correlation, and analysis
- **Taranis AI:** Automated collection → AI analysis → Human refinement

**Multi-Source Aggregation**
- **Traditional:** Focus on specific source types (web, DNS, social media)
- **Taranis AI:** Unified platform for web, RSS, email, Twitter, Slack, and more

**AI-Enhanced Analysis**
- **Traditional:** Raw data presentation, manual analysis required
- **Taranis AI:** Automatic entity extraction, story clustering, summarization, sentiment analysis

**Story-Based Intelligence Model**
- **Traditional:** Feed-based or alert-based presentation
- **Taranis AI:** Automatic grouping into coherent narratives (stories)

**Collaborative Intelligence**
- **Traditional:** Siloed intelligence within organization
- **Taranis AI:** Built-in MISP integration for community sharing

**Analyst Workflow Optimization**
- **Traditional:** Analysts spend significant time on collection and correlation
- **Taranis AI:** Analysts focus on refinement and decision-making, AI handles repetitive tasks

**Domain-Specific Focus**
- **Traditional:** General-purpose OSINT with manual specialization
- **Taranis AI:** Cybersecurity-specific with built-in entity extraction for CVEs, IoCs, APTs

**Report Generation**
- **Traditional:** Manual report writing from collected intelligence
- **Taranis AI:** Structured report generation with multi-format export

### 10.3 Feature Comparison Matrix

| Feature | Traditional OSINT Tools | Taranis AI |
|---------|-------------------------|------------|
| **Collection Automation** | Limited | Comprehensive |
| **Multi-Source Aggregation** | Partial | Full (web, RSS, email, social) |
| **Entity Extraction** | Manual | Automated (NER, ML) |
| **CVE/IoC Recognition** | Manual search | Automatic extraction |
| **Story Clustering** | Manual correlation | Automated event-based |
| **Summarization** | Manual | Automated (extractive/abstractive) |
| **Sentiment Analysis** | N/A | Multi-language XLM-RoBERTa |
| **Threat Classification** | Manual tagging | ML-based classification |
| **Report Generation** | Manual writing | Structured template-based |
| **Collaborative Sharing** | Manual export | MISP integration |
| **Real-Time Monitoring** | Depends on tool | Continuous (Celery workers) |
| **Scalability** | Typically desktop-scale | Enterprise-scale (microservices) |
| **Deployment Model** | Desktop applications | Containerized platform (Docker) |
| **Licensing** | Mixed (commercial/open) | Open source (EUPL-1.2) |
| **Target Users** | Individual analysts/researchers | CSIRT teams, NIS authorities, defense |

### 10.4 Complementary vs. Replacement

**Taranis AI is Not a Replacement For:**
- Specialized tools like Shodan (IoT search), Maltego (visual analytics), or Nmap (network scanning)
- Deep-dive investigation tools for specific source types
- Forensic analysis platforms

**Taranis AI Complements By:**
- Providing centralized aggregation of intelligence from multiple specialized sources
- Automating the routine collection and initial analysis
- Creating contextual narratives (stories) that connect disparate findings
- Enabling team collaboration and knowledge sharing
- Supporting strategic intelligence production, not just tactical indicators

**Ideal Hybrid Workflow:**
1. Taranis AI continuously monitors broad threat landscape
2. Stories and alerts identify areas requiring deep investigation
3. Analysts use specialized tools (Maltego, Shodan, etc.) for detailed investigation
4. Findings incorporated back into Taranis AI reports and stories
5. Intelligence disseminated via MISP and organizational workflows

### 10.5 Use Case Fit Analysis

**When Traditional Tools Are Better:**
- Single-source deep-dive investigations
- Visual link analysis and relationship mapping
- Real-time interactive exploration
- Highly specialized technical reconnaissance (e.g., subdomain enumeration)

**When Taranis AI Is Better:**
- Continuous multi-source threat monitoring
- Automated intelligence production for CSIRT teams
- Collaborative intelligence sharing across organizations
- High-volume OSINT processing with AI-assisted analysis
- Strategic threat intelligence reporting
- Cybersecurity-focused intelligence (CVEs, APTs, IoCs)

---

## 11. Technical Implementation Details

### 11.1 Deployment and Configuration

**Container-Based Deployment:**

**Quick Start:**
```bash
# Clone repository
git clone --depth 1 https://github.com/taranis-ai/taranis-ai
cd taranis-ai/docker/

# Configure environment
cp env.sample .env
# Edit .env file with custom settings

# Deploy with Docker Compose
docker compose pull  # Avoid reusing older local images
docker compose up -d
```

**Access:**
- **URL:** `http://<server>:<TARANIS_PORT>/login`
- **Default Credentials:**
  - User: `user/user`
  - Admin: `admin/admin`
- **Password Override:** Set `PRE_SEED_PASSWORD_ADMIN` or `PRE_SEED_PASSWORD_USER` environment variables before first launch

**System Requirements:**
- **With NLP:** 16 GB RAM, 4 CPU cores, 50 GB storage
- **Without NLP:** 2 GB RAM, 2 CPU cores, 20 GB storage

**Docker Image Tags:**
- **Release Versions:** Specific version tags (e.g., `1.1.7`)
- **Stable:** `stable` tag for latest official release
- **Latest:** `latest` tag for most recent uploaded image

**PostgreSQL Configuration:**
- Default: PostgreSQL 17
- Configurable via `POSTGRES_TAG` in `.env` file

### 11.2 Monitoring and Observability

**Sentry Integration:**
- **Supported Components:** GUI, Core, Database
- **Configuration:** Set `SENTRY_DSN` environment variables for respective components
- **Capabilities:**
  - Error tracking and alerting
  - Performance monitoring
  - Application health dashboards
  - Automated incident management

### 11.3 Source Configuration

**OSINT Sources Management:**

**Configuration Steps:**
1. Navigate to **Configuration → OSINT Sources**
2. Create or select collectors node
3. View registered collectors for the node
4. Select collector type (RSS, Web, Email, Twitter, etc.)
5. Configure collector-specific parameters:
   - Feed URL or connection details
   - Content location selectors (CSS, XPath)
   - Collection frequency
   - Word lists (include/exclude)

**Import/Export:**
- Export sources as JSON for backup or sharing
- Import source configurations for rapid deployment
- Word lists exportable/importable as JSON

**Collector Types:**
- **RSS Collector:** RSS/Atom feed monitoring
- **Web Collector:** HTML scraping with selectors
- **Email Collector:** IMAP/POP3 email monitoring
- **Twitter Collector:** Twitter API integration
- **Slack Collector:** Slack channel monitoring
- **Custom Collectors:** Extensible framework for additional sources

### 11.4 GitHub Repository Structure

**Main Repository:** `taranis-ai/taranis-ai`
- Core platform (GUI, API, workers)
- Docker deployment configuration
- Documentation and guides

**Bot Repositories:**
- `taranis-ai/summarize_bot` - Summarization
- `taranis-ai/story-clustering` - Event detection and clustering
- `taranis-ai/sentiment-analysis` - Sentiment classification
- `taranis-ai/cybersec-classifier` - Threat group classification
- `taranis-ai/natural-language-processing` - Core NLP functions
- `taranis-ai/taranis-base-bot` - Common bot framework

**Total Repositories:** 19 (including additional utilities, landing page, etc.)

### 11.5 Licensing and Contributions

**License:** EUPL-1.2 (European Union Public License version 1.2)
- OSI-approved open source license
- Permissive for use, modification, and distribution
- Compatible with other open source licenses
- Contributor warranties on copyright and licensing

**Contributing:**
- Development Setup Guide available in repository
- Community contributions welcomed
- Active development team from European research institutions

**Community:**
- Documentation comprehensive and well-maintained
- Supportive community (GitHub issues, discussions)
- Academic research publications (ERCIM News, ACM conferences)

---

## 12. Research and Academic Contributions

### 12.1 Published Research

**ERCIM News Publication (January 2024):**
- **Title:** "Taranis AI: Applying Natural Language Processing for Advanced Open-Source Intelligence Analysis"
- **Publication:** ERCIM News 136 - Special Theme: Large Language Models
- **Authors:** Taranis AI development team (AIT Austrian Institute of Technology, collaborators)

**Key Research Findings:**
- Examined integration of modern NLP methods into Taranis AI
- Demonstrated machine learning-based categorization and entity extraction
- Validated story clustering approach for reducing analyst workload
- Explored five essential user stories from national authorities and CERTs

**ACM Conference Paper (2024):**
- **Title:** "On the Application of Natural Language Processing for Advanced OSINT Analysis in Cyber Defence"
- **Conference:** 19th International Conference on Availability, Reliability and Security (ARES 2024)
- **Institution:** AIT Austrian Institute of Technology
- **Focus:** Application of NLP techniques for cyber defense OSINT

### 12.2 European Research Projects

**AWAKE (CEF Project):**
- **Objective:** Improve cyber situational awareness through analysis of clear and dark web
- **Role:** Initial assessment and validation of Taranis AI
- **Status:** Completed, led to follow-on EDF projects

**NEWSROOM (European Defence Fund):**
- **Objective:** Mission-oriented cyber situational awareness
- **Focus:** Leveraging NLP and AI for defense intelligence
- **Status:** Active research project

**EUCINF (European Defence Fund):**
- **Full Name:** European Cyber and Information Warfare Toolbox
- **Coordinator:** Airbus Defence and Space
- **Objective:** Equip EU member states with resources and strategies to counter cyber threats and disinformation
- **Capabilities:**
  - Technological infrastructure for threat detection
  - Countermeasures to secure confidential data
  - Tools for information warfare defense
- **Status:** Active development (funded EDF 2022)


---

**Navigation**: [← Part 2](./02_Intelligence_Collection.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Deployment_Integration.md)
**Part 3 of 4** | Lines 779-1167 of original document
