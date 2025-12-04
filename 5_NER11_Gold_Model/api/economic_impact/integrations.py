"""
E10 Economic Impact Integrations
Integration helpers for E08 RAMS, E03 SBOM, E15 Vendor Equipment
"""

from typing import Dict, List, Optional
from datetime import datetime
from qdrant_client import QdrantClient


class RAMSIntegration:
    """Integration with E08 RAMS for reliability-based economic factors"""

    def __init__(self, qdrant_client: QdrantClient):
        self.qdrant_client = qdrant_client
        self.rams_collection = "ner11_rams"

    async def get_reliability_impact(
        self, customer_id: str, entity_id: str
    ) -> Dict[str, float]:
        """
        Get reliability scores and economic impact factors from E08 RAMS

        Returns:
            - reliability_score: 0-1 scale
            - availability_score: 0-1 scale
            - maintainability_score: 0-1 scale
            - safety_score: 0-1 scale
            - failure_cost: Estimated cost per failure
            - economic_impact_factor: Multiplier for business value
        """
        try:
            results = self.qdrant_client.scroll(
                collection_name=self.rams_collection,
                scroll_filter={
                    "must": [
                        {"key": "customer_id", "match": {"value": customer_id}},
                        {"key": "entity_id", "match": {"value": entity_id}}
                    ]
                },
                limit=1
            )

            if not results[0]:
                # Return default values if no RAMS data
                return {
                    "reliability_score": 0.8,
                    "availability_score": 0.95,
                    "maintainability_score": 0.85,
                    "safety_score": 0.9,
                    "failure_cost": 10000.0,
                    "economic_impact_factor": 1.0
                }

            rams_data = results[0][0].payload

            # Calculate economic impact factor from RAMS scores
            avg_score = (
                rams_data.get("reliability_score", 0.8) +
                rams_data.get("availability_score", 0.95) +
                rams_data.get("maintainability_score", 0.85) +
                rams_data.get("safety_score", 0.9)
            ) / 4

            # Higher RAMS scores = lower risk = higher economic impact factor
            economic_impact_factor = 0.5 + (avg_score * 0.5)

            # Estimate failure cost based on reliability
            base_failure_cost = 10000.0
            failure_cost = base_failure_cost / max(rams_data.get("reliability_score", 0.8), 0.1)

            return {
                "reliability_score": rams_data.get("reliability_score", 0.8),
                "availability_score": rams_data.get("availability_score", 0.95),
                "maintainability_score": rams_data.get("maintainability_score", 0.85),
                "safety_score": rams_data.get("safety_score", 0.9),
                "failure_cost": failure_cost,
                "economic_impact_factor": economic_impact_factor
            }

        except Exception as e:
            print(f"Error retrieving RAMS data: {e}")
            return {
                "reliability_score": 0.8,
                "availability_score": 0.95,
                "maintainability_score": 0.85,
                "safety_score": 0.9,
                "failure_cost": 10000.0,
                "economic_impact_factor": 1.0
            }

    async def calculate_maintenance_costs(
        self, customer_id: str, entity_id: str, period_years: int = 1
    ) -> float:
        """Calculate maintenance costs based on RAMS maintainability scores"""
        rams_data = await self.get_reliability_impact(customer_id, entity_id)

        # Lower maintainability = higher costs
        maintainability = rams_data["maintainability_score"]
        base_maintenance = 5000.0  # Base annual maintenance cost

        annual_cost = base_maintenance / max(maintainability, 0.1)
        return annual_cost * period_years


