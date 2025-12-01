# AEON Cyber Digital Twin: Master Frontend Development Plan (Dec 2025)

## 1. Executive Summary
This master plan unifies the development efforts for the AEON Cyber Digital Twin frontend (`aeon-dashboard`). It combines two critical initiatives:
1.  **Psychohistory Landing Page Integration**: Establishing the public face of the application using the "Psychohistory" aesthetic.
2.  **Dashboard Realignment**: Refactoring the protected dashboard to align with the McKenney-Lacan Neo4j schema and integrate the NER11 Gold pipeline.

**Goal**: A seamless, secure, and architecturally aligned application where the public landing page draws users into the "Psychohistory" narrative, and the private dashboard provides the rigorous tools to analyze it.

## 2. Architecture Overview

| Layer | Component | Status | Action |
|-------|-----------|--------|--------|
| **Public** | Landing Page (`/`) | External Repo | **Integrate** (Port from Vite to Next.js) |
| **Auth** | Clerk | Implemented | **Style** (Match Psychohistory theme) |
| **Private** | Dashboard (`/dashboard`) | Existing App | **Move & Refactor** |
| **Service** | Graph Layer | Generic | **Rebuild** (`lib/aeon-graph.ts`) |
| **Ingestion**| Upload API | Empty | **Implement** (NER11 Integration) |

## 3. Implementation Roadmap

### Phase 1: Landing Page Integration (The "Face")
*Objective: Establish the visual identity and separate public/private contexts.*

1.  **Asset Migration**:
    - [ ] Move current `app/page.tsx` to `app/dashboard/page.tsx`.
    - [ ] Create `components/landing` and migrate assets from `AEON-Cyber-DT-Actual-Landing-Psychohistory-Page---GREAT`.
    - [ ] Port `App.tsx` to `components/landing/LandingPage.tsx` (Client Component).
2.  **Style Unification**:
    - [ ] Merge custom colors (`dark`, `primary`, `secondary`) into `tailwind.config.ts`.
    - [ ] Update `globals.css` with required animations (`wave`, `fade-in`).
3.  **Routing & Navigation**:
    - [ ] Create new `app/page.tsx` rendering `<LandingPage />`.
    - [ ] Update Landing Navigation to link to `/dashboard` (triggers Clerk auth).

### Phase 2: Service Layer Realignment (The "Brain")
*Objective: Align the frontend with the McKenney-Lacan Neo4j schema.*

1.  **Schema Definition**:
    - [ ] Create `lib/aeon-graph.ts`.
    - [ ] Define Interfaces: `Actor`, `Asset`, `Concept`, `Event`, `Group`, `Vulnerability`, `ThreatActor`.
2.  **Core Methods**:
    - [ ] Implement `getPsychometrics(actorId)`.
    - [ ] Implement `getEventTimeline(eventId)`.
    - [ ] Implement `findPath(startNode, endNode)`.

### Phase 3: NER11 Pipeline Integration (The "Eyes")
*Objective: Enable intelligent document ingestion.*

1.  **Upload API**:
    - [ ] Implement `api/upload/route.ts`.
    - [ ] Connect to `ner11-gold-api` (gRPC/HTTP).
2.  **Entity Review UI**:
    - [ ] Create `components/ingestion/EntityReview.tsx`.
    - [ ] Display extracted entities (Actor, Event, etc.) for user verification.
    - [ ] Submit verified entities to Neo4j via `aeon-graph.ts`.

### Phase 4: Dashboard Refactoring (The "Control")
*Objective: Visualize the Psychohistory state.*

1.  **Threat Intel View**:
    - [ ] Update queries to use `ThreatActor` -> `Event` (Campaign) -> `Group` (Sector).
2.  **Graph Explorer**:
    - [ ] Implement `react-force-graph` to visualize the 7-node schema.
3.  **Psychometrics Panel**:
    - [ ] Display "Global Tension" and "Sector Risk" metrics derived from the graph.

## 4. ICE Analysis (Integrated)
- **Impact (High)**: Delivers the complete vision: Aesthetic + Functionality + Intelligence.
- **Confidence (High)**: We have all components (Landing Code, NER11 API, Schema).
- **Ease (Medium)**: Step-by-step migration reduces risk.

## 5. Verification Plan
1.  **Public Access**: Visit `/` -> Verify Psychohistory Sphere & Animations.
2.  **Auth Flow**: Click "Dashboard" -> Login via Clerk -> Land on `/dashboard`.
3.  **Data Flow**: Upload Document -> NER Extraction -> Graph Visualization.
