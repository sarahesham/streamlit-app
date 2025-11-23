# ✅ Streamlit Cloud Deployment Checklist

Use this checklist to ensure your project is ready for Streamlit Cloud deployment.

## Pre-Deployment Checklist

### ✅ Required Files

- [x] `streamlit_app.py` - Main entry point (created)
- [x] `requirements.txt` - Python dependencies (exists)
- [x] `packages.txt` - System dependencies for Playwright (created)
- [x] `setup.sh` - Post-install script (updated)
- [x] `.streamlit/config.toml` - Streamlit configuration (created)
- [x] `.streamlit/secrets.toml.example` - Secrets example (created)

### ✅ Code Updates

- [x] `streamlit_app.py` uses `st.secrets` for API keys (Cloud) and falls back to `.env` (local)
- [x] `st.py` updated to support Streamlit secrets
- [x] All imports are available in `requirements.txt`

### ✅ Configuration

- [ ] **GitHub Repository**: Code is pushed to GitHub
- [ ] **API Key**: You have a Firecrawl API key ready
- [ ] **Secrets**: You know how to add secrets in Streamlit Cloud

## Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `streamlit_app.py`
   - Click "Deploy!"

3. **Configure Secrets**
   - Go to app settings → Secrets
   - Add:
     ```toml
     FIRECRAWL_API_KEY = "your_api_key_here"
     ```
   - Save (app will auto-redeploy)

4. **Verify Deployment**
   - Check that app loads successfully
   - Test API key configuration
   - Test a simple course extraction

## Troubleshooting

### App won't start
- Check build logs in Streamlit Cloud dashboard
- Verify `streamlit_app.py` exists and is set as main file
- Check that all dependencies are in `requirements.txt`

### API Key errors
- Verify secrets are configured correctly
- Check secret name matches: `FIRECRAWL_API_KEY`
- Ensure no extra quotes or spaces

### Playwright errors
- Check `packages.txt` exists with system dependencies
- Verify `setup.sh` is executable
- Check build logs for Playwright installation

## Files Created/Modified

### New Files
- `streamlit_app.py` - Main Streamlit app entry point
- `.streamlit/config.toml` - Streamlit configuration
- `.streamlit/secrets.toml.example` - Secrets example
- `packages.txt` - System dependencies
- `DEPLOYMENT.md` - Detailed deployment guide
- `DEPLOYMENT_CHECKLIST.md` - This file

### Modified Files
- `st.py` - Updated to support Streamlit secrets
- `setup.sh` - Updated to work for both local and Cloud
- `README.md` - Added deployment section
- `.gitignore` - Updated to exclude secrets

## Next Steps After Deployment

1. Test all features in the deployed app
2. Monitor logs for any errors
3. Share your app URL with users
4. Consider adding custom domain (if using Streamlit Cloud for Teams)

## Support Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Deployment Guide](DEPLOYMENT.md)
- [Streamlit Forums](https://discuss.streamlit.io)

