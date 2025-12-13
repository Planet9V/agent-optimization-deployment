#!/usr/bin/env python3
"""
Fix serve_model.py to properly register Phase B API routers
Inserts code AFTER the Sprint 1 try/except block completes
"""
import sys

def fix_serve_model():
    """Add Phase B router imports and registrations to serve_model.py"""

    # Read current serve_model.py
    with open('/app/serve_model.py', 'r') as f:
        lines = f.readlines()

    # Find the line with Sprint 1 exception handler END
    sprint1_except_end_line = None
    for i, line in enumerate(lines):
        if "SPRINT1_ROUTERS_AVAILABLE = False" in line:
            # Find the end of this except block (next blank line or next try/function)
            for j in range(i+1, min(i+10, len(lines))):
                if lines[j].strip() == "":
                    sprint1_except_end_line = j
                    break
                if "traceback.print_exc()" in lines[j]:
                    sprint1_except_end_line = j + 1
                    break
            break

    if sprint1_except_end_line is None:
        print("ERROR: Could not find Sprint 1 exception block end")
        sys.exit(1)

    print(f"Found Sprint 1 block end at line {sprint1_except_end_line}")

    # Phase B router imports (to insert AFTER Sprint 1 block)
    phase_b_imports = [
        "\n",
        "# =============================================================================\n",
        "# PHASE B API ROUTERS (B2-B5) - Sprint 2-5 Capabilities\n",
        "# =============================================================================\n",
        "\n",
        "try:\n",
        "    # Phase B2: Threat Intelligence & Risk Scoring\n",
        "    from api.threat_intelligence.threat_router import router as threat_router\n",
        "    from api.risk_scoring.risk_router import router as risk_router\n",
        "\n",
        "    # Phase B3: Remediation & Compliance\n",
        "    from api.remediation.remediation_router import router as remediation_router\n",
        "    from api.compliance_mapping.compliance_router import router as compliance_router\n",
        "\n",
        "    # Phase B4: Scanning & Alerting\n",
        "    from api.automated_scanning.scanning_router import router as scanning_router\n",
        "    from api.alert_management.alert_router import router as alert_router\n",
        "\n",
        "    # Phase B5: Economic Impact & Demographics & Prioritization\n",
        "    from api.economic_impact.economic_router import router as economic_router\n",
        "    from api.demographics.demographics_router import router as demographics_router\n",
        "    from api.prioritization.prioritization_router import router as prioritization_router\n",
        "\n",
        "    PHASE_B_ROUTERS_AVAILABLE = True\n",
        "    logger.info(\"✅ Phase B API routers (B2-B5) loaded successfully\")\n",
        "\n",
        "except ImportError as e:\n",
        "    PHASE_B_ROUTERS_AVAILABLE = False\n",
        "    logger.warning(f\"⚠️  Phase B API routers not available: {e}\")\n",
        "    import traceback\n",
        "    traceback.print_exc()\n",
        "\n",
    ]

    # Insert Phase B imports after Sprint 1 block
    lines = lines[:sprint1_except_end_line] + phase_b_imports + lines[sprint1_except_end_line:]

    # Now find Sprint 1 router registration end
    sprint1_register_end_line = None
    for i, line in enumerate(lines):
        if '"   - Equipment Management: /api/v2/equipment/*"' in line:
            # Next few lines after this
            for j in range(i+1, min(i+10, len(lines))):
                if lines[j].strip() == "" or "except Exception" in lines[j]:
                    sprint1_register_end_line = j
                    break
            break

    if sprint1_register_end_line is None:
        print("ERROR: Could not find Sprint 1 registration end")
        sys.exit(1)

    print(f"Found Sprint 1 registration end at line {sprint1_register_end_line}")

    # Phase B router registrations
    phase_b_registrations = [
        "\n",
        "# Register Phase B API routers (B2-B5)\n",
        "if PHASE_B_ROUTERS_AVAILABLE:\n",
        "    try:\n",
        "        # Phase B2: Threat Intelligence & Risk Scoring\n",
        "        app.include_router(threat_router, tags=[\"Threat Intelligence\"])\n",
        "        app.include_router(risk_router, tags=[\"Risk Scoring\"])\n",
        "\n",
        "        # Phase B3: Remediation & Compliance\n",
        "        app.include_router(remediation_router, tags=[\"Remediation\"])\n",
        "        app.include_router(compliance_router, tags=[\"Compliance Mapping\"])\n",
        "\n",
        "        # Phase B4: Scanning & Alerting\n",
        "        app.include_router(scanning_router, tags=[\"Automated Scanning\"])\n",
        "        app.include_router(alert_router, tags=[\"Alert Management\"])\n",
        "\n",
        "        # Phase B5: Economic Impact & Demographics & Prioritization\n",
        "        app.include_router(economic_router, tags=[\"Economic Impact\"])\n",
        "        app.include_router(demographics_router, tags=[\"Demographics\"])\n",
        "        app.include_router(prioritization_router, tags=[\"Prioritization\"])\n",
        "\n",
        "        logger.info(\"✅ Phase B API routers registered successfully\")\n",
        "        logger.info(\"   - Threat Intelligence: /api/v2/threat-intel/*\")\n",
        "        logger.info(\"   - Risk Scoring: /api/v2/risk/*\")\n",
        "        logger.info(\"   - Remediation: /api/v2/remediation/*\")\n",
        "        logger.info(\"   - Compliance: /api/v2/compliance/*\")\n",
        "        logger.info(\"   - Scanning: /api/v2/scanning/*\")\n",
        "        logger.info(\"   - Alerts: /api/v2/alerts/*\")\n",
        "        logger.info(\"   - Economic Impact: /api/v2/economic/*\")\n",
        "        logger.info(\"   - Demographics: /api/v2/demographics/*\")\n",
        "        logger.info(\"   - Prioritization: /api/v2/prioritization/*\")\n",
        "\n",
        "    except Exception as e:\n",
        "        logger.error(f\"❌ Failed to register Phase B routers: {e}\")\n",
        "        import traceback\n",
        "        traceback.print_exc()\n",
        "\n",
    ]

    # Insert registrations
    lines = lines[:sprint1_register_end_line] + phase_b_registrations + lines[sprint1_register_end_line:]

    # Write updated content
    with open('/app/serve_model.py', 'w') as f:
        f.writelines(lines)

    print("✅ serve_model.py updated successfully")
    return True

if __name__ == "__main__":
    try:
        fix_serve_model()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