class SBOMIntegration:
    """Integration with E03 SBOM for component-based economic analysis"""

    def __init__(self, qdrant_client: QdrantClient):
        self.qdrant_client = qdrant_client
        self.sbom_collection = "ner11_sbom"

    async def get_component_economics(
        self, customer_id: str, component_id: Optional[str] = None
    ) -> List[Dict[str, any]]:
        """
        Get economic data for SBOM components

        Returns component economics including:
            - Vulnerability remediation costs
            - Replacement costs
            - License compliance costs
            - Support costs
        """
        search_filter = {
            "must": [
                {"key": "customer_id", "match": {"value": customer_id}},
                {"key": "type", "match": {"value": "component"}}
            ]
        }

        if component_id:
            search_filter["must"].append({
                "key": "component_id", "match": {"value": component_id}
            })

        try:
            results = self.qdrant_client.scroll(
                collection_name=self.sbom_collection,
                scroll_filter=search_filter,
                limit=500
            )

            components = []
            for point, _ in results:
                payload = point.payload

                # Calculate costs based on component data
                vulnerability_count = payload.get("vulnerability_count", 0)
                remediation_cost = vulnerability_count * 2500  # $2500 per vulnerability

                is_eol = payload.get("end_of_life", False)
                replacement_cost = 50000.0 if is_eol else 0.0

                license_type = payload.get("license_type", "permissive")
                compliance_cost = 10000.0 if license_type == "copyleft" else 0.0

                support_cost = 5000.0 if not payload.get("has_support", False) else 0.0

                components.append({
                    "component_id": payload.get("component_id"),
                    "component_name": payload.get("name"),
                    "vulnerability_count": vulnerability_count,
                    "remediation_cost": remediation_cost,
                    "replacement_cost": replacement_cost,
                    "compliance_cost": compliance_cost,
                    "support_cost": support_cost,
                    "total_cost": remediation_cost + replacement_cost + compliance_cost + support_cost,
                    "criticality": payload.get("criticality", "medium")
                })

            return components

        except Exception as e:
            print(f"Error retrieving SBOM economics: {e}")
            return []

    async def calculate_vulnerability_impact(
        self, customer_id: str
    ) -> Dict[str, float]:
        """Calculate total economic impact of vulnerabilities"""
        components = await self.get_component_economics(customer_id)

        total_remediation = sum(c["remediation_cost"] for c in components)
        total_replacement = sum(c["replacement_cost"] for c in components)
        total_compliance = sum(c["compliance_cost"] for c in components)

        critical_count = len([c for c in components if c["criticality"] == "critical"])
        high_count = len([c for c in components if c["criticality"] == "high"])

        return {
            "total_remediation_cost": total_remediation,
            "total_replacement_cost": total_replacement,
            "total_compliance_cost": total_compliance,
            "total_cost": total_remediation + total_replacement + total_compliance,
            "critical_vulnerabilities": critical_count,
            "high_vulnerabilities": high_count,
            "component_count": len(components)
        }


