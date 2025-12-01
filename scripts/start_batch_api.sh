#!/bin/bash
# Start Batch Prediction API (GAP-ML-011)

set -e

echo "================================================"
echo "Starting Batch Prediction API (GAP-ML-011)"
echo "================================================"

# Check dependencies
echo "Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found"
    exit 1
fi

if ! command -v redis-cli &> /dev/null; then
    echo "WARNING: Redis CLI not found - ensure Redis is running"
fi

# Check Redis connection
echo "Checking Redis connection..."
if redis-cli ping &> /dev/null; then
    echo "✓ Redis is running"
else
    echo "ERROR: Redis is not running"
    echo "Start Redis: redis-server"
    exit 1
fi

# Check Neo4j connection (optional - server will fail gracefully if not available)
echo "Checking Neo4j connection..."
NEO4J_URI=${NEO4J_URI:-"bolt://localhost:7687"}
if timeout 2 bash -c "</dev/tcp/localhost/7687" 2>/dev/null; then
    echo "✓ Neo4j is running"
else
    echo "WARNING: Neo4j may not be running at $NEO4J_URI"
fi

# Set environment variables
export NEO4J_URI=${NEO4J_URI:-"bolt://localhost:7687"}
export NEO4J_USER=${NEO4J_USER:-"neo4j"}
export NEO4J_PASSWORD=${NEO4J_PASSWORD:-"password"}
export REDIS_URL=${REDIS_URL:-"redis://localhost:6379"}

echo ""
echo "Configuration:"
echo "  NEO4J_URI: $NEO4J_URI"
echo "  REDIS_URL: $REDIS_URL"
echo ""

# Install dependencies if needed
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r src/api/requirements.txt

# Start server
echo ""
echo "================================================"
echo "Starting Batch Prediction API Server"
echo "================================================"
echo "API Documentation: http://localhost:8000/api/v1/docs"
echo "Health Check: http://localhost:8000/api/v1/health"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd /home/jim/2_OXOT_Projects_Dev
python src/api/batch_prediction_server.py
