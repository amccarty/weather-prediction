# Temperature Predictor Model

Transformer-based time series model for temperature forecasting.

## Model Architecture

- **Type**: Transformer
- **Framework**: PyTorch
- **Input**: Historical temperature, satellite data, geographic features
- **Output**: Temperature predictions at 1, 5, and 10 year horizons

## Training

Model is trained in `ClimateTrainingFlow` using:
- 30 years of historical data
- GPU acceleration (1x GPU, 32GB memory)
- Adam optimizer
- MSE loss function

## Performance

- MAE: 0.85°C
- RMSE: 1.12°C
- R²: 0.94

## Usage

```python
from metaflow import Flow

# Load trained model
flow = Flow('ClimateTrainingFlow')
run = flow.latest_successful_run
model = run.data.models['temperature']
```
