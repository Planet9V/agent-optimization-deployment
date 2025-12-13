# IEC 62443 Agentic MVP – Product Requirements Document

**Version:** 1.0  
**Status:** Ready for Development  
**Target Release:** Q1 2025  
**Audience:** Engineering, Product, QA  
**Document Owner:** System Architect  

---

## Executive Summary

This PRD defines a **single-tenant, phase-gated IEC 62443-3-2 workshop application** for security consultants to conduct live risk assessments with clients. The MVP covers **Phases 1–2 only** (Scoping + HARA; Partitioning + Threat Modeling), integrating a custom spaCy NER pipeline with Qdrant vector search and Neo4j graph persistence for semantic document ingestion and AI-assisted threat elicitation.

**Key constraints:**
- Single admin login (no multi-tenancy)
- React Flow canvas (no 3D digital twin)
- OpenRouter LLM backend (no on-premises model serving)
- Designed for **Docker containerized deployment** with full IaC support

---

## 1. Vision & Scope

### 1.1 Problem Statement

Security consultants running IEC 62443 compliance workshops lack integrated tooling to:
- Rapidly capture and structure system scoping and hazard analysis in live sessions
- Link evidence documents (RAMS, FMEA) to safety/security zones and assets
- Query compliance standards and threat libraries contextually
- Persist workshop artifacts in a queryable, relationship-aware format

### 1.2 Solution Overview

**IEC 62443 Workshop MVP** is a web application that:
1. Guides facilitators through a **HARA (Hazard Analysis & Risk Assessment)** wizard for Phase 1
2. Provides a **visual threat canvas** (React Flow) for Phase 2 zone/asset/threat partitioning
3. Integrates **semantic document search** via Qdrant + Neo4j for referenced standards and hazard evidence
4. Uses **AI co-pilot** (OpenRouter) to suggest threats, explain controls, and summarize findings
5. Stores all data in a **queryable graph** (Neo4j) and **relational database** (Postgres) for reproducibility

### 1.3 Scope (MVP)

**In Scope:**
- Track A (system lifecycle), Phases 1–2 only
- Single admin user with full capabilities
- Postgres + Neo4j + Qdrant data layer
- Custom spaCy NER ingestion for RAMS/FMEA documents
- React + React Flow UI
- OpenRouter LLM integration (chat, embeddings, threat suggestions)
- Docker deployment with docker-compose

**Out of Scope (V1+):**
- Multi-tenant organization structure
- Phases 3–8 (CMDB, Requirements Engine, Evidence Locker, CSMS, Security Case)
- 3D digital twin (Babylon.js)
- Access control beyond admin login
- Secure enclave / on-premises model serving
- OSCAL evidence packaging

---

## 2. Goals & Success Metrics

### 2.1 Business Goals
1. Enable one security consultant + client to complete Phase 1–2 of IEC 62443 in a 2–4 hour live session
2. Reduce manual document collation and threat enumeration time by 50%
3. Provide reusable, queryable workshop artifacts for compliance case generation (post-MVP)

### 2.2 User Goals
- **Facilitator (Admin):**
  - Create a project in <2 minutes
  - Run HARA wizard with 3–5 high-level assets in <30 minutes
  - Canvas rapid threat modeling with 15+ zones/assets/threats in <60 minutes
  - Ask AI questions about relevant standards and threats in seconds
  
### 2.3 Success Metrics (MVP)
- **Usability:** No more than 3 clicks to reach any major feature
- **Performance:** Canvas responsive with 100+ nodes/edges (sub-500ms updates)
- **Uptime:** 99.5% for Docker-deployed stack
- **Data integrity:** 100% round-trip consistency between Postgres ↔ Neo4j ↔ Qdrant
- **Cost:** <$10/month infra for single-user deployment

---

## 3. Personas & Use Cases

### 3.1 Primary Persona: Admin/Facilitator
- **Role:** Security consultant or internal CybOT lead
- **Goals:** Conduct workshops, capture evidence, generate compliance reports
- **Responsibilities:**
  - Project creation and management
  - HARA facilitation
  - Canvas threat modeling
  - Document upload and ingestion
  - AI co-pilot configuration and use
- **Success:** Complete Phase 1–2 in <4 hours with all artifacts recorded

### 3.2 Secondary Persona: Client Stakeholder (Future)
- Role: Plant manager, ops lead, or engineering director
- Observes workshop in view-only mode (not in MVP)

---

## 4. Core Functional Requirements

### 4.1 Module 1: Authentication & Admin Panel

**FR-AUTH-1:** Single-user login
- Simple username/password form
- JWT or secure session cookie (no OAuth yet)
- Hard-coded or seeded admin user
- Logout clears session

**FR-AUTH-2:** Admin configuration panel
- **Database connection settings:**
  - Postgres DSN
  - Neo4j connection (bolt or http)
  - Qdrant API endpoint
