# Deployment Guide for TalentScout

This guide provides instructions for deploying the TalentScout technical interview assistant application using Streamlit Cloud.

## Prerequisites

Before deploying, ensure you have:
- A Hugging Face API key
- A GitHub account
- Your code pushed to a GitHub repository

## Deployment Steps

### 1. Prepare Your Repository

1. Make sure your repository has these files:
   - `app.py` (main application file)
   - `utils.py` (utility functions)
   - `requirements.txt` (Python dependencies)
   - `.gitignore` (to exclude sensitive files)

2. Ensure your `requirements.txt` includes:
   ```
   streamlit==1.32.0
   python-dotenv==1.0.1
   requests>=2.32.3
   huggingface-hub>=0.20.3
   ```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to `app.py`
6. Click "Deploy"

### 3. Configure Environment Variables

1. After deployment, go to your app's settings:
   - Click the three dots menu (⋮) in the top right
   - Select "Settings"
   - Scroll down to "Secrets"

2. Add your Hugging Face API key:
   ```toml
   HUGGINGFACE_API_KEY = "your_api_key_here"
   ```

### 4. Verify Deployment

1. Visit your deployed app URL (https://talentscout5484.streamlit.app/)
2. Test the application:
   - Fill in candidate information
   - Start an interview
   - Verify that questions are generated
   - Check that responses are analyzed

## Common Issues and Solutions

### 1. API Key Not Found
If you see the error "HUGGINGFACE_API_KEY not found in environment variables":
- Double-check that you've added the API key in Streamlit Cloud secrets
- Verify the key format in secrets (should be in TOML format)
- Make sure there are no extra spaces or quotes

### 2. Dependencies Issues
If you encounter dependency-related errors:
- Check your `requirements.txt` file
- Verify all required packages are listed
- Make sure version numbers are compatible

### 3. Application Errors
If the app shows errors:
- Check the Streamlit Cloud logs
- Verify your code is working locally
- Ensure all required files are in the repository

## Maintenance

### 1. Updating the Application
1. Make changes to your local code
2. Commit and push to GitHub
3. Streamlit Cloud will automatically redeploy

### 2. Monitoring
- Check the Streamlit Cloud dashboard for:
  - App status
  - Error logs
  - Usage statistics

### 3. Security
- Never commit API keys or sensitive data
- Use Streamlit Cloud secrets for sensitive information
- Regularly rotate your API keys

## Support

For deployment support:
1. Check the [Streamlit Cloud documentation](https://docs.streamlit.io/cloud)
2. Review the [Hugging Face documentation](https://huggingface.co/docs)
3. Visit the [Streamlit Community Forum](https://discuss.streamlit.io)

## Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/cloud)
- [Hugging Face API Documentation](https://huggingface.co/docs)
- [Streamlit Best Practices](https://docs.streamlit.io/knowledge-base)

