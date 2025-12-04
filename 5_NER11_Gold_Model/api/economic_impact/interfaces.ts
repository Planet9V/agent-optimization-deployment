/**
 * E10 Economic Impact Modeling - TypeScript Interfaces
 * Frontend integration types for economic impact API
 */

export enum CostCategory {
  EQUIPMENT = "equipment",
  PERSONNEL = "personnel",
  DOWNTIME = "downtime",
  REMEDIATION = "remediation",
  COMPLIANCE = "compliance",
  INSURANCE = "insurance",
  TRAINING = "training",
  MAINTENANCE = "maintenance"
}

export enum InvestmentCategory {
  SECURITY_TOOLS = "security_tools",
  INFRASTRUCTURE = "infrastructure",
  PERSONNEL = "personnel",
  TRAINING = "training",
  CONSULTING = "consulting",
  COMPLIANCE = "compliance",
  INSURANCE = "insurance"
}

export enum ScenarioType {
  RANSOMWARE = "ransomware",
  DATA_BREACH = "data_breach",
  SYSTEM_OUTAGE = "system_outage",
  SUPPLY_CHAIN = "supply_chain",
  INSIDER_THREAT = "insider_threat",
  DDOS_ATTACK = "ddos_attack"
}

export enum Currency {
  USD = "USD",
  EUR = "EUR",
  GBP = "GBP",
  CAD = "CAD"
}

// ============================================================================
// Cost Analysis Interfaces
// ============================================================================

export interface CostBreakdownItem {
  category: CostCategory;
  description: string;
  amount: number;
  currency: Currency;
  date: string;
  recurring: boolean;
  frequency?: string;
}

export interface CostMetrics {
  customer_id: string;
  total_costs: number;
  cost_categories: Record<CostCategory, number>;
  period_start: string;
  period_end: string;
  currency: Currency;
  trend_percentage?: number;
}

export interface CostByCategory {
  customer_id: string;
  category: CostCategory;
  total_amount: number;
  item_count: number;
  average_cost: number;
  items: CostBreakdownItem[];
  currency: Currency;
}

export interface EntityCostBreakdown {
  entity_id: string;
  entity_type: string;
  total_cost: number;
  direct_costs: CostBreakdownItem[];
  indirect_costs: CostBreakdownItem[];
  allocated_overhead: number;
  currency: Currency;
}

export interface CostCalculationRequest {
  customer_id: string;
  scenario_type: string;
  duration_hours: number;
  affected_systems: string[];
  personnel_count: number;
  equipment_value: number;
  revenue_per_hour?: number;
  additional_factors?: Record<string, number>;
}

export interface HistoricalCostTrend {
  customer_id: string;
  data_points: Array<[string, number]>;
  category?: CostCategory;
  trend_direction: "increasing" | "decreasing" | "stable";
  percentage_change: number;
  currency: Currency;
}

// ============================================================================
// ROI Calculation Interfaces
// ============================================================================

export interface ROICalculation {
  investment_id: string;
  customer_id: string;
  investment_name: string;
  category: InvestmentCategory;
  initial_investment: number;
  annual_savings: number;
  annual_costs: number;
  roi_percentage: number;
  payback_period_months: number;
  npv: number;
  irr: number;
  calculation_date: string;
  currency: Currency;
}

export interface ROICalculationRequest {
  customer_id: string;
  investment_name: string;
  category: InvestmentCategory;
  initial_investment: number;
  expected_annual_savings: number;
  annual_operating_costs: number;
  project_lifetime_years?: number;
  discount_rate?: number;
  currency?: Currency;
}

export interface ROISummary {
  customer_id: string;
  total_investments: number;
  total_invested: number;
  total_annual_savings: number;
  average_roi_percentage: number;
  best_performing?: ROICalculation;
  worst_performing?: ROICalculation;
  by_category: Record<InvestmentCategory, number>;
  currency: Currency;
}

