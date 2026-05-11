from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
import requests


class GeoGLOWSForecastPlot(TethysDashPlugin):
    name = "geoglows_forecast_plot"
    group = "Tutorials"
    label = "GeoGLOWS Forecast Plot"
    type = "plotly"
    tags = [
        "example",
        "plotly",
        "tutorial",
        "geoglows",
    ]
    description = "A GeoGLOWS forecast plot for the GeoGLOWS tutorial"
    args = {"river_ID": "number"}

    def run(self):
        """
        Return plotly information
        """
        self.send_update("Loading forecast data from GeoGLOWS API...")
        url = f"https://geoglows.ecmwf.int/api/v2/forecast/{self.river_ID}?format=json"
        response = requests.get(url)
        forecast_data = response.json()

        self.send_update("Processing forecast data...")
        data = [
            {
                "type": "scatter",
                "x": forecast_data["datetime"],
                "y": forecast_data["flow_uncertainty_lower"],
                "name": "Lower Uncertainty",
                "line": {"color": "lightblue"},
            },
            {
                "type": "scatter",
                "x": forecast_data["datetime"],
                "y": forecast_data["flow_uncertainty_upper"],
                "name": "Upper Uncertainty",
                "line": {"color": "lightblue"},
                "fill": "tonexty",
                "fillcolor": "lightblue",
            },
            {
                "type": "scatter",
                "x": forecast_data["datetime"],
                "y": forecast_data["flow_median"],
                "name": "Median Forecast",
                "line": {"color": "darkblue"},
            },
        ]

        layout = {
            "title": f"GeoGLOWS Forecast ({self.river_ID})",
        }

        config = {"displayModeBar": True}

        return {"data": data, "layout": layout, "config": config}
