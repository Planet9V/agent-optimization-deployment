#!/bin/bash
# NER v9 API Startup Script

set -e

echo "🚀 Starting NER v9 Comprehensive MITRE API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if model exists
MODEL_PATH="/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/models/ner_v9_comprehensive"
if [ ! -d "$MODEL_PATH" ]; then
    echo "❌ Error: V9 model not found at $MODEL_PATH"
    exit 1
fi

echo "✅ Model found at $MODEL_PATH"

# Load environment variables
if [ -f ".env" ]; then
    echo "📋 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  No .env file found, using defaults"
fi

# Start the API server
echo "🌐 Starting API server on port 8001..."
python main.py
