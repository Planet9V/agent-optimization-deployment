#!/usr/bin/env python3
"""
Cost Tracker - OpenAI API cost monitoring and budget management
Tracks embedding generation costs with budget alerts
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict
import structlog

logger = structlog.get_logger()

# OpenAI Pricing (as of 2025)
PRICING = {
    "text-embedding-3-small": {
        "per_1k_tokens": 0.00002,
        "dimensions": 1536
    },
    "text-embedding-3-large": {
        "per_1k_tokens": 0.00013,
        "dimensions": 3072
    },
    "text-embedding-ada-002": {
        "per_1k_tokens": 0.00010,
        "dimensions": 1536
    }
}

class CostTracker:
    """
    Tracks OpenAI API costs for embedding generation
    """

    def __init__(
        self,
        storage_path: Optional[Path] = None,
        daily_budget: Optional[float] = None,
        monthly_budget: Optional[float] = None
    ):
        """
        Initialize cost tracker

        Args:
            storage_path: Path to store cost data
            daily_budget: Daily spending limit in USD
            monthly_budget: Monthly spending limit in USD
        """
        self.storage_path = storage_path or Path(
            "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup/cost_tracking.json"
        )
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget

        # Load existing data
        self.costs = self._load_costs()

        logger.info(
            "cost_tracker_initialized",
            daily_budget=daily_budget,
            monthly_budget=monthly_budget
        )

    def _load_costs(self) -> Dict[str, Any]:
        """Load cost data from storage"""
        if not self.storage_path.exists():
            return {
                "daily": defaultdict(float),
                "monthly": defaultdict(float),
                "operations": [],
                "total_tokens": 0,
                "total_cost": 0.0
            }

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Convert date strings back to defaultdicts
            data["daily"] = defaultdict(float, data.get("daily", {}))
            data["monthly"] = defaultdict(float, data.get("monthly", {}))

            return data

        except Exception as e:
            logger.error("cost_data_load_failed", error=str(e))
            return {
                "daily": defaultdict(float),
                "monthly": defaultdict(float),
                "operations": [],
                "total_tokens": 0,
                "total_cost": 0.0
            }

    def _save_costs(self):
        """Save cost data to storage"""
        try:
            # Convert defaultdicts to regular dicts for JSON
            save_data = {
                "daily": dict(self.costs["daily"]),
                "monthly": dict(self.costs["monthly"]),
                "operations": self.costs["operations"],
                "total_tokens": self.costs["total_tokens"],
                "total_cost": self.costs["total_cost"]
            }

            with open(self.storage_path, 'w') as f:
                json.dump(save_data, f, indent=2)

        except Exception as e:
            logger.error("cost_data_save_failed", error=str(e))

    def estimate_cost(
        self,
        text: str,
        model: str = "text-embedding-3-large"
    ) -> Dict[str, Any]:
        """
        Estimate cost for embedding generation

        Args:
            text: Text to embed
            model: Embedding model

        Returns:
            Cost estimate with breakdown
        """
        # Rough token estimation: ~4 chars per token
        estimated_tokens = len(text) / 4

        if model not in PRICING:
            logger.warning("unknown_model_pricing", model=model)
            return {"error": "Unknown model"}

        price_per_1k = PRICING[model]["per_1k_tokens"]
        estimated_cost = (estimated_tokens / 1000) * price_per_1k

        return {
            "model": model,
            "estimated_tokens": int(estimated_tokens),
            "estimated_cost_usd": round(estimated_cost, 6),
            "price_per_1k_tokens": price_per_1k
        }

    def estimate_batch_cost(
        self,
        texts: List[str],
        model: str = "text-embedding-3-large"
    ) -> Dict[str, Any]:
        """
        Estimate cost for batch embedding generation

        Args:
            texts: List of texts to embed
            model: Embedding model

        Returns:
            Batch cost estimate
        """
        total_chars = sum(len(t) for t in texts)
        estimated_tokens = total_chars / 4

        if model not in PRICING:
            return {"error": "Unknown model"}

        price_per_1k = PRICING[model]["per_1k_tokens"]
        estimated_cost = (estimated_tokens / 1000) * price_per_1k

        return {
            "model": model,
            "num_texts": len(texts),
            "estimated_tokens": int(estimated_tokens),
            "estimated_cost_usd": round(estimated_cost, 6),
            "avg_cost_per_text": round(estimated_cost / len(texts), 6)
        }

    def record_operation(
        self,
        tokens: int,
        model: str = "text-embedding-3-large",
        operation_type: str = "embedding",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record an API operation and its cost

        Args:
            tokens: Tokens used
            model: Model used
            operation_type: Type of operation
            metadata: Additional metadata

        Returns:
            Operation record with cost
        """
        if model not in PRICING:
            logger.warning("unknown_model_pricing", model=model)
            cost = 0.0
        else:
            price_per_1k = PRICING[model]["per_1k_tokens"]
            cost = (tokens / 1000) * price_per_1k

        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")

        # Update totals
        self.costs["total_tokens"] += tokens
        self.costs["total_cost"] += cost
        self.costs["daily"][today] += cost
        self.costs["monthly"][month] += cost

        # Record operation
        operation = {
            "timestamp": datetime.now().isoformat(),
            "date": today,
            "model": model,
            "tokens": tokens,
            "cost_usd": round(cost, 6),
            "operation_type": operation_type,
            "metadata": metadata or {}
        }
        self.costs["operations"].append(operation)

        # Save to disk
        self._save_costs()

        # Check budgets
        self._check_budgets(today, month, cost)

        logger.info(
            "operation_recorded",
            type=operation_type,
            tokens=tokens,
            cost_usd=round(cost, 6)
        )

        return operation

    def _check_budgets(self, today: str, month: str, new_cost: float):
        """Check if budgets are exceeded"""
        if self.daily_budget:
            daily_total = self.costs["daily"][today]
            if daily_total > self.daily_budget:
                logger.warning(
                    "daily_budget_exceeded",
                    budget=self.daily_budget,
                    spent=round(daily_total, 2),
                    overage=round(daily_total - self.daily_budget, 2)
                )

        if self.monthly_budget:
            monthly_total = self.costs["monthly"][month]
            if monthly_total > self.monthly_budget:
                logger.warning(
                    "monthly_budget_exceeded",
                    budget=self.monthly_budget,
                    spent=round(monthly_total, 2),
                    overage=round(monthly_total - self.monthly_budget, 2)
                )

    def get_daily_cost(self, date: Optional[str] = None) -> float:
        """
        Get cost for specific date

        Args:
            date: Date in YYYY-MM-DD format (default: today)

        Returns:
            Cost in USD
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        return self.costs["daily"].get(date, 0.0)

    def get_monthly_cost(self, month: Optional[str] = None) -> float:
        """
        Get cost for specific month

        Args:
            month: Month in YYYY-MM format (default: current month)

        Returns:
            Cost in USD
        """
        if month is None:
            month = datetime.now().strftime("%Y-%m")

        return self.costs["monthly"].get(month, 0.0)

    def get_cost_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive cost summary

        Returns:
            Summary with daily, monthly, and total costs
        """
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")

        summary = {
            "total": {
                "tokens": self.costs["total_tokens"],
                "cost_usd": round(self.costs["total_cost"], 2)
            },
            "today": {
                "date": today,
                "cost_usd": round(self.get_daily_cost(today), 2),
                "budget": self.daily_budget,
                "remaining": round(self.daily_budget - self.get_daily_cost(today), 2) if self.daily_budget else None
            },
            "this_month": {
                "month": month,
                "cost_usd": round(self.get_monthly_cost(month), 2),
                "budget": self.monthly_budget,
                "remaining": round(self.monthly_budget - self.get_monthly_cost(month), 2) if self.monthly_budget else None
            },
            "operations_count": len(self.costs["operations"])
        }

        # Add budget warnings
        summary["warnings"] = []
        if self.daily_budget and summary["today"]["cost_usd"] > self.daily_budget:
            summary["warnings"].append("Daily budget exceeded")
        if self.monthly_budget and summary["this_month"]["cost_usd"] > self.monthly_budget:
            summary["warnings"].append("Monthly budget exceeded")

        return summary

    def get_cost_breakdown(
        self,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Get cost breakdown for recent days

        Args:
            days: Number of days to include

        Returns:
            Daily breakdown
        """
        breakdown = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            cost = self.get_daily_cost(date)
            breakdown.append({
                "date": date,
                "cost_usd": round(cost, 2)
            })

        return {
            "period_days": days,
            "breakdown": breakdown,
            "total": round(sum(d["cost_usd"] for d in breakdown), 2)
        }

    def get_operations(
        self,
        operation_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get recent operations

        Args:
            operation_type: Filter by operation type
            limit: Maximum operations to return

        Returns:
            List of operations
        """
        operations = self.costs["operations"]

        if operation_type:
            operations = [
                op for op in operations
                if op.get("operation_type") == operation_type
            ]

        # Return most recent first
        return list(reversed(operations[-limit:]))

    def reset_budgets(self):
        """Reset all cost tracking (use with caution)"""
        self.costs = {
            "daily": defaultdict(float),
            "monthly": defaultdict(float),
            "operations": [],
            "total_tokens": 0,
            "total_cost": 0.0
        }
        self._save_costs()
        logger.warning("cost_tracking_reset")

    def export_report(
        self,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Export detailed cost report

        Args:
            output_path: Path to save report

        Returns:
            Report content
        """
        summary = self.get_cost_summary()
        breakdown = self.get_cost_breakdown(30)

        report = f"""# OpenAI API Cost Report
Generated: {datetime.now().isoformat()}

## Summary
- **Total Tokens**: {summary['total']['tokens']:,}
- **Total Cost**: ${summary['total']['cost_usd']:.2f}
- **Operations**: {summary['operations_count']}

## Today ({summary['today']['date']})
- **Cost**: ${summary['today']['cost_usd']:.2f}
- **Budget**: ${summary['today']['budget'] or 'Not set'}
- **Remaining**: ${summary['today']['remaining'] or 'N/A'}

## This Month ({summary['this_month']['month']})
- **Cost**: ${summary['this_month']['cost_usd']:.2f}
- **Budget**: ${summary['this_month']['budget'] or 'Not set'}
- **Remaining**: ${summary['this_month']['remaining'] or 'N/A'}

## 30-Day Breakdown
"""
        for day in breakdown['breakdown']:
            report += f"- {day['date']}: ${day['cost_usd']:.2f}\n"

        report += f"\n**30-Day Total**: ${breakdown['total']:.2f}\n"

        if summary['warnings']:
            report += "\n## ⚠️ Warnings\n"
            for warning in summary['warnings']:
                report += f"- {warning}\n"

        if output_path:
            output_path.write_text(report)
            logger.info("cost_report_exported", path=str(output_path))

        return report
