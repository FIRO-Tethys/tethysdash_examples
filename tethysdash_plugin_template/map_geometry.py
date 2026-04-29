import json
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
import requests
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
from pyproj import Transformer
import plotly.express as px

pop_fields = [
    {"value": "ALAND", "label": "Area of Land (m²)"},
    {"value": "AWATER", "label": "Area of Water (m²)"},
    {"value": "P0010001", "label": "Total Population"},
    {"value": "H0010001", "label": "Total Housing Units"},
    {"value": "H0030002", "label": "Occupied Households"},
    {"value": "P001_calc_pctPopDensity", "label": "Population Density"},
    {"value": "P0020002", "label": "Urban Population"},
    {"value": "P0020003", "label": "Rural Population"},
    {"value": "P002_calc_pct0002", "label": "Percent Urban Population"},
    {"value": "P002_calc_pct0003", "label": "Percent Rural Population"},
    {"value": "P0030002", "label": "Population White Alone"},
    {
        "value": "P0030003",
        "label": "Population Black or African American Alone",
    },
    {
        "value": "P0030004",
        "label": "Population American Indian & Alaska Native Alone",
    },
    {"value": "P0030005", "label": "Population Asian Alone"},
    {
        "value": "P0030006",
        "label": "Population Native Hawaiian & Pacific Islander Alone",
    },
    {"value": "P0030007", "label": "Population Some Other Race Alone"},
    {"value": "P0030008", "label": "Population Two or More Races"},
    {"value": "P0050002", "label": "Population Not Hispanic or Latino"},
    {"value": "P0050003", "label": "White Alone, Not Hispanic or Latino"},
    {"value": "P0050004", "label": "Black Alone, Not Hispanic or Latino"},
    {
        "value": "P0050005",
        "label": "American Indian Alone, Not Hispanic or Latino",
    },
    {"value": "P0050006", "label": "Asian Alone, Not Hispanic or Latino"},
    {
        "value": "P0050007",
        "label": "Native Hawaiian Alone, Not Hispanic or Latino",
    },
    {
        "value": "P0050008",
        "label": "Some Other Race Alone, Not Hispanic or Latino",
    },
    {"value": "P0050009", "label": "Two or More Races, Not Hispanic or Latino"},
    {"value": "P0050010", "label": "Hispanic or Latino"},
    {
        "value": "P005_calc_pct0003",
        "label": "Percent White Alone, Not Hispanic or Latino",
    },
    {
        "value": "P005_calc_pct0004",
        "label": "Percent Black Alone, Not Hispanic or Latino",
    },
    {
        "value": "P005_calc_pct0005",
        "label": "Percent American Indian Alone, Not Hispanic or Latino",
    },
    {
        "value": "P005_calc_pct0006",
        "label": "Percent Asian Alone, Not Hispanic or Latino",
    },
    {
        "value": "P005_calc_pct0007",
        "label": "Percent Native Hawaiian Alone, Not Hispanic or Latino",
    },
    {
        "value": "P005_calc_pct0008",
        "label": "Percent Some Other Race Alone, Not Hispanic or Latino",
    },
    {
        "value": "P005_calc_pct0009",
        "label": "Percent Two or More Races, Not Hispanic or Latino",
    },
    {"value": "P005_calc_pct0010", "label": "Percent Hispanic or Latino"},
    {"value": "P0120002", "label": "Male Population"},
    {"value": "P0120026", "label": "Female Population"},
    {"value": "P012_calc_pctRatio", "label": "Ratio of Males to Females"},
    {"value": "P012_calc_numLT18", "label": "Population Under 18 Years"},
    {"value": "P012_calc_pctLT18", "label": "Percent Under 18 Years"},
    {"value": "P012_calc_numGE65", "label": "Population 65 Years and Over"},
    {"value": "P012_calc_pctGE65", "label": "Percent 65 Years and Over"},
    {
        "value": "P012_calc_numDepend",
        "label": "Dependent Population (Under 18 & 65+)",
    },
    {"value": "P012_calc_pctDepend", "label": "Percent Dependent Population"},
    {"value": "P012_calc_numWork", "label": "Working-Age Population (18-64)"},
    {"value": "P012_calc_pctWork", "label": "Percent Working-Age Population"},
    {"value": "P0130001", "label": "Median Age, Total Population"},
    {"value": "P0130002", "label": "Median Age, Male Population"},
    {"value": "P0130003", "label": "Median Age, Female Population"},
]


