# Engine Health Model API - Deployment Guide (Render)

## Prerequisites
- GitHub account with this repository pushed
- Render account (free at https://render.com)

## Step-by-Step Deployment

### 1. **Push Code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit - Engine Health Model API"
git remote add origin https://github.com/YOUR_USERNAME/engine-health-model-api.git
git push -u origin main
```

### 2. **Create Render Account & Connect GitHub**
- Go to https://render.com
- Sign up with GitHub
- Authorize Render to access your GitHub repositories

### 3. **Create a New Web Service**
- Click **"New +"** → **"Web Service"**
- Select your GitHub repository
- Configure as follows:

| Setting | Value |
|---------|-------|
| **Name** | engine-health-api |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port 8000` |
| **Plan** | Free (or Starter if you need more resources) |

### 4. **Deploy**
- Click **"Create Web Service"**
- Render will automatically build and deploy
- You'll get a URL like: `https://engine-health-api.onrender.com`

## Testing the Deployment

Once deployed, test the API:

```bash
# Health check
curl https://engine-health-api.onrender.com/

# Make a prediction
curl -X POST https://engine-health-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "engine_rpm": 1200,
    "lub_oil_pressure": 4.5,
    "fuel_pressure": 15.0,
    "coolant_pressure": 2.5,
    "lub_oil_temp": 85.0,
    "coolant_temp": 85.0
  }'
```

## Important Notes

⚠️ **Free Tier Limitations:**
- Auto-spinning down after 15 minutes of inactivity
- Limited memory (~512MB)
- Slower performance
- For production, upgrade to Starter plan ($7/month)

📦 **Model File:**
- Ensure `engine_model.pkl` is committed to GitHub
- If it's too large (>100MB), use Git LFS or upload separately

✅ **Environment Variables:**
- Add any API keys via Render dashboard → Environment Variables

## Auto-Redeployment
Render automatically redeploys when you push to GitHub. To disable:
- Service Settings → Auto-Deploy: Off

## Local Testing Before Deployment
```bash
uvicorn app:app --reload
# Visit http://localhost:8000/docs for API documentation
```

## Troubleshooting

**"Build Failed"**
- Check logs in Render dashboard
- Verify requirements.txt is correct
- Ensure all imports work locally first

**"Service Keeps Spinning Down"**
- Upgrade from Free to Starter plan
- Or use a monitoring service to keep it alive

**"Model Not Found"**
- Commit `engine_model.pkl` to GitHub
- Check file path in `app.py`
