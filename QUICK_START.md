# 🚀 Quick Start Guide

## For Your Brother - Easy Setup Instructions

### Step 1: Get the Code
- Copy the entire `Sara` folder to your computer
- Or download it as a ZIP and extract it

### Step 2: Run Setup

**On Linux/Mac:**
```bash
cd Sara
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
cd Sara
setup.bat
```

This will:
- ✅ Create a Python virtual environment
- ✅ Install all required packages
- ✅ Set up Playwright browsers
- ✅ Create a `.env` file template

### Step 3: Add Your API Key

1. Get a free API key from: https://firecrawl.dev
2. Open the `.env` file in the project folder
3. Replace `your_api_key_here` with your actual API key:
   ```
   FIRECRAWL_API_KEY=fc-your-actual-key-here
   ```

### Step 4: Run the App

**On Linux/Mac:**
```bash
./run.sh
```

**On Windows:**
```bash
run.bat
```

The app will automatically open in your browser at `http://localhost:8501`

### That's It! 🎉

You can now:
- Enter course URLs to extract details
- Use the bulk extraction feature for entire university websites
- Download results as JSON files

### Need Help?

- Check `README.md` for detailed documentation
- See `ENV_SETUP.md` for environment setup help
- Make sure Python 3.8+ is installed on your system

