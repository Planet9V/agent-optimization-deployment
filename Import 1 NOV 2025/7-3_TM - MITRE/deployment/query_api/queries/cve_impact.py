"""
CVE Impact Query Executor
File: queries/cve_impact.py
Created: 2025-11-08
Purpose: Execute queries for Question 1 and 3 (CVE impact analysis)
"""

from typing import Dict, Any
from queries.base import QueryExecutor


class CVEImpactExecutor(QueryExecutor):
    """Execute CVE impact queries"""

    def get_query_simple(self) -> str:
        """Simple query - Direct CVE to Equipment"""
        return """
        MATCH (cve:CVE {id: $cveId})
        MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
        MATCH (v)-[:FOUND_IN]->(eq:Equipment)
        RETURN
          cve.id AS cveId,
          cve.description AS cveDescription,
          cve.severity AS severity,
          collect(DISTINCT {
            equipmentId: eq.id,
            equipmentName: eq.name,
            equipmentType: eq.type,
            location: eq.location
          }) AS affectedEquipment,
          count(DISTINCT eq) AS totalAffectedCount
        """

    def get_query_intermediate(self) -> str:
        """Intermediate query - CVE Impact Through Software/OS"""
        return """
        MATCH (cve:CVE {id: $cveId})
        MATCH path = (cve)-[:AFFECTS]->(v:Vulnerability)
          -[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)
        WITH cve, eq, path,
          [n IN nodes(path) WHERE n:Application OR n:OperatingSystem OR n:Software | n] AS impactedComponents
        RETURN
          cve.id AS cveId,
          cve.severity AS severity,
          cve.cvssScore AS cvssScore,
          collect(DISTINCT {
            equipmentId: eq.id,
            equipmentName: eq.name,
            equipmentType: eq.type,
            facilityId: eq.facilityId,
            impactPath: [c IN impactedComponents |
              CASE
                WHEN c:Application THEN 'App: ' + c.name + ' v' + c.version
                WHEN c:OperatingSystem THEN 'OS: ' + c.name + ' ' + c.version
                WHEN c:Software THEN 'Software: ' + c.name + ' v' + c.version
              END
            ]
          }) AS affectedEquipment,
          count(DISTINCT eq) AS totalImpact
        ORDER BY cve.cvssScore DESC
        """

    def get_query_advanced(self) -> str:
        """Advanced query - Multi-Facility CVE Impact with CWE/CAPEC Context"""
        return """
        MATCH (cve:CVE {id: $cveId})

        OPTIONAL MATCH (cve)-[:EXPLOITS]->(cwe:CWE)
        OPTIONAL MATCH (cwe)-[:ENABLES]->(capec:CAPEC)

        MATCH path = (cve)-[:AFFECTS]->(v:Vulnerability)
          -[:FOUND_IN|RUNS_ON|INSTALLED_ON*1..4]->(eq:Equipment)

        OPTIONAL MATCH (eq)-[:LOCATED_IN]->(facility:Facility)

        WITH cve, cwe, capec, eq, facility, path,
          [n IN nodes(path) WHERE n:Application OR n:OperatingSystem OR n:Software | n] AS components

        RETURN
          cve.id AS cveId,
          cve.description AS description,
          cve.severity AS severity,
          cve.cvssScore AS cvssScore,
          cve.publishedDate AS publishedDate,

          collect(DISTINCT {
            cweId: cwe.id,
            cweName: cwe.name,
            cweType: cwe.type
          }) AS exploitedWeaknesses,

          collect(DISTINCT {
            capecId: capec.id,
            capecName: capec.name,
            capecLikelihood: capec.likelihood
          }) AS enabledAttackPatterns,

          collect(DISTINCT {
            facility: {
              id: facility.id,
              name: facility.name,
              location: facility.location
            },
            equipment: {
              id: eq.id,
              name: eq.name,
              type: eq.type,
              criticality: eq.criticality
            },
            vulnerableComponents: [c IN components |
              CASE
                WHEN c:Application THEN {type: 'Application', name: c.name, version: c.version}
                WHEN c:OperatingSystem THEN {type: 'OS', name: c.name, version: c.version}
                WHEN c:Software THEN {type: 'Software', name: c.name, version: c.version}
              END
            ],
            pathLength: length(path)
          }) AS impactDetails,

          count(DISTINCT eq) AS totalEquipmentImpacted,
          count(DISTINCT facility) AS totalFacilitiesImpacted
        """


