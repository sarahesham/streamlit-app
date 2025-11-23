@echo off
REM Course Extractor Run Script for Windows
REM Quick script to activate venv and run the Streamlit app

echo 🎓 Course Extractor - Starting...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ❌ Virtual environment not found!
    echo    Please run setup.bat first
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ⚠️  Warning: .env file not found!
    echo    Please create .env file with your FIRECRAWL_API_KEY
    echo    You can copy .env.example to .env and edit it
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if API key is set
findstr /C:"your_api_key_here" .env >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Warning: FIRECRAWL_API_KEY appears to be a placeholder!
    echo    Please edit .env and add your actual API key
    echo.
)

echo 🚀 Starting Streamlit application...
echo    The app will open in your browser at http://localhost:8501
echo    Press Ctrl+C to stop
echo.

REM Run Streamlit
streamlit run st.py

pause

