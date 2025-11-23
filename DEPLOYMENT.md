# 🚀 Streamlit Cloud Deployment Guide

This guide will help you deploy the Course Extractor app to Streamlit Community Cloud.

## Prerequisites

1. **GitHub Account**: Your code needs to be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Firecrawl API Key**: Get one from [firecrawl.dev](https://firecrawl.dev)

## Deployment Steps

### 1. Push Your Code to GitHub

Make sure your code is in a GitHub repository:

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account if not already connected
4. Select your repository
5. Set the **Main file path** to: `streamlit_app.py`
6. Set the **Python version** to: `3.11` or `3.12` (recommended)
7. Click "Deploy!"

### 3. Configure Secrets

After deployment, configure your API key:

1. Go to your app's settings (click the hamburger menu → Settings)
2. Click on "Secrets" tab
3. Add the following:

```toml
FIRECRAWL_API_KEY = "your_firecrawl_api_key_here"
```

4. Click "Save"
5. Your app will automatically redeploy with the new secrets

## File Structure for Streamlit Cloud

Your repository should have this structure:

```
Sara/
├── streamlit_app.py          # Main Streamlit app (entry point)
├── st.py                      # Original Streamlit app (also works)
├── requirements.txt           # Python dependencies
├── packages.txt               # System dependencies (for Playwright)
├── setup.sh                   # Post-install script (optional)
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml.example   # Example secrets file
├── course_extractor.py        # Course extraction module
├── extractor.py               # Web scraping module
├── university_config.py       # University configurations
└── README.md                  # Project documentation
```

## Important Files Explained

### `streamlit_app.py`
- Main entry point for Streamlit Cloud
- Automatically detected by Streamlit Cloud
- Uses `st.secrets` for API keys (Cloud) and falls back to `.env` (local)

### `requirements.txt`
- Lists all Python package dependencies
- Streamlit Cloud installs these automatically

### `packages.txt`
- Lists system-level dependencies needed for Playwright
- Required for Playwright browser automation on Linux

### `setup.sh` (Optional)
- Post-install script that runs after `pip install`
- Installs Playwright browsers
- Must be executable (`chmod +x setup.sh`)

### `.streamlit/config.toml`
- Streamlit configuration
- Customizes theme, server settings, etc.

## Troubleshooting

### Issue: "FIRECRAWL_API_KEY not configured"

**Solution:**
1. Go to app settings → Secrets
2. Add: `FIRECRAWL_API_KEY = "your_key_here"`
3. Save and wait for redeploy

### Issue: Playwright browser not found

**Solution:**
1. Ensure `packages.txt` exists with system dependencies
2. Ensure `setup.sh` exists and is executable
3. Check build logs for Playwright installation errors

### Issue: App fails to start

**Solution:**
1. Check the build logs in Streamlit Cloud dashboard
2. Verify `streamlit_app.py` exists and is the main file
3. Check that all imports are available in `requirements.txt`
4. Ensure Python version is 3.8+ (3.11 or 3.12 recommended)

### Issue: Timeout errors

**Solution:**
- Streamlit Cloud has execution time limits
- Long-running extractions may timeout
- Consider breaking large extractions into smaller batches

## Environment Variables vs Secrets

- **Streamlit Cloud**: Use `st.secrets` (configured in app settings)
- **Local Development**: Use `.env` file (not committed to git)

The app automatically detects which environment it's running in and uses the appropriate method.

## Updating Your App

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. Streamlit Cloud automatically detects changes and redeploys
4. Check the deployment status in your Streamlit Cloud dashboard

## Best Practices

1. **Never commit secrets**: Use Streamlit secrets for API keys
2. **Pin versions**: Consider pinning package versions in `requirements.txt` for stability
3. **Test locally**: Test your app locally before deploying
4. **Monitor logs**: Check Streamlit Cloud logs for errors
5. **Optimize imports**: Only import what you need to reduce startup time

## Support

- Streamlit Cloud Docs: [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- Streamlit Forums: [discuss.streamlit.io](https://discuss.streamlit.io)

## Notes

- Streamlit Cloud provides free hosting with some limitations
- Apps may go to sleep after inactivity
- First load after sleep may be slower
- Consider upgrading to Streamlit Cloud for Teams for production use

