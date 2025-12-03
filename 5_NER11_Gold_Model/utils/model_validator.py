"""
Model Validation Module for NER11 Gold Model
=============================================

Ensures model integrity and correct loading at startup and runtime.
Uses Claude-Flow memory and Qdrant for persistent registry.

Features:
1. Checksum verification for model files
2. Entity extraction validation tests
3. Single source of truth from registry
4. Integration with Claude-Flow memory
5. Health check API support

Version: 1.0.0
Author: AEON Architecture Team
"""

import hashlib
import json
import logging
import os
import sys
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Registry Configuration
QDRANT_HOST = os.environ.get('QDRANT_HOST', 'localhost')
QDRANT_PORT = int(os.environ.get('QDRANT_PORT', 6333))
QDRANT_COLLECTION = 'ner11_model_registry'

CLAUDE_FLOW_MEMORY_NAMESPACE = 'ner11_model_registry'

# Production Model Configuration
PRODUCTION_MODEL_ID = 'ner11_v3'
MODEL_BASE_PATH = Path(__file__).parent.parent / 'models'

# Expected checksums (from registry)
EXPECTED_CHECKSUMS = {
    'ner11_v3': {
        'meta_json': '0710e14d78a87d54866208cc6a5c8de3',
        'ner_model': 'f326672a81a00c54be06422aae07ecf1'
    }
}


@dataclass
class ValidationResult:
    """Result of model validation."""
    model_id: str
    passed: bool
    checksum_valid: bool
    entity_tests_passed: int
    entity_tests_total: int
    errors: List[str]
    validated_at: str


@dataclass
class TestCase:
    """Entity extraction test case."""
    id: str
    input: str
    expected_label: str
    confidence_min: float = 0.8
    method: str = 'pattern'  # 'pattern' or 'model'


# Critical validation tests (must all pass)
CRITICAL_TESTS = [
    TestCase('T001', 'APT29', 'APT_GROUP', 0.9, 'pattern'),
    TestCase('T002', 'CVE-2024-12345', 'CVE', 1.0, 'pattern'),
    TestCase('T003', 'T1566.001', 'TECHNIQUE', 1.0, 'pattern'),
    TestCase('T004', 'CWE-79', 'CWE', 1.0, 'pattern'),
    TestCase('T005', 'Cobalt Strike', 'MALWARE', 0.9, 'pattern'),
    TestCase('T006', 'TA0001', 'TACTIC', 1.0, 'pattern'),
    TestCase('T007', 'IEC 62443-3-3', 'IEC_62443', 0.85, 'pattern'),
    TestCase('T008', 'TID-001', 'MITRE_EM3D', 1.0, 'pattern'),
]


