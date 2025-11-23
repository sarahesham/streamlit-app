@echo off
REM Course Extractor Setup Script for Windows
REM This script sets up the Python environment and installs all dependencies

echo 🎓 Course Extractor - Setup Script
echo ====================================
echo.

REM Check Python version
echo 📋 Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

python --version
echo ✅ Python found

REM Create virtual environment
echo.
echo 🔧 Creating virtual environment...
if exist venv (
    echo ⚠️  Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo.
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Install Playwright browsers
echo.
echo 🌐 Installing Playwright browsers (this may take a few minutes)...
playwright install chromium

REM Create .env file if it doesn't exist
echo.
if not exist .env (
    if exist .env.example (
        echo 📝 Creating .env file from .env.example...
        copy .env.example .env >nul
        echo ✅ .env file created
        echo.
        echo ⚠️  IMPORTANT: Please edit .env and add your FIRECRAWL_API_KEY
        echo    Get your API key from: https://firecrawl.dev
    ) else (
        echo ⚠️  .env.example not found. Creating basic .env file...
        echo FIRECRAWL_API_KEY=your_api_key_here > .env
        echo ✅ .env file created
        echo.
        echo ⚠️  IMPORTANT: Please edit .env and add your FIRECRAWL_API_KEY
    )
) else (
    echo ✅ .env file already exists
)

echo.
echo ====================================
echo ✅ Setup completed successfully!
echo.
echo 📝 Next steps:
echo    1. Edit .env and add your FIRECRAWL_API_KEY
echo    2. Run: run.bat
echo    Or manually: venv\Scripts\activate && streamlit run st.py
echo.
echo 🎉 You're all set!
pause

