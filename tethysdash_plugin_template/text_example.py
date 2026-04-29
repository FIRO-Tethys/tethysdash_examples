from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class TextExample(TethysDashPlugin):
    name = "text_example"
    args = {}
    group = "Example"
    label = "Text Example"
    type = "text"
    tags = [
        "example",
        "text",
    ]
    description = "An example plugin for the text visualization"

    def run(self):
        """
        Return the data for the text
        """

        return {"text": "Here is some text"}
