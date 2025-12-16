# Climate Change Impact Predictor 🌍🌡️

A production ML system that combines historical climate data, satellite imagery, and weather patterns to predict localized climate impacts for specific regions.

## Project Overview

This project uses Metaflow/Outerbounds to build an end-to-end climate prediction pipeline that:
- Fetches data from public sources (NOAA, NASA MODIS, ERA5)
- Trains multiple ML models (Transformers for temperature, LSTM for precipitation, XGBoost for extreme events)
- Runs scheduled data refreshes every 6 hours
- Deploys a REST API and interactive dashboard
- Uses GPUs for model training and inference

## Architecture

The project consists of three main flows:

1. **ClimateTrainingFlow** - Initial model training on historical data
2. **ClimateDataRefreshFlow** - Scheduled data ingestion (cron: every 6 hours)
3. **ClimateAPIDeployment** - Production API and dashboard deployment

## Project Structure

```
weather-prediction/
├── .github/workflows/          # GitHub Actions for CI/CD
├── data/                       # Data assets and schemas
│   └── climate-observations/
├── deployments/                # Application deployments
│   └── climate-api/
├── docs/                       # Documentation
├── flows/                      # Metaflow workflows
├── models/                     # Model assets
│   ├── temperature-predictor/
│   ├── precipitation-predictor/
│   └── extreme-events-classifier/
├── src/                        # Shared utility code
│   └── climate_utils/
├── obproject.toml              # Outerbounds project configuration
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.9+
- Outerbounds account with API key
- AWS credentials (for S3 storage)

### Installation

```bash
# Clone the repository
git clone https://github.com/amccarty/weather-prediction.git
cd weather-prediction

# Install dependencies
pip install -r requirements.txt

# Configure Outerbounds
export OUTERBOUNDS_API_KEY=your_api_key_here
```

### Running the Flows

```bash
# Train initial models
python flows/climate_training_flow.py run --region "30.2672,-97.7431,50"

# Start scheduled data refresh (deploys to cloud)
python flows/climate_data_refresh_flow.py create

# Deploy the API
python flows/climate_api_deployment.py create
```

## Data Sources

- **NOAA Climate Data Online (CDO)**: Historical weather station data
- **NASA MODIS**: Satellite imagery (land surface temperature, NDVI)
- **ERA5 (Copernicus)**: Global climate reanalysis
- **USGS Earth Explorer**: Land use/land cover changes

## Models

### Temperature Predictor
- Architecture: Transformer-based time series model
- Inputs: Historical temps, satellite data, geographic features
- Outputs: Temperature predictions at 1, 5, and 10 year horizons

### Precipitation Predictor
- Architecture: LSTM
- Captures seasonal cycles and trend changes
- Outputs: Precipitation pattern predictions

### Extreme Events Classifier
- Architecture: XGBoost
- Predicts probability of: heat waves, droughts, floods, cold snaps

## API Endpoints

- `GET /predictions/{region_name}` - Get latest predictions for a region
- `POST /predict` - Generate predictions for custom lat/lon
- `GET /map` - Interactive map with climate impacts
- `GET /dashboard/{region_name}` - Interactive dashboard with charts
- `GET /alerts` - Current climate anomaly alerts
- `GET /compare` - Compare climate impacts between regions

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black src/ flows/ deployments/
flake8 src/ flows/ deployments/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- NOAA for climate data access
- NASA for satellite imagery
- Outerbounds for ML infrastructure
- Metaflow community
