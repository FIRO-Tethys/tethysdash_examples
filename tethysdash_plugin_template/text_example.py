from intake.source import base


class TextExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "text_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Text Example"
    visualization_type = "text"
    visualization_tags = [
        "example",
        "text",
    ]
    visualization_description = "An example plugin for the text visualization"

    def __init__(self, metadata=None):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return the data for the text
        """

        return {"text": "Here is some text"}