- **LLM configuration:**
  - OpenRouter API key
  - Model IDs for:
    - Chat (e.g., "meta-llama/llama-3-70b")
    - Embeddings (e.g., "openai/text-embedding-3-large")
    - Threat elicitation (e.g., "anthropic/claude-3-opus")
    - Summarization (e.g., "openai/gpt-4")
- **Ingestion status:**
  - Pre-ingested collections (IEC 62443 standards, MITRE ICS)
  - Project document ingestion progress
- **Audit log:** View login, config changes, ingestion events

**Acceptance Criteria:**
- User can modify all config fields without restarting app
- Config is persisted in Postgres (encrypted key fields)
- UI warns on missing/invalid API keys before running AI features

---

### 4.2 Module 2: Project Shell & Workflow

**FR-PROJECT-1:** Project CRUD
- `POST /projects` – create project with:
  - Name, description, location, operational criticality (Low/Med/High)
  - Owner defaults to current admin user
- `GET /projects` – list all projects with status badges
- `GET /projects/:id` – fetch full project state
- `PATCH /projects/:id` – update metadata
- `DELETE /projects/:id` – soft delete (archive)

**FR-PROJECT-2:** Workflow state machine
- States: `Draft` → `SubmittedForReview` → `Approved`
- Phase-aware: each phase can have independent state
- `PATCH /projects/:id/phases/:phase/status` – transition phase state
- State transitions are logged with timestamp and admin user

**FR-PROJECT-3:** Project dashboard
- Left panel: workflow map showing Phases 1–2 with "You are here" indicator
- Right panel: tabs for "Scoping & HARA", "Zones & Threats", "AI Search"
- Phase state badge with Submit/Approve buttons
- Audit trail: show last 5 state changes
- Content locking: Phase is read-only if state != Draft

**Acceptance Criteria:**
- Create project in <2 minutes
- Workflow transitions logged and auditable
- UI reflects phase state in real-time

---

### 4.3 Module 3: HARA (Hazard Analysis & Risk Assessment) Wizard

**FR-HARA-1:** System Under Consideration (SuC) step
- Fields:
  - System name (required, max 256 chars)
  - Description (optional, max 2000 chars)
  - Location / site (optional)
  - Operational criticality (Low/Med/High dropdown)
  - Custom notes field
- Auto-save to Postgres as user types
- Validation: name is unique within project

**FR-HARA-2:** Impact categories configuration step
- Facilitator defines 3–5 impact axes (e.g., Safety, Environmental, Financial, Operational, Reputational)
- For each axis:
  - Define 1–5 severity scale (e.g., 1=Negligible, 5=Catastrophic)
  - Add rationale text
- Store in Postgres; UI shows as editable table
- Default preset: "Safety/Environmental/Financial/Operational" with IEC 62443 SIL definitions

**FR-HARA-3:** Document upload & ingestion
- Upload RAMS, FMEA, HAZOP, or other PDFs
- Trigger async spaCy NER → Qdrant → Neo4j pipeline
- Show ingestion status (queued, processing, complete, error)
- Store original file in object storage (or Postgres blob for MVP)
- Extracted entities (hazards, assets, zones) appear in Neo4j and are searchable

**FR-HARA-4:** HARA workshop table
- Collaborative table of high-level functions/assets
- Columns: Name, Description, Impact Category 1, Impact Category 2, ..., Risk Level (auto-calc), Notes
- Rows can be added in-workshop by facilitator
- Each row maps to a potential "high-risk candidate" for Phase 2 asset creation
- "Suggest from uploaded docs" button: use spaCy + Neo4j to populate rows from recognized hazards
- Export as CSV

**FR-HARA-5:** AI-assisted field population
- `POST /api/ai/hara-suggestions`: given project + uploaded docs, suggest high-level functions/assets
- Use spaCy NER → Neo4j to extract candidate assets → LLM to rank by relevance
- Return top 10 suggestions with confidence scores

**Acceptance Criteria:**
- Complete HARA wizard (all steps) in <30 minutes
- HARA items saved durably to Postgres
- Uploaded documents indexed in Qdrant within 30 seconds
- Risk levels computed correctly from impact ratings
- Export CSV includes all fields

---

### 4.4 Module 4: Threat Canvas (React Flow + Neo4j)

**FR-CANVAS-1:** React Flow full-screen editor
- **Node types:**
  - Zone: represents a security zone or network segment
  - Asset: system, device, or subsystem within a zone
  - Conduit: communication link between zones
  - Threat: attack vector or hazard targeting an asset
- **Edge types:**
  - `asset-in-zone`: Zone contains Asset
  - `conduit-connects`: Conduit between Zones
  - `threat-targets`: Threat targets Asset
- **Basic toolbar:**
  - Add Zone, Add Asset, Add Conduit, Add Threat buttons
  - Delete selected node/edge
  - Undo/Redo
  - Save / Revert buttons

