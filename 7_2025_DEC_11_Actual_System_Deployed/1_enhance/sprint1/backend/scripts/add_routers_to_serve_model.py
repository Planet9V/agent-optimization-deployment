#!/usr/bin/env python3
"""
Add API routers to serve_model.py
Extends existing NER API with Sprint 1 endpoints
"""

import sys

def add_routers_to_serve_model(serve_model_path: str) -> str:
    """Add router imports and registrations to serve_model.py"""

    with open(serve_model_path, 'r') as f:
        content = f.read()

    # Find the FastAPI app initialization
    app_init_marker = 'app = FastAPI('
    if app_init_marker not in content:
        raise ValueError("Could not find FastAPI app initialization")

    # Router imports to add after other imports
    router_imports = '''
# Sprint 1 API Routers - Added for SBOM and Equipment APIs
try:
    from api.sbom_analysis import sbom_router
    from api.vendor_equipment import vendor_router
    SPRINT1_ROUTERS_AVAILABLE = True
    logger.info("✅ Sprint 1 API routers loaded successfully")
except ImportError as e:
    SPRINT1_ROUTERS_AVAILABLE = False
    logger.warning(f"⚠️ Sprint 1 API routers not available: {e}")
'''

    # Find where to insert imports (after other imports, before app initialization)
    lines = content.split('\n')
    insert_index = 0

    for i, line in enumerate(lines):
        if line.startswith('# Initialize FastAPI app') or 'app = FastAPI' in line:
            insert_index = i
            break

    # Insert router imports
    lines.insert(insert_index, router_imports)

    # Router registrations to add after app initialization
    router_registrations = '''
# Register Sprint 1 API routers
if SPRINT1_ROUTERS_AVAILABLE:
    try:
        app.include_router(sbom_router, prefix="/api/v1", tags=["SBOM Analysis"])
        app.include_router(vendor_router, prefix="/api/v1", tags=["Vendor Equipment"])
        logger.info("✅ Sprint 1 API routers registered successfully")
        logger.info("   - SBOM Analysis: /api/v1/sbom/*")
        logger.info("   - Vendor Equipment: /api/v1/vendor/*")
    except Exception as e:
        logger.error(f"❌ Failed to register Sprint 1 routers: {e}")
'''

    # Find where to add router registrations (after app initialization, before @app decorators)
    content_updated = '\n'.join(lines)

    # Find first @app.post or @app.get decorator
    first_endpoint = content_updated.find('@app.post(')
    if first_endpoint == -1:
        first_endpoint = content_updated.find('@app.get(')

    if first_endpoint > 0:
        # Insert before first endpoint
        content_updated = (
            content_updated[:first_endpoint] +
            router_registrations + '\n\n' +
            content_updated[first_endpoint:]
        )

    return content_updated


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: add_routers_to_serve_model.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        updated_content = add_routers_to_serve_model(input_file)

        with open(output_file, 'w') as f:
            f.write(updated_content)

        print(f"✅ Successfully updated serve_model.py")
        print(f"   Input: {input_file}")
        print(f"   Output: {output_file}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
