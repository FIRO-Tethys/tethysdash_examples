from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class VariableInputExample(TethysDashPlugin):
    name = "variable_input_example"
    args = {}
    group = "Example"
    label = "Variable Input Example"
    type = "variable_input"
    tags = [
        "example",
        "variable input",
    ]
    description = "An example plugin for the variable input visualization"

    def run(self):
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
