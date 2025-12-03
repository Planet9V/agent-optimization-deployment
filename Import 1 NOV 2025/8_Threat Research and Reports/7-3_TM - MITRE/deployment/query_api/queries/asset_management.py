"""
Asset Management Query Executor
File: queries/asset_management.py
Created: 2025-11-08
Purpose: Execute queries for Question 6, 7, 8 (Asset inventory and location)
"""

from typing import Dict, Any
from queries.base import QueryExecutor


class EquipmentInventoryExecutor(QueryExecutor):
    """Execute equipment inventory queries (Question 6)"""

    def get_query_simple(self) -> str:
        """Simple query - Equipment Count by Type"""
        return """
        MATCH (eq:Equipment)
        WHERE eq.type = $equipmentType
        RETURN
          eq.type AS equipmentType,
          count(eq) AS totalCount,
          collect(eq.name) AS equipmentNames
        """

    def get_query_intermediate(self) -> str:
        """Intermediate query - Equipment Inventory with Facility Breakdown"""
        return """
        MATCH (eq:Equipment)
        WHERE $equipmentType IS NULL OR eq.type = $equipmentType

        OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)

        RETURN
          eq.type AS equipmentType,
          count(eq) AS totalCount,

          collect(DISTINCT {
            facilityId: f.id,
            facilityName: f.name,
            facilityLocation: f.location,
            equipmentInFacility: count(eq)
          }) AS facilityBreakdown,

          collect(DISTINCT {
            status: eq.status,
            count: count(eq)
          }) AS statusBreakdown,

          collect(DISTINCT {
            criticality: eq.criticality,
            count: count(eq)
          }) AS criticalityBreakdown

        ORDER BY totalCount DESC
        """

    def get_query_advanced(self) -> str:
        """Advanced query - Comprehensive Equipment Inventory Analysis"""
        return """
        MATCH (eq:Equipment)
        WHERE $equipmentType IS NULL OR eq.type = $equipmentType
          AND ($facilityId IS NULL OR EXISTS((eq)-[:LOCATED_IN]->(:Facility {id: $facilityId})))
          AND ($criticalityLevel IS NULL OR eq.criticality = $criticalityLevel)

        OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)
        OPTIONAL MATCH (eq)<-[:INSTALLED_ON|RUNS_ON]-(software)
        WHERE software:Application OR software:OperatingSystem OR software:Software

        OPTIONAL MATCH (eq)-[:MANUFACTURED_BY]->(vendor:Vendor)
        OPTIONAL MATCH (eq)<-[:FOUND_IN|RUNS_ON*1..3]-(v:Vulnerability)
        OPTIONAL MATCH (v)<-[:AFFECTS]-(cve:CVE)

        WITH eq.type AS equipmentType,
          eq, f, vendor, software, v, cve,

          duration.between(date(eq.installDate), date()).days AS ageInDays,

          CASE
            WHEN date(eq.lastMaintenanceDate) < date() - duration({days: 90}) THEN 'OVERDUE'
            WHEN date(eq.lastMaintenanceDate) < date() - duration({days: 30}) THEN 'DUE_SOON'
            ELSE 'CURRENT'
          END AS maintenanceStatus

        RETURN
          equipmentType,
          count(DISTINCT eq) AS totalCount,

          {
            avgAge: avg(ageInDays),
            oldestEquipment: max(ageInDays),
            newestEquipment: min(ageInDays)
          } AS ageStatistics,

          collect(DISTINCT {
            facilityId: f.id,
            facilityName: f.name,
            location: f.location,
            count: count(DISTINCT eq)
          }) AS facilityDistribution,

          {
            operational: count(DISTINCT CASE WHEN eq.status = 'OPERATIONAL' THEN eq END),
            maintenance: count(DISTINCT CASE WHEN eq.status = 'MAINTENANCE' THEN eq END),
            decommissioned: count(DISTINCT CASE WHEN eq.status = 'DECOMMISSIONED' THEN eq END),
            offline: count(DISTINCT CASE WHEN eq.status = 'OFFLINE' THEN eq END)
          } AS statusBreakdown,

          {
            critical: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
            high: count(DISTINCT CASE WHEN eq.criticality = 'HIGH' THEN eq END),
            medium: count(DISTINCT CASE WHEN eq.criticality = 'MEDIUM' THEN eq END),
            low: count(DISTINCT CASE WHEN eq.criticality = 'LOW' THEN eq END)
          } AS criticalityBreakdown,

          collect(DISTINCT {
            vendor: vendor.name,
            count: count(DISTINCT eq),
            models: collect(DISTINCT eq.model)
          }) AS vendorDistribution,

          {
            totalApplications: count(DISTINCT CASE WHEN software:Application THEN software END),
            totalOS: count(DISTINCT CASE WHEN software:OperatingSystem THEN software END),
            totalSoftware: count(DISTINCT CASE WHEN software:Software THEN software END),
            softwareList: collect(DISTINCT {
              type: labels(software)[0],
              name: software.name,
              version: software.version,
              equipmentCount: count(DISTINCT eq)
            })
          } AS softwareInventory,

          {
            totalVulnerabilities: count(DISTINCT v),
            criticalVulnerabilities: count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END),
            highVulnerabilities: count(DISTINCT CASE WHEN cve.severity = 'HIGH' THEN v END),
            equipmentWithVulnerabilities: count(DISTINCT CASE WHEN v IS NOT NULL THEN eq END),
            vulnerabilityRate: CASE
              WHEN count(DISTINCT eq) > 0
              THEN toFloat(count(DISTINCT CASE WHEN v IS NOT NULL THEN eq END)) / count(DISTINCT eq)
              ELSE 0.0
            END
          } AS vulnerabilityAssessment,

          {
            current: count(DISTINCT CASE WHEN maintenanceStatus = 'CURRENT' THEN eq END),
            dueSoon: count(DISTINCT CASE WHEN maintenanceStatus = 'DUE_SOON' THEN eq END),
            overdue: count(DISTINCT CASE WHEN maintenanceStatus = 'OVERDUE' THEN eq END)
          } AS maintenanceStatusBreakdown,

          {
            externallyAccessible: count(DISTINCT CASE WHEN eq.networkAccessible = true THEN eq END),
            internalOnly: count(DISTINCT CASE WHEN eq.networkAccessible = false THEN eq END),
            unknown: count(DISTINCT CASE WHEN eq.networkAccessible IS NULL THEN eq END)
          } AS networkAccessibility,

          collect(DISTINCT {
            equipmentId: eq.id,
            name: eq.name,
            model: eq.model,
            serialNumber: eq.serialNumber,
            status: eq.status,
            criticality: eq.criticality,
            facilityId: f.id,
            facilityName: f.name,
            vendor: vendor.name,
            installDate: eq.installDate,
            ageInDays: ageInDays,
            maintenanceStatus: maintenanceStatus,
            lastMaintenance: eq.lastMaintenanceDate,
            vulnerabilityCount: count(DISTINCT v),
            criticalVulnerabilities: count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END)
          }) AS detailedInventory

        ORDER BY totalCount DESC
        """


