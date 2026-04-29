from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class PlotlyExample(TethysDashPlugin):
    name = "plotly_example"
    group = "Example"  # Group for visualization plugin discovery
    label = "Plotly Example"  # Visualization plugin name
    type = "plotly"  # Type of visualization
    tags = [
        "example",
        "plotly",
    ]  # Tags for visualization plugin discovery
    description = "An example plugin for the plotly visualization"

    def run(self):
        """
        Return plotly information
        """
        data = [
            {
                "type": "scatter",
                "x": [1, 2, 3],
                "y": [3, 1, 6],
            },
        ]

        layout = {
            "title": "simple example",
        }

        return {"data": data, "layout": layout}
