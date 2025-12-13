"""
Psychometric API Router - Expose personality traits, cognitive biases, and Lacanian framework data
Built for OXOT Threat Intelligence Platform

Available Data:
- 161 PsychTrait nodes
- 20 Personality_Trait nodes
- 7 Cognitive_Bias nodes
- 1,460 ThreatActor→PsychTrait relationships
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

# Pydantic Models
class PsychTrait(BaseModel):
    trait_id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    intensity: Optional[float] = None

class PersonalityTrait(BaseModel):
    trait_id: str
    name: str
    description: Optional[str] = None
    big_five_category: Optional[str] = None

class CognitiveBias(BaseModel):
    bias_id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None

class ActorProfile(BaseModel):
    actor_id: str
    actor_name: str
    traits: List[Dict[str, Any]]
    personality_summary: Optional[str] = None
    dominant_traits: List[str]

class LacanianRegister(BaseModel):
    register_type: str
    description: str
    traits: List[str]
    count: int

class DashboardStats(BaseModel):
    total_psych_traits: int
    total_personality_traits: int
    total_cognitive_biases: int
    total_actor_profiles: int
    trait_distribution: Dict[str, int]
    top_traits: List[Dict[str, Any]]

# Initialize router
router = APIRouter(
    prefix="/api/v2/psychometrics",
    tags=["psychometrics"],
    responses={404: {"description": "Not found"}},
)

def get_neo4j_driver():
    """Get Neo4j driver instance"""
    from api.customer_isolation.neo4j_client import Neo4jConnection
    return Neo4jConnection.get_driver()

# API Endpoints

@router.get("/traits", response_model=List[PsychTrait])
async def list_traits(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of results")
):
    """
    List all psychological traits

    Returns all PsychTrait nodes with optional filtering
    """
    try:
        driver = get_neo4j_driver()

        cypher = """
        MATCH (pt:PsychTrait)
        WHERE $category IS NULL OR pt.category = $category
        RETURN pt.id AS trait_id,
               pt.name AS name,
               pt.description AS description,
               pt.category AS category,
               pt.intensity AS intensity
        ORDER BY pt.name
        LIMIT $limit
        """

        with driver.session() as session:
            result = session.run(cypher, category=category, limit=limit)
            traits = [
                PsychTrait(
                    trait_id=record["trait_id"] or f"trait_{idx}",
                    name=record["name"],
                    description=record["description"],
                    category=record["category"],
                    intensity=record["intensity"]
                )
                for idx, record in enumerate(result)
            ]

        logger.info(f"Retrieved {len(traits)} psychological traits")
        return traits

    except Exception as e:
        logger.error(f"Error retrieving traits: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/traits/{trait_id}", response_model=Dict[str, Any])
async def get_trait_details(trait_id: str):
    """
    Get detailed information about a specific trait

    Includes related actors and trait relationships
    """
    try:
        driver = get_neo4j_driver()

        cypher = """
        MATCH (pt:PsychTrait)
        WHERE pt.id = $trait_id OR pt.name = $trait_id
        OPTIONAL MATCH (ta:ThreatActor)-[r:HAS_TRAIT]->(pt)
        RETURN pt.id AS trait_id,
               pt.name AS name,
               pt.description AS description,
               pt.category AS category,
               pt.intensity AS intensity,
               collect(DISTINCT {
                   actor_id: ta.id,
                   actor_name: ta.name,
                   relationship_type: type(r)
               }) AS actors
        """

        with driver.session() as session:
            result = session.run(cypher, trait_id=trait_id)
            record = result.single()

            if not record:
                raise HTTPException(status_code=404, detail=f"Trait {trait_id} not found")

            trait_details = {
                "trait_id": record["trait_id"] or trait_id,
                "name": record["name"],
                "description": record["description"],
                "category": record["category"],
                "intensity": record["intensity"],
                "actors": [a for a in record["actors"] if a["actor_id"]],
                "actor_count": len([a for a in record["actors"] if a["actor_id"]])
            }

        logger.info(f"Retrieved details for trait: {trait_id}")
        return trait_details

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving trait details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/actors/{actor_id}/profile", response_model=ActorProfile)
async def get_actor_profile(actor_id: str):
    """
    Get psychological profile for a threat actor

    Returns all traits associated with the actor
    """
    try:
        driver = get_neo4j_driver()

        cypher = """
        MATCH (ta:ThreatActor)
        WHERE ta.id = $actor_id OR ta.name = $actor_id
        OPTIONAL MATCH (ta)-[r:HAS_TRAIT]->(pt:PsychTrait)
        RETURN ta.id AS actor_id,
               ta.name AS actor_name,
               collect({
                   trait_id: pt.id,
                   trait_name: pt.name,
                   category: pt.category,
                   intensity: pt.intensity,
                   description: pt.description
               }) AS traits
        """

        with driver.session() as session:
            result = session.run(cypher, actor_id=actor_id)
            record = result.single()

            if not record:
                raise HTTPException(status_code=404, detail=f"Actor {actor_id} not found")

            traits = [t for t in record["traits"] if t["trait_id"]]

            # Extract dominant traits (highest intensity)
            dominant = sorted(
                [t for t in traits if t.get("intensity")],
                key=lambda x: x["intensity"],
                reverse=True
            )[:5]

            profile = ActorProfile(
                actor_id=record["actor_id"] or actor_id,
                actor_name=record["actor_name"],
                traits=traits,
                personality_summary=f"Profile based on {len(traits)} traits",
                dominant_traits=[t["trait_name"] for t in dominant]
            )

        logger.info(f"Retrieved profile for actor: {actor_id}")
        return profile

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving actor profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/actors/by-trait/{trait_id}", response_model=List[Dict[str, Any]])
async def get_actors_by_trait(
    trait_id: str,
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results")
):
    """
    Get all actors exhibiting a specific trait

    Returns threat actors associated with the given trait
    """
    try:
        driver = get_neo4j_driver()

        cypher = """
        MATCH (pt:PsychTrait)<-[r:HAS_TRAIT]-(ta:ThreatActor)
        WHERE pt.id = $trait_id OR pt.name = $trait_id
        RETURN ta.id AS actor_id,
               ta.name AS actor_name,
               ta.description AS description,
               pt.name AS trait_name,
               pt.intensity AS trait_intensity
        ORDER BY trait_intensity DESC
        LIMIT $limit
        """

        with driver.session() as session:
            result = session.run(cypher, trait_id=trait_id, limit=limit)
            actors = [
                {
                    "actor_id": record["actor_id"],
                    "actor_name": record["actor_name"],
                    "description": record["description"],
                    "trait_name": record["trait_name"],
                    "trait_intensity": record["trait_intensity"]
                }
                for record in result
            ]

        if not actors:
            raise HTTPException(status_code=404, detail=f"No actors found with trait {trait_id}")

        logger.info(f"Retrieved {len(actors)} actors with trait: {trait_id}")
        return actors

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving actors by trait: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/biases", response_model=List[CognitiveBias])
async def list_biases(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of results")
):
    """
    List all cognitive biases

    Returns all Cognitive_Bias nodes with optional filtering
    """
    try:
        driver = get_neo4j_driver()

        cypher = """
        MATCH (cb:Cognitive_Bias)
        WHERE $category IS NULL OR cb.category = $category
        RETURN cb.id AS bias_id,
               cb.name AS name,
               cb.description AS description,
               cb.category AS category,
               cb.severity AS severity
        ORDER BY cb.name
        LIMIT $limit
        """

        with driver.session() as session:
            result = session.run(cypher, category=category, limit=limit)
            biases = [
                CognitiveBias(
                    bias_id=record["bias_id"] or f"bias_{idx}",
                    name=record["name"],
                    description=record["description"],
                    category=record["category"],
                    severity=record["severity"]
                )
                for idx, record in enumerate(result)
            ]

        logger.info(f"Retrieved {len(biases)} cognitive biases")
        return biases

    except Exception as e:
        logger.error(f"Error retrieving biases: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/biases/{bias_id}", response_model=Dict[str, Any])
async def get_bias_details(bias_id: str):
    """
    Get detailed information about a specific cognitive bias

    Includes related actors and examples
    """
    try:
        driver = get_neo4j_driver()

        cypher = """
        MATCH (cb:Cognitive_Bias)
        WHERE cb.id = $bias_id OR cb.name = $bias_id
        OPTIONAL MATCH (ta:ThreatActor)-[r]->(cb)
        RETURN cb.id AS bias_id,
               cb.name AS name,
               cb.description AS description,
               cb.category AS category,
               cb.severity AS severity,
               collect(DISTINCT {
                   actor_id: ta.id,
                   actor_name: ta.name
               }) AS actors
        """

        with driver.session() as session:
            result = session.run(cypher, bias_id=bias_id)
            record = result.single()

            if not record:
                raise HTTPException(status_code=404, detail=f"Bias {bias_id} not found")

            bias_details = {
                "bias_id": record["bias_id"] or bias_id,
                "name": record["name"],
                "description": record["description"],
                "category": record["category"],
                "severity": record["severity"],
                "actors": [a for a in record["actors"] if a["actor_id"]],
                "actor_count": len([a for a in record["actors"] if a["actor_id"]])
            }

        logger.info(f"Retrieved details for bias: {bias_id}")
        return bias_details

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving bias details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lacanian/registers", response_model=List[LacanianRegister])
async def get_lacanian_registers():
    """
    Get Lacanian psychoanalytic framework registers

    Returns the three registers: Real, Imaginary, Symbolic with associated traits
    """
    try:
        driver = get_neo4j_driver()

        # Query for traits grouped by Lacanian register
        cypher = """
        MATCH (pt:PsychTrait)
        WHERE pt.lacanian_register IS NOT NULL
        WITH pt.lacanian_register AS register, collect(pt.name) AS traits
        RETURN register, traits, size(traits) AS count
        ORDER BY register
        """

        with driver.session() as session:
            result = session.run(cypher)
            registers = []

            for record in result:
                register_type = record["register"]
                registers.append(LacanianRegister(
                    register_type=register_type,
                    description=get_lacanian_description(register_type),
                    traits=record["traits"],
                    count=record["count"]
                ))

            # If no data, return theoretical framework
            if not registers:
                registers = [
                    LacanianRegister(
                        register_type="Real",
                        description="The traumatic, impossible-to-symbolize dimension of experience",
                        traits=["anxiety", "trauma", "jouissance"],
                        count=0
                    ),
                    LacanianRegister(
                        register_type="Imaginary",
                        description="The realm of images, identification, and the ego",
                        traits=["narcissism", "rivalry", "identification"],
                        count=0
                    ),
                    LacanianRegister(
                        register_type="Symbolic",
                        description="The domain of language, law, and the social order",
                        traits=["authority", "language", "social_norms"],
                        count=0
                    )
                ]

        logger.info(f"Retrieved {len(registers)} Lacanian registers")
        return registers

    except Exception as e:
        logger.error(f"Error retrieving Lacanian registers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard():
    """
    Get psychometric dashboard statistics

    Returns comprehensive overview of all psychometric data
    """
    try:
        driver = get_neo4j_driver()

        cypher = """
        // Count all node types
        MATCH (pt:PsychTrait) WITH count(pt) AS psych_traits
        MATCH (prt:Personality_Trait) WITH psych_traits, count(prt) AS personality_traits
        MATCH (cb:Cognitive_Bias) WITH psych_traits, personality_traits, count(cb) AS cognitive_biases
        MATCH (ta:ThreatActor)-[:HAS_TRAIT]->(:PsychTrait)
        WITH psych_traits, personality_traits, cognitive_biases, count(DISTINCT ta) AS actor_profiles

        // Get trait distribution
        MATCH (pt:PsychTrait)
        WITH psych_traits, personality_traits, cognitive_biases, actor_profiles,
             pt.category AS category, count(pt) AS count
        WHERE category IS NOT NULL

        // Get top traits by actor count
        MATCH (pt:PsychTrait)<-[:HAS_TRAIT]-(ta:ThreatActor)
        WITH psych_traits, personality_traits, cognitive_biases, actor_profiles,
             collect({category: category, count: count}) AS distribution,
             pt.name AS trait_name, count(ta) AS actor_count
        ORDER BY actor_count DESC
        LIMIT 10

        RETURN psych_traits, personality_traits, cognitive_biases, actor_profiles,
               distribution,
               collect({trait: trait_name, actors: actor_count}) AS top_traits
        """

        with driver.session() as session:
            result = session.run(cypher)
            record = result.single()

            if not record:
                # Return empty dashboard
                return DashboardStats(
                    total_psych_traits=0,
                    total_personality_traits=0,
                    total_cognitive_biases=0,
                    total_actor_profiles=0,
                    trait_distribution={},
                    top_traits=[]
                )

            # Convert distribution list to dict
            distribution_dict = {
                item["category"]: item["count"]
                for item in record["distribution"]
            }

            dashboard = DashboardStats(
                total_psych_traits=record["psych_traits"],
                total_personality_traits=record["personality_traits"],
                total_cognitive_biases=record["cognitive_biases"],
                total_actor_profiles=record["actor_profiles"],
                trait_distribution=distribution_dict,
                top_traits=record["top_traits"]
            )

        logger.info("Retrieved dashboard statistics")
        return dashboard

    except Exception as e:
        logger.error(f"Error retrieving dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_lacanian_description(register_type: str) -> str:
    """Get description for Lacanian register"""
    descriptions = {
        "Real": "The traumatic, impossible-to-symbolize dimension of experience - what resists symbolization",
        "Imaginary": "The realm of images, identification, and the ego - the domain of mirror-stage identification",
        "Symbolic": "The domain of language, law, and the social order - the structure that governs desire"
    }
    return descriptions.get(register_type, "Unknown register")
