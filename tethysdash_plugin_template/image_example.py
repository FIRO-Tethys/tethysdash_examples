from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class ImageExample(TethysDashPlugin):
    name = "image_example"
    args = {}
    group = "Example"
    label = "Image Example"
    type = "image"
    tags = [
        "example",
        "image",
    ]
    description = "An example plugin for the image visualization"

    def run(self):
        """
        Return an image url
        """

        return "https://aquaveo.com/pub/media/wysiwyg/aquaveo-logo-bw.svg"