**FR-CANVAS-2:** Persistence layer
- **Postgres (system of record):**
  - `graph_nodes` table: id, project_id, node_type, label, metadata (JSON), position_x, position_y, created_at, updated_at
  - `graph_edges` table: id, project_id, source_id, target_id, edge_type, created_at
- **Neo4j (relationship engine, synced from Postgres):**
  - Node labels: `Project`, `Zone`, `Asset`, `Threat`, `Conduit`, `Document`
  - Relationships: `HAS_ZONE`, `HAS_ASSET`, `CONNECTED_VIA`, `TARGETS`, `EVIDENCED_BY`
- **Sync job:** Every node/edge mutation in Postgres triggers async Neo4j write via message queue (or direct call)

**FR-CANVAS-3:** Collaborative session
- Basic shared session: when admin adds node, all connected clients see it in <2 seconds
- Use Supabase Realtime or simple polling (GET /projects/:id/graph every 5 sec)
- No multi-user cursors or presence in MVP
- Conflict resolution: last-write-wins for position/metadata

**FR-CANVAS-4:** AI-assisted threat suggestions
- Right-click Asset node → "Suggest threats from MITRE ICS"
- `POST /api/ai/threat-suggestions` with asset id + zone metadata
- Pipeline:
  1. Qdrant semantic search in `mitre_ics` collection using asset type/description
  2. Neo4j graph context: pull related zone, other assets in zone, existing threats
  3. LLM prompt: "Given asset {name} in zone {zone}, in {industry}, suggest 5 plausible threats from MITRE ATT&CK ICS"
  4. Return list: [{id, title, mitre_id, description, rationale}]
- User picks threat to instantiate as node

**FR-CANVAS-5:** Threat details panel
- Click Threat node → side panel shows:
  - MITRE ID and name
  - Tactic + technique (if MITRE sourced)
  - Description
  - Recommended mitigations (from IEC 62443 SR requirements, via AI query)
  - Related documents (from Qdrant search)
  - Free-text notes field

**Acceptance Criteria:**
- Add/edit/delete nodes in <500ms
- 100+ nodes in canvas remain responsive
- All nodes persisted correctly to Postgres and Neo4j
- Threat suggestions generated in <5 seconds
- Canvas state recovers correctly after reload

---

### 4.5 Module 5: AI Search Panel (GraphRAG-lite)

**FR-SEARCH-1:** Global search input
- Text input: "Ask IEC 62443-aware co-pilot"
- Placeholder examples: "What are threats to SCADA systems?", "Which SRs apply to authentication?"
- Context awareness: search scoped to current project if in project view

**FR-SEARCH-2:** Query pipeline
1. **NER:** spaCy extracts entities (standards, assets, hazards, zones) from user query
2. **Qdrant search:** Multi-collection search
   - `iec62443_standards`: IEC 62443-3-2 SR/CR text + explanations
   - `mitre_ics`: ATT&CK ICS tactics, techniques, procedures
   - `project_docs`: Uploaded RAMS, FMEA, hazard logs (project-scoped)
3. **Neo4j context:** For current project, fetch related nodes (zones, assets, threats) as graph context
4. **LLM prompt assembly:** Combine user query + NER entities + Qdrant results + Neo4j context
5. **LLM call:** Query OpenRouter with assembled prompt
6. **Response formatting:** Return markdown-formatted answer with cited sources (Qdrant collection + document)

**FR-SEARCH-3:** Search results display
- Results include:
  - Main answer (markdown rendered)
  - Source references: document name, page number (if PDF)
  - Related nodes in current project (linked in side panel)
  - Confidence score (optional, 0–100%)
- Allow user to refine search with follow-up questions in same conversation thread

**FR-SEARCH-4:** Caching & performance
- Cache embeddings for repeated queries within same session (Redis or in-memory)
- LLM response cached for identical queries within 24 hours
- Qdrant searches return top 5 results by relevance

**Acceptance Criteria:**
- Search query processed and answered in <10 seconds
- Results cited and traceable to source documents
- Follow-up questions in same thread work correctly
- No query exceeds 2000 tokens to LLM

---

### 4.6 Module 6: Document Management & Ingestion

**FR-DOC-1:** Document upload
- `POST /api/projects/:id/documents` (multipart/form-data)
- Supported: PDF, .docx, .txt, .csv
- Max file size: 50 MB
- Store file in:
  - Postgres `documents` table (blob), or
  - Local filesystem (for MVP), or
  - S3 (future)

**FR-DOC-2:** Async spaCy ingestion pipeline
- Trigger on upload:
  1. Extract text from PDF/DOCX using pypdf or similar
  2. Chunk text into 512-token paragraphs with 128-token overlap
  3. Run spaCy NER on each chunk (labels: ASSET, ZONE, HAZARD, PROTOCOL, STANDARD_REF)
  4. For each chunk:
     - Generate embedding via OpenRouter embedding model
     - Store in Qdrant `project_docs` collection with metadata {project_id, doc_id, chunk_idx, entities}
     - Create Neo4j `Document` node linked to extracted entities
