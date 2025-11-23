# Environment Setup Instructions

## Required Environment Variable

This application requires a Firecrawl API key to function.

### Step 1: Get Your API Key

1. Visit [https://firecrawl.dev](https://firecrawl.dev)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key

### Step 2: Create .env File

Create a file named `.env` in the project root directory with the following content:

```
FIRECRAWL_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with the API key you copied from Firecrawl.

### Example .env File

```
FIRECRAWL_API_KEY=fc-1234567890abcdefghijklmnopqrstuvwxyz
```

### Important Notes

- Never commit your `.env` file to version control
- Keep your API key secure and private
- The `.env` file should be in the same directory as `st.py`

### Troubleshooting

If you see the error "FIRECRAWL_API_KEY not set":
1. Make sure the `.env` file exists in the project root
2. Check that the file is named exactly `.env` (not `.env.txt` or `env`)
3. Verify the API key is correctly formatted (no extra spaces or quotes)
4. Restart the application after creating/modifying `.env`