export interface ROIProjection {
  investment_id: string;
  customer_id: string;
  projections: Array<[number, number]>;
  confidence_interval_low: number[];
  confidence_interval_high: number[];
  assumptions: Record<string, string>;
}

export interface InvestmentComparison {
  customer_id: string;
  investments: ROICalculation[];
  comparison_metrics: Record<string, number[]>;
  recommendation: string;
  ranking: string[];
}

// ============================================================================
// Business Value Interfaces
// ============================================================================

export interface BusinessValue {
  entity_id: string;
  entity_type: string;
  customer_id: string;
  replacement_cost: number;
  revenue_impact: number;
  reputation_value: number;
  regulatory_exposure: number;
  intellectual_property_value: number;
  operational_criticality: number;
  total_value: number;
  confidence_score: number;
  assessment_date: string;
  currency: Currency;
}

export interface ValueMetrics {
  customer_id: string;
  total_asset_value: number;
  critical_asset_count: number;
  at_risk_value: number;
  protected_value: number;
  value_by_category: Record<string, number>;
  top_value_assets: BusinessValue[];
  currency: Currency;
}

export interface ValueCalculationRequest {
  customer_id: string;
  entity_id: string;
  entity_type: string;
  replacement_cost?: number;
  annual_revenue?: number;
  market_share?: number;
  customer_base?: number;
  regulatory_requirements?: string[];
  ip_patents?: number;
  operational_hours?: number;
}

export interface RiskAdjustedValue {
  entity_id: string;
  customer_id: string;
  nominal_value: number;
  risk_score: number;
  risk_adjusted_value: number;
  expected_loss: number;
  value_at_risk: number;
  confidence_level: number;
  currency: Currency;
}

// ============================================================================
// Impact Modeling Interfaces
// ============================================================================

export interface ScenarioParameters {
  affected_systems: string[];
  duration_hours: number;
  severity: "low" | "medium" | "high" | "critical";
  data_volume_gb?: number;
  user_count?: number;
  geographic_scope?: string;
  regulatory_implications?: string[];
}

export interface ImpactScenario {
  scenario_id: string;
  customer_id: string;
  scenario_type: ScenarioType;
  scenario_name: string;
  description: string;
  parameters: ScenarioParameters;
  estimated_cost: number;
  confidence_interval: [number, number];
  probability: number;
  created_date: string;
  currency: Currency;
}

export interface ImpactModelRequest {
  customer_id: string;
  scenario_type: ScenarioType;
  parameters: ScenarioParameters;
  include_indirect_costs?: boolean;
  include_reputation_impact?: boolean;
  time_horizon_days?: number;
}

export interface ImpactSimulation {
  simulation_id: string;
  customer_id: string;
  scenario: ImpactScenario;
  direct_costs: number;
  indirect_costs: number;
  opportunity_costs: number;
  reputation_impact: number;
  regulatory_fines: number;
  total_impact: number;
  recovery_timeline_days: number;
  mitigation_recommendations: string[];
  currency: Currency;
}

export interface HistoricalImpact {
  customer_id: string;
  incident_date: string;
  scenario_type: ScenarioType;
  actual_cost: number;
  estimated_cost: number;
  variance_percentage: number;
  lessons_learned: string[];
  currency: Currency;
}

// ============================================================================
// Dashboard Interfaces
// ============================================================================

export interface EconomicDashboard {
  customer_id: string;
  timestamp: string;
  total_costs_ytd: number;
  total_investments_ytd: number;
  average_roi: number;
  at_risk_value: number;
  cost_trend: string;
  roi_trend: string;
  alerts: string[];
  key_metrics: Record<string, number>;
  currency: Currency;
}

export interface EconomicTrends {
  customer_id: string;
  period: string;
  cost_trend: Array<[string, number]>;
  roi_trend: Array<[string, number]>;
  value_trend: Array<[string, number]>;
  incident_impact_trend: Array<[string, number]>;
  currency: Currency;
}

