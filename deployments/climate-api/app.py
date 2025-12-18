"""
Climate Impact Predictor API

FastAPI application that serves climate predictions and provides
an interactive dashboard.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import json
from datetime import datetime
from metaflow import Flow, namespace
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Climate Impact Predictor API",
    description="REST API for climate change impact predictions",
    version="1.0.0"
)

# Add CORS middleware to allow web UI to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for loaded models and predictions
class ModelRegistry:
    """Manages loaded models and predictions from Metaflow flows"""

    def __init__(self):
        self.models = None
        self.metrics = None
        self.training_run_id = None
        self.predictions = None
        self.anomalies = None
        self.refresh_run_id = None
        self.last_updated = None

    def load_latest_artifacts(self):
        """Load artifacts from latest successful flow runs"""
        try:
            # Set namespace to default (or configure as needed)
            namespace(None)

            # Load training flow artifacts
            logger.info("Loading latest ClimateTrainingFlow...")
            training_flow = Flow('ClimateTrainingFlow')
            training_run = training_flow.latest_successful_run

            if training_run:
                self.models = training_run.data.models
                self.metrics = training_run.data.metrics
                self.training_run_id = training_run.id
                logger.info(f"Loaded models from training run: {self.training_run_id}")
            else:
                logger.warning("No successful ClimateTrainingFlow runs found")

            # Load refresh flow artifacts
            logger.info("Loading latest ClimateDataRefreshFlow...")
            refresh_flow = Flow('ClimateDataRefreshFlow')
            refresh_run = refresh_flow.latest_successful_run

            if refresh_run:
                self.predictions = refresh_run.data.all_predictions
                self.anomalies = refresh_run.data.all_anomalies
                self.refresh_run_id = refresh_run.id
                self.last_updated = refresh_run.data.fetch_timestamp
                logger.info(f"Loaded predictions from refresh run: {self.refresh_run_id}")
            else:
                logger.warning("No successful ClimateDataRefreshFlow runs found")

        except Exception as e:
            logger.error(f"Error loading artifacts: {e}")
            logger.warning("Metaflow client not configured - API will serve mock data")
            # Don't raise in deployment environment - gracefully degrade to mock data
            pass

# Initialize model registry
registry = ModelRegistry()

@app.on_event("startup")
async def startup_event():
    """Load artifacts on startup"""
    logger.info("Starting Climate API...")
    registry.load_latest_artifacts()

    if registry.models and registry.predictions:
        logger.info(f"✓ Loaded artifacts successfully")
        logger.info(f"  - Training run: {registry.training_run_id}")
        logger.info(f"  - Refresh run: {registry.refresh_run_id}")
    else:
        logger.warning("⚠ Metaflow artifacts not loaded - serving mock data")
        logger.info("API is ready (mock mode)")

class PredictionRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    horizon_years: int = Field(5, ge=1, le=50, description="Prediction horizon in years")

class RegionImpact(BaseModel):
    region_name: str
    current_temp: float
    predicted_temp_change: Dict[str, float]
    precipitation_change: Dict[str, float]
    extreme_event_probabilities: Dict[str, float]
    confidence_intervals: Dict[str, Dict[str, float]]
    last_updated: str

@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "Climate Impact Predictor API v1.0",
        "documentation": "/docs",
        "endpoints": {
            "predictions": "/predictions/{region_name}",
            "custom_predict": "/predict",
            "map": "/map",
            "dashboard": "/dashboard/{region_name}",
            "alerts": "/alerts",
            "compare": "/compare",
            "status": "/status"
        },
        "loaded_runs": {
            "training": registry.training_run_id,
            "refresh": registry.refresh_run_id,
            "last_updated": str(registry.last_updated) if registry.last_updated else None
        }
    }

@app.get("/status")
def get_status():
    """Get API status and loaded run information"""
    return {
        "status": "running",
        "models_loaded": registry.models is not None,
        "predictions_loaded": registry.predictions is not None,
        "training_run_id": registry.training_run_id,
        "refresh_run_id": registry.refresh_run_id,
        "last_updated": str(registry.last_updated) if registry.last_updated else None,
        "available_regions": list(registry.predictions.keys()) if registry.predictions else []
    }

@app.post("/refresh")
def refresh_artifacts():
    """Manually trigger a refresh of artifacts from Metaflow"""
    try:
        registry.load_latest_artifacts()
        return {
            "status": "success",
            "training_run_id": registry.training_run_id,
            "refresh_run_id": registry.refresh_run_id,
            "message": "Artifacts reloaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload artifacts: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "climate-api"}

@app.get("/predictions/{region_name}", response_model=RegionImpact)
def get_region_predictions(region_name: str) -> RegionImpact:
    """
    Get latest predictions for a named region

    Args:
        region_name: Name of the region (e.g., "Austin, TX")

    Returns:
        RegionImpact with climate predictions
    """
    # Check if predictions are loaded
    if registry.predictions is None:
        logger.warning("No predictions loaded, returning mock data")
        return _get_mock_predictions(region_name)

    # Look up region in predictions
    if region_name not in registry.predictions:
        # Try to find a close match (case-insensitive)
        available_regions = list(registry.predictions.keys())
        region_lower = region_name.lower()
        for available in available_regions:
            if available.lower() == region_lower:
                region_name = available
                break
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Region '{region_name}' not found. Available regions: {available_regions}"
            )

    # Get predictions from loaded artifacts
    pred_data = registry.predictions[region_name]

    return RegionImpact(
        region_name=region_name,
        current_temp=25.5,  # TODO: Get from current observations
        predicted_temp_change={
            "1_year": pred_data['temperature']['1_year'],
            "5_year": pred_data['temperature']['5_year'],
            "10_year": pred_data['temperature']['10_year']
        },
        precipitation_change={
            "1_year": pred_data['precipitation']['1_year'],
            "5_year": pred_data['precipitation']['5_year'],
            "10_year": pred_data['precipitation']['10_year']
        },
        extreme_event_probabilities=pred_data['extreme_events'],
        confidence_intervals={
            "temperature": {"lower": -0.5, "upper": 0.8},
            "precipitation": {"lower": -3.0, "upper": -1.0}
        },
        last_updated=str(registry.last_updated) if registry.last_updated else "unknown"
    )

def _get_mock_predictions(region_name: str) -> RegionImpact:
    """Return mock data when no predictions are loaded"""
    return RegionImpact(
        region_name=region_name,
        current_temp=25.5,
        predicted_temp_change={
            "1_year": 0.3,
            "5_year": 1.8,
            "10_year": 3.2
        },
        precipitation_change={
            "1_year": -2.0,
            "5_year": -8.5,
            "10_year": -15.0
        },
        extreme_event_probabilities={
            "heatwave": 0.15,
            "drought": 0.12,
            "flood": 0.08,
            "cold_snap": 0.05
        },
        confidence_intervals={
            "temperature": {"lower": -0.5, "upper": 0.8},
            "precipitation": {"lower": -3.0, "upper": -1.0}
        },
        last_updated="mock-data"
    )

@app.post("/predict", response_model=RegionImpact)
def predict_custom_location(request: PredictionRequest) -> RegionImpact:
    """
    Generate predictions for custom latitude/longitude
    
    Args:
        request: PredictionRequest with location and horizon
    
    Returns:
        RegionImpact with climate predictions
    """
    # TODO: Load models and run inference
    return RegionImpact(
        region_name=f"Custom ({request.latitude}, {request.longitude})",
        current_temp=22.0,
        predicted_temp_change={
            "1_year": 0.2,
            "5_year": 1.5,
            "10_year": 2.8
        },
        precipitation_change={
            "1_year": -1.0,
            "5_year": -5.0,
            "10_year": -10.0
        },
        extreme_event_probabilities={
            "heatwave": 0.10,
            "drought": 0.08,
            "flood": 0.06,
            "cold_snap": 0.04
        },
        confidence_intervals={
            "temperature": {"lower": -0.3, "upper": 0.5},
            "precipitation": {"lower": -2.0, "upper": -0.5}
        },
        last_updated="2024-12-15T10:00:00Z"
    )

@app.get("/map", response_class=HTMLResponse)
def get_interactive_map():
    """
    Generate interactive map with climate impacts
    
    Returns:
        HTML page with Folium map
    """
    # TODO: Create actual interactive map with folium
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Climate Impact Map</title>
    </head>
    <body>
        <h1>Climate Impact Map</h1>
        <p>Interactive map showing climate predictions by region</p>
        <p>TODO: Implement Folium map</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/dashboard/{region_name}", response_class=HTMLResponse)
def get_dashboard(region_name: str):
    """
    Interactive dashboard with charts for a region
    
    Args:
        region_name: Name of the region
    
    Returns:
        HTML page with Plotly charts
    """
    # TODO: Create actual dashboard with plotly
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Climate Dashboard - {region_name}</title>
    </head>
    <body>
        <h1>Climate Dashboard: {region_name}</h1>
        <p>Interactive charts showing climate trends and predictions</p>
        <p>TODO: Implement Plotly dashboard</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/alerts")
def get_active_alerts():
    """
    Get current climate anomaly alerts

    Returns:
        List of active alerts
    """
    # Check if anomalies are loaded
    if registry.anomalies is None:
        logger.warning("No anomalies loaded, returning empty list")
        return {
            "alerts": [],
            "count": 0,
            "message": "No anomaly data loaded yet"
        }

    # Convert anomalies to alert format
    alerts = []
    for anomaly in registry.anomalies:
        severity = "high" if anomaly['probability'] > 0.25 else "medium" if anomaly['probability'] > 0.15 else "low"
        alerts.append({
            "type": anomaly['type'],
            "region": anomaly['region'],
            "probability": anomaly['probability'],
            "severity": severity,
            "issued_at": str(registry.last_updated) if registry.last_updated else "unknown"
        })

    return {
        "alerts": alerts,
        "count": len(alerts),
        "last_updated": str(registry.last_updated) if registry.last_updated else None
    }

@app.get("/compare")
def compare_regions(
    region1: str = Query(..., description="First region name"),
    region2: str = Query(..., description="Second region name")
):
    """
    Compare climate impacts between two regions
    
    Args:
        region1: Name of first region
        region2: Name of second region
    
    Returns:
        Comparison data
    """
    # TODO: Load predictions and generate comparison
    return {
        "region1": region1,
        "region2": region2,
        "comparison": {
            "temperature_change_diff": 0.5,
            "precipitation_change_diff": -3.0,
            "higher_risk_region": region1
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
