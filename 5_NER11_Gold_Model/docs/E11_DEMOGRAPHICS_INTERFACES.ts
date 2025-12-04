/**
 * E11 Psychohistory Demographics Baseline - TypeScript Interfaces
 * ================================================================
 *
 * Type definitions for demographics API endpoints.
 * Foundation for advanced psychometric modules (E19-E25).
 *
 * Version: 1.0.0
 * Created: 2025-12-04
 */

// ===== Enums =====

export enum CriticalityLevel {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  CRITICAL = "critical"
}

export enum TurnoverRisk {
  MINIMAL = "minimal",
  LOW = "low",
  MODERATE = "moderate",
  HIGH = "high",
  CRITICAL = "critical"
}

export enum SkillCategory {
  TECHNICAL = "technical",
  SECURITY = "security",
  MANAGEMENT = "management",
  OPERATIONAL = "operational",
  ANALYTICAL = "analytical",
  SPECIALIZED = "specialized"
}

// ===== Core Data Models =====

export interface PopulationSegment {
  segment_id: string;
  name: string;
  count: number;
  percentage: number;
  characteristics: Record<string, any>;
}

export interface DemographicDistribution {
  by_age_group: Record<string, number>;
  by_tenure: Record<string, number>;
  by_education: Record<string, number>;
  by_department: Record<string, number>;
}

export interface BaselineMetrics {
  population_stability_index: number;  // 0-1, higher is more stable
  role_diversity_score: number;        // 0-1, measures role distribution
  skill_concentration_risk: number;    // 0-1, higher is riskier
  succession_coverage: number;         // 0-1, percentage with succession plans
  insider_threat_baseline: number;     // 0-10, baseline threat level
}

export interface PopulationProfile {
  customer_id: string;
  total_population: number;
  segments: PopulationSegment[];
  distribution: DemographicDistribution;
  baseline_metrics: BaselineMetrics;
}

export interface RoleBreakdown {
  role_id: string;
  role_name: string;
  count: number;
  percentage: number;
  security_relevant: boolean;
  criticality: CriticalityLevel;
}

export interface DepartmentBreakdown {
  department_id: string;
  department_name: string;
  count: number;
  percentage: number;
  turnover_rate: number;
}

export interface SkillDistribution {
  category: SkillCategory;
  skill_name: string;
  employee_count: number;
  proficiency_avg: number;
  criticality: CriticalityLevel;
}

export interface WorkforceComposition {
  org_unit_id: string;
  org_unit_name: string;
  customer_id: string;
  total_employees: number;
  by_role: RoleBreakdown[];
  by_department: DepartmentBreakdown[];
  skill_distribution: SkillDistribution[];
  turnover_rate: number;
}

export interface OrganizationUnit {
  unit_id: string;
  name: string;
  customer_id: string;
  parent_id: string | null;
  level: number;
  employee_count: number;
  criticality: CriticalityLevel;
  security_roles_count: number;
  children: string[];
}

// ===== API Request Models =====

export interface PopulationQueryRequest {
  filters: Record<string, any>;
  group_by?: string;
  aggregations?: string[];
}

export interface OrganizationAnalysisRequest {
  analysis_type: string;
  parameters?: Record<string, any>;
}

// ===== API Response Models =====

export interface PopulationSummaryResponse {
  customer_id: string;
  total_population: number;
  active_employees: number;
  contractors: number;
  growth_rate_30d: number;
  stability_index: number;
}

export interface PopulationDistributionResponse {
  customer_id: string;
  distribution: Record<string, Record<string, number>>;
  generated_at: string;
}

export interface PopulationTrendsResponse {
  customer_id: string;
  trends: Array<{
    period: string;
    population: number;
    growth_rate: number;
  }>;
  forecast_90d: Record<string, number>;
}

export interface WorkforceCompositionResponse {
  org_unit_id: string;
  org_unit_name: string;
  customer_id: string;
  total_employees: number;
  by_role: RoleBreakdown[];
  by_department: DepartmentBreakdown[];
  turnover_rate: number;
}

export interface SkillsInventoryResponse {
  customer_id: string;
  total_skills: number;
  by_category: Record<string, number>;
  critical_skills: Array<{
    skill_name: string;
    category: string;
    employee_count: number;
    proficiency_avg: number;
    criticality: string;
  }>;
  skill_gaps: Array<{
    skill_name: string;
    required_count: number;
    current_count: number;
    gap: number;
  }>;
}

export interface TurnoverMetricsResponse {
  customer_id: string;
  current_turnover_rate: number;
  predicted_turnover_30d: number;
  high_risk_employees: number;
  retention_score: number;
}

export interface TeamProfileResponse {
  team_id: string;
  team_name: string;
  customer_id: string;
  member_count: number;
  demographics: Record<string, any>;
  cohesion_score: number;
  diversity_index: number;
}

export interface CapacityMetricsResponse {
  customer_id: string;
  total_capacity_hours: number;
  utilized_capacity: number;
  available_capacity: number;
  overutilized_teams: string[];
}

export interface OrganizationHierarchyResponse {
  customer_id: string;
  root_units: Array<{
    unit_id: string;
    name: string;
    level: number;
    employee_count: number;
    children: string[];
  }>;
  total_units: number;
  max_depth: number;
}