class SoftwareInventoryExecutor(QueryExecutor):
    """Execute software inventory queries (Question 7)"""

    def get_query_simple(self) -> str:
        """Simple query - Check Application/OS Existence"""
        return """
        MATCH (software)
        WHERE (software:Application OR software:OperatingSystem)
          AND software.name = $softwareName
          AND ($version IS NULL OR software.version = $version)

        RETURN
          EXISTS((software)) AS exists,
          count(software) AS instanceCount,
          labels(software)[0] AS softwareType,
          collect(DISTINCT software.version) AS versionsFound
        """

    def get_query_intermediate(self) -> str:
        """Intermediate query - Application/OS Inventory with Equipment Mapping"""
        return """
        MATCH (software)
        WHERE (software:Application OR software:OperatingSystem OR software:Software)
          AND ($softwareName IS NULL OR software.name CONTAINS $softwareName)
          AND ($version IS NULL OR software.version = $version)
          AND ($vendor IS NULL OR EXISTS((software)-[:MANUFACTURED_BY]->(:Vendor {name: $vendor})))

        OPTIONAL MATCH (software)-[:INSTALLED_ON|RUNS_ON]->(eq:Equipment)
        OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)
        OPTIONAL MATCH (software)-[:MANUFACTURED_BY]->(vendor:Vendor)

        RETURN
          labels(software)[0] AS softwareType,
          software.name AS name,
          software.version AS version,
          vendor.name AS vendor,

          count(DISTINCT eq) AS installedOnCount,

          collect(DISTINCT {
            equipmentId: eq.id,
            equipmentName: eq.name,
            equipmentType: eq.type,
            facilityId: f.id,
            facilityName: f.name,
            installDate: software.installDate,
            licenseStatus: software.licenseStatus
          }) AS installations,

          collect(DISTINCT f.name) AS facilities

        ORDER BY installedOnCount DESC
        """

    def get_query_advanced(self) -> str:
        """Advanced query - Complete Software Asset Inventory with Vulnerabilities"""
        return """
        MATCH (software)
        WHERE (software:Application OR software:OperatingSystem OR software:Software)
          AND ($softwareName IS NULL OR software.name CONTAINS $softwareName)
          AND ($version IS NULL OR software.version = $version)
          AND ($softwareType IS NULL OR $softwareType IN labels(software))

        OPTIONAL MATCH (software)-[:MANUFACTURED_BY]->(vendor:Vendor)
        OPTIONAL MATCH (software)-[:INSTALLED_ON|RUNS_ON]->(eq:Equipment)
        OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)
        OPTIONAL MATCH (software)<-[:FOUND_IN]-(v:Vulnerability)
        OPTIONAL MATCH (v)<-[:AFFECTS]-(cve:CVE)
        OPTIONAL MATCH (software)-[:DEPENDS_ON]->(dependency)
        WHERE dependency:Application OR dependency:Software OR dependency:OperatingSystem

        WITH software, vendor, eq, f, v, cve, dependency,
          CASE
            WHEN software.endOfLife IS NOT NULL AND date(software.endOfLife) < date() THEN 'EOL'
            WHEN software.endOfLife IS NOT NULL AND date(software.endOfLife) < date() + duration({months: 6}) THEN 'APPROACHING_EOL'
            WHEN software.endOfLife IS NOT NULL THEN 'SUPPORTED'
            ELSE 'UNKNOWN'
          END AS eolStatus,

          CASE
            WHEN software.licenseExpiration IS NOT NULL AND date(software.licenseExpiration) < date() THEN 'EXPIRED'
            WHEN software.licenseExpiration IS NOT NULL AND date(software.licenseExpiration) < date() + duration({months: 3}) THEN 'EXPIRING_SOON'
            WHEN software.licenseExpiration IS NOT NULL THEN 'VALID'
            ELSE 'UNKNOWN'
          END AS licenseStatus

        RETURN
          {
            type: labels(software)[0],
            name: software.name,
            version: software.version,
            vendor: vendor.name,
            releaseDate: software.releaseDate,
            latestVersion: software.latestVersion,
            architecture: software.architecture,
            language: software.language
          } AS softwareDetails,

          {
            eolStatus: eolStatus,
            endOfLifeDate: software.endOfLife,
            daysUntilEOL: CASE
              WHEN software.endOfLife IS NOT NULL
              THEN duration.between(date(), date(software.endOfLife)).days
              ELSE null
            END,
            licenseStatus: licenseStatus,
            licenseExpiration: software.licenseExpiration,
            licenseType: software.licenseType,
            supportLevel: software.supportLevel
          } AS lifecycleStatus,

          {
            totalInstallations: count(DISTINCT eq),
            facilities: count(DISTINCT f),
            facilityList: collect(DISTINCT {
              facilityId: f.id,
              facilityName: f.name,
              installationCount: count(DISTINCT eq)
            }),
            criticalSystems: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
            productionSystems: count(DISTINCT CASE WHEN eq.environment = 'PRODUCTION' THEN eq END)
          } AS installationSummary,

          {
            totalVulnerabilities: count(DISTINCT v),
            criticalVulns: count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END),
            highVulns: count(DISTINCT CASE WHEN cve.severity = 'HIGH' THEN v END),
            mediumVulns: count(DISTINCT CASE WHEN cve.severity = 'MEDIUM' THEN v END),
            lowVulns: count(DISTINCT CASE WHEN cve.severity = 'LOW' THEN v END),
            vulnerabilitiesList: collect(DISTINCT {
              vulnerabilityId: v.id,
              cveId: cve.id,
              severity: cve.severity,
              cvssScore: cve.cvssScore,
              publishedDate: cve.publishedDate,
              patchAvailable: v.patchAvailable
            })[0..10]
          } AS vulnerabilityAssessment,

          {
            dependencyCount: count(DISTINCT dependency),
            dependencies: collect(DISTINCT {
              type: labels(dependency)[0],
              name: dependency.name,
              version: dependency.version,
              required: dependency.required
            })
          } AS dependencyInfo,

          collect(DISTINCT {
            equipment: {
              id: eq.id,
              name: eq.name,
              type: eq.type,
              criticality: eq.criticality,
              environment: eq.environment
            },
            facility: {
              id: f.id,
              name: f.name,
              location: f.location
            },
            installDetails: {
              installDate: software.installDate,
              installedBy: software.installedBy,
              purpose: software.purpose,
              configurationProfile: software.configProfile
            },
            vulnerabilityCount: count(DISTINCT v),
            criticalVulns: count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END)
          }) AS detailedInstallations,

          {
            complianceStatus: software.complianceStatus,
            regulatoryRequirements: software.regulatoryRequirements,
            riskScore: CASE
              WHEN eolStatus = 'EOL' THEN 10
              WHEN eolStatus = 'APPROACHING_EOL' THEN 7
              WHEN count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END) > 0 THEN 8
              WHEN count(DISTINCT CASE WHEN cve.severity = 'HIGH' THEN v END) > 0 THEN 6
              ELSE 3
            END,
            recommendedAction: CASE
              WHEN eolStatus = 'EOL' THEN 'IMMEDIATE UPGRADE REQUIRED'
              WHEN eolStatus = 'APPROACHING_EOL' THEN 'PLAN UPGRADE'
              WHEN count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END) > 0 THEN 'PATCH IMMEDIATELY'
              WHEN licenseStatus = 'EXPIRED' THEN 'RENEW LICENSE'
              ELSE 'MONITOR'
            END
          } AS complianceAndRisk

        ORDER BY
          complianceAndRisk.riskScore DESC,
          installationSummary.totalInstallations DESC
        """


