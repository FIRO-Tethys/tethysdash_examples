from intake.source import base


class TextExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "text_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Text Example"
    visualization_type = "text"

    def __init__(self, metadata=None):
        super(TextExample, self).__init__(metadata=metadata)

    def read(self):
        """
        Return the data for the text
        """

        return {"text": "Here is some text"}
