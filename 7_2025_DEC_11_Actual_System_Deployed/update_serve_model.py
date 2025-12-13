#!/usr/bin/env python3
"""
Update serve_model.py to register Phase B API routers
"""
import sys

def update_serve_model():
    """Add Phase B router imports and registrations to serve_model.py"""

    # Read current serve_model.py
    with open('/app/serve_model.py', 'r') as f:
        content = f.read()

    # Check if Phase B routers are already added
    if "PHASE_B_ROUTERS_AVAILABLE" in content:
        print("⚠️  Phase B routers already registered in serve_model.py")
        return False

    # Find insertion point after Sprint 1 imports
    sprint1_import_end = "    traceback.print_exc()"

    if sprint1_import_end not in content:
        print("ERROR: Could not find Sprint 1 import marker")
        sys.exit(1)

    # Phase B router imports
    phase_b_imports = '''


# =============================================================================
# PHASE B API ROUTERS (B2-B5) - Sprint 2-5 Capabilities
# =============================================================================

try:
    # Phase B2: Threat Intelligence & Risk Scoring
    from api.threat_intelligence.threat_router import router as threat_router
    from api.risk_scoring.risk_router import router as risk_router

    # Phase B3: Remediation & Compliance
    from api.remediation.remediation_router import router as remediation_router
    from api.compliance_mapping.compliance_router import router as compliance_router

    # Phase B4: Scanning & Alerting
    from api.automated_scanning.scanning_router import router as scanning_router
    from api.alert_management.alert_router import router as alert_router

    # Phase B5: Economic Impact & Demographics & Prioritization
    from api.economic_impact.economic_router import router as economic_router
    from api.demographics.demographics_router import router as demographics_router
    from api.prioritization.prioritization_router import router as prioritization_router

    PHASE_B_ROUTERS_AVAILABLE = True
    logger.info("✅ Phase B API routers (B2-B5) loaded successfully")

except ImportError as e:
    PHASE_B_ROUTERS_AVAILABLE = False
    logger.warning(f"⚠️  Phase B API routers not available: {e}")
    import traceback
    traceback.print_exc()'''

    # Find first occurrence and insert
    insertion_point = content.find(sprint1_import_end)
    if insertion_point == -1:
        print("ERROR: Could not find insertion point")
        sys.exit(1)

    insertion_point += len(sprint1_import_end)
    content = content[:insertion_point] + phase_b_imports + content[insertion_point:]

    # Find Sprint 1 registration end marker
    sprint1_register_end = '        logger.info("   - Equipment Management: /api/v2/equipment/*")'

    if sprint1_register_end not in content:
        print("ERROR: Could not find Sprint 1 registration marker")
        sys.exit(1)

    # Phase B router registrations
    phase_b_registrations = '''

# Register Phase B API routers (B2-B5)
if PHASE_B_ROUTERS_AVAILABLE:
    try:
        # Phase B2: Threat Intelligence & Risk Scoring
        app.include_router(threat_router, tags=["Threat Intelligence"])
        app.include_router(risk_router, tags=["Risk Scoring"])

        # Phase B3: Remediation & Compliance
        app.include_router(remediation_router, tags=["Remediation"])
        app.include_router(compliance_router, tags=["Compliance Mapping"])

        # Phase B4: Scanning & Alerting
        app.include_router(scanning_router, tags=["Automated Scanning"])
        app.include_router(alert_router, tags=["Alert Management"])

        # Phase B5: Economic Impact & Demographics & Prioritization
        app.include_router(economic_router, tags=["Economic Impact"])
        app.include_router(demographics_router, tags=["Demographics"])
        app.include_router(prioritization_router, tags=["Prioritization"])

        logger.info("✅ Phase B API routers registered successfully")
        logger.info("   - Threat Intelligence: /api/v2/threat-intel/*")
        logger.info("   - Risk Scoring: /api/v2/risk/*")
        logger.info("   - Remediation: /api/v2/remediation/*")
        logger.info("   - Compliance: /api/v2/compliance/*")
        logger.info("   - Scanning: /api/v2/scanning/*")
        logger.info("   - Alerts: /api/v2/alerts/*")
        logger.info("   - Economic Impact: /api/v2/economic/*")
        logger.info("   - Demographics: /api/v2/demographics/*")
        logger.info("   - Prioritization: /api/v2/prioritization/*")

    except Exception as e:
        logger.error(f"❌ Failed to register Phase B routers: {e}")
        import traceback
        traceback.print_exc()'''

    # Insert registrations
    registration_point = content.find(sprint1_register_end)
    if registration_point == -1:
        print("ERROR: Could not find registration point")
        sys.exit(1)

    registration_point += len(sprint1_register_end)
    content = content[:registration_point] + phase_b_registrations + content[registration_point:]

    # Write updated content
    with open('/app/serve_model.py', 'w') as f:
        f.write(content)

    print("✅ serve_model.py updated successfully")
    return True

if __name__ == "__main__":
    try:
        updated = update_serve_model()
        sys.exit(0 if updated != False else 0)
    except Exception as e:
        print(f"❌ Error updating serve_model.py: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
