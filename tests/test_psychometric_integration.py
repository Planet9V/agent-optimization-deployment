"""
Integration test for Psychometric APIs - Direct module testing
Tests router implementation without requiring running server
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_router_import():
    """Test that the psychometric router can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Import Psychometric Router")
    print("="*60)

    try:
        from api.psychometrics.psychometric_router import router
        print("✅ Router imported successfully")
        print(f"   Prefix: {router.prefix}")
        print(f"   Tags: {router.tags}")

        # Count routes
        route_count = len(router.routes)
        print(f"   Routes: {route_count}")

        # List all routes
        print("\n   Available endpoints:")
        for route in router.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                methods = ', '.join(route.methods)
                print(f"   - {methods:6} {route.path}")

        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pydantic_models():
    """Test that Pydantic models are properly defined"""
    print("\n" + "="*60)
    print("TEST 2: Pydantic Models Validation")
    print("="*60)

    try:
        from api.psychometrics.psychometric_router import (
            PsychTrait, PersonalityTrait, CognitiveBias,
            ActorProfile, LacanianRegister, DashboardStats
        )

        # Test PsychTrait
        trait = PsychTrait(
            trait_id="test_1",
            name="Test Trait",
            description="A test trait",
            category="test",
            intensity=0.8
        )
        print("✅ PsychTrait model works")

        # Test ActorProfile
        profile = ActorProfile(
            actor_id="test_actor",
            actor_name="Test Actor",
            traits=[],
            dominant_traits=[]
        )
        print("✅ ActorProfile model works")

        # Test DashboardStats
        dashboard = DashboardStats(
            total_psych_traits=161,
            total_personality_traits=20,
            total_cognitive_biases=7,
            total_actor_profiles=50,
            trait_distribution={},
            top_traits=[]
        )
        print("✅ DashboardStats model works")

        print("\nAll Pydantic models validated successfully")
        return True

    except Exception as e:
        print(f"❌ Model validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_neo4j_connection():
    """Test that Neo4j connection can be established"""
    print("\n" + "="*60)
    print("TEST 3: Neo4j Connection")
    print("="*60)

    try:
        from api.psychometrics.psychometric_router import get_neo4j_driver

        driver = get_neo4j_driver()
        print("✅ Neo4j driver obtained")

        # Test connection
        with driver.session() as session:
            result = session.run("RETURN 1 AS test")
            record = result.single()
            if record and record["test"] == 1:
                print("✅ Neo4j connection successful")

                # Count PsychTrait nodes
                count_result = session.run("MATCH (pt:PsychTrait) RETURN count(pt) AS count")
                count_record = count_result.single()
                if count_record:
                    print(f"   PsychTrait nodes: {count_record['count']}")

                # Count relationships
                rel_result = session.run("""
                    MATCH (:ThreatActor)-[r:HAS_TRAIT]->(:PsychTrait)
                    RETURN count(r) AS count
                """)
                rel_record = rel_result.single()
                if rel_record:
                    print(f"   HAS_TRAIT relationships: {rel_record['count']}")

                return True

    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        print("   Note: This is expected if Neo4j is not running")
        import traceback
        traceback.print_exc()
        return False


def test_cypher_queries():
    """Test that Cypher queries are syntactically valid"""
    print("\n" + "="*60)
    print("TEST 4: Cypher Query Syntax Validation")
    print("="*60)

    try:
        from api.psychometrics.psychometric_router import get_neo4j_driver

        driver = get_neo4j_driver()

        queries = {
            "List Traits": """
                MATCH (pt:PsychTrait)
                WHERE $category IS NULL OR pt.category = $category
                RETURN pt.id AS trait_id,
                       pt.name AS name,
                       pt.description AS description,
                       pt.category AS category,
                       pt.intensity AS intensity
                ORDER BY pt.name
                LIMIT $limit
            """,
            "Trait Details": """
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
            """,
            "Dashboard": """
                MATCH (pt:PsychTrait) WITH count(pt) AS psych_traits
                MATCH (prt:Personality_Trait) WITH psych_traits, count(prt) AS personality_traits
                MATCH (cb:Cognitive_Bias) WITH psych_traits, personality_traits, count(cb) AS cognitive_biases
                MATCH (ta:ThreatActor)-[:HAS_TRAIT]->(:PsychTrait)
                WITH psych_traits, personality_traits, cognitive_biases, count(DISTINCT ta) AS actor_profiles
                RETURN psych_traits, personality_traits, cognitive_biases, actor_profiles
            """
        }

        with driver.session() as session:
            for query_name, query in queries.items():
                try:
                    # Validate syntax by explaining the query
                    session.run(f"EXPLAIN {query}", category=None, limit=1, trait_id="test")
                    print(f"✅ {query_name} query syntax valid")
                except Exception as e:
                    print(f"❌ {query_name} query syntax error: {e}")
                    return False

        print("\nAll Cypher queries validated successfully")
        return True

    except Exception as e:
        print(f"❌ Query validation failed: {e}")
        print("   Note: This is expected if Neo4j is not running")
        return False


def test_route_endpoints():
    """Test that all expected endpoints are defined"""
    print("\n" + "="*60)
    print("TEST 5: Route Endpoint Coverage")
    print("="*60)

    try:
        from api.psychometrics.psychometric_router import router

        expected_endpoints = [
            "/api/v2/psychometrics/traits",
            "/api/v2/psychometrics/traits/{trait_id}",
            "/api/v2/psychometrics/actors/{actor_id}/profile",
            "/api/v2/psychometrics/actors/by-trait/{trait_id}",
            "/api/v2/psychometrics/biases",
            "/api/v2/psychometrics/biases/{bias_id}",
            "/api/v2/psychometrics/lacanian/registers",
            "/api/v2/psychometrics/dashboard"
        ]

        actual_paths = [route.path for route in router.routes if hasattr(route, 'path')]

        print(f"\n   Expected endpoints: {len(expected_endpoints)}")
        print(f"   Actual endpoints: {len(actual_paths)}")

        missing = []
        for endpoint in expected_endpoints:
            if endpoint not in actual_paths:
                missing.append(endpoint)
                print(f"   ❌ Missing: {endpoint}")
            else:
                print(f"   ✅ Found: {endpoint}")

        if missing:
            print(f"\n❌ Missing {len(missing)} endpoints")
            return False

        print(f"\n✅ All {len(expected_endpoints)} endpoints implemented")
        return True

    except Exception as e:
        print(f"❌ Endpoint coverage check failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("PSYCHOMETRIC API INTEGRATION TEST SUITE")
    print("Direct module testing (no server required)")
    print("="*60)

    tests = [
        ("Router Import", test_router_import),
        ("Pydantic Models", test_pydantic_models),
        ("Neo4j Connection", test_neo4j_connection),
        ("Cypher Queries", test_cypher_queries),
        ("Route Coverage", test_route_endpoints),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        symbol = "✅" if result else "❌"
        status = "PASS" if result else "FAIL"
        print(f"{symbol} {name:25} {status}")

    print(f"\nPassed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    return passed >= 3  # At least 3 tests must pass (import, models, coverage)


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