class VendorEquipmentIntegration:
    """Integration with E15 Vendor Equipment for equipment economics"""

    def __init__(self, qdrant_client: QdrantClient):
        self.qdrant_client = qdrant_client
        self.vendor_collection = "ner11_vendor_equipment"

    async def get_equipment_economics(
        self, customer_id: str, equipment_id: Optional[str] = None
    ) -> List[Dict[str, any]]:
        """
        Get economic data for vendor equipment

        Returns:
            - Equipment value
            - Annual maintenance costs
            - Replacement timeline and costs
            - Vendor lock-in risk premium
            - Total cost of ownership
        """
        search_filter = {
            "must": [
                {"key": "customer_id", "match": {"value": customer_id}},
                {"key": "type", "match": {"value": "equipment"}}
            ]
        }

        if equipment_id:
            search_filter["must"].append({
                "key": "equipment_id", "match": {"value": equipment_id}
            })

        try:
            results = self.qdrant_client.scroll(
                collection_name=self.vendor_collection,
                scroll_filter=search_filter,
                limit=500
            )

            equipment_list = []
            for point, _ in results:
                payload = point.payload

                equipment_value = float(payload.get("purchase_value", 50000))
                age_years = payload.get("age_years", 0)
                expected_life = payload.get("expected_life_years", 10)

                # Calculate depreciation
                depreciation_rate = 1.0 / expected_life
                current_value = equipment_value * max(0, 1 - (depreciation_rate * age_years))

                # Maintenance costs increase with age
                base_maintenance = equipment_value * 0.05  # 5% of value
                maintenance_multiplier = 1 + (age_years * 0.1)  # +10% per year
                annual_maintenance = base_maintenance * maintenance_multiplier

                # Replacement timeline
                remaining_life = max(0, expected_life - age_years)
                replacement_cost = float(payload.get("replacement_cost", equipment_value * 1.2))

                # Vendor lock-in risk premium
                vendor_lock_in = payload.get("vendor_lock_in", False)
                lock_in_premium = replacement_cost * 0.3 if vendor_lock_in else 0.0

                # Total cost of ownership
                tco = (
                    current_value +
                    (annual_maintenance * remaining_life) +
                    replacement_cost +
                    lock_in_premium
                )

                equipment_list.append({
                    "equipment_id": payload.get("equipment_id"),
                    "vendor_name": payload.get("vendor_name"),
                    "equipment_type": payload.get("equipment_type"),
                    "current_value": current_value,
                    "annual_maintenance": annual_maintenance,
                    "remaining_life_years": remaining_life,
                    "replacement_cost": replacement_cost,
                    "vendor_lock_in_premium": lock_in_premium,
                    "total_cost_of_ownership": tco,
                    "criticality": payload.get("criticality_score", 0.5)
                })

            return equipment_list

        except Exception as e:
            print(f"Error retrieving vendor equipment economics: {e}")
            return []

    async def calculate_equipment_portfolio_value(
        self, customer_id: str
    ) -> Dict[str, float]:
        """Calculate total portfolio value and costs"""
        equipment = await self.get_equipment_economics(customer_id)

        total_value = sum(e["current_value"] for e in equipment)
        total_maintenance = sum(e["annual_maintenance"] for e in equipment)
        total_replacement = sum(e["replacement_cost"] for e in equipment)
        total_tco = sum(e["total_cost_of_ownership"] for e in equipment)

        critical_equipment = [e for e in equipment if e["criticality"] > 0.7]
        critical_value = sum(e["current_value"] for e in critical_equipment)

        return {
            "total_current_value": total_value,
            "total_annual_maintenance": total_maintenance,
            "total_replacement_cost": total_replacement,
            "total_cost_of_ownership": total_tco,
            "equipment_count": len(equipment),
            "critical_equipment_count": len(critical_equipment),
            "critical_equipment_value": critical_value
        }


class IntegrationOrchestrator:
    """Orchestrate all economic integrations"""

    def __init__(self, qdrant_client: QdrantClient):
        self.rams = RAMSIntegration(qdrant_client)
        self.sbom = SBOMIntegration(qdrant_client)
        self.vendor = VendorEquipmentIntegration(qdrant_client)

    async def get_comprehensive_economics(
        self, customer_id: str, entity_id: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Get comprehensive economic data from all integrations

        Combines RAMS reliability, SBOM vulnerabilities, and vendor equipment
        into unified economic view.
        """
        results = {
            "customer_id": customer_id,
            "timestamp": datetime.utcnow().isoformat(),
            "rams": {},
            "sbom": {},
            "vendor_equipment": {},
            "total_economic_impact": 0.0
        }

        try:
            # Get RAMS data
            if entity_id:
                results["rams"] = await self.rams.get_reliability_impact(customer_id, entity_id)

            # Get SBOM vulnerabilities
            results["sbom"] = await self.sbom.calculate_vulnerability_impact(customer_id)

            # Get vendor equipment portfolio
            results["vendor_equipment"] = await self.vendor.calculate_equipment_portfolio_value(customer_id)

            # Calculate total economic impact
            total_impact = (
                results["rams"].get("failure_cost", 0) +
                results["sbom"].get("total_cost", 0) +
                results["vendor_equipment"].get("total_annual_maintenance", 0)
            )

            results["total_economic_impact"] = total_impact

            return results

        except Exception as e:
            print(f"Error in comprehensive economics: {e}")
            return results
