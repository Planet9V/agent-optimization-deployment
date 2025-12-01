"""
AEON Web Interface - System Diagnostics Page
Comprehensive health checks and connection testing
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import os
import platform
import psutil
import socket

# Setup paths - add parent project for parent utils
parent_project_dir = Path(__file__).parent.parent.parent
if str(parent_project_dir) not in sys.path:
    sys.path.insert(0, str(parent_project_dir))

# Import from web_utils (renamed to avoid conflict with parent utils)
from web_utils.neo4j_connector import get_connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="System Diagnostics - AEON",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 System Diagnostics")
st.markdown("Comprehensive health checks for all AEON components")
st.markdown("---")

# Diagnostic test functions
def test_python_environment():
    """Test Python environment and core libraries"""
    try:
        results = {
            "Python Version": platform.python_version(),
            "Platform": platform.platform(),
            "Architecture": platform.machine(),
            "CPU Cores": psutil.cpu_count(),
            "Memory Total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "Memory Available": f"{psutil.virtual_memory().available / (1024**3):.2f} GB"
        }

        # Test critical imports
        import streamlit
        import neo4j
        import pandas
        import plotly
        import rich

        results["Streamlit Version"] = streamlit.__version__
        results["Neo4j Driver Version"] = neo4j.__version__
        results["Pandas Version"] = pandas.__version__
        results["Plotly Version"] = plotly.__version__

        return {"status": "✅ PASS", "details": results, "error": None}
    except Exception as e:
        return {"status": "❌ FAIL", "details": {}, "error": str(e)}

def test_neo4j_connection():
    """Test Neo4j database connection and query"""
    import time
    try:
        connector = get_connector()

        # Test connection
        start_time = time.time()
        is_connected = connector.test_connection()
        latency = (time.time() - start_time) * 1000

        if not is_connected:
            return {"status": "❌ FAIL", "details": {}, "error": "Connection failed"}

        # Get counts
        with connector.driver.session() as session:
            doc_count = session.run("MATCH (d:Document) RETURN count(d) as count").single()["count"]
            entity_count = session.run("MATCH (e:Entity) RETURN count(e) as count").single()["count"]
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]

        results = {
            "Connection": "✅ Connected",
            "Latency": f"{latency:.2f} ms",
            "URI": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            "Documents": f"{doc_count:,}",
            "Entities": f"{entity_count:,}",
            "Relationships": f"{rel_count:,}"
        }

        return {"status": "✅ PASS", "details": results, "error": None}
    except Exception as e:
        return {"status": "❌ FAIL", "details": {}, "error": str(e)}

def test_qdrant_connection():
    """Test Qdrant vector database connection"""
    try:
        from qdrant_client import QdrantClient

        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", 6333))

        client = QdrantClient(host=qdrant_host, port=qdrant_port)

        # List collections
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]

        results = {
            "Connection": "✅ Connected",
            "Host": f"{qdrant_host}:{qdrant_port}",
            "Collections": ", ".join(collection_names) if collection_names else "None",
            "Collection Count": len(collection_names)
        }

        # Get vector counts if collections exist
        if collection_names:
            for coll_name in collection_names[:3]:  # Show first 3
                try:
                    info = client.get_collection(coll_name)
                    results[f"Vectors ({coll_name})"] = f"{info.points_count:,}"
                except:
                    pass

        return {"status": "✅ PASS", "details": results, "error": None}
    except Exception as e:
        return {"status": "⚠️ WARN", "details": {"Note": "Qdrant optional for basic functionality"}, "error": str(e)}

def test_openrouter_api():
    """Test OpenRouter API connection"""
    try:
        import requests

        api_key = os.getenv("OPENROUTER_API_KEY", "")

        if not api_key or api_key == "your_openrouter_api_key_here":
            return {"status": "⏳ PENDING", "details": {"Note": "API key not configured"}, "error": "Set OPENROUTER_API_KEY in .env file"}

        # Test API connection
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:8501"
        }

        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            models = response.json()
            results = {
                "Connection": "✅ Connected",
                "API Key": f"{api_key[:15]}...{api_key[-4:]}",
                "Available Models": len(models.get("data", [])),
                "Status": "Authenticated"
            }
            return {"status": "✅ PASS", "details": results, "error": None}
        else:
            return {"status": "❌ FAIL", "details": {}, "error": f"HTTP {response.status_code}"}

    except Exception as e:
        return {"status": "⚠️ WARN", "details": {"Note": "Optional for AI features"}, "error": str(e)}

def test_file_system():
    """Test file system access and permissions"""
    try:
        base_path = Path(__file__).parent.parent.parent

        results = {
            "Base Directory": str(base_path),
            "Base Exists": "✅" if base_path.exists() else "❌",
            "Base Writable": "✅" if os.access(base_path, os.W_OK) else "❌"
        }

        # Check key directories
        key_dirs = ["data", "agents", "utils", "config", "web_interface"]
        for dir_name in key_dirs:
            dir_path = base_path / dir_name
            if dir_path.exists():
                results[f"{dir_name}/"] = "✅ Exists"
            else:
                results[f"{dir_name}/"] = "❌ Missing"

        # Test write permission
        test_file = base_path / "web_interface" / ".diagnostic_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
            results["Write Test"] = "✅ Success"
        except:
            results["Write Test"] = "❌ Failed"

        return {"status": "✅ PASS", "details": results, "error": None}
    except Exception as e:
        return {"status": "❌ FAIL", "details": {}, "error": str(e)}

def test_environment_variables():
    """Test environment variable configuration"""
    try:
        required_vars = [
            "NEO4J_URI",
            "NEO4J_USER",
            "NEO4J_PASSWORD",
            "QDRANT_HOST",
            "QDRANT_PORT"
        ]

        optional_vars = [
            "OPENROUTER_API_KEY",
            "OPENROUTER_MODEL",
            "AI_ASSISTANT_ENABLED"
        ]

        results = {}
        all_set = True

        for var in required_vars:
            value = os.getenv(var)
            if value:
                # Mask sensitive values
                if "PASSWORD" in var or "KEY" in var:
                    display = f"{value[:3]}...{value[-3:]}" if len(value) > 6 else "***"
                else:
                    display = value
                results[var] = f"✅ {display}"
            else:
                results[var] = "❌ Not set"
                all_set = False

        for var in optional_vars:
            value = os.getenv(var)
            if value and value != "your_openrouter_api_key_here":
                if "KEY" in var:
                    display = f"{value[:3]}...{value[-3:]}" if len(value) > 6 else "***"
                else:
                    display = value
                results[var] = f"⏳ {display}"
            else:
                results[var] = "⏳ Optional (not set)"

        status = "✅ PASS" if all_set else "⚠️ WARN"
        return {"status": status, "details": results, "error": None}
    except Exception as e:
        return {"status": "❌ FAIL", "details": {}, "error": str(e)}

def test_network_connectivity():
    """Test network and port connectivity"""
    try:
        results = {}

        # Test localhost
        results["Localhost Reachable"] = "✅" if socket.gethostbyname("localhost") == "127.0.0.1" else "❌"

        # Test port 8501 (Streamlit)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        streamlit_port = sock.connect_ex(('localhost', 8501))
        results["Port 8501 (Streamlit)"] = "✅ Open" if streamlit_port == 0 else "⚠️ Closed"
        sock.close()

        # Test port 7687 (Neo4j)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        neo4j_port = sock.connect_ex(('localhost', 7687))
        results["Port 7687 (Neo4j)"] = "✅ Open" if neo4j_port == 0 else "❌ Closed"
        sock.close()

        # Test port 6333 (Qdrant)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        qdrant_port = sock.connect_ex(('localhost', 6333))
        results["Port 6333 (Qdrant)"] = "✅ Open" if qdrant_port == 0 else "⚠️ Closed (optional)"
        sock.close()

        return {"status": "✅ PASS", "details": results, "error": None}
    except Exception as e:
        return {"status": "⚠️ WARN", "details": {}, "error": str(e)}

# Run all diagnostic tests
with st.spinner("Running comprehensive diagnostics..."):

    # Run tests
    python_test = test_python_environment()
    neo4j_test = test_neo4j_connection()
    qdrant_test = test_qdrant_connection()
    openrouter_test = test_openrouter_api()
    filesystem_test = test_file_system()
    env_test = test_environment_variables()
    network_test = test_network_connectivity()

# Display results in organized sections
st.header("📊 Diagnostic Results")
st.markdown(f"**Scan Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

# Overall Status Summary
col1, col2, col3, col4 = st.columns(4)

def count_status(tests):
    passed = sum(1 for t in tests if t["status"].startswith("✅"))
    failed = sum(1 for t in tests if t["status"].startswith("❌"))
    warned = sum(1 for t in tests if t["status"].startswith("⚠️"))
    pending = sum(1 for t in tests if t["status"].startswith("⏳"))
    return passed, failed, warned, pending

all_tests = [python_test, neo4j_test, qdrant_test, openrouter_test, filesystem_test, env_test, network_test]
passed, failed, warned, pending = count_status(all_tests)

with col1:
    st.metric("✅ Passed", passed)
with col2:
    st.metric("❌ Failed", failed)
with col3:
    st.metric("⚠️ Warnings", warned)
with col4:
    st.metric("⏳ Pending", pending)

st.markdown("---")

# Detailed test results
def display_test_result(title, icon, result):
    """Display a test result in expandable section"""
    status_color = {
        "✅ PASS": "🟢",
        "❌ FAIL": "🔴",
        "⚠️ WARN": "🟡",
        "⏳ PENDING": "🔵"
    }

    with st.expander(f"{icon} **{title}** - {status_color.get(result['status'], '')} {result['status']}", expanded=(result['status'].startswith("❌"))):
        if result["details"]:
            for key, value in result["details"].items():
                st.markdown(f"**{key}**: {value}")

        if result["error"]:
            st.error(f"**Error**: {result['error']}")

        if result["status"].startswith("✅"):
            st.success("All checks passed")
        elif result["status"].startswith("❌"):
            st.error("Critical issue detected - requires attention")
        elif result["status"].startswith("⚠️"):
            st.warning("Non-critical issue - system functional")

# Display all test results
display_test_result("Python Environment", "🐍", python_test)
display_test_result("Neo4j Database", "🗄️", neo4j_test)
display_test_result("Qdrant Vector DB", "🔍", qdrant_test)
display_test_result("OpenRouter AI API", "🤖", openrouter_test)
display_test_result("File System Access", "📁", filesystem_test)
display_test_result("Environment Variables", "⚙️", env_test)
display_test_result("Network Connectivity", "🌐", network_test)

# Action buttons
st.markdown("---")
st.header("🔧 Diagnostic Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Re-run All Tests"):
        st.rerun()

with col2:
    if st.button("📋 Export Report"):
        report = {
            "timestamp": datetime.now().isoformat(),
            "tests": {
                "python": python_test,
                "neo4j": neo4j_test,
                "qdrant": qdrant_test,
                "openrouter": openrouter_test,
                "filesystem": filesystem_test,
                "environment": env_test,
                "network": network_test
            }
        }

        import json
        report_json = json.dumps(report, indent=2)
        st.download_button(
            "Download JSON Report",
            report_json,
            file_name=f"aeon_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

with col3:
    if st.button("📊 View System Metrics"):
        st.info("System metrics feature coming soon")

# Recommendations section
st.markdown("---")
st.header("💡 Recommendations")

if failed > 0:
    st.error("**Critical Issues Detected**")
    st.markdown("""
    - Review failed tests above
    - Check error messages for details
    - Verify service connectivity
    - Contact support if issues persist
    """)
elif warned > 0:
    st.warning("**Minor Issues Detected**")
    st.markdown("""
    - System is functional
    - Some optional features may be unavailable
    - Review warnings for enhancement opportunities
    """)
else:
    st.success("**All Systems Operational**")
    st.markdown("""
    ✅ All critical components are functioning correctly
    ✅ Database connections are healthy
    ✅ Environment is properly configured
    ✅ System is ready for production use
    """)

# Footer
st.markdown("---")
st.caption("AEON System Diagnostics | Comprehensive Health Monitoring")
