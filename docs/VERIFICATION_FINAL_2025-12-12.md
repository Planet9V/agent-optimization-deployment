# FINAL VERIFICATION REPORT - 2025-12-12

**Date**: 2025-12-12T15:06:19.023019
**Tester**: Independent Verification Agent
**Method**: Actual HTTP testing of all deployed APIs

## Summary

- **total_apis**: 103
- **passing**: 36
- **failing**: 67
- **success_rate**: 35.0%
- **avg_response_time**: 291ms
- **max_response_time**: 1327ms

## Category Results

- **remediation**: 0/22 passing (0.0%)
- **risk**: 9/19 passing (47.4%)
- **sbom**: 8/25 passing (32.0%)
- **threat-intel**: 12/19 passing (63.2%)
- **unknown**: 2/2 passing (100.0%)
- **vendor-equipment**: 5/16 passing (31.2%)

## Errors by Category


### remediation

- /api/v2/remediation/tasks/open: HTTP 500 - Internal Server Error
- /api/v2/remediation/sla/policies: HTTP 500 - Internal Server Error
- /api/v2/remediation/tasks/overdue: HTTP 500 - Internal Server Error
- /api/v2/remediation/tasks/search: HTTP 500 - Internal Server Error
- /api/v2/remediation/plans/active: HTTP 500 - Internal Server Error
- /api/v2/remediation/sla/breaches: HTTP 500 - Internal Server Error
- /api/v2/remediation/metrics/sla-compliance: HTTP 500 - Internal Server Error
- /api/v2/remediation/plans/{plan_id}/progress: HTTP 500 - Internal Server Error
- /api/v2/remediation/metrics/trends: HTTP 500 - Internal Server Error
- /api/v2/remediation/metrics/mttr: HTTP 500 - Internal Server Error

### risk

- /api/v2/risk/exposure/high-exposure: HTTP 404 - Exposure score for asset high-exposure not found
- /api/v2/risk/assets/{asset_id}/criticality: HTTP 404 - Asset criticality for {asset_id} not found
- /api/v2/risk/exposure/attack-surface: HTTP 404 - Exposure score for asset attack-surface not found
- /api/v2/risk/assets/by-criticality/{level}: HTTP 400 - '{level}' is not a valid CriticalityLevel
- /api/v2/risk/scores/trending: HTTP 400 - 'increasing' is not a valid RiskTrend
- /api/v2/risk/scores/history/{entity_type}/{entity_id}: HTTP 500 - Internal Server Error
- /api/v2/risk/exposure/internet-facing: HTTP 404 - Exposure score for asset internet-facing not found
- /api/v2/risk/scores/{entity_type}/{entity_id}: HTTP 500 - Internal Server Error
- /api/v2/risk/aggregation/{aggregation_type}/{group_id}: HTTP 400 - Unsupported aggregation type: {aggregation_type}
- /api/v2/risk/exposure/{asset_id}: HTTP 404 - Exposure score for asset {asset_id} not found

### sbom

- /api/v2/sbom/vulnerabilities/by-apt: HTTP 404 - Vulnerability by-apt not found
- /api/v2/sbom/vulnerabilities/kev: HTTP 404 - Vulnerability kev not found
- /api/v2/sbom/components/high-risk: HTTP 404 - Component high-risk not found
- /api/v2/sbom/components/{component_id}/vulnerabilities: HTTP 500 - Internal Server Error
- /api/v2/sbom/sboms/{sbom_id}/license-compliance: HTTP 500 - Internal Server Error
- /api/v2/sbom/vulnerabilities/epss-prioritized: HTTP 404 - Vulnerability epss-prioritized not found
- /api/v2/sbom/vulnerabilities/search: HTTP 404 - Vulnerability search not found
- /api/v2/sbom/vulnerabilities/{vulnerability_id}: HTTP 404 - Vulnerability {vulnerability_id} not found
- /api/v2/sbom/sboms/{sbom_id}: HTTP 404 - SBOM {sbom_id} not found
- /api/v2/sbom/sboms/{sbom_id}/components: HTTP 500 - Internal Server Error

### threat-intel

- /api/v2/threat-intel/actors/search: HTTP 404 - Threat actor search not found
- /api/v2/threat-intel/campaigns/{campaign_id}: HTTP 404 - Campaign {campaign_id} not found
- /api/v2/threat-intel/campaigns/search: HTTP 404 - Campaign search not found
- /api/v2/threat-intel/actors/active: HTTP 404 - Threat actor active not found
- /api/v2/threat-intel/campaigns/active: HTTP 404 - Campaign active not found
- /api/v2/threat-intel/feeds: HTTP 500 - Internal Server Error
- /api/v2/threat-intel/actors/{actor_id}: HTTP 404 - Threat actor {actor_id} not found

### vendor-equipment

- /api/v2/vendor-equipment/vendors/high-risk: HTTP 404 - Vendor high-risk not found
- /api/v2/vendor-equipment/equipment/approaching-eol: HTTP 404 - Equipment approaching-eol not found
- /api/v2/vendor-equipment/work-orders/summary: HTTP 404 - Work order summary not found
- /api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary: HTTP 404 - Vendor {vendor_id} not found
- /api/v2/vendor-equipment/maintenance-windows: HTTP 500 - Internal Server Error
- /api/v2/vendor-equipment/work-orders: HTTP 500 - Internal Server Error
- /api/v2/vendor-equipment/equipment/{model_id}: HTTP 404 - Equipment {model_id} not found
- /api/v2/vendor-equipment/work-orders/{work_order_id}: HTTP 404 - Work order {work_order_id} not found
- /api/v2/vendor-equipment/vendors/{vendor_id}: HTTP 404 - Vendor {vendor_id} not found
- /api/v2/vendor-equipment/maintenance-windows/{window_id}: HTTP 404 - Maintenance window {window_id} not found
