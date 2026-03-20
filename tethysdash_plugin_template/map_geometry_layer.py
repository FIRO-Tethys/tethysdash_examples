from intake.source import base


class MapGeometryLayerExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "map_geometry_layer_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Map Geometry Example Layer"
    visualization_type = "map_layer"
    visualization_tags = ["example", "map", "map_layer"]
    visualization_description = "An layer for the map geometry example plugin"

    def __init__(self, metadata=None, **kwargs):
        super().__init__(metadata=metadata)

    def read(self):
        """
        Return map layer configuration
        """
        layer_source = {
            "type": "ESRI Feature Service",
            "props": {
                "url": "https://p3eplmys2rvchkjx.svcs.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Census_2020_DHC_Total_Population/FeatureServer",
                "layer": "3",
            },
        }

        layer_configuration = {
            "type": "VectorLayer",
            "props": {
                "name": "Population Density Per KM2",
                "minZoom": "9",
                "source": {
                    "type": "ESRI Feature Service",
                    "props": {
                        "url": "https://p3eplmys2rvchkjx.svcs.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Census_2020_DHC_Total_Population/FeatureServer",
                        "layer": "3",
                    },
                },
            },
            "style": {
                "rules": [
                    {
                        "geometryType": "polygon",
                        "conditionField": "P001_calc_pctPopDensity",
                        "conditionType": "<=",
                        "conditionValue": "10000",
                        "fill": "#980043",
                        "name": "lte 10000",
                    },
                    {
                        "geometryType": "polygon",
                        "conditionField": "P001_calc_pctPopDensity",
                        "conditionType": "<=",
                        "conditionValue": "3000",
                        "fill": "#dd1c77",
                        "name": "lte 3000",
                    },
                    {
                        "geometryType": "polygon",
                        "conditionField": "P001_calc_pctPopDensity",
                        "conditionType": "<=",
                        "conditionValue": "1000",
                        "fill": "#6a51a3",
                        "name": "lte 1000",
                    },
                    {
                        "geometryType": "polygon",
                        "conditionField": "P001_calc_pctPopDensity",
                        "conditionType": "<=",
                        "conditionValue": "500",
                        "fill": "#9ecae1",
                        "name": "lte 500",
                    },
                    {
                        "geometryType": "polygon",
                        "conditionField": "P001_calc_pctPopDensity",
                        "conditionType": "<=",
                        "conditionValue": "200",
                        "fill": "#deebf7",
                        "name": "lte 200",
                    },
                ],
                "default": {},
            },
        }

        legend = "default"

        return {
            "configuration": layer_configuration,
            "queryable": True,
            "legend": legend,
        }
