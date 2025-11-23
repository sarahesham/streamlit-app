# 🎓 Course Extractor - BoldStep.AI

A powerful web application for extracting detailed course information from university websites using AI-powered extraction.

## ✨ Features

- **Web Interface**: Beautiful Streamlit-based UI for easy interaction
- **Batch Extraction**: Extract multiple courses at once
- **AI-Powered**: Uses Firecrawl API for intelligent data extraction
- **Course Discovery**: Automatically discovers and extracts courses from university websites
- **Export Options**: Download results as JSON files

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed on your system
- **Firecrawl API Key** (get one from [Firecrawl](https://firecrawl.dev))
- **Internet connection** (for API calls and web scraping)

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Clone or download this repository**
   ```bash
   cd Sara
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure your API key**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your Firecrawl API key:
     ```
     FIRECRAWL_API_KEY=your_api_key_here
     ```

4. **Run the application**
   ```bash
   ./run.sh
   ```
   Or manually:
   ```bash
   streamlit run st.py
   ```

### Option 2: Manual Setup

1. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your FIRECRAWL_API_KEY
   ```

5. **Run the application**
   ```bash
   streamlit run st.py
   ```

## 📝 Configuration

### Environment Variables

Create a `.env` file in the project root with:

```env
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

**To get a Firecrawl API key:**
1. Visit [https://firecrawl.dev](https://firecrawl.dev)
2. Sign up for an account
3. Get your API key from the dashboard
4. Add it to your `.env` file

## 🎯 Usage

### Web Interface (Recommended)

1. Start the application:
   ```bash
   streamlit run st.py
   ```

2. Open your browser to `http://localhost:8501`

3. **Extract Individual Courses:**
   - Enter one or more course URLs (one per line)
   - Click "🚀 Extract Course Details"
   - View results in the interface

4. **Bulk Extraction:**
   - Enter a university website URL
   - Click "🔍 Extract course links"
   - The system will discover and extract all courses

### Command Line Usage

You can also use the extraction modules directly:

```python
from course_extractor import extract_all_courses

course_urls = [
    "https://www.university.edu/courses/computer-science",
    "https://www.university.edu/courses/business-studies"
]

results = extract_all_courses(course_urls, output_file="courses.json")
```

## 📁 Project Structure

```
Sara/
├── st.py                 # Streamlit web application (main entry point)
├── course_extractor.py   # Course extraction module using Firecrawl
├── extractor.py          # Web scraping module using Playwright
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── setup.sh             # Automated setup script
├── run.sh               # Quick run script
└── README.md            # This file
```

## 🔧 Troubleshooting

### Common Issues

**1. "FIRECRAWL_API_KEY not set" error**
   - Make sure you created a `.env` file
   - Check that the API key is correctly set in `.env`
   - Ensure `.env` is in the project root directory

**2. Playwright browser not found**
   - Run: `playwright install chromium`
   - On Linux, you may need: `playwright install-deps`

**3. Import errors**
   - Make sure virtual environment is activated
   - Run: `pip install -r requirements.txt`

**4. Port already in use**
   - Streamlit defaults to port 8501
   - Change it: `streamlit run st.py --server.port 8502`

**5. Python 3.13 on Windows - NotImplementedError with asyncio**
   - This is a known issue with Python 3.13 on Windows and asyncio subprocess transport
   - The code includes automatic fixes for this issue
   - If you still encounter errors, ensure you're using the latest version of the code
   - Alternative: Use Python 3.11 or 3.12 on Windows for better compatibility

## 📦 Dependencies

- `streamlit` - Web interface framework
- `playwright` - Web scraping and browser automation
- `firecrawl-py` - AI-powered web extraction API
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management
- `nest-asyncio` - Async event loop support

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Project Structure

- `st.py` - Main Streamlit application
- `course_extractor.py` - Firecrawl-based extraction logic
- `extractor.py` - Playwright-based web scraping
- `tests/` - Unit tests

## 📄 License

This project is for educational and research purposes.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments for detailed documentation
3. Ensure all dependencies are correctly installed

## ☁️ Streamlit Cloud Deployment

This app is ready to deploy on Streamlit Community Cloud!

### Quick Deployment Steps

1. **Push your code to GitHub**
2. **Go to [share.streamlit.io](https://share.streamlit.io)** and create a new app
3. **Select your repository** and set main file to `streamlit_app.py`
4. **Add your API key** in app settings → Secrets:
   ```toml
   FIRECRAWL_API_KEY = "your_api_key_here"
   ```
5. **Deploy!** 🚀

For detailed deployment instructions, see **[DEPLOYMENT.md](DEPLOYMENT.md)**

### Files for Streamlit Cloud

- `streamlit_app.py` - Main entry point (automatically detected)
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies for Playwright
- `setup.sh` - Post-install script for Playwright browsers
- `.streamlit/config.toml` - Streamlit configuration

## 🎉 Enjoy!

Happy course extracting! 🚀