export interface OrganizationUnitsResponse {
  customer_id: string;
  units: Array<{
    unit_id: string;
    name: string;
    parent_id: string | null;
    level: number;
    employee_count: number;
    criticality: string;
  }>;
  total: number;
}

export interface UnitDetailsResponse {
  unit_id: string;
  name: string;
  customer_id: string;
  parent_id: string | null;
  level: number;
  employee_count: number;
  criticality: string;
  security_roles_count: number;
  demographics: Record<string, any>;
}

export interface OrganizationRelationshipsResponse {
  customer_id: string;
  relationships: Array<{
    from_unit: string;
    to_unit: string;
    relationship_type: string;
    strength: number;
  }>;
  total: number;
}

export interface RoleDistributionResponse {
  customer_id: string;
  total_roles: number;
  by_category: Record<string, number>;
  security_relevant_roles: number;
  roles: Array<{
    role_id: string;
    role_name: string;
    category: string;
    count: number;
    security_relevant: boolean;
  }>;
}

export interface RoleDemographicsResponse {
  role_id: string;
  role_name: string;
  customer_id: string;
  employee_count: number;
  demographics: Record<string, any>;
  turnover_rate: number;
}

export interface SecurityRolesResponse {
  customer_id: string;
  total_security_roles: number;
  roles: Array<{
    role_id: string;
    role_name: string;
    count: number;
    criticality: string;
    coverage: number;
  }>;
  coverage_score: number;
}

export interface AccessPatternsResponse {
  customer_id: string;
  patterns: Array<{
    role_id: string;
    role_name: string;
    access_level: string;
    resource_types: string[];
  }>;
  anomalies: Array<{
    employee_id: string;
    role_id: string;
    anomaly_type: string;
    severity: string;
  }>;
}

export interface DashboardSummaryResponse {
  customer_id: string;
  population_summary: Record<string, any>;
  workforce_summary: Record<string, any>;
  organization_summary: Record<string, any>;
  generated_at: string;
}

export interface BaselineMetricsResponse {
  customer_id: string;
  population_stability_index: number;
  role_diversity_score: number;
  skill_concentration_risk: number;
  succession_coverage: number;
  insider_threat_baseline: number;
  generated_at: string;
}

export interface DemographicIndicatorsResponse {
  customer_id: string;
  indicators: Array<{
    indicator: string;
    value: number;
    trend: string;
    threshold: number;
    status: string;
  }>;
  warnings: string[];
}

export interface DemographicAlertsResponse {
  customer_id: string;
  alerts: Array<{
    alert_id: string;
    type: string;
    severity: string;
    affected_unit: string;
    description: string;
    created_at: string;
  }>;
  total: number;
}

export interface TrendAnalysisResponse {
  customer_id: string;
  trends: Array<{
    metric: string;
    trend: string;
    rate: number;
    confidence: number;
  }>;
  forecast: Record<string, any>;
}

// ===== API Client Interface =====

export interface DemographicsAPIClient {
  // Population Metrics (5 endpoints)
  getPopulationSummary(): Promise<PopulationSummaryResponse>;
  getPopulationDistribution(): Promise<PopulationDistributionResponse>;
  getOrgUnitProfile(orgUnitId: string): Promise<any>;
  getPopulationTrends(): Promise<PopulationTrendsResponse>;
  queryPopulation(request: PopulationQueryRequest): Promise<any>;

  // Workforce Analytics (5 endpoints)
  getWorkforceComposition(): Promise<WorkforceCompositionResponse>;
  getSkillsInventory(): Promise<SkillsInventoryResponse>;
  getTurnoverMetrics(): Promise<TurnoverMetricsResponse>;
  getTeamProfile(teamId: string): Promise<TeamProfileResponse>;
  getCapacityMetrics(): Promise<CapacityMetricsResponse>;

  // Organization Structure (5 endpoints)
  getOrganizationHierarchy(): Promise<OrganizationHierarchyResponse>;
  listOrganizationUnits(): Promise<OrganizationUnitsResponse>;
  getUnitDetails(unitId: string): Promise<UnitDetailsResponse>;
  getOrganizationRelationships(): Promise<OrganizationRelationshipsResponse>;
  analyzeOrganizationStructure(request: OrganizationAnalysisRequest): Promise<any>;

  // Role Analysis (4 endpoints)
  getRoleDistribution(): Promise<RoleDistributionResponse>;
  getRoleDemographics(roleId: string): Promise<RoleDemographicsResponse>;
  getSecurityRelevantRoles(): Promise<SecurityRolesResponse>;
  getAccessPatterns(): Promise<AccessPatternsResponse>;

  // Dashboard (5 endpoints)
  getDashboardSummary(): Promise<DashboardSummaryResponse>;
  getBaselineMetrics(): Promise<BaselineMetricsResponse>;
  getDemographicIndicators(): Promise<DemographicIndicatorsResponse>;
  getDemographicAlerts(): Promise<DemographicAlertsResponse>;
  getTrendAnalysis(): Promise<TrendAnalysisResponse>;
}
