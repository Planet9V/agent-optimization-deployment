# Neo4j Schema Inventory (Exhaustive Discovery)

**Date**: 2025-11-26
**Source**: Direct Cypher Queries (`db.schema.nodeTypeProperties`, `SHOW CONSTRAINTS`, `MATCH (n)`)
**Database Status**: Mixed State (Active Data + Dormant Constraints)
**Total Nodes**: 2068

This document provides the **absolute ground truth** of the Neo4j database schema. It distinguishes between **Active Nodes** (currently populated with data) and **Dormant Schema** (labels defined by constraints but currently having 0 nodes).

---

## 1. Active Node Labels (Populated)
These 8 label types currently exist in the database with data.

### 1.1 Threat Intelligence
*   **`AttackTechnique`** (Count: 823)
    *   *Properties*: `id`, `name`, `description`, `tactics`, `is_subtechnique`, `stix_id`, `modified`
*   **`ThreatActor`** (Count: 187)
    *   *Properties*: `actorId`, `name`, `description`, `aliases`, `country`, `sophistication`, `capabilityLevel`, `operatingModel`, `primaryTargets`, `attributionConfidence`, `stix_id`
*   **`Mitigation`** (Count: 285)
    *   *Properties*: `id`, `name`, `description`, `stix_id`

### 1.2 Infrastructure & Software
*   **`Software`** (Count: 760)
    *   *Properties*: `name`, `description`, `type`, `stix_id`

### 1.3 Governance & Context
*   **`Sector`** (Count: 5)
    *   *Properties*: `sectorId`, `name`, `description`, `criticalityLevel`, `estimatedAssets`, `regulatoryFramework`, `knownThreatActors`
*   **`ComplianceFramework`** (Count: 3)
    *   *Properties*: `frameworkId`, `name`, `description`, `version`, `effectiveDate`, `controlCount`, `applicableSectors`
*   **`Organization`** (Count: 2)
    *   *Properties*: `organizationId`, `name`, `acronym`, `organizationType`, `sector`, `country`, `state`, `primaryMission`, `employeeCount`, `riskProfile`, `criticality`
*   **`Location`** (Count: 3)
    *   *Properties*: `locationId`, `name`, `locationType`, `city`, `state`, `country`, `timezone`, `population`, `riskProfile`, `criticalAssets`

---

## 2. Dormant Schema (Constraints Only)
The following **17 labels** are defined in the database schema (via Uniqueness Constraints) but currently have **0 nodes**. These represent the "Intended" or "Previous" schema, largely focused on OT/ICS and Vulnerabilities.

*   **`AttackPattern`** (Constraint: `patternId` must be unique)
*   **`CVE`** (Constraint: `cveId` must be unique)
*   **`DistributedEnergyResource`** (Constraint: `derId` must be unique)
*   **`EnergyDevice`** (Constraint: `deviceId` must be unique)
*   **`EnergyManagementSystem`** (Constraint: `emsId` must be unique)
*   **`EnergyProperty`** (Constraint: `propertyId` must be unique)
*   **`Exploit`** (Constraint: `exploitId` must be unique)
*   **`IncidentReport`** (Constraint: `incidentId` must be unique)
*   **`MalwareVariant`** (Constraint: `malwareId` must be unique)
*   **`Measurement`** (Constraint: `measurementId` must be unique)
*   **`NERCCIPStandard`** (Constraint: `standardId` must be unique)
*   **`Substation`** (Constraint: `substationId` must be unique)
*   **`TransmissionLine`** (Constraint: `lineId` must be unique)
*   **`VulnerabilityReport`** (Constraint: `reportId` must be unique)
*   **`WaterProperty`** (Constraint: `propertyId` must be unique)
*   **`WaterSystem`** (Constraint: `waterSystemId` must be unique)

---

## 3. Relationship Types (Active)
The following relationship types are currently in use connecting the active nodes.

*   **`BELONGS_TO_SECTOR`**
*   **`MITIGATED_BY`** (`description`)
*   **`MITIGATES`** (`description`)
*   **`OPERATES_IN`**
*   **`PARENT_OF`** (`description`)
*   **`REVOKED_BY`** (`description`)
*   **`REVOKED_BY_REV`** (`description`)
*   **`SUBTECHNIQUE_OF`** (`description`)
*   **`TARGETS_SECTOR`** (`confidence`, `lastObserved`)
*   **`USED_BY`** (`description`)
*   **`USES`** (`description`)

---

## 4. Summary of Discrepancy
*   **Active Graph**: A small, high-level Threat Intelligence graph (Actors, Techniques, Software, Mitigations).
*   **Shadow Schema**: A large, detailed OT/ICS schema (Energy, Water, Devices) that is currently **empty**.

This confirms the "Split Brain" state of the database: The structure for the OT/ICS Digital Twin exists (as constraints), but the data currently loaded is primarily STIX-based Threat Intelligence.