class TodayCVEImpactExecutor(QueryExecutor):
    """Execute today's CVE impact queries (Question 3)"""

    def get_query_simple(self) -> str:
        """Simple query - Today's CVEs by Facility"""
        return """
        MATCH (cve:CVE)
        WHERE date(cve.publishedDate) = date($today)

        MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
          -[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)
          -[:LOCATED_IN]->(f:Facility {id: $facilityId})

        RETURN
          cve.id AS cveId,
          cve.severity AS severity,
          cve.cvssScore AS cvssScore,
          cve.publishedDate AS publishedDate,
          count(DISTINCT eq) AS affectedEquipmentCount,
          collect(DISTINCT eq.name) AS affectedEquipmentNames
        ORDER BY cve.cvssScore DESC
        """

    def get_query_intermediate(self) -> str:
        """Intermediate query - Today's CVEs with SBOM Component Matching"""
        return """
        MATCH (cve:CVE)
        WHERE date(cve.publishedDate) = date($today)

        MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
        MATCH (v)-[:FOUND_IN]->(component)
        WHERE component:Application OR component:Software OR component:OperatingSystem

        MATCH (component)-[:INSTALLED_ON|RUNS_ON]->(eq:Equipment)
          -[:LOCATED_IN]->(f:Facility {id: $facilityId})

        OPTIONAL MATCH (component)-[:MANUFACTURED_BY]->(vendor:Vendor)

        RETURN
          cve.id AS cveId,
          cve.description AS description,
          cve.severity AS severity,
          cve.cvssScore AS cvssScore,
          cve.publishedDate AS publishedDate,

          collect(DISTINCT {
            componentType: labels(component)[0],
            componentName: component.name,
            componentVersion: component.version,
            vendor: vendor.name,
            equipmentId: eq.id,
            equipmentName: eq.name,
            equipmentType: eq.type,
            criticality: eq.criticality
          }) AS sbomImpact,

          count(DISTINCT eq) AS totalAffectedEquipment,
          count(DISTINCT component) AS totalAffectedComponents

        ORDER BY cve.cvssScore DESC, totalAffectedEquipment DESC
        """

    def get_query_advanced(self) -> str:
        """Advanced query - Multi-Facility Today's CVE Impact with Complete SBOM Analysis"""
        return """
        MATCH (cve:CVE)
        WHERE date(cve.publishedDate) = date($today)
          AND ($minSeverity IS NULL OR cve.severity IN $minSeverity)

        OPTIONAL MATCH (cve)-[:EXPLOITS]->(cwe:CWE)
        OPTIONAL MATCH (cwe)-[:ENABLES]->(capec:CAPEC)

        MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
        MATCH (v)-[:FOUND_IN]->(component)
        WHERE component:Application OR component:Software OR component:OperatingSystem

        MATCH (component)-[:INSTALLED_ON|RUNS_ON]->(eq:Equipment)
          -[:LOCATED_IN]->(f:Facility)
        WHERE $facilityIds IS NULL OR f.id IN $facilityIds

        OPTIONAL MATCH (component)-[:MANUFACTURED_BY]->(vendor:Vendor)
        OPTIONAL MATCH (cve)-[:MITIGATED_BY]->(mitigation:Mitigation)

        WITH cve, cwe, capec, v, component, vendor, eq, f, mitigation,
          [(eq)-[:RUNS|INSTALLS*1..2]->(sbomItem)
           WHERE sbomItem:Application OR sbomItem:Software OR sbomItem:OperatingSystem |
           {
             type: labels(sbomItem)[0],
             name: sbomItem.name,
             version: sbomItem.version,
             vulnerable: EXISTS((v)-[:FOUND_IN]->(sbomItem))
           }
          ] AS fullSBOM

        RETURN
          {
            id: cve.id,
            description: cve.description,
            severity: cve.severity,
            cvssScore: cve.cvssScore,
            publishedDate: cve.publishedDate,
            lastModified: cve.lastModifiedDate
          } AS cveDetails,

          collect(DISTINCT {
            cweId: cwe.id,
            cweName: cwe.name,
            cweDescription: cwe.description,
            associatedAttackPatterns: [(cwe)-[:ENABLES]->(cap:CAPEC) |
              {id: cap.id, name: cap.name, likelihood: cap.likelihood}
            ]
          }) AS weaknessContext,

          collect(DISTINCT {
            facilityId: f.id,
            facilityName: f.name,
            facilityLocation: f.location,
            criticalityLevel: f.criticality,
            equipmentCount: count(DISTINCT eq)
          }) AS facilityImpact,

          collect(DISTINCT {
            equipment: {
              id: eq.id,
              name: eq.name,
              type: eq.type,
              criticality: eq.criticality,
              facilityId: f.id
            },
            vulnerableComponent: {
              type: labels(component)[0],
              name: component.name,
              version: component.version,
              vendor: vendor.name,
              endOfLife: component.endOfLife
            },
            completeSBOM: fullSBOM,
            vulnerabilityDetails: {
              id: v.id,
              description: v.description,
              exploitable: v.exploitable
            }
          }) AS detailedImpact,

          collect(DISTINCT {
            mitigationId: mitigation.id,
            description: mitigation.description,
            type: mitigation.type,
            effectiveness: mitigation.effectiveness
          }) AS availableMitigations,

          count(DISTINCT f) AS totalFacilitiesAffected,
          count(DISTINCT eq) AS totalEquipmentAffected,
          count(DISTINCT component) AS totalSBOMComponentsAffected,
          avg(cve.cvssScore) AS avgCVSSScore

        ORDER BY cve.cvssScore DESC, totalEquipmentAffected DESC
        """

    def _prepare_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare parameters with today's date default"""
        from datetime import datetime

        if 'today' not in params:
            params['today'] = datetime.utcnow().strftime('%Y-%m-%d')

        return params