export interface EconomicKPIs {
  customer_id: string;
  security_investment_percentage: number;
  roi_average: number;
  cost_per_asset: number;
  value_protected_ratio: number;
  incident_cost_trend: number;
  payback_period_average: number;
  budget_utilization: number;
}

export interface EconomicAlert {
  alert_id: string;
  customer_id: string;
  alert_type: string;
  severity: "info" | "warning" | "critical";
  message: string;
  threshold_value: number;
  current_value: number;
  created_date: string;
  acknowledged: boolean;
}

export interface ExecutiveSummary {
  customer_id: string;
  period: string;
  total_security_spend: number;
  total_value_protected: number;
  roi_on_security: number;
  incidents_prevented: number;
  cost_avoidance: number;
  top_risks: string[];
  investment_recommendations: string[];
  executive_insights: string;
  currency: Currency;
}

// ============================================================================
// API Response Interface
// ============================================================================

export interface EconomicImpactResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: string[];
  timestamp: string;
}

// ============================================================================
// API Client Class
// ============================================================================

export class EconomicImpactAPI {
  private baseUrl: string;
  private customerId: string;

  constructor(baseUrl: string, customerId: string) {
    this.baseUrl = baseUrl;
    this.customerId = customerId;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'X-Customer-ID': this.customerId,
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    const result: EconomicImpactResponse<T> = await response.json();
    if (!result.success) {
      throw new Error(result.message || 'API request failed');
    }

    return result.data as T;
  }

  // Cost Analysis Methods
  async getCostSummary(periodDays: number = 30): Promise<CostMetrics> {
    return this.request<CostMetrics>(`/costs/summary?period_days=${periodDays}`);
  }

  async getCostsByCategory(category?: CostCategory): Promise<{ categories: CostByCategory[] }> {
    const url = category ? `/costs/by-category?category=${category}` : '/costs/by-category';
    return this.request(url);
  }

  async getEntityCostBreakdown(entityId: string): Promise<EntityCostBreakdown> {
    return this.request<EntityCostBreakdown>(`/costs/${entityId}/breakdown`);
  }

  async calculateCosts(request: CostCalculationRequest): Promise<Record<string, number>> {
    return this.request('/costs/calculate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getHistoricalCosts(category?: CostCategory, days: number = 90): Promise<HistoricalCostTrend> {
    const url = category
      ? `/costs/historical?category=${category}&days=${days}`
      : `/costs/historical?days=${days}`;
    return this.request<HistoricalCostTrend>(url);
  }

  // ROI Calculation Methods
  async getROISummary(): Promise<ROISummary> {
    return this.request<ROISummary>('/roi/summary');
  }

  async calculateROI(request: ROICalculationRequest): Promise<ROICalculation> {
    return this.request<ROICalculation>('/roi/calculate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getROIProjections(investmentId: string, years: number = 5): Promise<ROIProjection> {
    return this.request<ROIProjection>(`/roi/projections?investment_id=${investmentId}&years=${years}`);
  }

  async compareInvestments(investmentIds: string[]): Promise<InvestmentComparison> {
    return this.request<InvestmentComparison>('/roi/comparison', {
      method: 'POST',
      body: JSON.stringify(investmentIds),
    });
  }

  // Business Value Methods
  async getValueMetrics(): Promise<ValueMetrics> {
    return this.request<ValueMetrics>('/value/metrics');
  }

  async calculateBusinessValue(request: ValueCalculationRequest): Promise<BusinessValue> {
    return this.request<BusinessValue>('/value/calculate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Impact Modeling Methods
  async modelImpact(request: ImpactModelRequest): Promise<ImpactSimulation> {
    return this.request<ImpactSimulation>('/impact/model', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Dashboard Methods
  async getDashboardSummary(): Promise<EconomicDashboard> {
    return this.request<EconomicDashboard>('/dashboard/summary');
  }
}
