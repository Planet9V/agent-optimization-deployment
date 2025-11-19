---
title: AgentZero Integration Guide (Part 1 of 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 448
status: published
tags: [neocoder, mcp, documentation]
---


# AgentZero Integration Guide

[← Back to CVE Intelligence Tools](05_CVE_Intelligence_Tools.md) | [Next: Advanced Topics →](../06_Advanced_Topics/01_Hybrid_Reasoning.md)

## Overview

Complete guide for integrating NeoCoder MCP Server (including Phase 2.14 NVD Live Intelligence) with AgentZero running in a separate Docker container.

**Architecture:**
```
┌─────────────────────┐         ┌─────────────────────┐
│   AgentZero         │         │   NeoCoder MCP      │
│   Container         │────────▶│   Container         │
│   (agent-zero)      │  HTTP   │   (neocoder)        │
│   Port: 50001-50003 │         │   Port: 8002        │
└─────────────────────┘         └─────────────────────┘
         │                               │
         └───────────┬───────────────────┘
                     │
              Docker Network
           (agentzero_default)
```

---

## Step 1: Docker Network Configuration

### Verify Network Connectivity

Check that both containers are on the same Docker network:

```bash
# List Docker networks
docker network ls

# Expected: agentzero_default or container_agentzero_default

# Inspect network to verify both services
docker network inspect agentzero_default

# Should show both 'neocoder' and 'agent-zero' containers
```

### Docker Compose Configuration

Ensure `docker-compose.yml` has both services configured:

```yaml
version: '3.8'

services:
  neocoder:
    container_name: neocoder
    build: ./docker/neocoder
    ports:
      - "8002:8002"  # NeoCoder MCP server
    networks:
      - agentzero_network
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - QDRANT_URL=http://qdrant:6333
      - NVD_API_KEY=919ecb88-4e30-4f58-baeb-67c868314307
    depends_on:
      - neo4j
      - qdrant

  agent-zero:
    container_name: agent-zero
    build: ./agent-zero
    ports:
      - "50001:50001"  # AgentZero API
      - "50002:50002"  # AgentZero WebUI
    networks:
      - agentzero_network
    environment:
      - NEOCODER_API_URL=http://neocoder:8002  # NEW
    depends_on:
      - neocoder

networks:
  agentzero_network:
    driver: bridge
```

**Key Points:**
- Both services on `agentzero_network`
- `NEOCODER_API_URL` environment variable for AgentZero
- Service name `neocoder` is DNS-resolvable within network
- Port 8002 exposed for NeoCoder API

### Test Network Connectivity

```bash
# From AgentZero container, test connection to NeoCoder
docker exec agent-zero curl http://neocoder:8002/health

# Expected response:
# {"status": "healthy", "neo4j": "connected", "qdrant": "connected"}

# Test NVD Live Intelligence endpoint
docker exec agent-zero curl http://neocoder:8002/nvd/live/CVE-2021-44228

# Should return CVE data
```

---

## Step 2: AgentZero Tool Configuration

### Create Tool Definitions

AgentZero uses a tools directory structure. Create NVD intelligence tools:

**Location:** `/agent-zero/python/tools/neocoder_nvd.py`

```python
"""
NeoCoder NVD Live Intelligence Tools for AgentZero
Phase 2.14 - Real-time CVE queries and gap analysis
"""

import os
import requests
from typing import Optional, List, Dict
from python.helpers.tool import Tool, Response

# Configuration from environment
NEOCODER_API_URL = os.getenv("NEOCODER_API_URL", "http://neocoder:8002")


class NVDLiveLookup(Tool):
    """
    Real-time CVE lookup from NVD API via NeoCoder

    Use this tool when you need immediate, authoritative CVE information
    including CVSS scores, severity, CWE mappings, and references.
    """

    async def execute(self, cve_id: str, **kwargs) -> Response:
        """
        Fetch CVE data from NVD in real-time

        Args:
            cve_id: CVE identifier (e.g., "CVE-2021-44228")

        Returns:
            Response with CVE details including:
            - CVSS score and severity
            - Published/modified dates
            - CWE IDs
            - References
            - Whether it exists in Neo4j
        """
        try:
            url = f"{NEOCODER_API_URL}/nvd/live/{cve_id}"
            response = requests.get(url, timeout=10)

            if response.status_code == 404:
                return Response(
                    message=f"CVE {cve_id} not found in NVD",
                    break_loop=False
                )

            response.raise_for_status()
            data = response.json()

            # Format response for agent
            message = f"""
CVE Intelligence Report: {data['cve_id']}

**Severity:** {data['severity']} (CVSS: {data['cvss_score']})
**Published:** {data['published_date']}
**Last Modified:** {data['modified_date']}

**CWE Weaknesses:** {', '.join(data['cwe_ids']) if data['cwe_ids'] else 'None specified'}

**Description:**
{data['description']}

**In Local Database:** {'Yes' if data['in_neo4j'] else 'No - live NVD data only'}

**References:** {len(data['references'])} available
"""

            return Response(
                message=message,
                data=data,
                break_loop=False
            )

        except requests.exceptions.RequestException as e:
            return Response(
                message=f"Error querying NeoCoder NVD service: {str(e)}",
                break_loop=False
            )


class NVDGapAnalysis(Tool):
    """
    Analyze gaps between local Neo4j database and NVD

    Use this tool to identify missing CVEs in your local database,
    prioritize re-ingestion efforts, and validate data completeness.
    """

    async def execute(
        self,
        year: Optional[int] = None,
        min_cvss: Optional[float] = None,
        **kwargs
    ) -> Response:
        """
        Compare local database vs NVD to find gaps

        Args:
            year: Filter by year (e.g., 2021)
            min_cvss: Minimum CVSS score (e.g., 7.0 for HIGH+)

        Returns:
            Response with gap analysis including:
            - Total in Neo4j vs NVD
            - Missing CVE count
            - List of missing CVEs (first 100)
        """
        try:
            url = f"{NEOCODER_API_URL}/nvd/gap-analysis"
            payload = {}
            if year:
                payload["year"] = year
            if min_cvss:
                payload["min_cvss"] = min_cvss

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            message = f"""
Gap Analysis Report
{'='*60}

**Filter:** Year={data.get('year', 'All')} | Min CVSS={data.get('min_cvss', 'Any')}

**Current State:**
- CVEs in Neo4j: {data['total_in_neo4j']:,}
- CVEs in NVD: {data['total_in_nvd']:,}
- Missing: {data['missing_count']:,} ({data['missing_count']/data['total_in_nvd']*100:.1f}%)
- Outdated: {data['outdated_count']:,}

**Missing CVEs (first 100):**
{', '.join(data['missing_cves'][:20])}
{'...' if len(data['missing_cves']) > 20 else ''}

**Recommendation:**
"""

            if data['missing_count'] > 1000:
                message += "⚠️ Significant gap detected. Consider full re-ingestion."
            elif data['missing_count'] > 100:
                message += "⚠️ Moderate gap. Batch fetch high-priority CVEs."
            elif data['missing_count'] > 0:
                message += "✓ Small gap. Targeted batch fetch recommended."
            else:
                message += "✅ Database is up to date!"

            return Response(
                message=message,
                data=data,
                break_loop=False
            )

        except requests.exceptions.RequestException as e:
            return Response(
                message=f"Error performing gap analysis: {str(e)}",
                break_loop=False
            )


class NVDDeltaCheck(Tool):
    """
    Check for new or modified CVEs in NVD since timestamp

    Use this tool for continuous monitoring, automated alerts,
    and triggering incremental ingestion pipelines.
    """

    async def execute(
        self,
        since_hours: int = 24,
        **kwargs
    ) -> Response:
        """
        Check what's new/modified in NVD since timestamp

        Args:
            since_hours: Check last N hours (default: 24)

        Returns:
            Response with delta check including:
            - New CVEs published
            - Modified CVEs updated
            - Details for CRITICAL severity CVEs
        """
        try:
            url = f"{NEOCODER_API_URL}/nvd/delta-check"
            payload = {"since_hours": since_hours}

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Identify CRITICAL CVEs
            critical_new = [
                cve for cve in data['new_cves']
                if cve.get('severity') == 'CRITICAL'
            ]

            message = f"""
NVD Delta Check Report
{'='*60}

**Time Range:** Last {since_hours} hours
**Period:** {data['since_timestamp']} to {data['check_timestamp']}

**Summary:**
- New CVEs: {data['total_new']}
- Modified CVEs: {data['total_modified']}
- **CRITICAL New CVEs: {len(critical_new)}**

"""

            if critical_new:
                message += "🚨 **CRITICAL CVEs Detected:**\n"
                for cve in critical_new[:5]:
                    message += f"- {cve['cve_id']} (CVSS: {cve.get('cvss_score', 'N/A')})\n"

                if len(critical_new) > 5:
                    message += f"... and {len(critical_new) - 5} more\n"

                message += "\n⚠️ **Action Required:** Immediate investigation recommended\n"

            elif data['total_new'] > 0:
                message += f"ℹ️ {data['total_new']} new CVEs found (none CRITICAL)\n"
            else:
                message += "✅ No new CVEs in this period\n"

            return Response(
                message=message,
                data=data,
                break_loop=False
            )

        except requests.exceptions.RequestException as e:
            return Response(
                message=f"Error checking NVD delta: {str(e)}",
                break_loop=False
            )


class NVDBatchFetch(Tool):
    """
    Fetch multiple CVEs from NVD in parallel

    Use this tool after gap analysis to retrieve specific CVEs,
    or to backfill high-priority vulnerabilities.
    """

    async def execute(
        self,
        cve_ids: List[str],
        **kwargs
    ) -> Response:
        """
        Batch fetch CVEs from NVD (max 100)

        Args:
            cve_ids: List of CVE identifiers

        Returns:
            Response with batch fetch results
        """
        try:
            if len(cve_ids) > 100:
                return Response(
                    message="Maximum 100 CVE IDs per batch request",
                    break_loop=False
                )

            url = f"{NEOCODER_API_URL}/nvd/batch-fetch"
            payload = {"cve_ids": cve_ids}

            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()

            message = f"""
Batch Fetch Results
{'='*60}

**Requested:** {data['requested']} CVEs
**Found:** {data['found']} CVEs
**Success Rate:** {data['found']/data['requested']*100:.1f}%

**Retrieved CVEs:**
"""

            for cve in data['cves'][:10]:
                message += f"- {cve['cve_id']}: {cve['severity']} (CVSS: {cve.get('cvss_score', 'N/A')})\n"

            if len(data['cves']) > 10:
                message += f"... and {len(data['cves']) - 10} more\n"

            return Response(
                message=message,
                data=data,
                break_loop=False
            )

        except requests.exceptions.RequestException as e:
            return Response(
                message=f"Error batch fetching CVEs: {str(e)}",
                break_loop=False
            )
```

### Register Tools with AgentZero

Add to AgentZero's tool registry (usually in `initialize.py` or tool loader):

```python
from python.tools.neocoder_nvd import (
    NVDLiveLookup,
    NVDGapAnalysis,
    NVDDeltaCheck,
    NVDBatchFetch
)

# Register NVD tools
tools = [
    NVDLiveLookup(),
    NVDGapAnalysis(),
    NVDDeltaCheck(),
    NVDBatchFetch(),
]
```

---
