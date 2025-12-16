# Getting Started with Climate Change Impact Predictor

This guide will help you get up and running with the Climate Change Impact Predictor project.

## Prerequisites

1. **Python 3.10+** installed on your system
2. **Outerbounds account** - Sign up at https://outerbounds.com
3. **AWS credentials** (for S3 storage and compute)
4. **API keys** for data sources:
   - NOAA CDO API token
   - NASA Earthdata account
   - Copernicus CDS API key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/amccarty/weather-prediction.git
cd weather-prediction
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Outerbounds
OUTERBOUNDS_API_KEY=your_api_key_here

# AWS
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-west-2

# Data source APIs
NOAA_CDO_TOKEN=your_noaa_token
NASA_EARTHDATA_USERNAME=your_username
NASA_EARTHDATA_PASSWORD=your_password
COPERNICUS_CDS_UID=your_uid
COPERNICUS_CDS_API_KEY=your_api_key
```

## Running the Flows

### 1. Train Initial Models

```bash
# Train models for Austin, TX region
python flows/climate_training_flow.py run \
    --region "30.2672,-97.7431,50" \
    --lookback_years 30
```

### 2. Deploy Scheduled Data Refresh

```bash
# Create the scheduled flow (runs every 6 hours)
python flows/climate_data_refresh_flow.py create
```

### 3. Deploy the API

```bash
# Deploy to staging environment
python deployments/climate-api/deploy.py run --environment staging

# Deploy to production
python deployments/climate-api/deploy.py run --environment production
```

## Testing the API

Once deployed, you can test the API endpoints:

```bash
# Health check
curl https://climate-api-staging.outerbounds.com/health

# Get predictions for Austin, TX
curl https://climate-api-staging.outerbounds.com/predictions/Austin,%20TX

# Custom location prediction
curl -X POST https://climate-api-staging.outerbounds.com/predict \
  -H "Content-Type: application/json" \
  -d '{"latitude": 30.2672, "longitude": -97.7431, "horizon_years": 10}'
```

## Viewing Results

### Metaflow UI
View flow runs and cards at:
https://ui.outerbounds.com/flows

### API Documentation
Interactive API docs (Swagger):
https://climate-api-staging.outerbounds.com/docs

### Dashboard
Interactive dashboard:
https://climate-api-staging.outerbounds.com/dashboard/Austin,%20TX

## Next Steps

- Read the [Architecture Guide](ARCHITECTURE.md)
- Explore [Data Sources](DATA_SOURCES.md)
- Learn about [Model Training](TRAINING.md)
- Customize for your regions of interest

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'metaflow'`
**Solution**: Ensure you've activated the virtual environment and installed requirements

**Issue**: API deployment fails with authentication error
**Solution**: Check that your `OUTERBOUNDS_API_KEY` is set correctly

**Issue**: Data fetching fails
**Solution**: Verify your API keys for NOAA, NASA, and Copernicus are valid

For more help, see the [FAQ](FAQ.md) or open an issue on GitHub.
