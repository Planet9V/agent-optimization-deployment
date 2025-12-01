# AEON Cyber Digital Twin: Comprehensive Frontend Tree & Capability Map

## 1. Executive Summary
This document defines the full frontend hierarchy for the AEON Cyber Digital Twin, explicitly mapping the **McKenney-Lacan Schema (v3.1)** and **Psychohistory API (E27)** to user-facing interfaces. It is designed to express the full capability of the system: from raw NER11 ingestion to high-level Seldon Crisis forecasting.

**Design Philosophy**: "The Face of Psychohistory" - A UI that is not just a dashboard, but a command center for predictive civilization stability.

## 2. Site Map Overview

```mermaid
graph TD
    Public[Public Landing] --> Auth[Clerk Auth]
    Auth --> Dashboard[Protected Dashboard]
    
    Dashboard --> Global[Global State (Seldon Crisis)]
    Dashboard --> Intel[Threat Intelligence]
    Dashboard --> Psycho[Psychohistory Lab]
    Dashboard --> Graph[Graph Explorer]
    Dashboard --> Ingest[NER11 Ingestion]
    Dashboard --> Org[Organization & Assets]
```

## 3. Detailed Page Tree & Capability Map

### 3.1 Public Zone (The "Face")
*Objective: Immerse the user in the Psychohistory narrative.*

*   **`/` (Landing Page)**
    *   **Visuals**: Psychohistory Sphere, Particle Effects (React Three Fiber).
    *   **Components**:
        *   `CalculusPanel`: Interactive simulation parameters (Social Inertia, Entropy).
        *   `SimulationGraph`: Real-time visualization of stability metrics.
    *   **API**: None (Client-side simulation).

### 3.2 Protected Zone (The "Brain")

#### 3.2.1 Global State (`/dashboard`)
*Objective: High-level situational awareness.*

*   **`/dashboard` (Main View)**
    *   **Seldon Crisis Gauge**: Probability of system collapse.
        *   *API*: `POST /api/v1/predict/seldon-crisis`
        *   *Schema*: `Organization`, `EconomicMetric`, `Event`.
    *   **Critical Slowing Indicators**: Early warning signals (Autocorrelation, Variance).
        *   *API*: `POST /api/v1/predict/critical-slowing`
    *   **Global Tension Map**: Geospatial view of `ThreatActor` activity.
        *   *Schema*: `ThreatActor` -> `TARGETS` -> `Location`.

#### 3.2.2 Threat Intelligence (`/dashboard/intel`)
*Objective: Deep dive into the 16 Super Labels.*

*   **`/dashboard/intel/actors`**
    *   **List View**: Filter by `actorType` (Nation State, APT), `sophistication`.
    *   **Profile View (`/dashboard/intel/actors/[id]`)**:
        *   **Psychometric Profile**: Dark Triad scores, Cognitive Biases.
            *   *Schema*: `ThreatActor` -> `EXHIBITS` -> `PsychTrait`.
            *   *API*: `GET /api/v1/entities/psychtraits`.
        *   **Campaign Timeline**: Gantt chart of operations.
            *   *Schema*: `ThreatActor` -> `CONDUCTS` -> `Campaign`.
*   **`/dashboard/intel/malware`**
    *   **Family Tree**: Phylogenetic tree of malware variants.
        *   *Schema*: `Malware` (family, variant).
*   **`/dashboard/intel/vulnerabilities`**
    *   **Epidemic Potential**: R0 calculation for specific CVEs.
        *   *API*: `POST /api/v1/predict/epidemic`.
        *   *Schema*: `Vulnerability` -> `EXPLOITS` -> `Asset`.

#### 3.2.3 Psychohistory Lab (`/dashboard/lab`)
*Objective: Advanced predictive modeling and simulation.*

*   **`/dashboard/lab/epidemic`**
    *   **Tool**: SIR Model Simulator.
    *   **Input**: Select `Vulnerability` or `Malware`, set network parameters.
    *   **Output**: Infection curve, Peak Infection Day, Herd Immunity Threshold.
*   **`/dashboard/lab/cascade`**
    *   **Tool**: Granovetter Threshold Analyzer.
    *   **Input**: Initial Exploit, Network Topology.
    *   **Output**: Cascade depth, Critical Nodes (Hubs).
    *   *API*: `POST /api/v1/predict/cascade`.

#### 3.2.4 Graph Explorer (`/dashboard/graph`)
*Objective: Direct interaction with the Knowledge Graph.*

*   **`/dashboard/graph/explore`**
    *   **Visualizer**: 3D Force-Directed Graph (`react-force-graph-3d`).
    *   **Query Builder**: Visual Cypher builder.
    *   **capabilities**:
        *   Expand/Collapse nodes.
        *   "Find Shortest Path" between Actor and Asset.
        *   Filter by Super Label (e.g., "Show only OT Assets").

#### 3.2.5 Ingestion Pipeline (`/dashboard/ingest`)
*Objective: Feed the beast (NER11).*

*   **`/dashboard/ingest/upload`**
    *   **Dropzone**: Upload PDF/TXT/MD.
    *   **Process**:
        1.  **Extract**: Call `ner11-gold-api`.
        2.  **Review**: Entity Disambiguation Interface.
        3.  **Commit**: Write to Neo4j.
*   **`/dashboard/ingest/history`**
    *   **Status**: Track processing jobs.

#### 3.2.6 Organization (`/dashboard/org`)
*Objective: Manage the "Self" (Assets, Users, Economics).*

*   **`/dashboard/org/assets`**
    *   **Inventory**: IT/OT/IoT Assets.
    *   **Risk Heatmap**: Assets by `criticality` vs. `vulnerability`.
*   **`/dashboard/org/economics`**
    *   **Impact Analysis**: Financial loss from incidents.
    *   *Schema*: `EconomicMetric` -> `IMPACTS` -> `Organization`.

## 4. UI/UX Innovation Features

1.  **"The Seldon Stream"**: A ticker at the bottom of the screen showing real-time probability shifts (e.g., "Crisis Probability: 12% ▲").
2.  **"Psychometric HUD"**: When viewing a Threat Actor, a radar chart overlay shows their psychological profile immediately.
3.  **"Cascade Lens"**: In Graph View, hovering over a node highlights its potential downstream cascade victims based on the Granovetter model.
4.  **"Temporal Slider"**: Rewind/Fast-forward the graph state to see how campaigns evolved or are predicted to evolve.

## 5. Technical Stack Alignment

*   **Frontend**: Next.js 15 (App Router), React, Tailwind CSS (VulnCheck Theme).
*   **Visualization**: Recharts (Time series), React Force Graph (Network), Leaflet (Geospatial).
*   **State Management**: React Query (Server state), Zustand (Client simulation state).
*   **API Layer**: Strictly typed to `lib/aeon-graph.ts` (Neo4j) and `lib/psychohistory-api.ts` (Prediction).