def get_label_from_value(value):
    for field in pop_fields:
        if field["value"] == value:
            return field["label"]
    return None


class MapGeometryExample(TethysDashPlugin):
    name = "map_geometry_example"
    args = {
        "map_polygon": "text",
        "pop_field": pop_fields,
        "top_n": "text",
    }  # Arguments provided from TethysDash used for processing
    group = "Example"  # Group for visualization plugin discovery
    label = "Map Geometry Example"  # Visualization plugin name
    type = "plotly"  # Type of visualization
    tags = [
        "example",
        "plotly",
        "map",
    ]  # Tags for visualization plugin discovery
    description = "An example plugin for the map geometry visualization"

    def run(self):
        """
        Return plotly information
        """
        input_crs = self.map_polygon.get("projection", "EPSG:3857")
        target_crs = "EPSG:4326"  # ArcGIS service uses WGS84
        transformer = Transformer.from_crs(input_crs, target_crs, always_xy=True)

        def transform_ring(ring):
            return [list(transformer.transform(x, y)) for x, y in ring]

        def transform_geometry(geom):
            if geom["type"] == "Polygon":
                return [transform_ring(r) for r in geom["coordinates"]]
            elif geom["type"] == "MultiPolygon":
                rings = []
                for poly in geom["coordinates"]:
                    for r in poly:
                        rings.append(transform_ring(r))
                return rings
            else:
                raise ValueError(f"Unsupported geometry type: {geom['type']}")

        # Transform and merge all geometries into a single list of rings
        all_rings = []
        for g in self.map_polygon["geometries"]:
            all_rings.extend(transform_geometry(g))

        # Prepare ArcGIS geometry
        arcgis_geometry = {
            "rings": all_rings,
            "spatialReference": {"wkid": 4326},
        }

        # -----------------------------
        # Query ArcGIS Feature Service
        # -----------------------------
        url = "https://p3eplmys2rvchkjx.svcs.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Census_2020_DHC_Total_Population/FeatureServer/3/query"

        params = {
            "where": "1=1",
            "outFields": "*",
            "geometry": json.dumps(arcgis_geometry),  # proper JSON
            "geometryType": "esriGeometryPolygon",
            "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects",
            "f": "geojson",
        }

        response = requests.get(url, params=params)
        data = response.json()

        # -----------------------------
        # Load Features
        # -----------------------------
        if "features" not in data or len(data["features"]) == 0:
            return {"type": "text", "data": "No features found in selected area."}

        gdf = gpd.GeoDataFrame.from_features(data["features"])

        # -----------------------------
        # Population Field (explicit is better)
        # -----------------------------
        pop_field = self.pop_field

        if pop_field not in gdf.columns:
            return {"type": "text", "data": "Population field not found."}

        gdf[pop_field] = pd.to_numeric(gdf[pop_field], errors="coerce").fillna(0)

        # -----------------------------
        # Aggregate + Chart
        # -----------------------------
        total_population = int(gdf[pop_field].sum())
        top = gdf.sort_values(by=pop_field, ascending=False).head(self.top_n)

        label_field = "NAME" if "NAME" in gdf.columns else gdf.index.astype(str)

        fig = px.bar(
            top,
            x=label_field,
            y=pop_field,
            title=f"Top Areas by Population (Total: {total_population:,})",
            labels={pop_field: get_label_from_value(pop_field)},
        )

        return json.loads(fig.to_json())
