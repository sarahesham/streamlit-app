#!/bin/bash

# Course Extractor Setup Script
# Works for both local development and Streamlit Cloud deployment

set -e  # Exit on error

# Detect if running in Streamlit Cloud (post-install) or local development
# Streamlit Cloud runs this after pip install, so we just need Playwright browsers
if [ -n "$STREAMLIT_CLOUD" ] || [ ! -d "venv" ]; then
    # Streamlit Cloud post-install: Just install Playwright browsers
    echo "🌐 Installing Playwright browsers for Streamlit Cloud..."
    playwright install chromium
    playwright install-deps chromium || true
    echo "✅ Playwright browsers installed"
    exit 0
fi

# Local development: Full setup
echo "🎓 Course Extractor - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers (this may take a few minutes)..."
playwright install chromium

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Creating .env file from .env.example..."
        cp .env.example .env
        echo "✅ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env and add your FIRECRAWL_API_KEY"
        echo "   Get your API key from: https://firecrawl.dev"
    else
        echo "⚠️  .env.example not found. Creating basic .env file..."
        echo "FIRECRAWL_API_KEY=your_api_key_here" > .env
        echo "✅ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env and add your FIRECRAWL_API_KEY"
    fi
else
    echo "✅ .env file already exists"
fi

echo ""
echo "===================================="
echo "✅ Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env and add your FIRECRAWL_API_KEY"
echo "   2. Run: ./run.sh"
