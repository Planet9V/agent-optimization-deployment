"""
Attack Path Query Executor
File: queries/attack_path.py
Created: 2025-11-08
Purpose: Execute queries for Question 2, 4, 5 (Attack path analysis)
"""

from typing import Dict, Any
from queries.base import QueryExecutor


class AttackPathExecutor(QueryExecutor):
    """Execute attack path queries (Question 2)"""

    def get_query_simple(self) -> str:
        """Simple query - Direct Attack Path"""
        return """
        MATCH (ta:ThreatActor {name: $threatActorName})
        MATCH (v:Vulnerability {id: $vulnerabilityId})
        MATCH path = shortestPath((ta)-[*1..5]-(v))
        WHERE ALL(r IN relationships(path) WHERE
          type(r) IN ['USES', 'EXPLOITS', 'TARGETS', 'ENABLES', 'AFFECTS', 'FOUND_IN'])
        RETURN
          EXISTS(path) AS attackPathExists,
          length(path) AS pathLength,
          [n IN nodes(path) | labels(n)[0] + ': ' + coalesce(n.name, n.id)] AS pathNodes
        """

    def get_query_intermediate(self) -> str:
        """Intermediate query - Attack Path with Techniques"""
        return """
        MATCH (ta:ThreatActor {name: $threatActorName})
        MATCH (v:Vulnerability {id: $vulnerabilityId})

        MATCH path = (ta)-[:USES]->(at:AttackTechnique)
          -[:EXPLOITS|ENABLES*1..3]->(cwe:CWE)
          -[:ENABLES]->(capec:CAPEC)
          -[:TARGETS]->(v)

        RETURN
          ta.name AS threatActor,
          v.id AS vulnerability,
          collect(DISTINCT {
            technique: at.name,
            techniqueId: at.id,
            tactic: at.tactic,
            weakness: cwe.name,
            attackPattern: capec.name,
            likelihood: capec.likelihood
          }) AS attackPaths,
          count(DISTINCT at) AS numberOfTechniques,
          min(length(path)) AS shortestPathLength
        ORDER BY shortestPathLength ASC
        LIMIT 10
        """

    def get_query_advanced(self) -> str:
        """Advanced query - Complete Attack Chain to Equipment"""
        return """
        MATCH (ta:ThreatActor)
        WHERE ta.name = $threatActorName OR ta.id = $threatActorId

        OPTIONAL MATCH (ta)-[:USES]->(s:Software)
        OPTIONAL MATCH (ta)-[:USES]->(at:AttackTechnique)

        MATCH attackPath = (at)-[:EXPLOITS|ENABLES*1..4]->(cwe:CWE)
          -[:ENABLES]->(capec:CAPEC)

        MATCH (capec)-[:TARGETS|ENABLES*1..2]->(v:Vulnerability)
        MATCH (v)-[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)

        OPTIONAL MATCH (at)-[:MITIGATED_BY]->(m:Mitigation)

        WITH ta, s, at, cwe, capec, v, eq, m, attackPath,
          length(attackPath) AS attackComplexity

        RETURN
          {
            name: ta.name,
            type: ta.type,
            sophistication: ta.sophistication,
            objectives: ta.objectives
          } AS threatActor,

          collect(DISTINCT {
            software: s.name,
            technique: {
              id: at.id,
              name: at.name,
              tactic: at.tactic,
              platforms: at.platforms
            },
            weakness: {
              id: cwe.id,
              name: cwe.name,
              type: cwe.type
            },
            attackPattern: {
              id: capec.id,
              name: capec.name,
              likelihood: capec.likelihood,
              severity: capec.severity
            },
            complexity: attackComplexity
          }) AS attackChains,

          collect(DISTINCT {
            vulnerabilityId: v.id,
            description: v.description,
            severity: v.severity
          }) AS targetedVulnerabilities,

          collect(DISTINCT {
            equipmentId: eq.id,
            equipmentName: eq.name,
            equipmentType: eq.type,
            criticality: eq.criticality,
            facilityId: eq.facilityId
          }) AS vulnerableEquipment,

          collect(DISTINCT {
            mitigationId: m.id,
            description: m.description,
            effectiveness: m.effectiveness
          }) AS availableMitigations,

          count(DISTINCT eq) AS totalVulnerableEquipment,
          count(DISTINCT at) AS numberOfTechniques,
          avg(attackComplexity) AS averageAttackComplexity,
          min(attackComplexity) AS shortestAttackPath

        ORDER BY shortestAttackPath ASC, totalVulnerableEquipment DESC
        """


