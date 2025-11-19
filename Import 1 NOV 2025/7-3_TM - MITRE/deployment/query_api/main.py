"""
AEON MITRE Query API - Main Application
File: main.py
Created: 2025-11-08
Purpose: FastAPI application for MITRE query execution
"""

from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from config.settings import settings
from config.database import neo4j_connection, get_neo4j
from config.cache import cache_manager, get_cache
from queries.cve_impact import CVEImpactExecutor, TodayCVEImpactExecutor
from queries.attack_path import (
    AttackPathExecutor,
    ThreatActorPathwayExecutor,
    TodayCVEThreatPathExecutor
)
from queries.asset_management import (
    EquipmentInventoryExecutor,
    SoftwareInventoryExecutor,
    AssetLocationExecutor
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting AEON MITRE Query API")
    await neo4j_connection.initialize()
    await cache_manager.initialize()

    yield

    # Shutdown
    logger.info("Shutting down AEON MITRE Query API")
    await neo4j_connection.close()
    await cache_manager.close()


# Initialize FastAPI app
app = FastAPI(
    title="AEON MITRE Query API",
    description="Backend API for executing MITRE ATT&CK graph queries",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key security
api_key_header = APIKeyHeader(name=settings.api_key_header, auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key"""
    if not settings.api_keys_list:
        # No API keys configured, allow all requests
        return None

    if not api_key or api_key not in settings.api_keys_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return api_key


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "AEON MITRE Query API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check(db = Depends(get_neo4j)):
    """Health check endpoint"""
    try:
        # Test database connection
        await db.execute_read("RETURN 1 as test")

        return {
            "status": "healthy",
            "database": "connected",
            "cache": "available" if cache_manager._enabled else "disabled",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


# ============================================================================
# Question 1: Does this CVE impact my equipment?
# ============================================================================

@app.post("/api/v1/query/cve-impact")
async def cve_impact_query(
    cveId: str,
    complexity: str = "simple",
    use_cache: bool = True,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_neo4j),
    cache = Depends(get_cache)
):
    """
    Query: Does this CVE impact my equipment?

    **Complexity Levels:**
    - simple: Direct CVE to Equipment
    - intermediate: CVE Impact Through Software/OS
    - advanced: Multi-Facility CVE Impact with CWE/CAPEC Context
    """
    try:
        executor = CVEImpactExecutor(db, cache)
        result = await executor.execute(
            complexity=complexity,
            parameters={"cveId": cveId},
            use_cache=use_cache
        )
        return result
    except Exception as e:
        logger.error(f"CVE impact query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Question 2: Is there an attack path to vulnerability?
# ============================================================================

@app.post("/api/v1/query/attack-path")
async def attack_path_query(
    threatActorName: str,
    vulnerabilityId: str,
    complexity: str = "simple",
    use_cache: bool = True,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_neo4j),
    cache = Depends(get_cache)
):
    """
    Query: Is there an attack path to vulnerability?

    **Complexity Levels:**
    - simple: Direct Attack Path
    - intermediate: Attack Path with Techniques
    - advanced: Complete Attack Chain to Equipment
    """
    try:
        executor = AttackPathExecutor(db, cache)
        result = await executor.execute(
            complexity=complexity,
            parameters={
                "threatActorName": threatActorName,
                "vulnerabilityId": vulnerabilityId,
                "threatActorId": None
            },
            use_cache=use_cache
        )
        return result
    except Exception as e:
        logger.error(f"Attack path query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Question 3: Does new CVE released today impact facility equipment?
# ============================================================================

@app.post("/api/v1/query/cve-facility-impact")
async def cve_facility_impact_query(
    facilityId: Optional[str] = None,
    facilityIds: Optional[list] = None,
    minSeverity: Optional[list] = None,
    today: Optional[str] = None,
    complexity: str = "simple",
    use_cache: bool = True,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_neo4j),
    cache = Depends(get_cache)
):
    """
    Query: Does new CVE released today impact any equipment in my facility?

    **Complexity Levels:**
    - simple: Today's CVEs by Facility
    - intermediate: Today's CVEs with SBOM Component Matching
    - advanced: Multi-Facility Today's CVE Impact with Complete SBOM Analysis
    """
    try:
        executor = TodayCVEImpactExecutor(db, cache)

        params = {
            "facilityId": facilityId,
            "facilityIds": facilityIds,
            "minSeverity": minSeverity,
            "today": today or datetime.utcnow().strftime('%Y-%m-%d')
        }

        result = await executor.execute(
            complexity=complexity,
            parameters=params,
            use_cache=use_cache
        )
        return result
    except Exception as e:
        logger.error(f"CVE facility impact query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Question 4: Pathway for threat actor to vulnerability?
# ============================================================================

@app.post("/api/v1/query/threat-actor-path")
async def threat_actor_pathway_query(
    threatActorName: Optional[str] = None,
    threatActorId: Optional[str] = None,
    vulnerabilityId: Optional[str] = None,
    cveId: Optional[str] = None,
    complexity: str = "simple",
    use_cache: bool = True,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_neo4j),
    cache = Depends(get_cache)
):
    """
    Query: Is there a pathway for a threat actor to get to the vulnerability?

    **Complexity Levels:**
    - simple: Threat Actor to Vulnerability Path Check
    - intermediate: Multi-Path Analysis with Access Requirements
    - advanced: Complete Threat Path with Equipment Access and Defenses
    """
    try:
        executor = ThreatActorPathwayExecutor(db, cache)
        result = await executor.execute(
            complexity=complexity,
            parameters={
                "threatActorName": threatActorName,
                "threatActorId": threatActorId,
                "vulnerabilityId": vulnerabilityId,
                "cveId": cveId
            },
            use_cache=use_cache
        )
        return result
    except Exception as e:
        logger.error(f"Threat actor pathway query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Question 5: For CVE today, pathway for threat actor?
# ============================================================================

@app.post("/api/v1/query/cve-threat-path")
async def cve_threat_path_query(
    today: Optional[str] = None,
    severityFilter: Optional[list] = None,
    minCVSS: Optional[float] = None,
    complexity: str = "simple",
    use_cache: bool = True,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_neo4j),
    cache = Depends(get_cache)
):
    """
    Query: For CVE released today, is there pathway for threat actor?

    **Complexity Levels:**
    - simple: Today's CVE Threat Actor Pathway
    - intermediate: Today's CVEs with Active Threat Actor Campaigns
    - advanced: Today's CVE Complete Threat Landscape Analysis
    """
    try:
        executor = TodayCVEThreatPathExecutor(db, cache)
        result = await executor.execute(
            complexity=complexity,
            parameters={
                "today": today or datetime.utcnow().strftime('%Y-%m-%d'),
                "severityFilter": severityFilter,
                "minCVSS": minCVSS
            },
            use_cache=use_cache
        )
        return result
    except Exception as e:
        logger.error(f"CVE threat path query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Question 6: How many pieces of equipment type?
# ============================================================================

@app.get("/api/v1/query/equipment-count")
async def equipment_count_query(
    equipmentType: Optional[str] = None,
    facilityId: Optional[str] = None,
    criticalityLevel: Optional[str] = None,
    complexity: str = "simple",
    use_cache: bool = True,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_neo4j),
    cache = Depends(get_cache)
):
    """
    Query: How many pieces of a type of equipment do I have?

    **Complexity Levels:**
    - simple: Equipment Count by Type
    - intermediate: Equipment Inventory with Facility Breakdown
    - advanced: Comprehensive Equipment Inventory Analysis
    """
    try:
        executor = EquipmentInventoryExecutor(db, cache)
        result = await executor.execute(
            complexity=complexity,
            parameters={
                "equipmentType": equipmentType,
                "facilityId": facilityId,
                "criticalityLevel": criticalityLevel
            },
            use_cache=use_cache
        )
        return result
    except Exception as e:
        logger.error(f"Equipment count query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Question 7: Do I have specific application or OS?
# ============================================================================

@app.get("/api/v1/query/software-check")
async def software_check_query(
    softwareName: Optional[str] = None,
    version: Optional[str] = None,
    vendor: Optional[str] = None,
    softwareType: Optional[str] = None,
    complexity: str = "simple",
    use_cache: bool = True,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_neo4j),
    cache = Depends(get_cache)
):
    """
    Query: Do I have a specific application or operating system?

    **Complexity Levels:**
    - simple: Check Application/OS Existence
    - intermediate: Application/OS Inventory with Equipment Mapping
    - advanced: Complete Software Asset Inventory with Vulnerabilities
    """
    try:
        executor = SoftwareInventoryExecutor(db, cache)
        result = await executor.execute(
            complexity=complexity,
            parameters={
                "softwareName": softwareName,
                "version": version,
                "vendor": vendor,
                "softwareType": softwareType
            },
            use_cache=use_cache
        )
        return result
    except Exception as e:
        logger.error(f"Software check query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Question 8: Location of application/vulnerability/OS/library?
# ============================================================================

@app.get("/api/v1/query/asset-location")
async def asset_location_query(
    itemName: Optional[str] = None,
    itemId: Optional[str] = None,
    searchTerm: Optional[str] = None,
    version: Optional[str] = None,
    complexity: str = "simple",
    use_cache: bool = True,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_neo4j),
    cache = Depends(get_cache)
):
    """
    Query: Tell me the location (on what asset) is specific item?

    **Complexity Levels:**
    - simple: Find Asset Locations
    - intermediate: Asset Location with Facility Details
    - advanced: Complete Asset Location Mapping with Context
    """
    try:
        executor = AssetLocationExecutor(db, cache)
        result = await executor.execute(
            complexity=complexity,
            parameters={
                "itemName": itemName,
                "itemId": itemId,
                "searchTerm": searchTerm or itemName or itemId,
                "version": version
            },
            use_cache=use_cache
        )
        return result
    except Exception as e:
        logger.error(f"Asset location query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        log_level=settings.log_level.lower()
    )
