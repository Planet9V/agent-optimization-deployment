#!/bin/bash
# Run complete benchmark suite with proper environment setup

set -e

echo "🚀 Neo4j Cache Performance Benchmark Suite"
echo "=========================================="

# Check if Neo4j is running
if ! nc -z localhost 7687 2>/dev/null; then
    echo "❌ Neo4j is not running on localhost:7687"
    echo "Please start Neo4j before running benchmarks"
    exit 1
fi

# Install Python dependencies if needed
echo "📦 Checking Python dependencies..."
pip install -q neo4j matplotlib numpy 2>/dev/null || {
    echo "⚠️  Installing dependencies..."
    pip install neo4j matplotlib numpy
}

# Set Neo4j credentials (customize as needed)
export NEO4J_URI="${NEO4J_URI:-bolt://localhost:7687}"
export NEO4J_USER="${NEO4J_USER:-neo4j}"
export NEO4J_PASSWORD="${NEO4J_PASSWORD:-your_password}"

echo "📍 Neo4j Connection: $NEO4J_URI"
echo ""

# Run benchmarks
echo "⏱️  Running benchmark suite (this may take several minutes)..."
python3 /home/jim/2_OXOT_Projects_Dev/tests/performance/cache_benchmark.py

# Generate visualizations
echo ""
echo "🎨 Generating visualizations and reports..."
python3 /home/jim/2_OXOT_Projects_Dev/tests/performance/visualize_results.py

echo ""
echo "✅ Benchmark suite complete!"
echo ""
echo "📊 Results available at:"
echo "  - tests/performance/benchmark_results.json"
echo "  - tests/performance/BENCHMARK_REPORT.md"
echo "  - tests/performance/speedup_chart.png"
echo "  - tests/performance/latency_chart.png"
echo "  - tests/performance/percentile_chart.png"
echo ""
echo "📖 Read BENCHMARK_REPORT.md for detailed analysis"
