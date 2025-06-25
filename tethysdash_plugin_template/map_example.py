from intake.source import base


class MapExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "map_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Map Example"
    visualization_type = "map"
    visualization_tags = [
        "example",
        "map",
    ]
    visualization_description = "An example plugin for the map visualization"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):

        return {
            "baseMap": "https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer",
            "layers": [
                {
                    "configuration": {
                        "type": "ImageLayer",
                        "props": {
                            "name": "asda",
                            "source": {
                                "type": "ESRI Image and Map Service",
                                "props": {
                                    "url": "https://maps.water.noaa.gov/server/rest/services/rfc/rfc_max_forecast/MapServer"
                                },
                            },
                        },
                    },
                    "attributeVariables": {
                        "Max Status - Forecast Trend": {"nws_lid": "Location"}
                    },
                    "legend": {
                        "title": "a title",
                        "items": [
                            {
                                "label": "Major Flood",
                                "color": "#cc33ff",
                            },
                            {
                                "label": "Moderate Flood",
                                "color": "#ff0000",
                            },
                            {
                                "label": "Minor Flood",
                                "color": "#ff9900",
                            },
                            {
                                "label": "Action",
                                "color": "#ffff00",
                            },
                            {
                                "label": "No Flood",
                                "color": "#00ff00",
                            },
                        ],
                    },
                },
            ],
            "layerControl": True,
        }
