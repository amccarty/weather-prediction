"""
Climate Impact Predictor API

FastAPI application that serves climate predictions from Metaflow flows.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from metaflow import Flow, namespace
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Climate Impact Predictor API",
    description="REST API for climate change impact predictions",
    version="1.0.0",
)

# Add CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ModelRegistry:
    """Manages loaded models and predictions from Metaflow flows"""

    def __init__(self):
        self.models = None
        self.metrics = None
        self.predictions = None
        self.anomalies = None
        self.last_updated = None

    def load_latest_artifacts(self):
        """Load artifacts from latest successful flow runs"""
        try:
            namespace(None)

            # Load training flow artifacts
            logger.info("Loading ClimateTrainingFlow...")
            training_flow = Flow("ClimateTrainingFlow")
            training_run = training_flow.latest_successful_run

            if training_run:
                self.models = training_run.data.models
                self.metrics = training_run.data.metrics
                logger.info(f"✓ Loaded models from run {training_run.id}")

            # Load refresh flow artifacts
            logger.info("Loading ClimateDataRefreshFlow...")
            refresh_flow = Flow("ClimateDataRefreshFlow")
            refresh_run = refresh_flow.latest_successful_run

            if refresh_run:
                self.predictions = refresh_run.data.all_predictions
                self.anomalies = refresh_run.data.all_anomalies
                self.last_updated = refresh_run.data.fetch_timestamp
                logger.info(f"✓ Loaded predictions from run {refresh_run.id}")

        except Exception as e:
            logger.warning(f"Could not load artifacts: {e}")
            logger.info("Running in mock data mode")


registry = ModelRegistry()


@app.on_event("startup")
async def startup_event():
    """Load artifacts on startup"""
    logger.info("Starting Climate API...")
    registry.load_latest_artifacts()


@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "Climate Impact Predictor API v1.0",
        "documentation": "/docs",
        "endpoints": {
            "predictions": "/predictions/{region_name}",
            "alerts": "/alerts",
            "status": "/status",
        },
    }


@app.get("/status")
def get_status():
    """Get API status and loaded data information"""
    return {
        "status": "running",
        "models_loaded": registry.models is not None,
        "predictions_loaded": registry.predictions is not None,
        "last_updated": str(registry.last_updated) if registry.last_updated else None,
        "available_regions": (
            list(registry.predictions.keys()) if registry.predictions else []
        ),
    }


@app.get("/predictions/{region_name}")
def get_region_predictions(region_name: str):
    """
    Get climate predictions for a specific region

    Args:
        region_name: Name of the region (e.g., "Austin, TX")

    Returns:
        Predictions including temperature, precipitation, and extreme events
    """
    # Check if predictions are loaded
    if registry.predictions is None:
        logger.warning("No predictions loaded, returning mock data")
        return _get_mock_predictions(region_name)

    # Look up region
    if region_name not in registry.predictions:
        # Try case-insensitive match
        available_regions = list(registry.predictions.keys())
        region_lower = region_name.lower()
        for available in available_regions:
            if available.lower() == region_lower:
                region_name = available
                break
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Region '{region_name}' not found. Available: {available_regions}",
            )

    pred_data = registry.predictions[region_name]

    return {
        "region_name": region_name,
        "predicted_temp_change": pred_data["temperature"],
        "predicted_precip_change": pred_data["precipitation"],
        "extreme_event_probabilities": pred_data["extreme_events"],
        "last_updated": str(registry.last_updated) if registry.last_updated else "unknown",
    }


def _get_mock_predictions(region_name: str):
    """Return mock data when no predictions are loaded"""
    return {
        "region_name": region_name,
        "predicted_temp_change": {"1_year": 0.3, "5_year": 1.8, "10_year": 3.2},
        "predicted_precip_change": {"1_year": -2.0, "5_year": -8.5, "10_year": -15.0},
        "extreme_event_probabilities": {
            "heatwave": 0.15,
            "drought": 0.12,
            "flood": 0.08,
            "cold_snap": 0.05,
        },
        "last_updated": "mock-data",
    }


@app.get("/alerts")
def get_active_alerts():
    """
    Get current climate anomaly alerts

    Returns:
        List of active alerts with severity and probability
    """
    if registry.anomalies is None:
        return {"alerts": [], "count": 0}

    alerts = []
    for anomaly in registry.anomalies:
        severity = "high" if anomaly["probability"] > 0.25 else "medium"
        alerts.append(
            {
                "type": anomaly["type"],
                "region": anomaly["region"],
                "probability": anomaly["probability"],
                "severity": severity,
            }
        )

    return {
        "alerts": alerts,
        "count": len(alerts),
        "last_updated": str(registry.last_updated) if registry.last_updated else None,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
