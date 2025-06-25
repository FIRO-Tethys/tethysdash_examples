from intake.source import base


class ImageExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "image_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Image Example"
    visualization_type = "image"
    visualization_tags = [
        "example",
        "image",
    ]
    visualization_description = "An example plugin for the image visualization"

    def __init__(self, metadata=None):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return an image url
        """

        return "https://aquaveo.com/pub/media/wysiwyg/aquaveo-logo-bw.svg"