def compute_file_checksum(filepath: Path) -> str:
    """Compute MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        return ''


def verify_model_checksums(model_id: str, model_path: Path) -> Tuple[bool, List[str]]:
    """
    Verify model file checksums against expected values.

    Args:
        model_id: Model identifier (e.g., 'ner11_v3')
        model_path: Path to model directory

    Returns:
        Tuple of (passed, list of error messages)
    """
    errors = []
    expected = EXPECTED_CHECKSUMS.get(model_id)

    if not expected:
        errors.append(f"No expected checksums for model {model_id}")
        return False, errors

    # Check meta.json
    meta_path = model_path / 'meta.json'
    if meta_path.exists():
        actual_meta = compute_file_checksum(meta_path)
        if actual_meta != expected.get('meta_json'):
            errors.append(
                f"meta.json checksum mismatch: expected {expected['meta_json']}, got {actual_meta}"
            )
    else:
        errors.append(f"meta.json not found at {meta_path}")

    # Check ner/model
    ner_model_path = model_path / 'ner' / 'model'
    if ner_model_path.exists():
        actual_ner = compute_file_checksum(ner_model_path)
        if actual_ner != expected.get('ner_model'):
            errors.append(
                f"ner/model checksum mismatch: expected {expected['ner_model']}, got {actual_ner}"
            )
    else:
        errors.append(f"ner/model not found at {ner_model_path}")

    return len(errors) == 0, errors


def run_entity_tests(api_url: str = 'http://localhost:8000') -> Tuple[int, int, List[str]]:
    """
    Run entity extraction validation tests against the API.

    Args:
        api_url: Base URL of the NER API

    Returns:
        Tuple of (passed_count, total_count, error_messages)
    """
    passed = 0
    errors = []

    for test in CRITICAL_TESTS:
        try:
            response = requests.post(
                f"{api_url}/ner",
                json={"text": test.input},
                timeout=10
            )

            if response.status_code != 200:
                errors.append(f"{test.id}: API returned status {response.status_code}")
                continue

            result = response.json()
            entities = result.get('entities', [])

            # Check if expected label was found
            found = False
            for ent in entities:
                if ent.get('label') == test.expected_label:
                    # API returns 'score' field, not 'confidence'
                    confidence = ent.get('score', ent.get('confidence', 0))
                    if confidence >= test.confidence_min:
                        found = True
                        break
                    else:
                        errors.append(
                            f"{test.id}: {test.input} -> {test.expected_label} found but "
                            f"score {confidence} < {test.confidence_min}"
                        )

            if found:
                passed += 1
                logger.info(f"✅ {test.id}: {test.input} -> {test.expected_label}")
            else:
                labels = [e.get('label') for e in entities]
                errors.append(
                    f"{test.id}: {test.input} expected {test.expected_label}, got {labels}"
                )
                logger.error(f"❌ {test.id}: {test.input} -> expected {test.expected_label}, got {labels}")

        except requests.exceptions.RequestException as e:
            errors.append(f"{test.id}: Request failed - {str(e)}")
            logger.error(f"❌ {test.id}: Request failed - {str(e)}")

    return passed, len(CRITICAL_TESTS), errors


def validate_model_at_startup(
    model_id: str = PRODUCTION_MODEL_ID,
    api_url: str = 'http://localhost:8000',
    require_checksum: bool = True,
    require_tests: bool = True
) -> ValidationResult:
    """
    Complete model validation at startup.

    Args:
        model_id: Model to validate
        api_url: NER API URL
        require_checksum: Fail if checksum verification fails
        require_tests: Fail if entity tests fail

    Returns:
        ValidationResult with details
    """
    all_errors = []
    checksum_valid = True
    tests_passed = 0
    tests_total = 0

    # Step 1: Checksum verification
    model_path = MODEL_BASE_PATH / model_id / 'model-best'
    if model_path.exists():
        checksum_valid, checksum_errors = verify_model_checksums(model_id, model_path)
        all_errors.extend(checksum_errors)

        if checksum_valid:
            logger.info(f"✅ Checksum verification passed for {model_id}")
        else:
            logger.warning(f"⚠️ Checksum verification failed for {model_id}")
    else:
        all_errors.append(f"Model path not found: {model_path}")
        checksum_valid = False
        logger.error(f"❌ Model path not found: {model_path}")

    # Step 2: Entity extraction tests
    try:
        tests_passed, tests_total, test_errors = run_entity_tests(api_url)
        all_errors.extend(test_errors)

        if tests_passed == tests_total:
            logger.info(f"✅ All {tests_total} entity tests passed")
        else:
            logger.warning(f"⚠️ {tests_passed}/{tests_total} entity tests passed")
    except Exception as e:
        all_errors.append(f"Entity test execution failed: {str(e)}")
        logger.error(f"❌ Entity test execution failed: {str(e)}")

    # Determine overall pass/fail
    passed = True
    if require_checksum and not checksum_valid:
        passed = False
    if require_tests and tests_passed < tests_total:
        passed = False

    result = ValidationResult(
        model_id=model_id,
        passed=passed,
        checksum_valid=checksum_valid,
        entity_tests_passed=tests_passed,
        entity_tests_total=tests_total,
        errors=all_errors,
        validated_at=datetime.utcnow().isoformat()
    )

    return result


def store_validation_result_qdrant(result: ValidationResult) -> bool:
    """Store validation result in Qdrant for history tracking."""
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer('all-MiniLM-L6-v2')
        desc = f"Validation result for {result.model_id}: {'PASSED' if result.passed else 'FAILED'}"
        embedding = model.encode(desc).tolist()

        # Use timestamp-based ID for history
        point_id = int(datetime.utcnow().timestamp() * 1000) % (2**31)

        payload = {
            'points': [{
                'id': point_id,
                'vector': embedding,
                'payload': {
                    'type': 'validation_result',
                    **asdict(result)
                }
            }]
        }

        response = requests.put(
            f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{QDRANT_COLLECTION}/points",
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=10
        )

        return response.status_code == 200
    except Exception as e:
        logger.warning(f"Failed to store validation in Qdrant: {e}")
        return False


def get_production_model_info() -> Dict:
    """
    Get production model info from Qdrant registry.

    Returns:
        Model metadata dictionary
    """
    try:
        response = requests.post(
            f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{QDRANT_COLLECTION}/points/scroll",
            json={
                "limit": 10,
                "with_payload": True,
                "with_vector": False
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            for point in data.get('result', {}).get('points', []):
                payload = point.get('payload', {})
                if payload.get('status') == 'PRODUCTION':
                    return payload

        return {}
    except Exception as e:
        logger.warning(f"Failed to get model info from Qdrant: {e}")
        return {}


def health_check() -> Dict:
    """
    Generate health check response for API endpoint.

    Returns:
        Dictionary with health status
    """
    model_info = get_production_model_info()

    # Verify model path exists
    model_id = model_info.get('model_id', PRODUCTION_MODEL_ID)
    model_path = MODEL_BASE_PATH / model_id / 'model-best'
    model_exists = model_path.exists()

    return {
        'status': 'healthy' if model_exists else 'degraded',
        'model_id': model_id,
        'model_path': str(model_path),
        'model_exists': model_exists,
        'f1_score': model_info.get('f1_score'),
        'entity_types': model_info.get('entity_types'),
        'registry': 'qdrant' if model_info else 'fallback',
        'timestamp': datetime.utcnow().isoformat()
    }


# CLI interface
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='NER11 Model Validator')
    parser.add_argument('--model', default=PRODUCTION_MODEL_ID, help='Model ID to validate')
    parser.add_argument('--api-url', default='http://localhost:8000', help='NER API URL')
    parser.add_argument('--checksum-only', action='store_true', help='Only verify checksums')
    parser.add_argument('--tests-only', action='store_true', help='Only run entity tests')
    parser.add_argument('--store-result', action='store_true', help='Store result in Qdrant')

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"NER11 Model Validation - {args.model}")
    print(f"{'='*60}\n")

    if args.checksum_only:
        model_path = MODEL_BASE_PATH / args.model / 'model-best'
        valid, errors = verify_model_checksums(args.model, model_path)
        print(f"Checksum verification: {'PASSED' if valid else 'FAILED'}")
        for err in errors:
            print(f"  - {err}")
        sys.exit(0 if valid else 1)

    if args.tests_only:
        passed, total, errors = run_entity_tests(args.api_url)
        print(f"Entity tests: {passed}/{total} passed")
        for err in errors:
            print(f"  - {err}")
        sys.exit(0 if passed == total else 1)

    # Full validation
    result = validate_model_at_startup(
        model_id=args.model,
        api_url=args.api_url
    )

    print(f"\nValidation Result:")
    print(f"  Model: {result.model_id}")
    print(f"  Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
    print(f"  Checksum: {'✅' if result.checksum_valid else '❌'}")
    print(f"  Entity Tests: {result.entity_tests_passed}/{result.entity_tests_total}")

    if result.errors:
        print(f"\n  Errors:")
        for err in result.errors:
            print(f"    - {err}")

    if args.store_result:
        stored = store_validation_result_qdrant(result)
        print(f"\n  Stored in Qdrant: {'✅' if stored else '❌'}")

    print(f"\n  Validated at: {result.validated_at}")
    print(f"{'='*60}\n")

    sys.exit(0 if result.passed else 1)
