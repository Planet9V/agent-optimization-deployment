# Part 1 of 4: Platform Overview

**Series**: Taranis AI
**Navigation**: [📚 Series Overview](./00_Series_Overview.md) | [Part 2 →](./02_Intelligence_Collection.md)

---

# Taranis AI: Comprehensive Research Report
## Advanced Open-Source Intelligence Framework with AI-Powered Analysis

**Research Date:** October 16, 2025
**Research Scope:** Comprehensive investigation of Taranis AI OSINT framework
**Confidence Level:** High (multiple authoritative sources, official documentation)

---

## Executive Summary

Taranis AI is an advanced Open-Source Intelligence (OSINT) tool that leverages Artificial Intelligence and Natural Language Processing to revolutionize information gathering and situational analysis for cybersecurity threat intelligence. Developed as a successor to Taranis-NG (originally created by SK-CERT), Taranis AI is specifically designed for NIS authorities, CSIRT teams, and organizations requiring automated intelligence collection and analysis from diverse open sources.

**Key Distinguishing Features:**
- AI-enhanced content enrichment and quality improvement
- Machine learning-based entity extraction (CVEs, IoCs, APTs, locations, organizations)
- Automated story clustering to reduce analyst workload
- Multi-source data collection (web, RSS, email, Twitter, Slack, Atom feeds)
- Collaborative threat intelligence sharing via MISP integration
- Modular bot architecture for specialized NLP tasks
- Open-source under EUPL-1.2 license

**Primary Use Cases:**
- Cyber threat intelligence gathering for CSIRT teams
- National authority cyber situational awareness
- Automated OSINT analysis for defense organizations
- Multi-source intelligence aggregation and correlation

---

## 1. Framework Overview and Architecture

### 1.1 System Architecture

Taranis AI employs a microservices-oriented architecture built on modern web technologies:

**Technology Stack:**
- **Frontend:** Vue.js - Responsive single-page application
- **Backend:** Flask (Python) - RESTful API and business logic
- **Task Queue:** Celery - Asynchronous processing of OSINT collection and analysis
- **Database:** PostgreSQL 17 - Persistent storage for collected intelligence
- **Message Broker:** Redis/RabbitMQ (for Celery)
- **Containerization:** Docker and Docker Compose for deployment

**Architectural Components:**

```
┌─────────────────────────────────────────────────────────────┐
│                     Vue.js Frontend (GUI)                    │
│                  User Interface & Dashboards                 │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  Flask API (Core Backend)                    │
│        Authentication, Authorization, Orchestration          │
└────────┬───────────────────┬────────────────────┬───────────┘
         │                   │                    │
         ▼                   ▼                    ▼
┌────────────────┐  ┌───────────────┐  ┌──────────────────┐
│  OSINT Workers │  │  NLP Bots     │  │ Report Generator │
│   (Celery)     │  │  (Microservice│  │                  │
│                │  │   Architecture)│  │                  │
│ - Web Scraper  │  │ - Entity Ext. │  │ - PDF Export     │
│ - RSS Collector│  │ - Clustering  │  │ - Structured     │
│ - Email Reader │  │ - Summarize   │  │   Reports        │
│ - Twitter Feed │  │ - Sentiment   │  │                  │
│ - Slack Monitor│  │ - Classifier  │  │                  │
└────────┬───────┘  └───────┬───────┘  └──────────┬─────────┘
         │                  │                      │
         └──────────────────┴──────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │      PostgreSQL Database             │
         │  - News Items      - Stories         │
         │  - Reports         - Sources         │
         │  - Entities        - Analytics       │
         └──────────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │    External Integrations             │
         │  - MISP (Threat Intelligence)        │
         │  - Sentry (Monitoring)               │
         └──────────────────────────────────────┘
```

### 1.2 Workflow Architecture

Taranis AI follows a three-phase intelligence lifecycle:

**Phase 1: Collection**
- Workers retrieve OSINT information from configured sources
- Supports multiple collector types: web, RSS, Atom, email, Twitter, Slack
- Collectors create "news items" as atomic units of intelligence

**Phase 2: Analysis & Enhancement**
- NLP bots process news items through specialized pipelines
- Entity extraction identifies CVEs, IoCs, APTs, organizations, locations, people
- Machine learning categorizes and tags content
- Story clustering groups related news items into coherent narratives
- Sentiment analysis classifies content tonality

**Phase 3: Production**
- Analysts refine AI-augmented articles into structured reports
- Multi-format output generation (PDF, structured reports)
- Publication and dissemination of intelligence products
- Optional sharing via MISP for collaborative threat intelligence

### 1.3 System Requirements

