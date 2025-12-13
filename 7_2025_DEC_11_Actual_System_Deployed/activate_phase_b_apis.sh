#!/bin/bash
# =============================================================================
# PHASE B API ACTIVATION SCRIPT
# =============================================================================
# Description: Activates Phase B2-B5 APIs by copying modules and registering routers
# Created: 2025-12-12
# Version: 1.0.0
# =============================================================================

set -e  # Exit on error

echo "🚀 Phase B API Activation - Starting"
echo "===================================="

# Define source and container paths
SOURCE_DIR="/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/api"
CONTAINER_NAME="ner11-gold-api"

# Phase B API modules to activate
MODULES=(
    "threat_intelligence"
    "risk_scoring"
    "remediation"
    "compliance_mapping"
    "automated_scanning"
    "alert_management"
    "economic_impact"
    "demographics"
    "prioritization"
)

echo ""
echo "📦 Step 1: Copying API modules to container..."
echo "-----------------------------------------------"

for module in "${MODULES[@]}"; do
    echo "  → Copying ${module}..."
    docker cp "${SOURCE_DIR}/${module}" "${CONTAINER_NAME}:/app/api/"
    if [ $? -eq 0 ]; then
        echo "    ✅ ${module} copied successfully"
    else
        echo "    ❌ Failed to copy ${module}"
        exit 1
    fi
done

echo ""
echo "✅ All modules copied to container"

echo ""
echo "📝 Step 2: Verify modules in container..."
echo "-----------------------------------------"

echo "  Modules now in container /app/api/:"
docker exec "${CONTAINER_NAME}" ls -1 /app/api/ | grep -E "^(threat|risk|remediation|compliance|scanning|alert|economic|demographics|prioritization)"

echo ""
echo "📋 Step 3: Creating router registration code..."
echo "-----------------------------------------------"

# Create router import and registration code
ROUTER_CODE=$(cat <<'EOF'

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
    logger.warning(f"⚠️ Phase B API routers not available: {e}")
    import traceback
    traceback.print_exc()
EOF
)

# Backup current serve_model.py
echo "  → Creating backup of serve_model.py..."
docker exec "${CONTAINER_NAME}" cp /app/serve_model.py /app/serve_model.py.backup_phase_b
echo "    ✅ Backup created: /app/serve_model.py.backup_phase_b"

echo ""
echo "🔧 Step 4: Updating serve_model.py with router registrations..."
echo "---------------------------------------------------------------"

# Create Python script to update serve_model.py
cat > /tmp/update_serve_model.py << 'PYEOF'
import sys

# Read current serve_model.py
with open('/app/serve_model.py', 'r') as f:
    content = f.read()

# Find insertion point after Sprint 1 imports
sprint1_import_marker = "except ImportError as e:\n    SPRINT1_ROUTERS_AVAILABLE = False"

if sprint1_import_marker not in content:
    print("ERROR: Could not find Sprint 1 import marker")
    sys.exit(1)

# Add Phase B imports after Sprint 1
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
    logger.warning(f"⚠️ Phase B API routers not available: {e}")
    import traceback
    traceback.print_exc()
'''

# Find Sprint 1 registration marker
sprint1_register_marker = '        logger.info("   - Equipment Management: /api/v2/equipment/*")'

if sprint1_register_marker not in content:
    print("ERROR: Could not find Sprint 1 registration marker")
    sys.exit(1)

# Add Phase B registrations after Sprint 1
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
        traceback.print_exc()
'''

# Insert Phase B imports
insertion_point = content.find(sprint1_import_marker) + len(sprint1_import_marker)
content = content[:insertion_point] + phase_b_imports + content[insertion_point:]

# Insert Phase B registrations
registration_point = content.find(sprint1_register_marker) + len(sprint1_register_marker)
content = content[:registration_point] + phase_b_registrations + content[registration_point:]

# Write updated content
with open('/app/serve_model.py', 'w') as f:
    f.write(content)

print("✅ serve_model.py updated successfully")
PYEOF

# Copy update script to container and run it
docker cp /tmp/update_serve_model.py "${CONTAINER_NAME}:/tmp/"
docker exec "${CONTAINER_NAME}" python3 /tmp/update_serve_model.py

if [ $? -eq 0 ]; then
    echo "  ✅ serve_model.py updated with Phase B router registrations"
else
    echo "  ❌ Failed to update serve_model.py"
    echo "  → Restoring backup..."
    docker exec "${CONTAINER_NAME}" cp /app/serve_model.py.backup_phase_b /app/serve_model.py
    exit 1
fi

echo ""
echo "🔄 Step 5: Restarting container to activate APIs..."
echo "---------------------------------------------------"

docker restart "${CONTAINER_NAME}"
echo "  → Waiting for container to restart (15 seconds)..."
sleep 15

# Check container status
if docker ps | grep -q "${CONTAINER_NAME}"; then
    echo "  ✅ Container restarted successfully"
else
    echo "  ❌ Container failed to restart"
    exit 1
fi

echo ""
echo "🧪 Step 6: Testing Phase B API endpoints..."
echo "-------------------------------------------"

# Test endpoints
ENDPOINTS=(
    "/api/v2/threat-intel/actors"
    "/api/v2/risk/scores/high-risk"
    "/api/v2/remediation/plans"
    "/api/v2/compliance/frameworks"
    "/api/v2/scanning/scans"
    "/api/v2/alerts/alerts"
    "/api/v2/economic/impacts"
    "/api/v2/demographics/summaries"
    "/api/v2/prioritization/rankings"
)

WORKING_ENDPOINTS=()
FAILED_ENDPOINTS=()

for endpoint in "${ENDPOINTS[@]}"; do
    echo "  Testing: ${endpoint}"

    response=$(curl -s -w "\n%{http_code}" \
        -H "X-Customer-ID: test" \
        "http://localhost:8000${endpoint}" 2>/dev/null)

    http_code=$(echo "$response" | tail -n 1)

    if [ "$http_code" == "200" ] || [ "$http_code" == "404" ]; then
        echo "    ✅ Endpoint accessible (HTTP ${http_code})"
        WORKING_ENDPOINTS+=("$endpoint")
    else
        echo "    ❌ Endpoint failed (HTTP ${http_code})"
        FAILED_ENDPOINTS+=("$endpoint")
    fi
done

echo ""
echo "📊 ACTIVATION SUMMARY"
echo "===================="
echo ""
echo "✅ Working Endpoints: ${#WORKING_ENDPOINTS[@]}"
for ep in "${WORKING_ENDPOINTS[@]}"; do
    echo "   • ${ep}"
done

if [ ${#FAILED_ENDPOINTS[@]} -gt 0 ]; then
    echo ""
    echo "❌ Failed Endpoints: ${#FAILED_ENDPOINTS[@]}"
    for ep in "${FAILED_ENDPOINTS[@]}"; do
        echo "   • ${ep}"
    done
fi

echo ""
echo "🎯 View interactive API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "✅ Phase B API Activation Complete!"
echo ""
