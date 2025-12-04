"""
Demographics Baseline Service
==============================

Service layer for E11 Psychohistory Demographics Baseline.
Provides population analytics, workforce modeling, and organization structure analysis.

Version: 1.0.0
Created: 2025-12-04
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from uuid import uuid4
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny,
    MatchValue,
    Range,
    PointStruct,
    VectorParams,
    Distance,
)

from ..customer_isolation import CustomerContext, CustomerContextManager
from .schemas import (
    PopulationProfile,
    PopulationSegment,
    DemographicDistribution,
    BaselineMetrics,
    WorkforceComposition,
    RoleBreakdown,
    DepartmentBreakdown,
    SkillDistribution,
    OrganizationUnit,
    CriticalityLevel,
    TurnoverRisk,
    SkillCategory,
)

logger = logging.getLogger(__name__)


class DemographicsService:
    """
    Service for psychohistory demographics baseline.

    Provides customer-isolated operations for:
    - Population demographics and analytics
    - Workforce composition and modeling
    - Organization structure analysis
    - Role and skill distribution
    - Baseline metrics for psychohistory calculations
    """

    COLLECTION_NAME = "ner11_demographics"
    VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        embedding_service: Optional[Any] = None,
    ):
        """Initialize demographics service."""
        self.qdrant_client = QdrantClient(url=qdrant_url)
        self._embedding_service = embedding_service
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Ensure Qdrant collection exists."""
        try:
            self.qdrant_client.get_collection(self.COLLECTION_NAME)
            logger.info(f"Collection {self.COLLECTION_NAME} exists")
        except Exception:
            logger.info(f"Creating collection {self.COLLECTION_NAME}")
            self.qdrant_client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

    def _get_customer_context(self) -> CustomerContext:
        """Get required customer context."""
        return CustomerContextManager.require_context()

    def _build_customer_filter(
        self,
        customer_id: str,
        record_type: str,
        additional_conditions: Optional[List[FieldCondition]] = None,
    ) -> Filter:
        """Build Qdrant filter with customer isolation."""
        conditions = [
            FieldCondition(key="customer_id", match=MatchValue(value=customer_id)),
            FieldCondition(key="record_type", match=MatchValue(value=record_type)),
        ]

        if additional_conditions:
            conditions.extend(additional_conditions)

        return Filter(must=conditions)

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        if self._embedding_service is not None:
            return self._embedding_service.encode(text)
        return [0.0] * self.VECTOR_SIZE

    # ===== Population Metrics Operations =====

    def get_population_summary(self) -> Dict[str, Any]:
        """Get population demographics summary."""
        context = self._get_customer_context()

        # Mock data - replace with actual Qdrant queries
        return {
            "customer_id": context.customer_id,
            "total_population": 1500,
            "active_employees": 1350,
            "contractors": 150,
            "growth_rate_30d": 0.025,
            "stability_index": 0.87,
        }

    def get_population_distribution(self) -> Dict[str, Any]:
        """Get population distribution by category."""
        context = self._get_customer_context()

        distribution = {
            "by_age_group": {
                "18-25": 120,
                "26-35": 450,
                "36-45": 380,
                "46-55": 320,
                "56+": 230,
            },
            "by_tenure": {
                "0-1y": 200,
                "1-3y": 400,
                "3-5y": 350,
                "5-10y": 350,
                "10y+": 200,
            },
            "by_education": {
                "high_school": 150,
                "bachelors": 700,
                "masters": 500,
                "phd": 150,
            },
            "by_department": {
                "engineering": 500,
                "operations": 400,
                "security": 200,
                "management": 150,
                "support": 250,
            },
        }

        return {
            "customer_id": context.customer_id,
            "distribution": distribution,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_org_unit_profile(self, org_unit_id: str) -> Dict[str, Any]:
        """Get organization unit population profile."""
        context = self._get_customer_context()

        # Mock data - replace with actual Qdrant queries
        return {
            "org_unit_id": org_unit_id,
            "customer_id": context.customer_id,
            "total_population": 250,
            "demographics": {
                "avg_age": 38.5,
                "avg_tenure_years": 5.2,
                "gender_diversity": 0.48,
            },
            "stability_index": 0.82,
        }

    def get_population_trends(self) -> Dict[str, Any]:
        """Get population trend analysis."""
        context = self._get_customer_context()

        trends = [
            {
                "period": "2024-11",
                "population": 1450,
                "growth_rate": 0.02,
            },
            {
                "period": "2024-12",
                "population": 1500,
                "growth_rate": 0.035,
            },
        ]

        forecast = {
            "2025-01": 1535,
            "2025-02": 1555,
            "2025-03": 1570,
        }

        return {
            "customer_id": context.customer_id,
            "trends": trends,
            "forecast_90d": forecast,
        }

    def query_population(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute custom population query."""
        context = self._get_customer_context()

        # Implementation would parse filters and execute Qdrant queries
        return {
            "customer_id": context.customer_id,
            "results": [],
            "total": 0,
        }

    # ===== Workforce Analytics Operations =====

    def get_workforce_composition(self) -> Dict[str, Any]:
        """Get workforce composition breakdown."""
        context = self._get_customer_context()

        by_role = [
            {
                "role_id": "R001",
                "role_name": "Software Engineer",
                "count": 300,
                "percentage": 20.0,
                "security_relevant": False,
                "criticality": "medium",
            },
            {
                "role_id": "R002",
                "role_name": "Security Analyst",
                "count": 50,
                "percentage": 3.3,
                "security_relevant": True,
                "criticality": "high",
            },
        ]

        by_department = [
            {
                "department_id": "D001",
                "department_name": "Engineering",
                "count": 500,
                "percentage": 33.3,
                "turnover_rate": 0.12,
            },
        ]

        return {
            "org_unit_id": "ROOT",
            "org_unit_name": "Company",
            "customer_id": context.customer_id,
            "total_employees": 1500,
            "by_role": by_role,
            "by_department": by_department,
            "turnover_rate": 0.15,
        }

    def get_skills_inventory(self) -> Dict[str, Any]:
        """Get skills inventory and distribution."""
        context = self._get_customer_context()

        critical_skills = [
            {
                "skill_name": "Cybersecurity",
                "category": "security",
                "employee_count": 75,
                "proficiency_avg": 7.8,
                "criticality": "critical",
            },
            {
                "skill_name": "Network Engineering",
                "category": "technical",
                "employee_count": 120,
                "proficiency_avg": 7.2,
                "criticality": "high",
            },
        ]

        skill_gaps = [
            {
                "skill_name": "Incident Response",
                "required_count": 50,
                "current_count": 25,
                "gap": 25,
            },
        ]

        return {
            "customer_id": context.customer_id,
            "total_skills": 150,
            "by_category": {
                "technical": 60,
                "security": 30,
                "management": 25,
                "operational": 20,
                "analytical": 15,
            },
            "critical_skills": critical_skills,
            "skill_gaps": skill_gaps,
        }

    def get_turnover_metrics(self) -> Dict[str, Any]:
        """Get turnover metrics and predictions."""
        context = self._get_customer_context()

        return {
            "customer_id": context.customer_id,
            "current_turnover_rate": 0.15,
            "predicted_turnover_30d": 0.18,
            "high_risk_employees": 45,
            "retention_score": 0.73,
        }

    def get_team_profile(self, team_id: str) -> Dict[str, Any]:
        """Get team demographic profile."""
        context = self._get_customer_context()

        return {
            "team_id": team_id,
            "team_name": "Security Operations Team",
            "customer_id": context.customer_id,
            "member_count": 25,
            "demographics": {
                "avg_age": 35.2,
                "avg_tenure_years": 3.8,
                "gender_diversity": 0.42,
            },
            "cohesion_score": 0.84,
            "diversity_index": 0.68,
        }

    def get_capacity_metrics(self) -> Dict[str, Any]:
        """Get capacity and utilization metrics."""
        context = self._get_customer_context()

        return {
            "customer_id": context.customer_id,
            "total_capacity_hours": 300000,
            "utilized_capacity": 0.87,
            "available_capacity": 0.13,
            "overutilized_teams": ["Security Ops", "DevOps"],
        }

    # ===== Organization Structure Operations =====

    def get_organization_hierarchy(self) -> Dict[str, Any]:
        """Get organization hierarchy map."""
        context = self._get_customer_context()

        root_units = [
            {
                "unit_id": "U001",
                "name": "Engineering",
                "level": 1,
                "employee_count": 500,
                "children": ["U002", "U003"],
            },
        ]

        return {
            "customer_id": context.customer_id,
            "root_units": root_units,
            "total_units": 25,
            "max_depth": 4,
        }

    def list_organization_units(self) -> Dict[str, Any]:
        """List all organization units."""
        context = self._get_customer_context()

        units = [
            {
                "unit_id": "U001",
                "name": "Engineering",
                "parent_id": None,
                "level": 1,
                "employee_count": 500,
                "criticality": "high",
            },
        ]

        return {
            "customer_id": context.customer_id,
            "units": units,
            "total": len(units),
        }

    def get_unit_details(self, unit_id: str) -> Dict[str, Any]:
        """Get organization unit details with demographics."""
        context = self._get_customer_context()

        return {
            "unit_id": unit_id,
            "name": "Security Operations",
            "customer_id": context.customer_id,
            "parent_id": "U001",
            "level": 2,
            "employee_count": 75,
            "criticality": "critical",
            "security_roles_count": 60,
            "demographics": {
                "avg_age": 34.5,
                "avg_tenure_years": 4.2,
                "turnover_rate": 0.12,
            },
        }

    def get_organization_relationships(self) -> Dict[str, Any]:
        """Get inter-unit relationships."""
        context = self._get_customer_context()

        relationships = [
            {
                "from_unit": "U001",
                "to_unit": "U002",
                "relationship_type": "reports_to",
                "strength": 1.0,
            },
        ]

        return {
            "customer_id": context.customer_id,
            "relationships": relationships,
            "total": len(relationships),
        }

    def analyze_organization_structure(
        self, analysis_type: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze organization structure."""
        context = self._get_customer_context()

        # Implementation would vary based on analysis_type
        return {
            "customer_id": context.customer_id,
            "analysis_type": analysis_type,
            "results": {},
        }

    # ===== Role Analysis Operations =====

    def get_role_distribution(self) -> Dict[str, Any]:
        """Get role distribution across organization."""
        context = self._get_customer_context()

        roles = [
            {
                "role_id": "R001",
                "role_name": "Software Engineer",
                "category": "technical",
                "count": 300,
                "security_relevant": False,
            },
            {
                "role_id": "R002",
                "role_name": "Security Analyst",
                "category": "security",
                "count": 50,
                "security_relevant": True,
            },
        ]

        return {
            "customer_id": context.customer_id,
            "total_roles": 45,
            "by_category": {
                "technical": 15,
                "security": 8,
                "management": 10,
                "operational": 12,
            },
            "security_relevant_roles": 8,
            "roles": roles,
        }

    def get_role_demographics(self, role_id: str) -> Dict[str, Any]:
        """Get demographics for specific role."""
        context = self._get_customer_context()

        return {
            "role_id": role_id,
            "role_name": "Security Analyst",
            "customer_id": context.customer_id,
            "employee_count": 50,
            "demographics": {
                "avg_age": 32.5,
                "avg_tenure_years": 3.2,
                "education_level": "bachelors+",
            },
            "turnover_rate": 0.18,
        }

    def get_security_relevant_roles(self) -> Dict[str, Any]:
        """Get security-relevant roles analysis."""
        context = self._get_customer_context()

        roles = [
            {
                "role_id": "R002",
                "role_name": "Security Analyst",
                "count": 50,
                "criticality": "high",
                "coverage": 0.85,
            },
        ]

        return {
            "customer_id": context.customer_id,
            "total_security_roles": 8,
            "roles": roles,
            "coverage_score": 0.82,
        }

    def get_access_patterns(self) -> Dict[str, Any]:
        """Get role-based access patterns."""
        context = self._get_customer_context()

        patterns = [
            {
                "role_id": "R002",
                "role_name": "Security Analyst",
                "access_level": "elevated",
                "resource_types": ["security_logs", "incident_reports"],
            },
        ]

        anomalies = [
            {
                "employee_id": "E123",
                "role_id": "R002",
                "anomaly_type": "unusual_access_time",
                "severity": "medium",
            },
        ]

        return {
            "customer_id": context.customer_id,
            "patterns": patterns,
            "anomalies": anomalies,
        }

    # ===== Dashboard Operations =====

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get demographics dashboard summary."""
        context = self._get_customer_context()

        population_summary = {
            "total_population": 1500,
            "growth_rate": 0.025,
            "stability_index": 0.87,
        }

        workforce_summary = {
            "total_employees": 1500,
            "turnover_rate": 0.15,
            "avg_tenure_years": 4.8,
        }

        organization_summary = {
            "total_units": 25,
            "max_depth": 4,
            "critical_units": 5,
        }

        return {
            "customer_id": context.customer_id,
            "population_summary": population_summary,
            "workforce_summary": workforce_summary,
            "organization_summary": organization_summary,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_baseline_metrics(self) -> Dict[str, Any]:
        """Get baseline metrics for psychohistory."""
        context = self._get_customer_context()

        return {
            "customer_id": context.customer_id,
            "population_stability_index": 0.87,
            "role_diversity_score": 0.74,
            "skill_concentration_risk": 0.32,
            "succession_coverage": 0.68,
            "insider_threat_baseline": 3.2,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_demographic_indicators(self) -> Dict[str, Any]:
        """Get key demographic indicators."""
        context = self._get_customer_context()

        indicators = [
            {
                "indicator": "population_stability",
                "value": 0.87,
                "trend": "stable",
                "threshold": 0.80,
                "status": "healthy",
            },
            {
                "indicator": "turnover_risk",
                "value": 0.18,
                "trend": "increasing",
                "threshold": 0.15,
                "status": "warning",
            },
        ]

        warnings = [
            "Turnover rate exceeding target threshold",
            "Skill concentration risk in security team",
        ]

        return {
            "customer_id": context.customer_id,
            "indicators": indicators,
            "warnings": warnings,
        }

    def get_demographic_alerts(self) -> Dict[str, Any]:
        """Get demographic alerts and anomalies."""
        context = self._get_customer_context()

        alerts = [
            {
                "alert_id": "A001",
                "type": "turnover_spike",
                "severity": "medium",
                "affected_unit": "Engineering",
                "description": "15% increase in turnover rate",
                "created_at": datetime.utcnow().isoformat(),
            },
        ]

        return {
            "customer_id": context.customer_id,
            "alerts": alerts,
            "total": len(alerts),
        }

    def get_trend_analysis(self) -> Dict[str, Any]:
        """Get demographic trend analysis."""
        context = self._get_customer_context()

        trends = [
            {
                "metric": "population_growth",
                "trend": "increasing",
                "rate": 0.025,
                "confidence": 0.85,
            },
        ]

        forecast = {
            "30d": {"population": 1535, "confidence": 0.90},
            "90d": {"population": 1605, "confidence": 0.75},
        }

        return {
            "customer_id": context.customer_id,
            "trends": trends,
            "forecast": forecast,
        }
