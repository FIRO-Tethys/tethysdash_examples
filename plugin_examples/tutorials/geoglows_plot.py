from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
import plotly.express as px
import json
import geoglows


class PlotlyExample(TethysDashPlugin):
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
        forecast_data = geoglows.data.forecast(int(self.river_ID))
        forecast_plot = geoglows.plots.forecast(forecast_data)
        return json.loads(forecast_plot.to_json())
