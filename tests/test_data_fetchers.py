"""
Tests for data fetching utilities
"""

from datetime import datetime
from src.climate_utils.data_fetchers import (
    fetch_noaa_data,
    fetch_modis_data,
    fetch_era5_data,
)


def test_fetch_noaa_data():
    """Test NOAA data fetching"""
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 12, 31)

    result = fetch_noaa_data(
        latitude=30.2672,
        longitude=-97.7431,
        start_date=start_date,
        end_date=end_date,
        radius_km=50,
    )

    assert isinstance(result, dict)
    assert "temperature" in result
    assert "precipitation" in result
    assert "wind_speed" in result


def test_fetch_modis_data():
    """Test MODIS satellite data fetching"""
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 12, 31)

    result = fetch_modis_data(
        latitude=30.2672, longitude=-97.7431, start_date=start_date, end_date=end_date
    )

    assert isinstance(result, dict)
    assert "land_surface_temp" in result
    assert "ndvi" in result


def test_fetch_era5_data():
    """Test ERA5 reanalysis data fetching"""
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 12, 31)

    result = fetch_era5_data(
        latitude=30.2672, longitude=-97.7431, start_date=start_date, end_date=end_date
    )

    assert isinstance(result, dict)
    assert "temperature_2m" in result
    assert "total_precipitation" in result