**Full NLP Features:**
- 16 GB RAM
- 4 CPU cores
- 50 GB disk storage

**Without NLP Features:**
- 2 GB RAM
- 2 CPU cores
- 20 GB disk storage

---

## 2. OSINT Collection and Processing Methodology

### 2.1 Data Source Integration

Taranis AI supports comprehensive multi-source intelligence gathering:

**Supported Source Types:**
- **Web Sources:** Direct web scraping with configurable selectors
- **RSS/Atom Feeds:** Automated feed monitoring and parsing
- **Email:** IMAP/POP3 integration for email-based intelligence
- **Twitter:** Social media monitoring (via API)
- **Slack:** Collaboration platform monitoring
- **Additional:** Extensible collector framework for custom sources

**Source Configuration:**
- **OSINT Sources Management:** Centralized configuration interface
- **Collector Selection:** Each source assigned to specific collector type
- **URL/Feed Configuration:** Feed URLs and content location selectors
- **Word Lists:** Include/exclude lists for content filtering
  - **Include Lists:** Accept news items containing specific keywords
  - **Exclude Lists:** Reject news items containing specific keywords
- **Import/Export:** JSON-based source configuration portability

### 2.2 Collection Process

**Worker Architecture:**
1. Celery workers execute collection tasks asynchronously
2. Each source polled at configurable intervals
3. Raw content extracted and normalized
4. Initial filtering applied (include/exclude lists)
5. News items created and persisted to PostgreSQL
6. Items queued for NLP analysis pipeline

**Content Normalization:**
- HTML cleaning and text extraction
- Character encoding normalization
- Metadata extraction (author, publication date, source)
- URL canonicalization and deduplication

### 2.3 Data Processing Pipeline

```
Raw Source Data → Collector → Normalization → Filtering → News Item Creation
                                                              ↓
                                                       NLP Processing
                                                              ↓
                                    ┌─────────────────────────┴────────────────────────┐
                                    ▼                         ▼                        ▼
                            Entity Extraction        Story Clustering        Sentiment Analysis
                                    ↓                         ↓                        ▼
                            Indexed News Item  →  Story Assignment  →  Enriched Intelligence
                                                              ↓
                                                    Analyst Review & Refinement
                                                              ↓
                                                     Structured Reports
```

---

## 3. NLP Analysis Capabilities and Techniques

### 3.1 Core NLP Features

Taranis AI implements modern NLP techniques through a modular bot architecture:

**Key Capabilities:**
1. **Named Entity Recognition (NER)** - Extraction of domain-specific entities
2. **Story Clustering** - Automated grouping of related intelligence
3. **Summarization** - Automatic report and story summarization
4. **Sentiment Analysis** - Classification of content tonality
5. **Cybersecurity Classification** - Threat group and attack technique identification
6. **Keyword Extraction** - Topic tagging and content indexing

### 3.2 Entity Extraction

**Extracted Entity Types:**

**Geographic Entities:**
- Locations (cities, countries, regions)
- Geolocated events and incidents

**Organizational Entities:**
- Company names and organizations
- Government agencies
- CSIRT teams and security vendors

**Personnel Entities:**
- Named individuals (security researchers, threat actors)
- Author attribution

**Cybersecurity-Specific Entities:**
- **CVEs (Common Vulnerabilities and Exposures)** - Vulnerability identifiers
- **IoCs (Indicators of Compromise)** - IP addresses, file hashes, domains, URLs
- **APTs (Advanced Persistent Threats)** - Threat actor group names
- **TTPs (Tactics, Techniques, and Procedures)** - Attack methodologies
- **Products** - Affected software and hardware
- **Malware Families** - Malicious software classifications

**Entity Extraction Methodology:**
- Pattern matching for structured identifiers (CVE-YYYY-NNNN)
- Named Entity Recognition models for unstructured entities
- Domain-specific lexicons for cybersecurity terminology
- Contextual disambiguation for ambiguous entities

### 3.3 Story Clustering

**Purpose:** Reduce analyst cognitive load by automatically grouping related news items into coherent narratives.

**Clustering Algorithm:**

The story clustering component uses incremental clustering to detect events and group related documents:

**Algorithm: `incremental_clustering_v2`**

```
Input:
  - new_news_items_aggregate: Dictionary of new items to cluster
  - clustered_news_items_aggregate: Existing clustered items

Process:
  1. Event Detection: Identify discrete events from news items
  2. Similarity Calculation: Compute semantic similarity between items
  3. Cluster Assignment:
     - Try to assign new items to existing story clusters
     - Create new clusters if similarity below threshold
  4. Cluster Merging: Merge related clusters based on event correlation

Output:
  - Updated story clusters with new items assigned
```

