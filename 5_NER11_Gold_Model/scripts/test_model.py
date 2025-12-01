#!/usr/bin/env python3
"""
NER11 Gold Standard - Model Testing Script

Tests model loading, entity extraction, and performance.
"""

import spacy
import time
from pathlib import Path

def test_model_loading():
    """Test 1: Model Loading"""
    print("\n" + "="*50)
    print("Test 1: Model Loading")
    print("="*50)
    
    try:
        nlp = spacy.load("./models/model-best")
        print(f"✓ Model loaded successfully")
        print(f"  Pipeline: {nlp.pipe_names}")
        print(f"  Entity types: {len(nlp.get_pipe('ner').labels)}")
        return nlp
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        return None

def test_entity_extraction(nlp):
    """Test 2: Entity Extraction"""
    print("\n" + "="*50)
    print("Test 2: Entity Extraction")
    print("="*50)
    
    test_text = """
    The APT29 threat actor exploited CVE-2023-12345, a zero-day vulnerability 
    in the Siemens S7-1200 PLC. The attack targeted critical infrastructure 
    in the energy sector using custom malware. The SCADA system was compromised 
    through a spear-phishing campaign that exhibited high levels of social 
    engineering sophistication.
    """
    
    doc = nlp(test_text)
    
    print(f"\nExtracted {len(doc.ents)} entities:\n")
    for ent in doc.ents:
        print(f"  {ent.text:30} → {ent.label_}")
    
    # Expected entities
    expected_types = {
        "THREAT_ACTOR", "VULNERABILITY", "OT_DEVICE", 
        "MALWARE", "SCADA_SYSTEM", "ATTACK_VECTOR"
    }
    
    found_types = {ent.label_ for ent in doc.ents}
    
    if expected_types.intersection(found_types):
        print(f"\n✓ Entity extraction working correctly")
        return True
    else:
        print(f"\n✗ Expected entity types not found")
        return False

def test_performance(nlp):
    """Test 3: Performance Benchmark"""
    print("\n" + "="*50)
    print("Test 3: Performance Benchmark")
    print("="*50)
    
    # Sample texts
    texts = [
        "APT29 exploited CVE-2023-12345 in the SCADA system.",
        "The malware targeted critical infrastructure using zero-day vulnerabilities.",
        "Social engineering attacks increased by 45% in Q3 2025.",
    ] * 10  # 30 texts total
    
    start_time = time.time()
    docs = list(nlp.pipe(texts))
    end_time = time.time()
    
    duration = end_time - start_time
    docs_per_sec = len(texts) / duration
    
    print(f"\n  Processed: {len(texts)} documents")
    print(f"  Duration: {duration:.2f} seconds")
    print(f"  Speed: {docs_per_sec:.1f} docs/second")
    
    if docs_per_sec > 10:
        print(f"\n✓ Performance acceptable")
        return True
    else:
        print(f"\n⚠ Performance below expected (>10 docs/sec)")
        return False

def test_gpu_support(nlp):
    """Test 4: GPU Support"""
    print("\n" + "="*50)
    print("Test 4: GPU Support")
    print("="*50)
    
    import torch
    
    cuda_available = torch.cuda.is_available()
    print(f"\n  CUDA available: {cuda_available}")
    
    if cuda_available:
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA version: {torch.version.cuda}")
        print(f"\n✓ GPU support enabled")
    else:
        print(f"\n⚠ GPU not available (using CPU)")
    
    return cuda_available

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" "*20 + "NER11 Gold Standard - Model Tests")
    print("="*70)
    
    # Test 1: Model Loading
    nlp = test_model_loading()
    if not nlp:
        print("\n✗ Tests failed: Cannot load model")
        return
    
    # Test 2: Entity Extraction
    extraction_ok = test_entity_extraction(nlp)
    
    # Test 3: Performance
    performance_ok = test_performance(nlp)
    
    # Test 4: GPU Support
    gpu_ok = test_gpu_support(nlp)
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"  Model Loading: ✓")
    print(f"  Entity Extraction: {'✓' if extraction_ok else '✗'}")
    print(f"  Performance: {'✓' if performance_ok else '⚠'}")
    print(f"  GPU Support: {'✓' if gpu_ok else '⚠'}")
    print("="*70)
    
    if extraction_ok and performance_ok:
        print("\n✅ All critical tests passed!")
        print("\nNext steps:")
        print("  - Review examples/ directory for usage patterns")
        print("  - See docs/03_INTEGRATION_GUIDE.md for integration")
        print("  - Check docs/04_NEO4J_INTEGRATION.md for graph setup")
    else:
        print("\n⚠ Some tests failed. Please review output above.")

if __name__ == "__main__":
    main()