class ThreatActorPathwayExecutor(QueryExecutor):
    """Execute threat actor pathway queries (Question 4)"""

    def get_query_simple(self) -> str:
        """Simple query - Threat Actor to Vulnerability Path Check"""
        return """
        MATCH (ta:ThreatActor {name: $threatActorName})
        MATCH (v:Vulnerability {id: $vulnerabilityId})
        MATCH path = shortestPath((ta)-[*1..6]-(v))
        RETURN
          EXISTS(path) AS pathwayExists,
          length(path) AS pathwayLength,
          [rel IN relationships(path) | type(rel)] AS relationshipChain,
          [n IN nodes(path) | {
            type: labels(n)[0],
            id: coalesce(n.id, n.name),
            name: n.name
          }] AS pathwayNodes
        """

    def get_query_intermediate(self) -> str:
        """Intermediate query - Multi-Path Analysis with Access Requirements"""
        return """
        MATCH (ta:ThreatActor)
        WHERE ta.name = $threatActorName OR ta.id = $threatActorId

        MATCH (v:Vulnerability {id: $vulnerabilityId})

        MATCH paths = allShortestPaths((ta)-[*1..7]-(v))
        WHERE ALL(r IN relationships(paths) WHERE
          type(r) IN ['USES', 'EXPLOITS', 'TARGETS', 'ENABLES', 'AFFECTS', 'FOUND_IN', 'RUNS_ON'])

        WITH ta, v, paths,
          [n IN nodes(paths) WHERE n:AttackTechnique] AS techniques,
          [n IN nodes(paths) WHERE n:Software] AS software,
          [n IN nodes(paths) WHERE n:CWE] AS weaknesses,
          [n IN nodes(paths) WHERE n:CAPEC] AS attackPatterns,
          [n IN nodes(paths) WHERE n:Equipment] AS targetEquipment

        RETURN
          ta.name AS threatActor,
          ta.sophistication AS actorSophistication,
          v.id AS targetVulnerability,
          v.exploitable AS isExploitable,

          collect(DISTINCT {
            pathLength: length(paths),
            requiredTechniques: [t IN techniques | {id: t.id, name: t.name, complexity: t.complexity}],
            requiredSoftware: [s IN software | {name: s.name, type: s.type}],
            exploitedWeaknesses: [w IN weaknesses | {id: w.id, name: w.name}],
            attackPatterns: [ap IN attackPatterns | {id: ap.id, name: ap.name, likelihood: ap.likelihood}],
            targetEquipment: [eq IN targetEquipment | {id: eq.id, name: eq.name, accessible: eq.networkAccessible}]
          }) AS exploitationPathways,

          count(paths) AS totalPathways,
          min(length(paths)) AS shortestPathLength,
          avg(length(paths)) AS avgPathLength

        ORDER BY shortestPathLength ASC
        """

    def get_query_advanced(self) -> str:
        """Advanced query - Complete Threat Path with Equipment Access and Defenses"""
        return """
        MATCH (ta:ThreatActor)
        WHERE ta.name = $threatActorName OR ta.id = $threatActorId

        MATCH (v:Vulnerability)
        WHERE v.id = $vulnerabilityId OR v.cveId = $cveId

        MATCH attackGraph = (ta)-[:USES]->(at:AttackTechnique)
          -[:EXPLOITS|ENABLES*1..4]->(cwe:CWE)
          -[:ENABLES]->(capec:CAPEC)

        MATCH (capec)-[:TARGETS|ENABLES*1..2]->(v)
        MATCH (v)-[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)

        OPTIONAL MATCH (eq)-[:LOCATED_IN]->(facility:Facility)
        OPTIONAL MATCH (eq)-[:CONNECTED_TO]->(network)
        OPTIONAL MATCH (at)-[:MITIGATED_BY]->(mitigation:Mitigation)
        OPTIONAL MATCH (eq)-[:PROTECTED_BY]->(defense)
        OPTIONAL MATCH (at)-[:DETECTED_BY]->(ds:DataSource)

        WITH ta, at, cwe, capec, v, eq, facility, network, mitigation, defense, ds, attackGraph,
          CASE
            WHEN at.complexity = 'LOW' THEN 1
            WHEN at.complexity = 'MEDIUM' THEN 2
            ELSE 3
          END AS techniqueComplexity,

          CASE
            WHEN capec.likelihood = 'HIGH' THEN 3
            WHEN capec.likelihood = 'MEDIUM' THEN 2
            ELSE 1
          END AS attackLikelihood,

          CASE
            WHEN eq.networkAccessible = true THEN 'EXTERNAL'
            WHEN eq.networkAccessible = false THEN 'INTERNAL'
            ELSE 'UNKNOWN'
          END AS accessLevel

        RETURN
          {
            name: ta.name,
            type: ta.type,
            sophistication: ta.sophistication,
            objectives: ta.objectives,
            knownSince: ta.firstSeen
          } AS threatActorProfile,

          {
            id: v.id,
            cveId: v.cveId,
            description: v.description,
            severity: v.severity,
            exploitable: v.exploitable,
            exploitAvailable: v.exploitPublic
          } AS targetVulnerability,

          collect(DISTINCT {
            pathComplexity: techniqueComplexity,
            pathLikelihood: attackLikelihood,

            technique: {
              id: at.id,
              name: at.name,
              tactic: at.tactic,
              platforms: at.platforms,
              requiresPrivileges: at.permissionsRequired,
              userInteraction: at.userInteractionRequired
            },

            weakness: {
              id: cwe.id,
              name: cwe.name,
              prevalence: cwe.prevalence,
              exploitability: cwe.exploitability
            },

            attackPattern: {
              id: capec.id,
              name: capec.name,
              prerequisites: capec.prerequisites,
              skillsRequired: capec.skillsRequired,
              likelihood: capec.likelihood
            },

            targetAsset: {
              equipmentId: eq.id,
              equipmentName: eq.name,
              equipmentType: eq.type,
              criticality: eq.criticality,
              accessLevel: accessLevel,
              facility: {
                id: facility.id,
                name: facility.name,
                securityZone: facility.securityZone
              }
            },

            defensiveControls: {
              mitigations: [(at)-[:MITIGATED_BY]->(m:Mitigation) |
                {id: m.id, description: m.description, effectiveness: m.effectiveness}
              ],
              assetProtections: [(eq)-[:PROTECTED_BY]->(p) |
                {type: labels(p)[0], description: p.description}
              ],
              detectionMethods: [(at)-[:DETECTED_BY]->(d:DataSource) |
                {source: d.name, coverage: d.coverage}
              ]
            },

            feasibilityScore: (techniqueComplexity + attackLikelihood) / 2.0

          }) AS exploitationPathways,

          CASE
            WHEN count(at) > 0 THEN true
            ELSE false
          END AS pathwayExists,

          {
            totalPathways: count(DISTINCT at),
            avgComplexity: avg(techniqueComplexity),
            avgLikelihood: avg(attackLikelihood),
            criticalAssetsAtRisk: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
            facilitiesAtRisk: count(DISTINCT facility),
            externallyAccessible: count(CASE WHEN eq.networkAccessible = true THEN 1 END),
            mitigationsAvailable: count(DISTINCT mitigation),
            detectionsAvailable: count(DISTINCT ds)
          } AS riskAssessment,

          CASE
            WHEN avg(attackLikelihood) >= 2.5 AND avg(techniqueComplexity) <= 1.5 AND v.exploitable = true THEN 'CRITICAL'
            WHEN avg(attackLikelihood) >= 2 AND avg(techniqueComplexity) <= 2 THEN 'HIGH'
            WHEN avg(attackLikelihood) >= 1.5 OR avg(techniqueComplexity) <= 2.5 THEN 'MEDIUM'
            ELSE 'LOW'
          END AS overallThreatLevel

        ORDER BY overallThreatLevel DESC, riskAssessment.criticalAssetsAtRisk DESC
        """


