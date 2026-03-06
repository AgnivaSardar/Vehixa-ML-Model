# Engine Health Model API - Deployment Guide (Render)

## Prerequisites
- GitHub account with this repository pushed
- Render account (free at https://render.com)

## ✅ What's Fixed
- **Removed Git LFS**: No more large file tracking issues
- **Build-time Training**: `train_model.py` automatically trains the model during Render deployment
- **Auto-Generated Model**: `engine_model.pkl` is created fresh on each deploy (no sync issues)

## Step-by-Step Deployment

### 1. **Code is Already Pushed** ✓
Your latest commit fixed the Git LFS issue. The model will be trained automatically.

### 2. **Create/Update on Render**
- Go to https://render.com home
- If you have an existing failed deployment:
  - Go to your service → **"Settings"** → **"Delete Service"**
  - Then create a new one
- Click **"New +"** → **"Web Service"**
- Select your GitHub repository: `Vehixa-ML-Model`
- Configure as follows:

| Setting | Value |
|---------|-------|
| **Name** | engine-health-api |
| **Environment** | Python 3 |
| **Region** | US East (or closest) |
| **Branch** | main |
| **Environment Variable** | `PYTHON_VERSION=3.11.11` |
| **Build Command** | `pip install -r requirements.txt && python train_model.py` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port 8000` |
| **Plan** | Free |

> If this is an existing Render service, set `PYTHON_VERSION=3.11.11` in **Environment** and trigger a **Manual Deploy**.

### 3. **Deploy**
- Click **"Create Web Service"**
- Render will:
  1. Install dependencies
  2. Train the RandomForest model (2-3 min)
  3. Start the FastAPI server
- You'll get a URL: `https://engine-health-api.onrender.com`

## Testing the Deployment

```bash
# Health check
curl https://your-service.onrender.com/

# Make a prediction
curl -X POST https://your-service.onrender.com/predict \
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

## Expected First Deploy Output

```
==> Building...
==> Step 1: Installing dependencies
pip install -r requirements.txt
...
Successfully installed scikit-learn, pandas, numpy, ...

==> Step 2: Training model
python train_model.py
DataFrame loaded and columns cleaned...
RandomForestClassifier model trained successfully...
✓ Model trained and saved as engine_model.pkl

==> Starting service
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Important Notes

⚠️ **Free Tier Limitations:**
- Auto-spins down after 15 mins of inactivity
- Limited memory (~512MB) - training takes 2-3 min
- Slower performance
- For production, upgrade to **Starter ($7/month)** or higher

✅ **Model Training:**
- `train_model.py` runs during each build
- Uses the same `engine_data.csv` included in the repo
- Takes ~2-3 minutes on Render servers
- Model is fresh and ready on each deployment

🔄 **Auto-Redeployment:**
- New commits to `main` branch auto-trigger redeployment
- Model gets retrained automatically

## Troubleshooting

**"Build Failed - ModuleNotFoundError"**
- Check `requirements.txt` has all dependencies
- Run locally: `pip install -r requirements.txt && python train_model.py`

**"pandas/_libs/... _PyLong_AsByteArray ... too few arguments"**
- Cause: Render selected Python 3.14, while pinned package versions expect Python 3.11 wheels.
- Fix: set `PYTHON_VERSION=3.11.11` in Render service Environment, then clear build cache and redeploy.

**"Model training timeout"**
- If training takes >10 min, upgrade to Starter plan
- Or reduce dataset size in `train_model.py`

**"Service keeps spinning down"**
- Free tier limitation
- Use a monitoring service (e.g., UptimeRobot) to ping it every 10 min
- Or upgrade plan

**"Prediction returns 404"**
- Ensure deployment completed successfully
- Check if model was created: look for "✓ Model trained" in logs
- Check your JSON payload matches required fields

## Local Testing Before Deployment

```bash
# Train model locally
python train_model.py

# Test API
uvicorn app:app --reload

# Visit: http://localhost:8000/docs (interactive API docs)
```

## File Structure

```
.
├── app.py                    # FastAPI application
├── train_model.py            # Training script (runs at build time)
├── vehicle_health_analytics.py  # Original training code
├── engine_data.csv           # Training dataset
├── requirements.txt          # Python dependencies
├── runtime.txt               # Python runtime pin for buildpacks
├── .python-version           # Python runtime pin for pyenv-based builders
├── render.yaml               # Render configuration
├── Procfile                  # Heroku-compatible config
├── README.md
└── Vehicle_health.ipynb      # Jupyter notebook for analysis
```