class AssetLocationExecutor(QueryExecutor):
    """Execute asset location queries (Question 8)"""

    def get_query_simple(self) -> str:
        """Simple query - Find Asset Locations"""
        return """
        MATCH (item)
        WHERE (item:Application OR item:OperatingSystem OR item:Software OR item:Vulnerability)
          AND (item.name = $itemName OR item.id = $itemId)

        MATCH (item)-[:INSTALLED_ON|RUNS_ON|FOUND_IN*1..2]->(eq:Equipment)

        RETURN
          labels(item)[0] AS itemType,
          coalesce(item.name, item.id) AS itemIdentifier,
          item.version AS version,

          collect(DISTINCT {
            equipmentId: eq.id,
            equipmentName: eq.name,
            equipmentType: eq.type,
            location: eq.location
          }) AS assetLocations,

          count(DISTINCT eq) AS totalAssets
        """

    def get_query_intermediate(self) -> str:
        """Intermediate query - Asset Location with Facility Details"""
        return """
        MATCH (item)
        WHERE (item:Application OR item:OperatingSystem OR item:Software OR item:Vulnerability)
          AND (
            item.name CONTAINS $searchTerm OR
            item.id = $searchTerm OR
            item.cveId = $searchTerm
          )

        MATCH path = (item)-[:INSTALLED_ON|RUNS_ON|FOUND_IN*1..3]->(eq:Equipment)

        OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)
        OPTIONAL MATCH (eq)-[:IN_ZONE]->(zone:NetworkZone)
        OPTIONAL MATCH (item)-[:MANUFACTURED_BY]->(vendor:Vendor)

        RETURN
          {
            type: labels(item)[0],
            name: item.name,
            id: item.id,
            version: item.version,
            vendor: vendor.name
          } AS itemDetails,

          collect(DISTINCT {
            equipment: {
              id: eq.id,
              name: eq.name,
              type: eq.type,
              model: eq.model,
              serialNumber: eq.serialNumber,
              ipAddress: eq.ipAddress,
              status: eq.status,
              criticality: eq.criticality
            },
            physicalLocation: {
              facilityId: f.id,
              facilityName: f.name,
              facilityAddress: f.location,
              building: eq.building,
              floor: eq.floor,
              room: eq.room,
              rack: eq.rack,
              rackUnit: eq.rackUnit
            },
            networkLocation: {
              zone: zone.name,
              zoneType: zone.type,
              vlan: eq.vlan,
              subnet: eq.subnet,
              networkAccessible: eq.networkAccessible
            },
            installationPath: [n IN nodes(path) |
              {
                type: labels(n)[0],
                name: coalesce(n.name, n.id)
              }
            ]
          }) AS locations,

          count(DISTINCT eq) AS totalAssets,
          count(DISTINCT f) AS totalFacilities

        ORDER BY itemDetails.name
        """

    def get_query_advanced(self) -> str:
        """Advanced query - Complete Asset Location Mapping with Context"""
        # This is the massive query from lines 1959-2209
        return """
        MATCH (item)
        WHERE (item:Application OR item:OperatingSystem OR item:Software OR item:Vulnerability)
          AND (
            ($itemName IS NOT NULL AND item.name CONTAINS $itemName) OR
            ($itemId IS NOT NULL AND (item.id = $itemId OR item.cveId = $itemId)) OR
            ($version IS NOT NULL AND item.version = $version)
          )

        MATCH installPath = (item)-[:INSTALLED_ON|RUNS_ON|FOUND_IN*1..4]->(eq:Equipment)

        OPTIONAL MATCH (eq)-[:LOCATED_IN]->(facility:Facility)
        OPTIONAL MATCH (eq)-[:IN_ZONE]->(zone:NetworkZone)
        OPTIONAL MATCH (item)-[:MANUFACTURED_BY]->(vendor:Vendor)
        OPTIONAL MATCH (item:Vulnerability)<-[:AFFECTS]-(cve:CVE)
        OPTIONAL MATCH (item)<-[:FOUND_IN]-(vuln:Vulnerability)
        OPTIONAL MATCH (vuln)<-[:AFFECTS]-(vulnCve:CVE)
        OPTIONAL MATCH (item)-[:DEPENDS_ON]->(dep)
        WHERE dep:Application OR dep:Software OR dep:OperatingSystem
        OPTIONAL MATCH (dependent)-[:DEPENDS_ON]->(item)
        WHERE dependent:Application OR dependent:Software OR dependent:OperatingSystem
        OPTIONAL MATCH (eq)<-[:INSTALLED_ON|RUNS_ON]-(colocated)
        WHERE colocated <> item
          AND (colocated:Application OR colocated:OperatingSystem OR colocated:Software)

        WITH item, vendor, cve, vuln, vulnCve, dep, dependent, colocated,
          eq, facility, zone, installPath,

          CASE
            WHEN eq.criticality = 'CRITICAL' THEN 4
            WHEN eq.criticality = 'HIGH' THEN 3
            WHEN eq.criticality = 'MEDIUM' THEN 2
            ELSE 1
          END AS criticalityScore,

          CASE
            WHEN eq.environment = 'PRODUCTION' THEN 'PROD'
            WHEN eq.environment = 'STAGING' THEN 'STAGE'
            WHEN eq.environment = 'DEVELOPMENT' THEN 'DEV'
            ELSE 'UNKNOWN'
          END AS envType

        RETURN
          {
            type: labels(item)[0],
            name: item.name,
            id: item.id,
            version: item.version,
            vendor: vendor.name,
            description: item.description,
            cveId: cve.id,
            severity: cve.severity,
            cvssScore: cve.cvssScore,
            exploitable: item.exploitable,
            releaseDate: item.releaseDate,
            endOfLife: item.endOfLife,
            supportStatus: item.supportStatus
          } AS itemDetails,

          collect(DISTINCT {
            facility: {
              id: facility.id,
              name: facility.name,
              address: facility.location,
              type: facility.type,
              securityZone: facility.securityZone,
              coordinates: {
                latitude: facility.latitude,
                longitude: facility.longitude
              }
            },

            equipment: {
              id: eq.id,
              name: eq.name,
              type: eq.type,
              model: eq.model,
              serialNumber: eq.serialNumber,
              manufacturer: eq.manufacturer,
              criticality: eq.criticality,
              environment: envType,
              status: eq.status,
              owner: eq.owner,
              managedBy: eq.managedBy
            },

            physicalLocation: {
              building: eq.building,
              floor: eq.floor,
              room: eq.room,
              rack: eq.rack,
              rackUnit: eq.rackUnit,
              position: eq.position,
              coordinates: eq.coordinates
            },

            networkLocation: {
              ipAddress: eq.ipAddress,
              macAddress: eq.macAddress,
              hostname: eq.hostname,
              domain: eq.domain,
              zone: zone.name,
              zoneType: zone.type,
              vlan: eq.vlan,
              subnet: eq.subnet,
              gateway: eq.gateway,
              networkAccessible: eq.networkAccessible,
              publiclyAccessible: eq.publiclyAccessible,
              firewallRules: eq.firewallRules
            },

            installationDetails: {
              installDate: item.installDate,
              installedBy: item.installedBy,
              installMethod: item.installMethod,
              configurationProfile: item.configProfile,
              purpose: item.purpose,
              pathToItem: [n IN nodes(installPath) |
                {
                  type: labels(n)[0],
                  name: coalesce(n.name, n.id),
                  version: n.version
                }
              ],
              pathLength: length(installPath)
            },

            colocatedSoftware: collect(DISTINCT {
              type: labels(colocated)[0],
              name: colocated.name,
              version: colocated.version,
              purpose: colocated.purpose
            })[0..5],

            criticalityScore: criticalityScore

          }) AS assetLocations,

          {
            hasVulnerabilities: count(DISTINCT vuln) > 0,
            totalVulnerabilities: count(DISTINCT vuln),
            criticalVulns: count(DISTINCT CASE WHEN vulnCve.severity = 'CRITICAL' THEN vuln END),
            highVulns: count(DISTINCT CASE WHEN vulnCve.severity = 'HIGH' THEN vuln END),
            vulnerabilities: collect(DISTINCT {
              vulnId: vuln.id,
              cveId: vulnCve.id,
              severity: vulnCve.severity,
              cvssScore: vulnCve.cvssScore,
              description: vulnCve.description,
              publishedDate: vulnCve.publishedDate,
              patchAvailable: vuln.patchAvailable
            })[0..10]
          } AS vulnerabilityContext,

          {
            dependencies: collect(DISTINCT {
              type: labels(dep)[0],
              name: dep.name,
              version: dep.version,
              required: dep.required,
              minVersion: dep.minVersion
            }),
            dependencyCount: count(DISTINCT dep),

            dependents: collect(DISTINCT {
              type: labels(dependent)[0],
              name: dependent.name,
              version: dependent.version
            }),
            dependentCount: count(DISTINCT dependent)
          } AS dependencyInfo,

          {
            totalAssets: count(DISTINCT eq),
            totalFacilities: count(DISTINCT facility),
            criticalAssets: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
            productionAssets: count(DISTINCT CASE WHEN eq.environment = 'PRODUCTION' THEN eq END),
            externallyAccessible: count(DISTINCT CASE WHEN eq.publiclyAccessible = true THEN eq END),

            facilitiesList: collect(DISTINCT facility.name),
            assetTypeDistribution: collect(DISTINCT {
              type: eq.type,
              count: count(eq)
            }),

            highestCriticality: max(criticalityScore),
            avgCriticality: avg(criticalityScore)
          } AS summary,

          {
            overallRiskScore: CASE
              WHEN count(DISTINCT CASE WHEN vulnCve.severity = 'CRITICAL' THEN vuln END) > 0
                AND max(criticalityScore) >= 3 THEN 10
              WHEN count(DISTINCT CASE WHEN vulnCve.severity = 'HIGH' THEN vuln END) > 0
                AND max(criticalityScore) >= 3 THEN 8
              WHEN count(DISTINCT vuln) > 0 THEN 6
              ELSE 3
            END,

            riskFactors: [
              CASE WHEN count(DISTINCT CASE WHEN vulnCve.severity = 'CRITICAL' THEN vuln END) > 0
                THEN 'Critical vulnerabilities present' ELSE null END,
              CASE WHEN count(DISTINCT CASE WHEN eq.publiclyAccessible = true THEN eq END) > 0
                THEN 'Externally accessible assets' ELSE null END,
              CASE WHEN max(criticalityScore) >= 3
                THEN 'High-criticality assets affected' ELSE null END,
              CASE WHEN item.endOfLife IS NOT NULL AND date(item.endOfLife) < date()
                THEN 'Software past end-of-life' ELSE null END
            ],

            recommendedActions: [
              CASE WHEN count(DISTINCT CASE WHEN vulnCve.severity = 'CRITICAL' THEN vuln END) > 0
                THEN 'Immediate patching required' ELSE null END,
              CASE WHEN item.endOfLife IS NOT NULL AND date(item.endOfLife) < date()
                THEN 'Upgrade to supported version' ELSE null END,
              CASE WHEN count(DISTINCT CASE WHEN eq.publiclyAccessible = true THEN eq END) > 0
                THEN 'Review external access requirements' ELSE null END
            ]
          } AS riskAssessment

        ORDER BY
          riskAssessment.overallRiskScore DESC,
          summary.totalAssets DESC
        """
