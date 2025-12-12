# Deploy to Render - Step by Step Guide

## Prerequisites

1. GitHub account with your code pushed (✅ Already done!)
2. Render account (sign up at https://render.com)

## Deployment Steps

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. **Click "New +"** → Select **"Web Service"**

2. **Connect Repository:**
   - Select your GitHub account
   - Choose repository: `Rag_chatbot_empiric`
   - Click "Connect"

3. **Configure Service:**
   - **Name:** `empiric-chatbot` (or any name you prefer)
   - **Region:** Choose closest to you (e.g., Singapore, US East)
   - **Branch:** `main`
   - **Root Directory:** Leave empty (root)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Environment Variables:**
   Click "Add Environment Variable" and add:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Your Gemini API key (AIzaSyCv9s8507542LykxMYQq806bi_GNPfqSgE)

5. **Plan Selection:**
   - Start with **Free** plan (can upgrade later)
   - Note: Free tier spins down after 15 minutes of inactivity

6. **Click "Create Web Service"**

### Step 3: Wait for Deployment

- Render will:
  1. Clone your repository
  2. Install dependencies (this may take 5-10 minutes)
  3. Build the vector store (first time only, 10-60 seconds)
  4. Start the web service

### Step 4: Access Your Chatbot

Once deployed, you'll get a URL like:
```
https://empiric-chatbot.onrender.com
```

## Important Notes

### Free Tier Limitations:
- ⚠️ **Spins down after 15 min inactivity** - First request after spin-down takes 30-60 seconds
- ✅ **Unlimited requests** when active
- ✅ **512 MB RAM** (should be enough)
- ✅ **Free SSL** certificate

### Upgrade Options:
- **Starter Plan ($7/month):** No spin-down, always on
- **Standard Plan ($25/month):** More resources, better performance

### First Deployment:
- First build may take 10-15 minutes (downloading models)
- Vector store will be built automatically
- Subsequent deployments are faster (2-5 minutes)

## Troubleshooting

### Build Fails:
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility

### App Crashes:
- Check logs in Render dashboard
- Verify `GEMINI_API_KEY` is set correctly
- Check if `Formated_data/` folder exists with .txt files

### Slow Response:
- First request after spin-down is slow (normal for free tier)
- Consider upgrading to Starter plan for always-on

## Environment Variables in Render

To update environment variables later:
1. Go to your service in Render dashboard
2. Click "Environment" tab
3. Add/Edit variables
4. Save changes (service will restart)

## Custom Domain (Optional)

1. Go to your service → Settings
2. Scroll to "Custom Domains"
3. Add your domain
4. Follow DNS configuration instructions

## Monitoring

- View logs in real-time from Render dashboard
- Set up alerts for errors
- Monitor usage and performance

## Cost Estimate

- **Free Tier:** $0/month (with limitations)
- **Starter:** $7/month (always on, no spin-down)
- **Standard:** $25/month (better performance)

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com

