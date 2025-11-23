#!/bin/bash

# Course Extractor Run Script
# Quick script to activate venv and run the Streamlit app

set -e  # Exit on error

echo "🎓 Course Extractor - Starting..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run ./setup.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create .env file with your FIRECRAWL_API_KEY"
    echo "   You can copy .env.example to .env and edit it"
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Check if API key is set
if grep -q "your_api_key_here" .env 2>/dev/null; then
    echo "⚠️  Warning: FIRECRAWL_API_KEY appears to be a placeholder!"
    echo "   Please edit .env and add your actual API key"
    echo ""
fi

echo "🚀 Starting Streamlit application..."
echo "   The app will open in your browser at http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""

# Run Streamlit
streamlit run st.py

