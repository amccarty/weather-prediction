"""
Climate Utils Package

Shared utility functions for climate data processing and analysis.
"""

from .data_fetchers import fetch_noaa_data, fetch_modis_data, fetch_era5_data
from .feature_engineering import (
    create_temperature_features,
    create_precipitation_features,
)
from .model_utils import load_model, save_model, evaluate_model

__all__ = [
    "fetch_noaa_data",
    "fetch_modis_data",
    "fetch_era5_data",
    "create_temperature_features",
    "create_precipitation_features",
    "load_model",
    "save_model",
    "evaluate_model",
]

__version__ = "0.1.0"
