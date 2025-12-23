# Climate Change Impact Predictor 🌍

A simplified ML system that predicts localized climate impacts for specific regions using Metaflow and Outerbounds.

## Project Overview

This project demonstrates an end-to-end climate prediction pipeline:
- **Training Flow**: Trains ML models on historical climate data (temperature, precipitation, extreme events)
- **Refresh Flow**: Fetches latest observations and generates predictions for 4 US regions
- **API**: REST API serving predictions from Metaflow flow runs
- **Dashboard**: Streamlit web UI for visualizing predictions

## Regions

The system monitors 4 major US cities:
- Austin, TX
- Miami, FL
- Phoenix, AZ
- Seattle, WA

## Project Structure

```
climate-prediction/
├── .github/workflows/      # GitHub Actions deployment
│   └── deploy.yml
├── deployments/            # Application deployments
│   ├── climate-api/       # FastAPI REST API
│   │   ├── app.py
│   │   ├── config.yml
│   │   └── requirements.txt
│   └── climate-ui/        # Streamlit dashboard
│       ├── app.py
│       ├── config.yml
│       └── requirements.txt
├── flows/                  # Metaflow workflows
│   ├── climate_training_flow.py
│   └── climate_data_refresh_flow.py
├── tests/                  # Tests
├── obproject.toml         # Outerbounds project config
├── requirements.txt       # Project dependencies
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.10+
- Outerbounds account
- GitHub repository connected to Outerbounds platform

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/climate-prediction.git
cd climate-prediction

# Install dependencies
pip install -r requirements.txt
```

### Running Flows Locally

```bash
# Run training flow
python flows/climate_training_flow.py run

# Run refresh flow
python flows/climate_data_refresh_flow.py run
```

### Running API Locally

```bash
cd deployments/climate-api
uvicorn app:app --reload --port 8000
```

Visit http://localhost:8000/docs for API documentation.

### Running Dashboard Locally

```bash
cd deployments/climate-ui
streamlit run app.py --server.port 8001
```

Visit http://localhost:8001 for the dashboard.

## Deployment

The project automatically deploys to Outerbounds when pushed to the `main` branch via GitHub Actions:

1. Tests run automatically
2. Project deploys to Outerbounds platform
3. Flows and apps become available on the platform

## API Endpoints

- `GET /` - API information
- `GET /status` - API status and loaded data
- `GET /predictions/{region_name}` - Get predictions for a region
- `GET /alerts` - Get active climate alerts

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Flow Development

Flows use placeholder data and TODOs for actual implementation:
- TODO: Implement actual data fetching from NOAA, MODIS, ERA5
- TODO: Implement actual model training
- TODO: Implement actual inference

## Tech Stack

- **Metaflow**: Workflow orchestration
- **FastAPI**: REST API framework
- **Streamlit**: Dashboard framework
- **Pandas**: Data manipulation
- **Outerbounds**: ML platform for deployment

## License

MIT License