**Clustering Features:**
- **Incremental Processing:** Handles streaming data without full recomputation
- **Event-Based Grouping:** Documents belonging to related events clustered together
- **Story Coherence:** Maintains narrative consistency across clustered items
- **Temporal Awareness:** Considers publication timestamps for event progression

**Benefits:**
- Reduces information overload for analysts
- Automatically identifies "hot topics" and emerging threats
- Eliminates redundant information from multiple sources
- Enables rapid situational awareness

### 3.4 Summarization

**Automatic Summarization Bot** (`summarize_bot` repository)

**Capabilities:**
- **News Item Summarization:** Generate concise summaries of individual articles
- **Story Summarization:** Create executive summaries of multi-article stories
- **Report Summarization:** Produce high-level overviews of analyst reports

**Techniques:**
- Extractive summarization (selecting key sentences)
- Abstractive summarization (generating new summary text)
- Multi-document summarization for story-level summaries

**Use Cases:**
- Rapid threat briefing generation
- Executive-level intelligence summaries
- Automated report abstracts

### 3.5 Sentiment Analysis

**Sentiment Analysis Integration** (`sentiment-analysis` repository, PyPI: `taranis-sentiment-analysis`)

**Capabilities:**
- **Multi-class Classification:** Positive, Negative, Neutral sentiment
- **Multi-language Support:** Uses XLM-RoBERTa for cross-lingual analysis
- **Pre-trained Models:** High-accuracy transformer-based classifiers

**Technical Implementation:**
- **Model:** XLM-RoBERTa (Cross-lingual Language Model - RoBERTa)
- **Framework:** Hugging Face Transformers
- **Deployment:** Microservice bot architecture

**Applications:**
- Threat urgency assessment
- Misinformation detection
- Source credibility evaluation
- Public perception analysis

**Model Details:**
XLM-RoBERTa is a large multilingual masked language model trained on 2.5TB of filtered CommonCrawl data across 100 languages, enabling sentiment analysis across diverse language sources.

### 3.6 Cybersecurity Classifier

**Threat Group Classification Bot** (`cybersec-classifier` repository)

**Purpose:** Classify cybersecurity threat groups based on textual descriptions of their tactics and techniques.

**Capabilities:**
- APT group identification from behavioral descriptions
- Attack technique classification (aligned with MITRE ATT&CK)
- Threat actor attribution support
- TTP extraction and categorization

**Training Data:** Likely trained on threat intelligence reports, APT profiles, and MITRE ATT&CK framework descriptions.

### 3.7 Natural Language Processing Pipeline

**Main NLP Bot** (`natural-language-processing` repository)

**Core Functions:**
- **Keyword Extraction:** Identify salient terms and concepts
- **Named Entity Recognition:** Extract entities across multiple types
- **Topic Tagging:** Automatic categorization of news items
- **Content Analysis:** Semantic analysis for improved search and retrieval

**Integration:**
All NLP bots operate as independent microservices that consume news items from the task queue, process them, and update the database with enriched metadata.

---

## 4. Information Extraction and Filtering

### 4.1 Extraction Methodology

**Multi-Stage Extraction Process:**

**Stage 1: Content Acquisition**
- Collectors retrieve raw content from sources
- HTML parsing and text extraction
- Metadata preservation (timestamps, authors, URLs)

**Stage 2: Initial Filtering**
- Word list filtering (include/exclude)
- Source-level filtering rules
- Duplicate detection and deduplication
- Language detection

**Stage 3: NLP-Based Extraction**
- Entity extraction via NER models
- Relationship extraction between entities
- Event extraction from narrative text
- Semantic indexing for search

**Stage 4: Relevance Scoring**
- Machine learning-based relevance classification
- Priority scoring based on entity types (CVEs, APTs higher priority)
- Urgency assessment from sentiment and content
- Analyst feedback loop for model improvement

### 4.2 Signal vs. Noise Filtering

**Noise Reduction Techniques:**

**Content-Based Filtering:**
- Exclude promotional content, advertisements
- Filter non-intelligence social media chatter
- Remove duplicate or near-duplicate content
- Language filtering for unsupported languages

**Relevance Classification:**
- Machine learning models trained to identify cybersecurity-relevant content
- Topic modeling to categorize articles
- Keyword-based filtering with customizable word lists

**Source Reputation:**
- Configurable source priority and trust levels
- Historical accuracy tracking
- Community-sourced source quality ratings

**Analyst Feedback:**
- Supervised learning from analyst actions


---

**Navigation**: [📚 Series Overview](./00_Series_Overview.md) | [Part 2 →](./02_Intelligence_Collection.md)
**Part 1 of 4** | Lines 1-389 of original document
