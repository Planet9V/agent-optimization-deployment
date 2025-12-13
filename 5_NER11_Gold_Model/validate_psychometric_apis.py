"""
Validation script for Psychometric APIs
Checks implementation completeness without requiring imports
"""

import re
import os
from pathlib import Path

def validate_router_file():
    """Check that the router file exists and has all required endpoints"""
    router_path = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/api/psychometrics/psychometric_router.py")

    if not router_path.exists():
        print("❌ Router file not found")
        return False

    print("✅ Router file exists")

    # Read the file
    with open(router_path, 'r') as f:
        content = f.read()

    # Check for required endpoints
    required_endpoints = [
        (r'@router\.get\("/traits"', "GET /traits"),
        (r'@router\.get\("/traits/\{trait_id\}"', "GET /traits/{trait_id}"),
        (r'@router\.get\("/actors/\{actor_id\}/profile"', "GET /actors/{actor_id}/profile"),
        (r'@router\.get\("/actors/by-trait/\{trait_id\}"', "GET /actors/by-trait/{trait_id}"),
        (r'@router\.get\("/biases"', "GET /biases"),
        (r'@router\.get\("/biases/\{bias_id\}"', "GET /biases/{bias_id}"),
        (r'@router\.get\("/lacanian/registers"', "GET /lacanian/registers"),
        (r'@router\.get\("/dashboard"', "GET /dashboard"),
    ]

    print("\nEndpoint validation:")
    all_found = True
    for pattern, name in required_endpoints:
        if re.search(pattern, content):
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - NOT FOUND")
            all_found = False

    # Check for Pydantic models
    print("\nPydantic model validation:")
    models = ["PsychTrait", "PersonalityTrait", "CognitiveBias", "ActorProfile", "LacanianRegister", "DashboardStats"]
    for model in models:
        if f"class {model}(BaseModel)" in content:
            print(f"  ✅ {model}")
        else:
            print(f"  ❌ {model} - NOT FOUND")
            all_found = False

    # Check for Neo4j integration
    print("\nNeo4j integration:")
    if "get_neo4j_driver" in content:
        print("  ✅ Neo4j driver function defined")
    else:
        print("  ❌ Neo4j driver function - NOT FOUND")
        all_found = False

    if "from app.graph.neo4j_connection import Neo4jConnection" in content:
        print("  ✅ Neo4j connection import")
    else:
        print("  ❌ Neo4j connection import - NOT FOUND")
        all_found = False

    # Count Cypher queries
    cypher_count = content.count('cypher = """')
    print(f"\n  📊 Cypher queries found: {cypher_count}")

    return all_found


def validate_serve_model_registration():
    """Check that the router is registered in serve_model.py"""
    serve_model_path = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/serve_model.py")

    if not serve_model_path.exists():
        print("❌ serve_model.py not found")
        return False

    print("\n✅ serve_model.py exists")

    with open(serve_model_path, 'r') as f:
        content = f.read()

    print("\nRouter registration validation:")
    checks = [
        ("PSYCHOMETRIC_ROUTERS_AVAILABLE", "Feature flag defined"),
        ("from api.psychometrics.psychometric_router import router as psychometric_router", "Router import"),
        ("app.include_router(psychometric_router)", "Router registration"),
    ]

    all_found = True
    for check_str, description in checks:
        if check_str in content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description} - NOT FOUND")
            all_found = False

    return all_found


def check_data_coverage():
    """Document what data the APIs expose"""
    print("\n" + "="*60)
    print("DATA COVERAGE SUMMARY")
    print("="*60)

    data_points = {
        "PsychTrait nodes": "161 (personality traits)",
        "Personality_Trait nodes": "20 (Big Five categories)",
        "Cognitive_Bias nodes": "7 (bias types)",
        "ThreatActor→PsychTrait rels": "1,460 (actor-trait associations)"
    }

    api_mappings = {
        "GET /traits": "Exposes all 161 PsychTrait nodes",
        "GET /traits/{id}": "Individual trait details + associated actors",
        "GET /actors/{id}/profile": "Actor's complete psychological profile",
        "GET /actors/by-trait/{id}": "All actors with specific trait",
        "GET /biases": "Exposes all 7 Cognitive_Bias nodes",
        "GET /biases/{id}": "Individual bias details + examples",
        "GET /lacanian/registers": "Lacanian psychoanalytic framework",
        "GET /dashboard": "Statistical overview of all psychometric data"
    }

    print("\nAvailable data in Neo4j:")
    for item, description in data_points.items():
        print(f"  📊 {item}: {description}")

    print("\nAPI endpoint mappings:")
    for endpoint, mapping in api_mappings.items():
        print(f"  🔗 {endpoint:30} → {mapping}")


def main():
    print("="*60)
    print("PSYCHOMETRIC API VALIDATION")
    print("="*60)

    router_ok = validate_router_file()
    serve_ok = validate_serve_model_registration()
    check_data_coverage()

    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    if router_ok and serve_ok:
        print("✅ ALL CHECKS PASSED")
        print("\nNext steps:")
        print("1. Start the container: docker-compose up -d")
        print("2. Test APIs: curl http://localhost:8000/api/v2/psychometrics/dashboard")
        print("3. Verify data: Check that actual Neo4j data is returned")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        if not router_ok:
            print("  - Router implementation issues")
        if not serve_ok:
            print("  - serve_model.py registration issues")
        return 1


if __name__ == "__main__":
    exit(main())
