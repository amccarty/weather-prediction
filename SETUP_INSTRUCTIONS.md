# Setup Instructions for GitHub Repository

## Project Created Successfully! 🎉

The `weather-prediction` project structure has been created locally at `/tmp/weather-prediction`.

## Next Steps to Push to GitHub

### 1. Create the GitHub Repository

You need to create a new repository on GitHub at: **github.com/amccarty/weather-prediction**

Option A: Via GitHub Web Interface
1. Go to https://github.com/new
2. Repository name: `weather-prediction`
3. Description: "Climate Change Impact Predictor using ML and public datasets"
4. Choose Public or Private
5. **Do NOT** initialize with README, .gitignore, or license (we have these already)
6. Click "Create repository"

Option B: Via GitHub CLI
```bash
gh repo create amccarty/weather-prediction --public --description "Climate Change Impact Predictor using ML and public datasets"
```

### 2. Push the Local Repository to GitHub

From the project directory:

```bash
cd /tmp/weather-prediction

# Set the remote URL
git remote add origin https://github.com/amccarty/weather-prediction.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 3. Configure GitHub Secrets

Go to your repository settings → Secrets and variables → Actions

Add these secrets:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `OUTERBOUNDS_API_KEY` - Your Outerbounds API key

### 4. Enable GitHub Actions

The CI/CD workflow is already configured in `.github/workflows/ci.yml`.
It will automatically run on:
- Push to `main` branch (production deployment)
- Push to `develop` branch (staging deployment)
- Pull requests to `main`

## Project Structure Overview

```
weather-prediction/
├── .github/workflows/     # CI/CD configuration
│   └── ci.yml            # GitHub Actions workflow
├── data/                 # Data assets
│   └── climate-observations/
├── deployments/          # Application deployments
│   └── climate-api/      # FastAPI application
├── docs/                 # Documentation
│   └── GETTING_STARTED.md
├── flows/                # Metaflow workflows
│   ├── climate_training_flow.py
│   └── climate_data_refresh_flow.py
├── models/               # Model assets
│   ├── temperature-predictor/
│   ├── precipitation-predictor/
│   └── extreme-events-classifier/
├── src/                  # Shared utilities
│   └── climate_utils/
├── tests/                # Test suite
├── obproject.toml        # Outerbounds configuration
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT License
└── README.md            # Project documentation
```

## What This Project Includes

### ✅ Metaflow Flows
1. **ClimateTrainingFlow** - Train ML models on historical climate data
   - Uses GPU resources
   - Parallel data fetching from NOAA, MODIS, ERA5
   - Trains 3 models: Transformer, LSTM, XGBoost

2. **ClimateDataRefreshFlow** - Scheduled data refresh (cron: every 6 hours)
   - Fetches latest observations
   - Runs inference on new data
   - Detects anomalies and sends alerts

### ✅ Deployment
- **FastAPI Application** with multiple endpoints:
  - `/predictions/{region}` - Regional predictions
  - `/predict` - Custom location predictions
  - `/map` - Interactive map
  - `/dashboard/{region}` - Dashboard with charts
  - `/alerts` - Active climate alerts
  - `/compare` - Region comparison

### ✅ GitHub Actions CI/CD
- Automated testing on PRs
- Linting with Black and Flake8
- Flow validation
- Automatic deployment to staging/production
- Release creation

### ✅ Documentation
- Comprehensive README
- Getting Started guide
- Data and model documentation

## Development Workflow

### Local Development
```bash
# Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/

# Lint code
black src/ flows/ deployments/
flake8 src/ flows/ deployments/

# Run a flow locally
python flows/climate_training_flow.py run
```

### Creating a Feature Branch
```bash
git checkout -b feature/my-new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push origin feature/my-new-feature
# Create PR on GitHub
```

## Important Notes

1. **API Keys Required**: You'll need to sign up for:
   - NOAA Climate Data Online API
   - NASA Earthdata account
   - Copernicus CDS account

2. **GPU Costs**: The training flow uses GPU resources. Monitor costs in Outerbounds dashboard.

3. **Scheduled Flow**: The data refresh flow is configured to run every 6 hours. Adjust in `obproject.toml` if needed.

4. **Placeholder Code**: The current implementation has placeholder data fetching and model training code. You'll need to implement:
   - Actual API calls to NOAA, MODIS, ERA5
   - Real model training logic
   - Feature engineering
   - Model persistence and loading

## Resources

- [Metaflow Documentation](https://docs.metaflow.org)
- [Outerbounds Documentation](https://docs.outerbounds.com)
- [NOAA CDO API](https://www.ncdc.noaa.gov/cdo-web/webservices/v2)
- [NASA Earthdata](https://earthdata.nasa.gov/)
- [Copernicus CDS](https://cds.climate.copernicus.eu/)

## Support

For questions or issues:
- Open a GitHub issue
- Check the documentation in `docs/`
- Contact Outerbounds support

---

**Next Action**: Create the GitHub repository and push the code!
