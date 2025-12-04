"""
E10 Economic Impact Service
Business logic for economic calculations, ROI analysis, and impact modeling
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from .schemas import (
    CostSummary, CostByCategory, EntityCostBreakdown, CostCalculationRequest,
    HistoricalCostTrend, ROICalculation, ROICalculationRequest, ROISummary,
    ROIProjection, InvestmentComparison, BusinessValue, ValueMetrics,
    ValueCalculationRequest, RiskAdjustedValue, ValueBySector,
    ImpactScenario, ImpactModelRequest, ImpactSimulation, HistoricalImpact,
    EconomicDashboard, EconomicTrends, EconomicKPIs, EconomicAlert,
    ExecutiveSummary, CostCategory, InvestmentCategory, ScenarioType,
    Currency, ScenarioParameters, CostBreakdownItem
)


class EconomicImpactService:
    """Service for economic impact calculations and analysis"""

    def __init__(self, qdrant_client: QdrantClient):
        self.qdrant_client = qdrant_client
        self.collection_name = "ner11_economic_impact"
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure Qdrant collection exists"""
        collections = self.qdrant_client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    # ========================================================================
    # Cost Analysis Methods
    # ========================================================================

    async def get_cost_summary(self, customer_id: str, period_days: int = 30) -> CostSummary:
        """Get cost summary dashboard"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=period_days)

        # Query costs from Qdrant
        search_results = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {"key": "customer_id", "match": {"value": customer_id}},
                    {"key": "type", "match": {"value": "cost"}},
                    {"key": "date", "range": {
                        "gte": start_date.isoformat(),
                        "lte": end_date.isoformat()
                    }}
                ]
            },
            limit=1000
        )

        costs = [point.payload for point, _ in search_results]

        # Calculate totals by category
        category_totals = {}
        total_costs = 0.0

        for cost in costs:
            category = CostCategory(cost.get("category", "equipment"))
            amount = float(cost.get("amount", 0))
            category_totals[category] = category_totals.get(category, 0) + amount
            total_costs += amount

        # Calculate trend (compare to previous period)
        previous_period = await self._get_previous_period_costs(
            customer_id, start_date, period_days
        )
        trend_percentage = None
        if previous_period > 0:
            trend_percentage = ((total_costs - previous_period) / previous_period) * 100

        return CostSummary(
            customer_id=customer_id,
            total_costs=total_costs,
            cost_categories=category_totals,
            period_start=start_date,
            period_end=end_date,
            trend_percentage=trend_percentage
        )

    async def get_costs_by_category(
        self, customer_id: str, category: Optional[CostCategory] = None
    ) -> List[CostByCategory]:
        """Get costs grouped by category"""
        search_filter = {
            "must": [
                {"key": "customer_id", "match": {"value": customer_id}},
                {"key": "type", "match": {"value": "cost"}}
            ]
        }

        if category:
            search_filter["must"].append({
                "key": "category", "match": {"value": category.value}
            })

        results = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter=search_filter,
            limit=1000
        )

        # Group by category
        category_groups = {}
        for point, _ in results:
            payload = point.payload
            cat = CostCategory(payload.get("category", "equipment"))

            if cat not in category_groups:
                category_groups[cat] = []

            category_groups[cat].append(CostBreakdownItem(
                category=cat,
                description=payload.get("description", ""),
                amount=float(payload.get("amount", 0)),
                currency=Currency(payload.get("currency", "USD")),
                date=datetime.fromisoformat(payload.get("date")),
                recurring=payload.get("recurring", False),
                frequency=payload.get("frequency")
            ))

        # Create response
        response = []
        for cat, items in category_groups.items():
            total = sum(item.amount for item in items)
            response.append(CostByCategory(
                customer_id=customer_id,
                category=cat,
                total_amount=total,
                item_count=len(items),
                average_cost=total / len(items) if items else 0,
                items=items
            ))

        return response

    async def get_entity_cost_breakdown(
        self, customer_id: str, entity_id: str
    ) -> EntityCostBreakdown:
        """Get detailed cost breakdown for entity"""
        results = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {"key": "customer_id", "match": {"value": customer_id}},
                    {"key": "entity_id", "match": {"value": entity_id}},
                    {"key": "type", "match": {"value": "cost"}}
                ]
            },
            limit=500
        )

        direct_costs = []
        indirect_costs = []
        overhead = 0.0

        for point, _ in results:
            payload = point.payload
            cost_item = CostBreakdownItem(
                category=CostCategory(payload.get("category", "equipment")),
                description=payload.get("description", ""),
                amount=float(payload.get("amount", 0)),
                currency=Currency(payload.get("currency", "USD")),
                date=datetime.fromisoformat(payload.get("date")),
                recurring=payload.get("recurring", False)
            )

            if payload.get("cost_type") == "direct":
                direct_costs.append(cost_item)
            else:
                indirect_costs.append(cost_item)

            if payload.get("is_overhead"):
                overhead += cost_item.amount

        total_cost = sum(c.amount for c in direct_costs + indirect_costs)

        return EntityCostBreakdown(
            entity_id=entity_id,
            entity_type=results[0][0].payload.get("entity_type", "asset") if results else "asset",
            total_cost=total_cost,
            direct_costs=direct_costs,
            indirect_costs=indirect_costs,
            allocated_overhead=overhead
        )

    async def calculate_costs(self, request: CostCalculationRequest) -> Dict[str, float]:
        """Calculate costs for scenario"""
        costs = {
            "direct_costs": 0.0,
            "indirect_costs": 0.0,
            "opportunity_costs": 0.0,
            "total": 0.0
        }

        # Direct costs
        costs["direct_costs"] += request.equipment_value * 0.1  # 10% damage assumption
        costs["direct_costs"] += request.personnel_count * request.duration_hours * 150  # $150/hr avg

        # Indirect costs
        if request.revenue_per_hour:
            costs["indirect_costs"] += request.revenue_per_hour * request.duration_hours

        # Opportunity costs
        costs["opportunity_costs"] = costs["indirect_costs"] * 0.3  # 30% of revenue loss

        # Additional factors
        if request.additional_factors:
            for factor, multiplier in request.additional_factors.items():
                costs["total"] += costs["direct_costs"] * multiplier

        costs["total"] = sum([
            costs["direct_costs"],
            costs["indirect_costs"],
            costs["opportunity_costs"]
        ])

        return costs

    async def get_historical_cost_trends(
        self, customer_id: str, category: Optional[CostCategory] = None, days: int = 90
    ) -> HistoricalCostTrend:
        """Get historical cost trends"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        search_filter = {
            "must": [
                {"key": "customer_id", "match": {"value": customer_id}},
                {"key": "type", "match": {"value": "cost"}},
                {"key": "date", "range": {
                    "gte": start_date.isoformat(),
                    "lte": end_date.isoformat()
                }}
            ]
        }

        if category:
            search_filter["must"].append({
                "key": "category", "match": {"value": category.value}
            })

        results = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter=search_filter,
            limit=1000
        )

        # Group by date
        daily_costs = {}
        for point, _ in results:
            payload = point.payload
            date = datetime.fromisoformat(payload.get("date")).date()
            amount = float(payload.get("amount", 0))
            daily_costs[date] = daily_costs.get(date, 0) + amount

        # Create time series
        data_points = [(datetime.combine(date, datetime.min.time()), cost)
                      for date, cost in sorted(daily_costs.items())]

        # Calculate trend
        if len(data_points) > 1:
            costs = [c for _, c in data_points]
            trend_slope = np.polyfit(range(len(costs)), costs, 1)[0]

            if trend_slope > 0.05:
                trend_direction = "increasing"
            elif trend_slope < -0.05:
                trend_direction = "decreasing"
            else:
                trend_direction = "stable"

            percentage_change = ((costs[-1] - costs[0]) / costs[0]) * 100 if costs[0] > 0 else 0
        else:
            trend_direction = "stable"
            percentage_change = 0.0

        return HistoricalCostTrend(
            customer_id=customer_id,
            data_points=data_points,
            category=category,
            trend_direction=trend_direction,
            percentage_change=percentage_change
        )

    # ========================================================================
    # ROI Calculation Methods
    # ========================================================================

    async def calculate_roi(self, request: ROICalculationRequest) -> ROICalculation:
        """Calculate ROI for investment"""
        # Calculate annual net benefit
        annual_net_benefit = request.expected_annual_savings - request.annual_operating_costs

        # Calculate simple ROI
        roi_percentage = (annual_net_benefit / request.initial_investment) * 100

        # Calculate payback period
        payback_period_months = (request.initial_investment / annual_net_benefit) * 12 if annual_net_benefit > 0 else float('inf')

        # Calculate NPV (Net Present Value)
        cash_flows = [annual_net_benefit] * request.project_lifetime_years
        discount_factors = [(1 / (1 + request.discount_rate) ** year)
                          for year in range(1, request.project_lifetime_years + 1)]
        npv = -request.initial_investment + sum(cf * df for cf, df in zip(cash_flows, discount_factors))

        # Calculate IRR (Internal Rate of Return) - simplified
        irr = self._calculate_irr(
            request.initial_investment,
            cash_flows,
            request.discount_rate
        )

        investment_id = f"inv_{customer_id}_{int(datetime.utcnow().timestamp())}"

        return ROICalculation(
            investment_id=investment_id,
            customer_id=request.customer_id,
            investment_name=request.investment_name,
            category=request.category,
            initial_investment=request.initial_investment,
            annual_savings=request.expected_annual_savings,
            annual_costs=request.annual_operating_costs,
            roi_percentage=roi_percentage,
            payback_period_months=payback_period_months,
            npv=npv,
            irr=irr,
            calculation_date=datetime.utcnow(),
            currency=request.currency
        )

    async def get_roi_summary(self, customer_id: str) -> ROISummary:
        """Get summary of all ROI calculations"""
        results = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {"key": "customer_id", "match": {"value": customer_id}},
                    {"key": "type", "match": {"value": "roi"}}
                ]
            },
            limit=500
        )

        investments = []
        category_totals = {}

        for point, _ in results:
            payload = point.payload
            roi = ROICalculation(**payload)
            investments.append(roi)

            category = roi.category
            category_totals[category] = category_totals.get(category, 0) + roi.roi_percentage

        if not investments:
            return ROISummary(
                customer_id=customer_id,
                total_investments=0,
                total_invested=0.0,
                total_annual_savings=0.0,
                average_roi_percentage=0.0,
                by_category={}
            )

        # Calculate aggregates
        total_invested = sum(inv.initial_investment for inv in investments)
        total_savings = sum(inv.annual_savings for inv in investments)
        avg_roi = sum(inv.roi_percentage for inv in investments) / len(investments)

        # Find best and worst
        best = max(investments, key=lambda x: x.roi_percentage)
        worst = min(investments, key=lambda x: x.roi_percentage)

        # Average by category
        category_averages = {
            cat: total / len([i for i in investments if i.category == cat])
            for cat, total in category_totals.items()
        }

        return ROISummary(
            customer_id=customer_id,
            total_investments=len(investments),
            total_invested=total_invested,
            total_annual_savings=total_savings,
            average_roi_percentage=avg_roi,
            best_performing=best,
            worst_performing=worst,
            by_category=category_averages
        )

    async def get_roi_projections(
        self, customer_id: str, investment_id: str, years: int = 5
    ) -> ROIProjection:
        """Get future ROI projections"""
        # Retrieve investment details
        results = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {"key": "customer_id", "match": {"value": customer_id}},
                    {"key": "investment_id", "match": {"value": investment_id}},
                    {"key": "type", "match": {"value": "roi"}}
                ]
            },
            limit=1
        )

        if not results[0]:
            raise ValueError(f"Investment {investment_id} not found")

        roi_data = results[0][0].payload
        annual_benefit = roi_data["annual_savings"] - roi_data["annual_costs"]

        # Project future values with growth assumptions
        projections = []
        confidence_low = []
        confidence_high = []

        growth_rate = 0.03  # 3% annual growth
        volatility = 0.15  # 15% volatility

        cumulative_value = -roi_data["initial_investment"]

        for year in range(1, years + 1):
            # Expected value with growth
            year_benefit = annual_benefit * ((1 + growth_rate) ** year)
            cumulative_value += year_benefit
            projections.append((year, cumulative_value))

            # Confidence intervals
            confidence_low.append(cumulative_value * (1 - volatility))
            confidence_high.append(cumulative_value * (1 + volatility))

        return ROIProjection(
            investment_id=investment_id,
            customer_id=customer_id,
            projections=projections,
            confidence_interval_low=confidence_low,
            confidence_interval_high=confidence_high,
            assumptions={
                "growth_rate": f"{growth_rate * 100}%",
                "volatility": f"{volatility * 100}%",
                "discount_rate": "10%"
            }
        )

    async def compare_investments(
        self, customer_id: str, investment_ids: List[str]
    ) -> InvestmentComparison:
        """Compare multiple investment options"""
        investments = []

        for inv_id in investment_ids:
            results = self.qdrant_client.scroll(
                collection_name=self.collection_name,
                scroll_filter={
                    "must": [
                        {"key": "customer_id", "match": {"value": customer_id}},
                        {"key": "investment_id", "match": {"value": inv_id}},
                        {"key": "type", "match": {"value": "roi"}}
                    ]
                },
                limit=1
            )

            if results[0]:
                investments.append(ROICalculation(**results[0][0].payload))

        # Comparison metrics
        metrics = {
            "roi_percentage": [inv.roi_percentage for inv in investments],
            "npv": [inv.npv for inv in investments],
            "payback_period": [inv.payback_period_months for inv in investments],
            "irr": [inv.irr for inv in investments]
        }

        # Rank by composite score
        scores = []
        for inv in investments:
            score = (
                inv.roi_percentage * 0.3 +
                inv.npv / 10000 * 0.3 +  # Normalize NPV
                (100 - inv.payback_period_months) * 0.2 +  # Lower is better
                inv.irr * 100 * 0.2
            )
            scores.append((inv.investment_id, score))

        ranking = [inv_id for inv_id, _ in sorted(scores, key=lambda x: x[1], reverse=True)]

        # Generate recommendation
        best_inv = next(inv for inv in investments if inv.investment_id == ranking[0])
        recommendation = (
            f"Recommended: {best_inv.investment_name} - "
            f"Highest ROI ({best_inv.roi_percentage:.1f}%) with NPV of ${best_inv.npv:,.2f}"
        )

        return InvestmentComparison(
            customer_id=customer_id,
            investments=investments,
            comparison_metrics=metrics,
            recommendation=recommendation,
            ranking=ranking
        )

    # ========================================================================
    # Business Value Methods
    # ========================================================================

    async def calculate_business_value(
        self, request: ValueCalculationRequest
    ) -> BusinessValue:
        """Calculate business value for entity"""
        # Replacement cost
        replacement_cost = request.replacement_cost or 0

        # Revenue impact calculation
        revenue_impact = 0.0
        if request.annual_revenue:
            # Percentage of revenue attributable to this entity
            revenue_impact = request.annual_revenue * 0.1  # 10% default attribution

        # Reputation value (based on customer base)
        reputation_value = 0.0
        if request.customer_base:
            # $100 per customer in reputation value
            reputation_value = request.customer_base * 100

        # Regulatory exposure
        regulatory_exposure = len(request.regulatory_requirements) * 500000  # $500k per requirement

        # IP value
        ip_value = request.ip_patents * 250000  # $250k per patent

        # Operational criticality (based on hours)
        criticality = request.operational_hours / 8760  # Ratio of 24/7
        operational_criticality = replacement_cost * criticality

        total_value = (
            replacement_cost +
            revenue_impact +
            reputation_value +
            regulatory_exposure +
            ip_value +
            operational_criticality
        )

        # Confidence score based on data completeness
        data_points = sum([
            1 if request.replacement_cost else 0,
            1 if request.annual_revenue else 0,
            1 if request.customer_base else 0,
            1 if request.regulatory_requirements else 0,
            1 if request.ip_patents else 0
        ])
        confidence = data_points / 5.0

        return BusinessValue(
            entity_id=request.entity_id,
            entity_type=request.entity_type,
            customer_id=request.customer_id,
            replacement_cost=replacement_cost,
            revenue_impact=revenue_impact,
            reputation_value=reputation_value,
            regulatory_exposure=regulatory_exposure,
            intellectual_property_value=ip_value,
            operational_criticality=operational_criticality,
            total_value=total_value,
            confidence_score=confidence,
            assessment_date=datetime.utcnow()
        )

    async def get_value_metrics(self, customer_id: str) -> ValueMetrics:
        """Get business value metrics dashboard"""
        results = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {"key": "customer_id", "match": {"value": customer_id}},
                    {"key": "type", "match": {"value": "business_value"}}
                ]
            },
            limit=500
        )

        values = [BusinessValue(**point.payload) for point, _ in results]

        if not values:
            return ValueMetrics(
                customer_id=customer_id,
                total_asset_value=0.0,
                critical_asset_count=0,
                at_risk_value=0.0,
                protected_value=0.0,
                value_by_category={},
                top_value_assets=[]
            )

        total_value = sum(v.total_value for v in values)
        critical_assets = [v for v in values if v.operational_criticality > total_value * 0.1]

        # Category breakdown
        category_values = {}
        for value in values:
            cat = value.entity_type
            category_values[cat] = category_values.get(cat, 0) + value.total_value

        # Top assets
        top_assets = sorted(values, key=lambda x: x.total_value, reverse=True)[:10]

        return ValueMetrics(
            customer_id=customer_id,
            total_asset_value=total_value,
            critical_asset_count=len(critical_assets),
            at_risk_value=total_value * 0.3,  # Assume 30% at risk
            protected_value=total_value * 0.7,  # Assume 70% protected
            value_by_category=category_values,
            top_value_assets=top_assets
        )

    # ========================================================================
    # Impact Modeling Methods
    # ========================================================================

    async def model_impact(self, request: ImpactModelRequest) -> ImpactSimulation:
        """Model financial impact of incident"""
        # Base cost calculation
        base_cost = await self._calculate_base_impact(request)

        # Direct costs
        direct_costs = base_cost["equipment_damage"] + base_cost["response_costs"]

        # Indirect costs
        indirect_costs = 0.0
        if request.include_indirect_costs:
            indirect_costs = base_cost["productivity_loss"] + base_cost["business_disruption"]

        # Opportunity costs
        opportunity_costs = indirect_costs * 0.5  # 50% of indirect

        # Reputation impact
        reputation_impact = 0.0
        if request.include_reputation_impact:
            reputation_impact = await self._calculate_reputation_impact(
                request.customer_id,
                request.scenario_type,
                request.parameters
            )

        # Regulatory fines
        regulatory_fines = 0.0
        if request.parameters.regulatory_implications:
            regulatory_fines = len(request.parameters.regulatory_implications) * 100000

        total_impact = (
            direct_costs +
            indirect_costs +
            opportunity_costs +
            reputation_impact +
            regulatory_fines
        )

        # Recovery timeline
        severity_multipliers = {"low": 1, "medium": 2, "high": 4, "critical": 8}
        recovery_days = int(
            request.parameters.duration_hours / 24 *
            severity_multipliers[request.parameters.severity]
        )

        # Mitigation recommendations
        recommendations = await self._generate_mitigation_recommendations(
            request.scenario_type,
            request.parameters.severity
        )

        # Create scenario
        scenario = ImpactScenario(
            scenario_id=f"scen_{int(datetime.utcnow().timestamp())}",
            customer_id=request.customer_id,
            scenario_type=request.scenario_type,
            scenario_name=f"{request.scenario_type.value} - {request.parameters.severity}",
            description=f"Impact simulation for {request.scenario_type.value}",
            parameters=request.parameters,
            estimated_cost=total_impact,
            confidence_interval=(total_impact * 0.7, total_impact * 1.3),
            probability=0.5,
            created_date=datetime.utcnow()
        )

        simulation_id = f"sim_{int(datetime.utcnow().timestamp())}"

        return ImpactSimulation(
            simulation_id=simulation_id,
            customer_id=request.customer_id,
            scenario=scenario,
            direct_costs=direct_costs,
            indirect_costs=indirect_costs,
            opportunity_costs=opportunity_costs,
            reputation_impact=reputation_impact,
            regulatory_fines=regulatory_fines,
            total_impact=total_impact,
            recovery_timeline_days=recovery_days,
            mitigation_recommendations=recommendations
        )

    # ========================================================================
    # Dashboard Methods
    # ========================================================================

    async def get_economic_dashboard(self, customer_id: str) -> EconomicDashboard:
        """Get economic dashboard summary"""
        # Get current year data
        year_start = datetime(datetime.utcnow().year, 1, 1)

        costs = await self.get_cost_summary(customer_id,
                                           (datetime.utcnow() - year_start).days)
        roi_summary = await self.get_roi_summary(customer_id)
        value_metrics = await self.get_value_metrics(customer_id)

        # Generate alerts
        alerts = []
        if costs.total_costs > 1000000:
            alerts.append("High costs detected - exceeding $1M")
        if roi_summary.average_roi_percentage < 10:
            alerts.append("Low average ROI - below 10%")
        if value_metrics.at_risk_value > value_metrics.total_asset_value * 0.4:
            alerts.append("High value at risk - exceeding 40%")

        return EconomicDashboard(
            customer_id=customer_id,
            timestamp=datetime.utcnow(),
            total_costs_ytd=costs.total_costs,
            total_investments_ytd=roi_summary.total_invested,
            average_roi=roi_summary.average_roi_percentage,
            at_risk_value=value_metrics.at_risk_value,
            cost_trend=costs.trend_percentage and (
                "increasing" if costs.trend_percentage > 0 else "decreasing"
            ) or "stable",
            roi_trend="stable",
            alerts=alerts,
            key_metrics={
                "cost_per_asset": costs.total_costs / max(value_metrics.critical_asset_count, 1),
                "protected_value_ratio": value_metrics.protected_value / value_metrics.total_asset_value
                if value_metrics.total_asset_value > 0 else 0
            }
        )

    # ========================================================================
    # Helper Methods
    # ========================================================================

    async def _get_previous_period_costs(
        self, customer_id: str, current_start: datetime, period_days: int
    ) -> float:
        """Get costs from previous period for comparison"""
        previous_end = current_start
        previous_start = previous_end - timedelta(days=period_days)

        results = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {"key": "customer_id", "match": {"value": customer_id}},
                    {"key": "type", "match": {"value": "cost"}},
                    {"key": "date", "range": {
                        "gte": previous_start.isoformat(),
                        "lt": previous_end.isoformat()
                    }}
                ]
            },
            limit=1000
        )

        return sum(float(point.payload.get("amount", 0)) for point, _ in results)

    def _calculate_irr(
        self, initial_investment: float, cash_flows: List[float], initial_guess: float
    ) -> float:
        """Calculate Internal Rate of Return using Newton-Raphson"""
        # Simplified IRR calculation
        total_return = sum(cash_flows)
        years = len(cash_flows)

        if total_return <= initial_investment:
            return 0.0

        # Simple approximation
        irr = ((total_return / initial_investment) ** (1 / years)) - 1
        return irr * 100

    async def _calculate_base_impact(self, request: ImpactModelRequest) -> Dict[str, float]:
        """Calculate base impact costs"""
        duration = request.parameters.duration_hours
        severity_multipliers = {"low": 1, "medium": 2, "high": 4, "critical": 8}
        multiplier = severity_multipliers[request.parameters.severity]

        return {
            "equipment_damage": len(request.parameters.affected_systems) * 50000 * multiplier,
            "response_costs": duration * 500 * multiplier,  # $500/hr response
            "productivity_loss": duration * 10000 * multiplier,  # $10k/hr productivity
            "business_disruption": duration * 25000 * multiplier  # $25k/hr disruption
        }

    async def _calculate_reputation_impact(
        self, customer_id: str, scenario_type: ScenarioType, parameters: ScenarioParameters
    ) -> float:
        """Calculate reputation impact costs"""
        base_reputation_cost = 500000  # Base $500k

        severity_multipliers = {"low": 0.5, "medium": 1.0, "high": 2.0, "critical": 4.0}
        multiplier = severity_multipliers[parameters.severity]

        # Data breach has higher reputation impact
        if scenario_type == ScenarioType.DATA_BREACH:
            multiplier *= 2

        return base_reputation_cost * multiplier

    async def _generate_mitigation_recommendations(
        self, scenario_type: ScenarioType, severity: str
    ) -> List[str]:
        """Generate mitigation recommendations"""
        recommendations = {
            ScenarioType.RANSOMWARE: [
                "Implement robust backup and recovery procedures",
                "Deploy advanced endpoint detection and response",
                "Conduct regular security awareness training",
                "Maintain offline backup copies"
            ],
            ScenarioType.DATA_BREACH: [
                "Implement data loss prevention (DLP) solutions",
                "Enhance access controls and authentication",
                "Encrypt sensitive data at rest and in transit",
                "Conduct regular security audits"
            ],
            ScenarioType.SYSTEM_OUTAGE: [
                "Implement redundant systems and failover",
                "Develop comprehensive disaster recovery plan",
                "Regular testing of backup systems",
                "Invest in infrastructure monitoring"
            ],
            ScenarioType.SUPPLY_CHAIN: [
                "Conduct vendor security assessments",
                "Implement supply chain risk management",
                "Diversify supplier base",
                "Monitor third-party security posture"
            ]
        }

        return recommendations.get(scenario_type, [
            "Implement security best practices",
            "Conduct regular risk assessments",
            "Maintain incident response plan"
        ])
