from intake.source import base


class MapLayerExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "map_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Map Layer Template Example"
    visualization_type = "map_layer"
    visualization_tags = ["example", "map", "map_layer"]
    visualization_description = "An example plugin for the map layer template"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return map layer configuration
        """
        layer_source = {
            "type": "ESRI Image and Map Service",
            "props": {
                "url": "https://maps.water.noaa.gov/server/rest/services/rfc/rfc_max_forecast/MapServer",
                "attributions": "National Water Center",
                "params": {"LAYERS": "show:0"},
            },
        }

        layer_configuration = {
            "type": "ImageLayer",
            "props": {
                "name": "RFC Max Forecast",
                "source": layer_source,
                "opacity": 0.5,
            },
            "layerVisibility": True,
        }

        aliases = {
            "Max Status - Forecast Trend": {
                "record_threshold": "Record Threshold",
                "major_threshold": "Major Threshold",
                "moderate_threshold": "Moderate Threshold",
                "minor_threshold": "Minor Threshold",
                "action_threshold": "Action Threshold",
            }
        }

        variables = {
            "Max Status - Forecast Trend": {
                "nws_lid": "LID",
            }
        }

        omitted_attributes = {
            "Max Status - Forecast Trend": [
                "geom",
                "oid",
            ]
        }

        return {
            "configuration": layer_configuration,
            "attributeVariables": variables,
            "omittedPopupAttributes": omitted_attributes,
            "attributeAliases": aliases,
        }
