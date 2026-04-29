from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class MapLayerExample(TethysDashPlugin):
    name = "map_example"
    args = {}
    group = "Example"
    label = "Map Layer Template Example"
    type = "map_layer"
    tags = ["example", "map", "map_layer"]
    description = "An example plugin for the map layer template"

    def run(self):
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
            "style": {
                "type": "Style",
                "props": {
                    "stroke": {
                        "type": "Stroke",
                        "props": {
                            "color": "#501020",
                            "width": 1,
                        },
                    },
                },
            },
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

        legend = {
            "title": "Some Title",
            "items": [{"label": "Some label", "color": "green", "symbol": "square"}],
        }

        return {
            "configuration": layer_configuration,
            "attributeVariables": variables,
            "omittedPopupAttributes": omitted_attributes,
            "attributeAliases": aliases,
            "queryable": True,
            "legend": legend,
        }