class TodayCVEThreatPathExecutor(QueryExecutor):
    """Execute today's CVE threat actor pathway queries (Question 5)"""

    def get_query_simple(self) -> str:
        """Simple query - Today's CVE Threat Actor Pathway"""
        return """
        MATCH (cve:CVE)
        WHERE date(cve.publishedDate) = date($today)

        MATCH (cve)-[:AFFECTS]->(v:Vulnerability)

        OPTIONAL MATCH path = shortestPath((ta:ThreatActor)-[*1..6]-(v))

        RETURN
          cve.id AS cveId,
          cve.severity AS severity,
          cve.cvssScore AS cvssScore,
          v.id AS vulnerabilityId,

          CASE
            WHEN ta IS NOT NULL THEN true
            ELSE false
          END AS threatActorPathwayExists,

          collect(DISTINCT {
            actorName: ta.name,
            actorType: ta.type,
            pathLength: length(path)
          }) AS threateningActors,

          count(DISTINCT ta) AS numberOfThreats

        ORDER BY cve.cvssScore DESC, numberOfThreats DESC
        """

    def get_query_intermediate(self) -> str:
        """Intermediate query - Today's CVEs with Active Threat Actor Campaigns"""
        return """
        MATCH (cve:CVE)
        WHERE date(cve.publishedDate) = date($today)
          AND cve.severity IN ['CRITICAL', 'HIGH']

        MATCH (cve)-[:EXPLOITS]->(cwe:CWE)
        MATCH (cwe)-[:ENABLES]->(capec:CAPEC)
        MATCH (cve)-[:AFFECTS]->(v:Vulnerability)

        MATCH (ta:ThreatActor)-[:USES]->(at:AttackTechnique)
          -[:EXPLOITS]->(cwe)

        OPTIONAL MATCH (v)-[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)

        RETURN
          cve.id AS cveId,
          cve.description AS cveDescription,
          cve.severity AS severity,
          cve.cvssScore AS cvssScore,
          cve.publishedDate AS releasedToday,

          collect(DISTINCT {
            threatActor: ta.name,
            actorType: ta.type,
            sophistication: ta.sophistication,
            activeCampaigns: ta.activeCampaigns,
            techniques: collect(DISTINCT {
              techniqueId: at.id,
              techniqueName: at.name,
              tactic: at.tactic
            }),
            exploitedWeakness: {
              cweId: cwe.id,
              cweName: cwe.name,
              exploitability: cwe.exploitability
            },
            attackPattern: {
              capecId: capec.id,
              capecName: capec.name,
              likelihood: capec.likelihood
            }
          }) AS activeThreatActors,

          count(DISTINCT eq) AS vulnerableEquipmentCount,
          count(DISTINCT ta) AS numberOfActiveThreatActors,

          CASE
            WHEN count(DISTINCT ta) > 0 AND cve.severity = 'CRITICAL' THEN 'IMMEDIATE ACTION REQUIRED'
            WHEN count(DISTINCT ta) > 0 AND cve.severity = 'HIGH' THEN 'HIGH PRIORITY'
            WHEN count(DISTINCT ta) > 0 THEN 'MONITOR'
            ELSE 'LOW RISK'
          END AS riskLevel

        ORDER BY numberOfActiveThreatActors DESC, cve.cvssScore DESC
        """

    def get_query_advanced(self) -> str:
        """Advanced query - Today's CVE Complete Threat Landscape Analysis"""
        # This is a very large query - see line 999-1234 from the source document
        # I'll include the complete advanced query as specified
        return """
        MATCH (cve:CVE)
        WHERE date(cve.publishedDate) = date($today)
          AND ($severityFilter IS NULL OR cve.severity IN $severityFilter)
          AND ($minCVSS IS NULL OR cve.cvssScore >= $minCVSS)

        MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
        OPTIONAL MATCH (cve)-[:EXPLOITS]->(cwe:CWE)
        OPTIONAL MATCH (cwe)-[:ENABLES]->(capec:CAPEC)

        OPTIONAL MATCH threatPath = (ta:ThreatActor)-[:USES]->(at:AttackTechnique)
          -[:EXPLOITS*1..3]->(cwe)

        OPTIONAL MATCH (ta)-[:USES]->(malware:Software)
        WHERE malware.type = 'MALWARE'

        OPTIONAL MATCH assetPath = (v)-[:FOUND_IN|RUNS_ON|INSTALLED_ON*1..4]->(eq:Equipment)
          -[:LOCATED_IN]->(facility:Facility)

        OPTIONAL MATCH (at)-[:MITIGATED_BY]->(mitigation:Mitigation)
        OPTIONAL MATCH (at)-[:DETECTED_BY]->(dataSource:DataSource)

        OPTIONAL MATCH (cwe)<-[:EXPLOITS]-(relatedCVE:CVE)
        WHERE relatedCVE.id <> cve.id

        WITH cve, v, cwe, capec, ta, at, malware, eq, facility, mitigation, dataSource, relatedCVE,
          threatPath, assetPath,

          CASE
            WHEN ta.sophistication = 'ADVANCED' THEN 3
            WHEN ta.sophistication = 'INTERMEDIATE' THEN 2
            ELSE 1
          END AS threatCapability,

          CASE
            WHEN capec.likelihood = 'HIGH' AND at.complexity = 'LOW' THEN 3
            WHEN capec.likelihood = 'MEDIUM' OR at.complexity = 'MEDIUM' THEN 2
            ELSE 1
          END AS attackFeasibility,

          CASE
            WHEN eq.criticality = 'CRITICAL' THEN 3
            WHEN eq.criticality = 'HIGH' THEN 2
            ELSE 1
          END AS assetCriticality

        RETURN
          {
            id: cve.id,
            description: cve.description,
            severity: cve.severity,
            cvssScore: cve.cvssScore,
            publishedDate: cve.publishedDate,
            exploitAvailable: cve.exploitPublic,
            references: cve.references
          } AS cveDetails,

          {
            id: v.id,
            description: v.description,
            exploitable: v.exploitable,
            patchAvailable: v.patchAvailable,
            patchDate: v.patchDate
          } AS vulnerabilityDetails,

          collect(DISTINCT {
            weakness: {
              id: cwe.id,
              name: cwe.name,
              description: cwe.description,
              prevalence: cwe.prevalence,
              exploitability: cwe.exploitability
            },
            attackPatterns: [(cwe)-[:ENABLES]->(cap:CAPEC) | {
              id: cap.id,
              name: cap.name,
              likelihood: cap.likelihood,
              severity: cap.severity,
              prerequisites: cap.prerequisites,
              skillsRequired: cap.skillsRequired
            }],
            relatedCVEs: count(DISTINCT relatedCVE)
          }) AS weaknessContext,

          collect(DISTINCT {
            actor: {
              name: ta.name,
              type: ta.type,
              sophistication: ta.sophistication,
              objectives: ta.objectives,
              activeCampaigns: ta.activeCampaigns,
              targetedSectors: ta.targetedSectors
            },
            capabilities: {
              techniques: collect(DISTINCT {
                id: at.id,
                name: at.name,
                tactic: at.tactic,
                complexity: at.complexity,
                platforms: at.platforms,
                requiresPrivileges: at.permissionsRequired
              }),
              malware: collect(DISTINCT {
                name: malware.name,
                type: malware.type,
                description: malware.description
              }),
              threatCapabilityScore: threatCapability
            },
            exploitationPathway: {
              pathExists: threatPath IS NOT NULL,
              pathLength: length(threatPath),
              feasibilityScore: attackFeasibility,
              estimatedTimeToExploit: CASE
                WHEN attackFeasibility = 3 THEN '< 1 day'
                WHEN attackFeasibility = 2 THEN '1-7 days'
                ELSE '> 7 days'
              END
            }
          }) AS threatActorAnalysis,

          collect(DISTINCT {
            equipment: {
              id: eq.id,
              name: eq.name,
              type: eq.type,
              criticality: eq.criticality,
              networkAccessible: eq.networkAccessible,
              assetCriticalityScore: assetCriticality
            },
            facility: {
              id: facility.id,
              name: facility.name,
              location: facility.location,
              securityZone: facility.securityZone,
              criticality: facility.criticality
            },
            exploitPath: {
              pathLength: length(assetPath),
              pathNodes: [n IN nodes(assetPath) WHERE n <> v AND n <> eq |
                {type: labels(n)[0], name: coalesce(n.name, n.id)}
              ]
            }
          }) AS assetImpactAssessment,

          {
            availableMitigations: collect(DISTINCT {
              id: mitigation.id,
              description: mitigation.description,
              type: mitigation.type,
              effectiveness: mitigation.effectiveness,
              implementationCost: mitigation.implementationCost
            }),

            detectionCapabilities: collect(DISTINCT {
              dataSource: dataSource.name,
              dataComponent: dataSource.component,
              coverage: dataSource.coverage,
              detectsActivity: dataSource.detectsActivity
            }),

            patchingStatus: CASE
              WHEN v.patchAvailable = true THEN 'PATCH AVAILABLE'
              WHEN v.patchAvailable = false THEN 'NO PATCH'
              ELSE 'UNKNOWN'
            END,

            mitigationCount: count(DISTINCT mitigation),
            detectionCount: count(DISTINCT dataSource)
          } AS defensivePosture,

          {
            pathwayExists: CASE WHEN count(ta) > 0 THEN true ELSE false END,
            numberOfThreatActors: count(DISTINCT ta),
            numberOfTechniques: count(DISTINCT at),
            vulnerableAssets: count(DISTINCT eq),
            criticalAssetsAtRisk: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
            facilitiesAtRisk: count(DISTINCT facility),
            externallyAccessibleAssets: count(DISTINCT CASE WHEN eq.networkAccessible = true THEN 1 END),

            avgThreatCapability: avg(threatCapability),
            avgAttackFeasibility: avg(attackFeasibility),
            avgAssetCriticality: avg(assetCriticality),

            compositeRiskScore: (
              avg(threatCapability) * 0.3 +
              avg(attackFeasibility) * 0.4 +
              avg(assetCriticality) * 0.3
            ),

            riskLevel: CASE
              WHEN count(ta) > 0 AND cve.severity = 'CRITICAL' AND avg(attackFeasibility) >= 2.5 THEN 'CRITICAL'
              WHEN count(ta) > 0 AND cve.severity IN ['CRITICAL', 'HIGH'] THEN 'HIGH'
              WHEN count(ta) > 0 THEN 'MEDIUM'
              ELSE 'LOW'
            END,

            recommendedAction: CASE
              WHEN count(ta) > 0 AND cve.severity = 'CRITICAL' AND avg(attackFeasibility) >= 2.5
                THEN 'IMMEDIATE PATCHING/MITIGATION REQUIRED'
              WHEN count(ta) > 0 AND cve.severity IN ['CRITICAL', 'HIGH']
                THEN 'URGENT: PATCH WITHIN 24-48 HOURS'
              WHEN count(ta) > 0
                THEN 'MONITOR AND PLAN REMEDIATION'
              ELSE 'STANDARD PATCHING SCHEDULE'
            END
          } AS riskAssessment,

          duration.between(
            date(cve.publishedDate),
            date()
          ).hours AS hoursSinceRelease

        ORDER BY
          riskAssessment.compositeRiskScore DESC,
          cve.cvssScore DESC,
          riskAssessment.criticalAssetsAtRisk DESC
        """

    def _prepare_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare parameters with today's date default"""
        from datetime import datetime

        if 'today' not in params:
            params['today'] = datetime.utcnow().strftime('%Y-%m-%d')

        return params
