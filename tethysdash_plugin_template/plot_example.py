from intake.source import base


class PlotlyExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "plotly_example"
    visualization_args = {}  # Arguments provided from TethysDash used for processing
    visualization_group = "Example"  # Group for visualization plugin discovery
    visualization_label = "Plotly Example"  # Visualization plugin name
    visualization_type = "plotly"  # Type of visualization
    visualization_tags = [
        "example",
        "plotly",
    ]  # Tags for visualization plugin discovery
    visualization_description = "An example plugin for the plotly visualization"

    def __init__(self, metadata=None):
        super().__init__(metadata=metadata)

    def read(self):
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