- Update ingestion status in UI (queued → processing → 25%/50%/75% → complete or error)
- Return extracted entity list to facilitator for review/tagging

**FR-DOC-3:** Entity review & mapping
- Show facilitator list of extracted entities with confidence scores
- Allow manual tagging: "This ASSET should be a Zone instead"
- Persist corrected tags to Neo4j and Qdrant

**FR-DOC-4:** Search & discovery
- `GET /api/projects/:id/documents` – list uploaded docs with entity counts and ingestion status
- Search documents by name or content
- Link documents to canvas nodes (e.g., "This RAMS doc is evidence for Asset X")

**Acceptance Criteria:**
- Document ingestion completes in <60 seconds for typical 10-page PDF
- Extracted entities accurate (manual spot-check on 3+ docs)
- Documents searchable in AI query within 5 minutes of upload
- Failed ingestion shows clear error message to admin

---

### 4.7 Module 7: Audit & Compliance Logging

**FR-AUDIT-1:** Comprehensive audit trail
- Log all user actions:
  - Project creation, state changes
  - Document uploads, ingestion completions
  - HARA item creation/updates
  - Canvas node/edge mutations
  - Config changes
  - AI queries (prompt + response summary)
  - Login/logout events
- Store in Postgres `audit_log` table: {id, timestamp, user, action, resource_type, resource_id, details}

**FR-AUDIT-2:** Audit access & export
- `GET /api/admin/audit-log?since=&action=` – filter audit logs
- Export audit trail as CSV for compliance review
- Audit logs are immutable (no delete, only archive)

**Acceptance Criteria:**
- All state-changing actions logged
- Audit trail complete for compliance review
- No audit logs lost due to app crash or restart

---

## 5. Data Model & Architecture

