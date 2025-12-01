// ============================================================================
// USE CASE 3: Determine attack paths from external network to SCADA
// ============================================================================
// Purpose: Find potential routes an attacker could take from external network
//          to reach critical SCADA systems, considering network zones and
//          firewall rules.
//
// Query Structure:
// 1. Start from EXTERNAL network zone
// 2. Traverse network connections (max 8 hops to prevent infinite loops)
// 3. Filter paths that don't get blocked by firewall rules
// 4. Target SCADA zone devices
// 5. Return paths ranked by hopcount (shortest paths = most likely routes)
//
// Expected Results: 5-50 attack paths
// Performance Target: < 2 seconds
// ============================================================================

MATCH path = (external:NetworkZone {name: 'EXTERNAL'})
  -[connection:CONNECTS_TO|ALLOWS_TRAFFIC*1..8]-(scada:Device {zone: 'SCADA'})

WITH path, [rel IN relationships(path) WHERE rel.blocked = true] AS blocked_rels

WHERE length(blocked_rels) = 0  // No blocked connections in path

WITH path, length(path) AS hop_count

RETURN
  path,
  hop_count AS hops,
  nodes(path) AS network_path,
  [n IN nodes(path) | n.name] AS device_names,
  [r IN relationships(path) | r.type] AS connection_types

ORDER BY hop_count ASC

LIMIT 20

// ============================================================================
// Detailed version: Show firewall rules affecting paths
// ============================================================================

MATCH path = (external:NetworkZone {name: 'EXTERNAL'})
  -[connection:CONNECTS_TO*1..8]-(scada:Device {zone: 'SCADA'})

WITH path, relationships(path) AS edges

UNWIND edges AS edge

OPTIONAL MATCH (fw:Firewall)-[rule:BLOCKS|ALLOWS]->(edge)

WITH
  path,
  length(path) AS hops,
  COLLECT({
    from: startNode(edge).name,
    to: endNode(edge).name,
    blocked_by: COALESCE(fw.name, 'None')
  }) AS edge_details

WHERE NOT ANY(detail IN edge_details WHERE detail.blocked_by <> 'None')

RETURN
  [n IN nodes(path) | n.name] AS attack_path,
  hops,
  edge_details AS firewall_status

ORDER BY hops ASC

// ============================================================================
// Alternative: Attack paths with risk scoring
// ============================================================================

MATCH path = (external:NetworkZone {name: 'EXTERNAL'})
  -[*1..8]-(scada:Device {zone: 'SCADA'})

WITH
  path,
  length(path) AS hops,
  nodes(path) AS path_nodes

// Calculate path vulnerability score
WITH
  path,
  hops,
  path_nodes,
  reduce(vuln_score = 0, node IN path_nodes |
    vuln_score + COALESCE(node.vulnerability_score, 0)
  ) AS total_vulnerability

RETURN
  [n IN path_nodes | n.name] AS attack_chain,
  hops,
  total_vulnerability AS path_risk_score,
  CASE
    WHEN total_vulnerability >= 50 THEN 'CRITICAL'
    WHEN total_vulnerability >= 30 THEN 'HIGH'
    WHEN total_vulnerability >= 15 THEN 'MEDIUM'
    ELSE 'LOW'
  END AS risk_level

ORDER BY total_vulnerability DESC, hops ASC

// ============================================================================
// Alternative: Multi-path analysis (all possible routes)
// ============================================================================

MATCH path = (external:NetworkZone {name: 'EXTERNAL'})
  -[*1..8]-(target:Device {zone: 'SCADA'})

WITH
  target.name AS target_device,
  path,
  length(path) AS hops

RETURN
  target_device,
  COUNT(path) AS number_of_paths,
  MIN(hops) AS shortest_path_hops,
  AVG(hops) AS average_path_hops,
  MAX(hops) AS longest_path_hops

// ============================================================================
// Alternative: Choke points (critical devices on most paths)
// ============================================================================

MATCH path = (external:NetworkZone {name: 'EXTERNAL'})
  -[*1..8]-(scada:Device {zone: 'SCADA'})

WITH DISTINCT nodes(path) AS path_nodes, path

UNWIND path_nodes AS node

WITH node.name AS device_name, COUNT(path) AS path_count

WHERE path_count >= 10  // Device appears in 10+ paths

RETURN
  device_name,
  path_count AS appears_in_attack_paths,
  path_count * 100.0 / COUNT(*) AS percentage_of_paths

ORDER BY path_count DESC

// ============================================================================
// Notes on Performance Optimization:
// ============================================================================
// 1. Use relationship type constraints to reduce search space
// 2. Filter blocked connections early in the path
// 3. Use bounded path lengths (max 8 hops) to prevent explosion
// 4. Create index on NetworkZone.name for initial lookup
// 5. Consider caching zone membership for repeated queries
//
// For complex analysis:
// 1. Pre-compute zone adjacency matrix
// 2. Cache firewall rule sets in memory
// 3. Use path caching for frequently queried source-destination pairs
//
// Query tuning:
// - Add LIMIT when doing exploratory queries
// - Use PROFILE to analyze query execution plan
// - Consider separating into multiple targeted queries for large networks
