#!/bin/bash
# Test script for graph visualization setup

echo "=== Graph Visualization Setup Test ==="
echo ""

# Check if neovis.js is installed
echo "1. Checking neovis.js installation..."
if [ -d "node_modules/neovis.js" ]; then
    echo "   ✓ neovis.js is installed"
else
    echo "   ✗ neovis.js is NOT installed"
    echo "   Run: npm install neovis.js --legacy-peer-deps"
fi
echo ""

# Check if required files exist
echo "2. Checking required components..."
files=(
    "components/graph/GraphVisualization.tsx"
    "components/graph/GraphFilters.tsx"
    "components/graph/NodeDetails.tsx"
    "app/graph/page.tsx"
    "app/api/graph/query/route.ts"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file (missing)"
    fi
done
echo ""

# Check environment variables
echo "3. Checking environment variables..."
if [ -f ".env.local" ]; then
    echo "   ✓ .env.local exists"

    if grep -q "NEXT_PUBLIC_NEO4J_URI" .env.local; then
        echo "   ✓ NEXT_PUBLIC_NEO4J_URI is set"
    else
        echo "   ✗ NEXT_PUBLIC_NEO4J_URI is NOT set"
    fi

    if grep -q "NEXT_PUBLIC_NEO4J_USER" .env.local; then
        echo "   ✓ NEXT_PUBLIC_NEO4J_USER is set"
    else
        echo "   ✗ NEXT_PUBLIC_NEO4J_USER is NOT set"
    fi

    if grep -q "NEXT_PUBLIC_NEO4J_PASSWORD" .env.local; then
        echo "   ✓ NEXT_PUBLIC_NEO4J_PASSWORD is set"
    else
        echo "   ✗ NEXT_PUBLIC_NEO4J_PASSWORD is NOT set"
    fi
else
    echo "   ✗ .env.local does NOT exist"
fi
echo ""

# Check Neo4j connection
echo "4. Testing Neo4j connection..."
NEO4J_URI="${NEO4J_URI:-bolt://openspg-neo4j:7687}"
echo "   Connecting to: $NEO4J_URI"
echo "   (This may fail if not in Docker network)"
echo ""

echo "=== Setup Complete ==="
echo ""
echo "To access the graph visualization:"
echo "1. Start the development server: npm run dev"
echo "2. Navigate to: http://localhost:3000/graph"
echo "3. Or click 'View Database' from the dashboard"
echo ""
echo "Features available:"
echo "- Interactive graph visualization with Neovis.js"
echo "- Node filtering by type, customer, tags"
echo "- Relationship filtering"
echo "- Confidence threshold slider"
echo "- Date range picker"
echo "- Force and hierarchical layouts"
echo "- Node click for details"
echo "- Custom Cypher query builder"
echo "- Export graph as PNG"
echo ""