### 5.1 Postgres Schema (System of Record)

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(512) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Projects
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  location VARCHAR(255),
  criticality ENUM('LOW', 'MED', 'HIGH'),
  owner_id UUID REFERENCES users(id),
  status ENUM('DRAFT', 'SUBMITTED_FOR_REVIEW', 'APPROVED') DEFAULT 'DRAFT',
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Phases
CREATE TABLE phases (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  phase_number INT (1-8),
  name VARCHAR(255),
  status ENUM('DRAFT', 'SUBMITTED_FOR_REVIEW', 'APPROVED') DEFAULT 'DRAFT',
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Impact Categories
CREATE TABLE impact_categories (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  name VARCHAR(255),
  severity_scale JSON, -- {1: "Negligible", 2: "Minor", ...}
  description TEXT,
  created_at TIMESTAMP
);

-- HARA Items
CREATE TABLE hara_items (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  impact_ratings JSON, -- {category_id: severity_score}
  risk_level ENUM('LOW', 'MED', 'HIGH', 'CRITICAL'),
  notes TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Documents
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  filename VARCHAR(255) NOT NULL,
  file_type VARCHAR(10),
  file_content BYTEA, -- or reference to S3
  ingestion_status ENUM('QUEUED', 'PROCESSING', 'COMPLETE', 'ERROR') DEFAULT 'QUEUED',
  extracted_entities JSON, -- {ASSET: [...], ZONE: [...], ...}
  ingestion_error TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Graph Nodes
CREATE TABLE graph_nodes (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  node_type VARCHAR(50), -- ZONE, ASSET, THREAT, CONDUIT
  label VARCHAR(255) NOT NULL,
  metadata JSON, -- {description, severity, mitre_id, ...}
  position_x FLOAT,
  position_y FLOAT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Graph Edges
CREATE TABLE graph_edges (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  source_id UUID REFERENCES graph_nodes(id),
  target_id UUID REFERENCES graph_nodes(id),
  edge_type VARCHAR(50), -- asset-in-zone, threat-targets, ...
  metadata JSON,
  created_at TIMESTAMP
);

-- Configuration
CREATE TABLE config (
  id UUID PRIMARY KEY,
  key VARCHAR(255) UNIQUE NOT NULL,
  value TEXT,
  is_encrypted BOOLEAN DEFAULT FALSE,
  updated_at TIMESTAMP
);

-- Audit Log
CREATE TABLE audit_log (
  id UUID PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  user_id UUID REFERENCES users(id),
  action VARCHAR(255), -- CREATE_PROJECT, UPLOAD_DOC, etc.
  resource_type VARCHAR(50),
  resource_id UUID,
  details JSON,
  created_at TIMESTAMP
);
```

### 5.2 Neo4j Graph Model

**Node Labels & Properties:**
- `Project {id, name, description, criticality}`
- `Phase {id, project_id, number, name, status}`
- `Zone {id, label, description, metadata}`
- `Asset {id, label, asset_type, description, severity}`
- `Threat {id, label, mitre_id, tactic, technique, description}`
- `Conduit {id, label, protocol, description}`
- `Document {id, filename, source_url, ingestion_date}`
- `Hazard {id, label, description, source_document_id}`

**Relationships:**
- `(Project)-[:HAS_PHASE]->(Phase)`
- `(Project)-[:HAS_ZONE]->(Zone)`
- `(Zone)-[:HAS_ASSET]->(Asset)`
- `(Zone)-[:CONNECTED_VIA]->(Conduit)`
- `(Conduit)-[:CONNECTS]->(Zone)`
- `(Asset)-[:EXPOSED_TO]->(Threat)`
- `(Threat)-[:TARGETS]->(Asset)`
- `(Document)-[:EVIDENCES]->(Hazard)`
- `(Hazard)-[:AFFECTS]->(Asset)`
- `(Asset)-[:IMPLEMENTS]->(Requirement)` [future]

### 5.3 Qdrant Vector Collections

**Collection: `iec62443_standards`**
- Documents: IEC 62443-3-2 foundational requirements (FR1–FR7) + SRs
- Chunk: Each SR with explanation (~200 tokens)
- Embedding model: OpenRouter `text-embedding-3-large`
- Size estimate: ~2000 documents
- Update frequency: Static (pre-ingested)

**Collection: `mitre_ics`**
- Documents: MITRE ATT&CK ICS techniques + descriptions
- Chunk: Tactic + Technique with description (~150 tokens)
- Embedding model: Same as above
- Size estimate: ~400 techniques
- Update frequency: Sync weekly from MITRE

**Collection: `project_docs`**
- Documents: Uploaded project-specific RAMS, FMEA, hazard logs (chunked)
- Metadata: {project_id, doc_id, chunk_idx, entities, confidence}
- Embedding: Same model
- Update frequency: On upload (async)
- Size estimate: Grows with project

---

## 6. API Specification

All endpoints require JWT authentication (admin login).

### 6.1 Authentication

```
POST /api/auth/login
Body: { "username": string, "password": string }
Response: { "token": string, "expires_in": number }
```

```
POST /api/auth/logout
Headers: { "Authorization": "Bearer {token}" }
Response: { "status": "ok" }
```

### 6.2 Projects

```
GET /api/projects
Response: { projects: [{id, name, description, status, owner, created_at}] }

POST /api/projects
Body: { "name": string, "description"?: string, "location"?: string, "criticality"?: "LOW"|"MED"|"HIGH" }
Response: { project: {id, ...} }

GET /api/projects/:id
Response: { project: {...}, phases: [...], hara_items: [...], graph_summary: {...} }

PATCH /api/projects/:id
Body: { "name"?: string, "description"?: string, ... }
Response: { project: {...} }

DELETE /api/projects/:id
Response: { status: "deleted" }

PATCH /api/projects/:id/phases/:phase_number/status
Body: { "status": "DRAFT"|"SUBMITTED_FOR_REVIEW"|"APPROVED" }
Response: { phase: {...} }
```

### 6.3 HARA Module

```
GET /api/projects/:id/hara
Response: { 
  suc: {...},
  impact_categories: [...],
  hara_items: [...]
}

POST /api/projects/:id/hara/suc
Body: { "name": string, "description"?: string, "location"?: string, "criticality": string }
Response: { suc: {...} }

POST /api/projects/:id/hara/categories
Body: { "name": string, "severity_scale": {...}, "description"?: string }
Response: { category: {...} }

POST /api/projects/:id/hara/items
Body: { "name": string, "description": string, "impact_ratings": {category_id: score} }
Response: { hara_item: {...} }

PATCH /api/hara/items/:id
Body: { "name"?: string, "notes"?: string, ... }
Response: { hara_item: {...} }

POST /api/ai/hara-suggestions
Body: { "project_id": string }
Response: { suggestions: [{name, description, confidence}] }
```

### 6.4 Documents

```
POST /api/projects/:id/documents (multipart/form-data)
Files: { "file": File }
Response: { document: {id, filename, status: "QUEUED"} }
Async: Triggers spaCy → Qdrant → Neo4j pipeline

GET /api/projects/:id/documents
Response: { documents: [{id, filename, status, extracted_entities}] }

GET /api/projects/:id/documents/:doc_id
Response: { document: {...} }

DELETE /api/projects/:id/documents/:doc_id
Response: { status: "deleted" }
```

### 6.5 Graph / Canvas

```
GET /api/projects/:id/graph
Response: { 
  nodes: [{id, type, label, metadata, position}],
  edges: [{id, source, target, type}]
}

POST /api/projects/:id/graph/nodes
Body: { "type": "ZONE"|"ASSET"|"THREAT"|"CONDUIT", "label": string, "metadata"?: {...} }
Response: { node: {...} }

PATCH /api/graph/nodes/:id
Body: { "label"?: string, "position"?: {x, y}, "metadata"?: {...} }
Response: { node: {...} }

DELETE /api/graph/nodes/:id
Response: { status: "deleted", removed_edges: number }

POST /api/projects/:id/graph/edges
Body: { "source_id": string, "target_id": string, "type": string }
Response: { edge: {...} }

DELETE /api/graph/edges/:id
Response: { status: "deleted" }
```

### 6.6 AI Features

```
POST /api/ai/threat-suggestions
Body: { "project_id": string, "asset_node_id": string }
Response: {
  threats: [
    { id, title, mitre_id, tactic, technique, description, rationale, confidence }
  ]
}

POST /api/ai/query
Body: { "project_id": string, "question": string, "conversation_id"?: string }
Response: {
  answer: string,
  sources: [{collection, document_id, chunk, relevance}],
  conversation_id: string
}

POST /api/ai/models/test-connection
Body: { "api_key": string, "model_id": string }
Response: { "status": "ok"|"error", "error_message"?: string }
```

### 6.7 Admin Configuration

```
GET /api/admin/config
Response: {
  postgres_status: "CONNECTED"|"ERROR",
  neo4j_status: "CONNECTED"|"ERROR",
  qdrant_status: "CONNECTED"|"ERROR",
  openrouter_key_valid: boolean,
  models: {
    chat: string,
    embedding: string,
    threat_elicitation: string,
    summarization: string
  },
  ingestion_status: {
    iec62443_standards: {count, last_updated},
    mitre_ics: {count, last_updated},
    project_docs: {projects, total_documents}
  }
}

PATCH /api/admin/config
Body: {
  "postgres_dsn"?: string,
  "neo4j_uri"?: string,
  "neo4j_user"?: string,
  "neo4j_password"?: string,
  "qdrant_url"?: string,
  "openrouter_key"?: string,
  "models"?: {...}
}
Response: { config: {...} }

GET /api/admin/audit-log?since=:timestamp&action=:action
Response: {
  logs: [{timestamp, user, action, resource_type, details}]
}

POST /api/admin/ingest/iec62443-standards
Response: { job_id: string, status: "QUEUED" }

POST /api/admin/ingest/mitre-ics
Response: { job_id: string, status: "QUEUED" }

GET /api/admin/ingestion-status/:job_id
Response: { job_id, status, progress: 0-100, error?: string }
```

---

## 7. UI/UX Architecture

### 7.1 Layout Structure

**App Shell:**
- Top nav: Logo, Project selector dropdown, user menu (logout), Admin link
- Left sidebar (conditional): Phase workflow map (when in project view)
- Main content area: Dynamic tabs/panels
- Right panel (conditional): Details, search results, or config

**Routes (MVP):**
- `/` → Login (if not authenticated)
- `/projects` → Project list
- `/projects/:id` → Project dashboard (tabbed: HARA, Canvas, Search)
- `/admin` → Admin config panel

### 7.2 Key Screens

**Screen 1: Login**
- Card-centered form: username, password, submit
- Error handling for invalid credentials
- Simple, minimal styling

**Screen 2: Project List**
- Table: Name, Location, Status, Created, Actions (Edit, Delete, Open)
- "New Project" button
- Filter/search by name

**Screen 3: Project Dashboard**
- **Left panel (2 sections):**
  1. Workflow map (Phases 1–2) with "You are here" indicator
  2. Phase state panel: current state, Submit/Approve buttons, audit log excerpt
- **Main content area (tabs):**
  1. **Scoping & HARA tab:** HARA wizard (step indicator, form content, Next/Back)
  2. **Zones & Threats tab:** React Flow canvas full-screen
  3. **AI Search tab:** Search input, results panel, conversation history

**Screen 4: HARA Wizard**
- **Step 1:** System Under Consideration (form)
- **Step 2:** Impact Categories (editable table + preset selector)
- **Step 3:** Document Upload (drag-and-drop file area + upload status)
- **Step 4:** HARA Workshop (editable table, add row, suggest from docs, risk calculation)
- Navigation: Previous, Next, Save Draft, Submit Phase

**Screen 5: Threat Canvas**
- Full-screen React Flow editor
- Toolbar (add zone, asset, conduit, threat; undo/redo; save/revert)
- Right-click context menu (add node, delete, properties)
- Bottom status bar: node count, last saved, connection status

**Screen 6: Admin Config**
- Sections: Database Connections, LLM Configuration, Ingestion Status, Audit Log
- Each section editable with Test Connection button
- Display health status (green/red indicators)

### 7.3 Design System

- **Colors:** Neutral (grays) + accents (teal for primary, red for critical/error)
- **Typography:** System fonts (Inter, SF Mono)
- **Spacing:** 8px base unit grid
- **Components:** Buttons, forms, cards, modals, tables (accessible, semantic HTML)
- **Responsive:** Desktop-first, but mobile-friendly form layouts

### 7.4 Interaction Patterns

- **Auto-save:** HARA and graph edits saved on blur (no explicit save button for user edits)
- **Phase locking:** If phase state != Draft, all UI in that tab is read-only
- **Errors:** Toast notifications (top-right, auto-dismiss after 5 sec)
- **Loading:** Skeleton screens or progress indicators for long operations
- **Undo/Redo:** Canvas only (React Flow native support)

---

## 8. Security & Compliance

### 8.1 Authentication & Authorization

- **Authentication:** Username/password JWT
- **Authorization:** Single admin user (hardcoded or seeded); all features enabled for admin
- **Session:** JWT with 24-hour expiration; refresh tokens not required for MVP
- **Password storage:** bcrypt (minimum rounds: 10)

### 8.2 Data Protection

- **Encryption at rest:**
  - Sensitive config (API keys, DB passwords) stored encrypted in Postgres
  - Use AES-256-GCM or similar
- **Encryption in transit:**
  - All API calls over HTTPS (enforced by deployment)
  - WebSocket (for Realtime) over WSS
- **API keys:**
  - OpenRouter API key stored encrypted
  - Never logged or returned to UI
  - Validated on change before persisting

### 8.3 Audit & Compliance

- **Comprehensive audit log:** All state-changing actions logged
- **Non-repudiation:** Audit log immutable (no delete, only archive)
- **Data retention:** No auto-purge of audit logs (retention policy TBD by customer)
- **Compliance readiness:** Audit trail exportable for IEC 62443 / ISO 27001 assessments

### 8.4 Input Validation

- All API inputs validated (type, length, format)
- SQL injection prevention: Parameterized queries (ORM)
- XSS prevention: Output encoding (React default)
- CSRF prevention: Token-based CSRF middleware (if needed for traditional forms)

---

## 9. Performance & Scalability

### 9.1 Performance Targets

- **Page load:** <2 seconds (initial, cold cache)
- **API response:** <500 ms (p99) for standard queries
- **Canvas interaction:** <200 ms (add node, drag, delete)
- **AI response:** <10 seconds (threat suggestions, query)
- **Ingestion:** <60 seconds for 10-page PDF

### 9.2 Scalability Notes (MVP)

- Single-tenant, single-user: no need for horizontal scaling
- DB connection pooling: 5–10 connections
- Qdrant: default single-shard setup (fine for <10k vectors)
- Neo4j: single instance (sufficient for <100k nodes)
- Cache: In-memory or Redis (optional for MVP)

### 9.3 Monitoring & Observability

- **Logging:** Structured logs (JSON) to stdout
- **Metrics:** Basic counters (API calls, errors, ingestion jobs)
- **Health checks:** `/health` endpoint (DB, Qdrant, Neo4j connectivity)
- **Error tracking:** Sentry or similar (optional, can be added later)

---

## 10. Deployment & Operations

### 10.1 Deployment Model

- **Target:** Docker Compose (single-machine deployment)
- **Services:** Next.js app, Postgres, Neo4j, Qdrant, Redis (optional), nginx (reverse proxy)
- **Infrastructure:** AWS EC2 (t3.medium or similar), or on-premises VM
- **IaC:** docker-compose.yml + .env configuration

### 10.2 Persistence

- **Postgres data:** Docker volume `postgres_data`
- **Neo4j data:** Docker volume `neo4j_data`
- **Qdrant data:** Docker volume `qdrant_data`
- **Backup:** Daily snapshots (via scheduled cronjobs in deployment)

### 10.3 Environment Configuration

Key environment variables:
- `NEXT_PUBLIC_API_URL` – API base URL
- `POSTGRES_DSN` – Database connection string
- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` – Graph DB
- `QDRANT_URL` – Vector DB endpoint
- `OPENROUTER_API_KEY` – LLM backend API key
- `JWT_SECRET` – Signing key for JWTs
- `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH` – Initial admin user
- `LOG_LEVEL` – debug | info | warn | error

---

## 11. Timeline & Milestones

### Phase 1: Core API & Data Layer (Weeks 1–3)
- [ ] Postgres schema and migrations
- [ ] Neo4j initialization and relationship setup
- [ ] Qdrant collections (IEC 62443, MITRE ICS pre-ingestion)
- [ ] Authentication API
- [ ] Project CRUD APIs
- [ ] Audit log setup

### Phase 2: HARA Module (Weeks 3–5)
- [ ] HARA API endpoints
- [ ] HARA UI (wizard, table)
- [ ] Document upload & spaCy ingestion pipeline
- [ ] AI suggestions (LLM + Qdrant)

### Phase 3: Threat Canvas (Weeks 5–7)
- [ ] Graph APIs (nodes, edges, persistence)
- [ ] React Flow UI integration
- [ ] Neo4j sync from Postgres
- [ ] Threat suggestions from MITRE
- [ ] Collaborative session (basic)

### Phase 4: AI Search & Polish (Weeks 7–8)
- [ ] GraphRAG-lite pipeline (NER → Qdrant → Neo4j → LLM)
- [ ] Search UI and conversation thread
- [ ] Admin config panel
- [ ] Error handling, validation, edge cases
- [ ] Performance optimization

### Phase 5: Testing & Deployment (Weeks 8–9)
- [ ] Unit tests (critical paths)
- [ ] E2E tests (happy path scenarios)
- [ ] Docker Compose setup
- [ ] Deployment docs
- [ ] User acceptance testing (UAT)

### Phase 6: Launch & Iteration (Week 10+)
- [ ] Soft launch (internal/beta users)
- [ ] Bug fixes and refinement
- [ ] First live workshop session
- [ ] V1 roadmap planning

---

## 12. Known Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| spaCy NER accuracy on domain docs | Medium | Medium | Implement entity review/correction UI; start with conservative thresholds |
| LLM latency > 10 sec | Medium | Medium | Cache responses; queue LLM calls; show spinner with timeout fallback |
| Neo4j sync lag with Postgres | Low | Low | Use message queue (RabbitMQ) or eventual consistency acknowledgment |
| Qdrant storage explosion with many projects | Low | Medium | Implement project archival; per-project Qdrant namespace limits |
| Admin password loss / single user lock-out | Low | High | Provide secure password reset mechanism; backup admin credentials in ops manual |

---

## 13. Definition of Done (MVP)

### API Layer
- [ ] All endpoints implemented per spec
- [ ] Authenticated (JWT required)
- [ ] Validated inputs (type, length, format)
- [ ] Error responses with HTTP status codes
- [ ] Documented (OpenAPI or similar)
- [ ] 80%+ test coverage (unit + integration)

### Data Layer
- [ ] Postgres schema migrated and tested
- [ ] Neo4j relationships synced from Postgres mutations
- [ ] Qdrant collections ingested (IEC 62443, MITRE)
- [ ] Project document ingestion working end-to-end
- [ ] Data integrity checks (no orphaned rows, consistency)

### UI Layer
- [ ] All screens built per spec
- [ ] Form validation and error messaging
- [ ] Phase state locking (read-only when non-Draft)
- [ ] Canvas with 100+ nodes performant (<500ms)
- [ ] Mobile-friendly layouts (at least tablet-sized)

### AI Features
- [ ] Threat suggestions generated in <5 sec
- [ ] GraphRAG query pipeline working (end-to-end)
- [ ] Results cited with sources
- [ ] Caching implemented (no duplicate queries to LLM)

### Deployment
- [ ] Docker Compose file with all services
- [ ] Environment configuration via .env
- [ ] Data volume persistence verified
- [ ] Deployment guide (spin-up, login, first project)
- [ ] Health check endpoint working

### Testing
- [ ] Happy path E2E test (create project → HARA → canvas → search)
- [ ] Error scenarios tested (invalid input, missing fields, API failures)
- [ ] Performance sanity checks (sub-500ms for standard operations)
- [ ] Audit log correctness verified

### Documentation
- [ ] API specification (OpenAPI or similar)
- [ ] Database schema diagram
- [ ] Architecture diagram (services, data flows)
- [ ] Deployment & ops guide
- [ ] User guide (facilitator workflow)

---

## 14. Glossary & References

| Term | Definition |
|------|-----------|
| **HARA** | Hazard Analysis & Risk Assessment; Phase 1 of IEC 62443 workshop |
| **SuC** | System Under Consideration; the boundary and scope of the analyzed system |
| **SR** | Security Requirement (IEC 62443-3-2); e.g., "SR 1.1 – Human user identification" |
| **SL-T** | Security Level - Target; the minimum required security maturity for a system (1–4) |
| **Zone** | Logical grouping of assets with similar security requirements |
| **Conduit** | Communication path between zones |
| **Threat** | Attack vector, adversary tactic, or hazard that can impact an asset |
| **Qdrant** | Vector database for semantic search |
| **Neo4j** | Graph database for relationship queries |
| **spaCy NER** | Named Entity Recognition model (custom-trained for IEC 62443 domain) |
| **OpenRouter** | API aggregator for multiple LLMs (Claude, GPT, Llama, etc.) |
| **GraphRAG** | Graph Retrieval-Augmented Generation; combining graph queries with LLM prompting |

**References:**
- IEC 62443-3-2:2020 – Security for Industrial Automation and Control Systems
- MITRE ATT&CK ICS Framework
- OpenRouter API Documentation
- React Flow Library
- Qdrant Vector Database Documentation
- Neo4j Graph Platform

---

## Approval & Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Manager | [TBD] | [TBD] | [TBD] |
| Tech Lead | [TBD] | [TBD] | [TBD] |
| Security / Compliance | [TBD] | [TBD] | [TBD] |

---

**Document Version History:**
- v1.0 – Initial comprehensive PRD (Dec 2024)

**Next Steps:**
1. Clarify remaining design decisions (see Section 14 questions in source docs)
2. Create detailed architecture diagram
3. Begin API implementation (Week 1)
4. Assign dev, QA, and devops resources
