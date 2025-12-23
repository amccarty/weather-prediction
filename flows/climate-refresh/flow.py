"""
Climate Data Refresh Flow

Scheduled flow that fetches latest climate observations and generates predictions.
"""

from metaflow import step
from obproject import ProjectFlow
from datetime import datetime


class ClimateDataRefreshFlow(ProjectFlow):
    """
    Fetch latest climate data and generate predictions for all regions
    """

    @step
    def start(self):
        """Initialize data refresh"""
        self.fetch_timestamp = datetime.now()
        print(f"Data refresh triggered at {self.fetch_timestamp}")

        # Define the 4 regions to monitor
        self.regions = [
            {"name": "Austin, TX", "lat": 30.2672, "lon": -97.7431},
            {"name": "Miami, FL", "lat": 25.7617, "lon": -80.1918},
            {"name": "Phoenix, AZ", "lat": 33.4484, "lon": -112.0740},
            {"name": "Seattle, WA", "lat": 47.6062, "lon": -122.3321},
        ]

        self.next(self.fetch_and_predict, foreach="regions")

    @step
    def fetch_and_predict(self):
        """Fetch data and generate predictions for each region"""
        region = self.input
        print(f"Processing {region['name']}...")

        # TODO: Fetch actual weather data from APIs
        self.current_weather = {
            "temperature": 25.5,
            "precipitation": 0.0,
            "wind_speed": 12.3,
        }

        # TODO: Load trained models and run inference
        self.predictions = {
            "temperature": {"1_year": 26.2, "5_year": 27.8, "10_year": 29.1},
            "precipitation": {"1_year": 850, "5_year": 820, "10_year": 790},
            "extreme_events": {
                "heatwave": 0.15,
                "drought": 0.12,
                "flood": 0.08,
                "cold_snap": 0.05,
            },
        }

        # Detect high-risk anomalies
        self.anomalies = []
        if self.predictions["extreme_events"]["heatwave"] > 0.20:
            self.anomalies.append(
                {
                    "type": "heatwave",
                    "probability": self.predictions["extreme_events"]["heatwave"],
                    "region": region["name"],
                }
            )

        self.next(self.join)

    @step
    def join(self, inputs):
        """Aggregate predictions from all regions"""
        print("Aggregating predictions from all regions...")

        # Convert inputs to list to get length
        inputs_list = list(inputs)

        self.fetch_timestamp = inputs_list[0].fetch_timestamp
        self.all_predictions = {}
        self.all_anomalies = []

        for input_data in inputs_list:
            region_name = input_data.input["name"]
            self.all_predictions[region_name] = input_data.predictions

            if input_data.anomalies:
                self.all_anomalies.extend(input_data.anomalies)

        print(f"Processed {len(inputs_list)} regions")
        print(f"Detected {len(self.all_anomalies)} anomalies")

        self.next(self.end)

    @step
    def end(self):
        """Complete data refresh"""
        print(f"Data refresh complete at {datetime.now()}")
        print(f"Predictions available for {len(self.all_predictions)} regions")


if __name__ == "__main__":
    ClimateDataRefreshFlow()
