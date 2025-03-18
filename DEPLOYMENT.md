# Deployment Guide for TalentScout

This guide provides instructions for deploying the TalentScout technical interview assistant application. The application can be deployed using various platforms, but this guide focuses on the most straightforward and reliable methods.

## Prerequisites

Before deploying, ensure you have:
- A Hugging Face API key
- A GitHub account (for version control)
- Access to a deployment platform (Streamlit Cloud, Heroku, or similar)

## Deployment Options

### 1. Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy this application since it's built with Streamlit.

#### Steps:
1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and branch
6. Set the main file path to `app.py`
7. Add your environment variables:
   - Go to "Secrets" in your app settings
   - Add your Hugging Face API key:
     ```toml
     HUGGINGFACE_API_KEY = "your_api_key_here"
     ```
8. Click "Deploy"

