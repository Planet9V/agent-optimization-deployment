# Frontend Realignment Plan: AEON Cyber Digital Twin

## 1. Executive Summary
The current frontend (`aeon-dashboard`) is a robust Next.js 15 + Clerk application but is currently misaligned with the core AEON Cyber Digital Twin architecture. It uses a generic "Document/Customer" schema and a STIX-like "ThreatActor/Campaign" schema, whereas the backend is moving towards the "McKenney-Lacan" schema (7 core nodes: Actor, Asset, Concept, Event, Group, Vulnerability, ThreatActor) and NER11 Gold integration.

This plan outlines the steps to realign the frontend to be the true "face" of the Psychohistory engine.

## 2. Current State Analysis

| Component | Current State | Target State (McKenney-Lacan) | Gap |
|-----------|---------------|-------------------------------|-----|
| **Location** | `Import_to_neo4j/.../web_interface` | Same | None |
| **Auth** | Clerk (Implemented) | Clerk | Aligned |
| **Graph Service** | `lib/neo4j-enhanced.ts` (Generic Docs) | `lib/aeon-graph.ts` (Domain Entities) | **Critical** |
| **Schema Usage** | `ThreatActor`, `Campaign`, `Sector` | `ThreatActor`, `Event`, `Group` | **High** |
| **Ingestion** | `api/upload` is EMPTY | NER11 Pipeline Integration | **Critical** |
| **Visualization** | Basic Charts | Graph Visualization + Psychometrics | Medium |

## 3. Proposed Changes

### Phase 1: Service Layer Refactoring
- **Create `lib/aeon-graph.ts`**: A new service layer strictly typed to the McKenney-Lacan schema.
- **Define Interfaces**: `Actor`, `Asset`, `Concept`, `Event`, `Group`, `Vulnerability`, `ThreatActor`.
- **Implement Methods**: `getPsychometrics(actorId)`, `getEventTimeline(eventId)`, `findPath(start, end)`.

### Phase 2: Ingestion Pipeline Integration (NER11)
- **Implement `api/upload/route.ts`**:
    1.  Receive file.
    2.  Call `ner11-gold-api` (gRPC/HTTP).
    3.  Display extracted entities to user for verification.
    4.  Submit to Neo4j via `aeon-graph.ts`.

### Phase 3: UI Realignment
- **Dashboard**: Show "Psychohistory State" (Global Tension, Sector Risk) instead of generic stats.
- **Threat Intel**: Update queries to use `ThreatActor` -> `Event` (Campaign) -> `Group` (Sector) relationships.
- **Graph Explorer**: Use `react-force-graph` or similar to visualize the 7-node schema.

## 4. Implementation Steps

1.  [ ] Create `lib/aeon-graph.ts` with McKenney-Lacan types.
2.  [ ] Update `api/threat-intel/landscape/route.ts` to use the new schema.
3.  [ ] Implement `api/upload/route.ts` with NER11 client.
4.  [ ] Create `components/graph/EntityReview.tsx` for NER results.

## 5. Verification
- **Unit Tests**: Test `aeon-graph.ts` against a local Neo4j instance.
- **Integration Tests**: Upload a document, verify entities appear in the graph.
- **User Review**: Verify the dashboard reflects the "Psychohistory" metrics.
