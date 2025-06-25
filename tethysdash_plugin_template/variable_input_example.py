from intake.source import base


class VariableInputExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "variable_input_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Variable Input Example"
    visualization_type = "variable_input"
    visualization_tags = [
        "example",
        "variable input",
    ]
    visualization_description = "An example plugin for the variable input visualization"

    def __init__(self, metadata=None):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return the data for the text
        """
        layer_names = [
            {"label": "Observed River Stage", "value": 0},
            {"label": "River Stages 24 Hour Forecast", "value": 1},
        ]

        return {
            "variable_name": "Layer Name",
            "initial_value": "",
            "variable_options_source": layer_names,
        }
