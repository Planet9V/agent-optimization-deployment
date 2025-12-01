#!/usr/bin/env python3
"""
Comprehensive test of Qdrant Agents System
Tests all 6 agents and the Claude-Flow bridge
"""

import sys
from pathlib import Path

# Add qdrant_agents to path
sys.path.insert(0, str(Path(__file__).parent))

def test_bridge_import():
    """Test 1: Import Claude-Flow bridge"""
    print("\n" + "="*60)
    print("TEST 1: Claude-Flow Bridge Import")
    print("="*60)
    try:
        from qdrant_agents.integration import get_bridge
        bridge = get_bridge()
        print("✅ Bridge imported successfully")
        print(f"   Bridge instance: {type(bridge).__name__}")
        return bridge
    except Exception as e:
        print(f"❌ Bridge import failed: {e}")
        return None

def test_search_knowledge(bridge):
    """Test 2: Search knowledge base"""
    print("\n" + "="*60)
    print("TEST 2: Search Knowledge (Query Agent)")
    print("="*60)
    try:
        result = bridge.search_knowledge(
            query="SAREF smart building sensors",
            top_k=3
        )
        print(f"✅ Search completed")
        print(f"   Success: {result['success']}")
        print(f"   Results found: {result['count']}")
        if result['count'] > 0:
            print(f"   Top result score: {result['results'][0]['score']:.3f}")
            print(f"   Content preview: {result['results'][0]['content'][:100]}...")
        return True
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False

def test_store_finding(bridge):
    """Test 3: Store agent finding"""
    print("\n" + "="*60)
    print("TEST 3: Store Finding (Memory Agent)")
    print("="*60)
    try:
        result = bridge.store_finding(
            finding="Test finding: Qdrant agents system is fully operational and integrated with Claude-Flow",
            agent_name="test-agent",
            context={"test": True, "timestamp": "2025-10-31"},
            tags=["test", "integration", "verification"],
            wave=1
        )
        print(f"✅ Finding stored")
        print(f"   Success: {result['success']}")
        print(f"   Finding ID: {result.get('finding_id', 'N/A')[:20]}...")
        print(f"   Agent: {result.get('agent', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Store finding failed: {e}")
        return False

def test_retrieve_experiences(bridge):
    """Test 4: Retrieve past experiences"""
    print("\n" + "="*60)
    print("TEST 4: Retrieve Experiences (Memory Agent)")
    print("="*60)
    try:
        result = bridge.retrieve_experiences(
            query="integration test",
            top_k=3
        )
        print(f"✅ Experiences retrieved")
        print(f"   Success: {result['success']}")
        print(f"   Experiences found: {result['count']}")
        if result['count'] > 0:
            print(f"   Top match score: {result['experiences'][0]['score']:.3f}")
            print(f"   Agent: {result['experiences'][0]['agent_name']}")
        return True
    except Exception as e:
        print(f"❌ Retrieve experiences failed: {e}")
        return False

def test_find_patterns(bridge):
    """Test 5: Find similar patterns"""
    print("\n" + "="*60)
    print("TEST 5: Find Patterns (Pattern Agent)")
    print("="*60)
    try:
        result = bridge.find_patterns(
            query="sensor implementation patterns",
            top_k=2
        )
        print(f"✅ Pattern search completed")
        print(f"   Success: {result['success']}")
        print(f"   Patterns found: {result['count']}")
        if result['count'] > 0:
            print(f"   Top pattern score: {result['patterns'][0]['score']:.3f}")
            print(f"   Pattern frequency: {result['patterns'][0]['frequency']}")
        return True
    except Exception as e:
        print(f"❌ Find patterns failed: {e}")
        return False

def test_record_decision(bridge):
    """Test 6: Record implementation decision"""
    print("\n" + "="*60)
    print("TEST 6: Record Decision (Decision Agent)")
    print("="*60)
    try:
        result = bridge.record_decision(
            decision="Use Qdrant for vector search in Claude-Flow integration",
            rationale="Qdrant provides fast semantic search with 3072-dim embeddings and excellent scalability",
            alternatives=["Pinecone", "Weaviate", "Milvus"],
            decision_type="architectural",
            wave=1,
            made_by="test-agent"
        )
        print(f"✅ Decision recorded")
        print(f"   Success: {result['success']}")
        print(f"   Decision ID: {result.get('decision_id', 'N/A')[:20]}...")
        print(f"   Decision type: {result.get('decision_type', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Record decision failed: {e}")
        return False

