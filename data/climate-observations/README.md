# Climate Observations Data

This directory contains climate observation data assets tracked by Metaflow.

## Data Sources

- **NOAA CDO**: Historical weather station data
- **NASA MODIS**: Satellite imagery composites
- **ERA5**: Climate reanalysis data

## Data Schema

Climate observations are stored with the following schema:

```
{
  "timestamp": "ISO 8601 datetime",
  "latitude": float,
  "longitude": float,
  "temperature": float (°C),
  "precipitation": float (mm),
  "wind_speed": float (m/s),
  "land_surface_temp": float (°C),
  "ndvi": float (0-1),
  "surface_pressure": float (hPa),
  "solar_radiation": float (W/m²)
}
```

## Data Access

Data is stored in S3 and accessed via Metaflow data artifacts:

```python
from metaflow import Flow

# Load latest data
flow = Flow('ClimateDataRefreshFlow')
run = flow.latest_successful_run
data = run.data.combined_data
```
