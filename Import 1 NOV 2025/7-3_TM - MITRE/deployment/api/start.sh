#!/bin/bash
# Quick start script for NER v8 API

set -e

echo "======================================"
echo "NER v8 MITRE API - Quick Start"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  WARNING: Please edit .env and set your API key!"
fi

# Create logs directory
mkdir -p logs

echo ""
echo "======================================"
echo "Starting API server..."
echo "======================================"
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/api/v1/docs"
echo "Health Check: http://localhost:8000/api/v1/ner/v8/health"
echo ""
echo "Press Ctrl+C to stop"
echo "======================================"
echo ""

# Start the server
python main.py