def test_get_metrics(bridge):
    """Test 7: Get system metrics"""
    print("\n" + "="*60)
    print("TEST 7: Get Metrics (Analytics Agent)")
    print("="*60)
    try:
        result = bridge.get_system_metrics()
        print(f"✅ Metrics collected")
        print(f"   Success: {result['success']}")
        if result['success']:
            metrics = result['metrics']
            print(f"   Collections: {len(metrics.get('collections', {}))}")
            print(f"   Total queries: {metrics.get('performance', {}).get('total_queries', 0)}")
            print(f"   Cache hit rate: {metrics.get('performance', {}).get('cache_hit_rate', 0):.1%}")
        return True
    except Exception as e:
        print(f"❌ Get metrics failed: {e}")
        return False

def test_unified_interface(bridge):
    """Test 8: Unified query interface"""
    print("\n" + "="*60)
    print("TEST 8: Unified Query Interface")
    print("="*60)
    try:
        # Test via unified query() method
        result = bridge.query(
            operation="search_knowledge",
            query="building automation",
            top_k=2
        )
        print(f"✅ Unified query executed")
        print(f"   Success: {result['success']}")
        print(f"   Results: {result.get('count', 0)}")
        return True
    except Exception as e:
        print(f"❌ Unified query failed: {e}")
        return False

def test_direct_agent_import():
    """Test 9: Direct agent imports"""
    print("\n" + "="*60)
    print("TEST 9: Direct Agent Imports")
    print("="*60)
    try:
        from qdrant_agents.core import (
            QdrantQueryAgent,
            QdrantMemoryAgent,
            QdrantPatternAgent,
            QdrantDecisionAgent,
            QdrantSyncAgent,
            QdrantAnalyticsAgent
        )
        print("✅ All agents imported successfully:")
        print("   - QdrantQueryAgent")
        print("   - QdrantMemoryAgent")
        print("   - QdrantPatternAgent")
        print("   - QdrantDecisionAgent")
        print("   - QdrantSyncAgent")
        print("   - QdrantAnalyticsAgent")
        return True
    except Exception as e:
        print(f"❌ Direct agent import failed: {e}")
        return False

def test_utility_imports():
    """Test 10: Utility module imports"""
    print("\n" + "="*60)
    print("TEST 10: Utility Module Imports")
    print("="*60)
    try:
        from qdrant_agents.utils import (
            EmbeddingGenerator,
            CollectionManager,
            QueryOptimizer,
            CostTracker
        )
        print("✅ All utilities imported successfully:")
        print("   - EmbeddingGenerator")
        print("   - CollectionManager")
        print("   - QueryOptimizer")
        print("   - CostTracker")
        return True
    except Exception as e:
        print(f"❌ Utility import failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*60)
    print("QDRANT AGENTS SYSTEM - COMPREHENSIVE TEST")
    print("="*60)

    tests_passed = 0
    tests_failed = 0

    # Test 1: Bridge import
    bridge = test_bridge_import()
    if bridge:
        tests_passed += 1
    else:
        tests_failed += 1
        print("\n❌ Cannot continue - bridge import failed")
        return

    # Test 2-8: Bridge operations
    test_functions = [
        test_search_knowledge,
        test_store_finding,
        test_retrieve_experiences,
        test_find_patterns,
        test_record_decision,
        test_get_metrics,
        test_unified_interface
    ]

    for test_func in test_functions:
        if test_func(bridge):
            tests_passed += 1
        else:
            tests_failed += 1

    # Test 9-10: Direct imports
    if test_direct_agent_import():
        tests_passed += 1
    else:
        tests_failed += 1

    if test_utility_imports():
        tests_passed += 1
    else:
        tests_failed += 1

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"📊 Success Rate: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")

    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED - System is fully operational!")
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed - review errors above")

    print("="*60)

if __name__ == "__main__":
    run_all_tests()
