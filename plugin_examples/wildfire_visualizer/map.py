from intake.source import base
import json
import os
import pandas as pd
import requests
import pandas as pd
from io import StringIO

script_dir = os.path.dirname(os.path.abspath(__file__))
extents_path = os.path.join(script_dir, "country_extents.json")


class Map(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "wildfire_visualizer_map"
    visualization_args = {
        "satellite": [
            {"label": "MODIS (URT+NRT)", "value": "MODIS_NRT"},
            {"label": "VIIRS NOAA-20 (URT+NRT)", "value": "VIIRS_NOAA20_NRT"},
            {"label": "VIIRS NOAA-21 (URT+NRT)", "value": "VIIRS_NOAA21_NRT"},
            {"label": "VIIRS S-NPP (URT+NRT)", "value": "VIIRS_SNPP_NRT"},
            {"label": "LANDSAT (NRT) [US/Canada Only]", "value": "LANDSAT_NRT"},
        ],
        "days": [str(i) for i in range(1, 11)],
        "date": "date",
        "color_code": ["Confidence", "Fire Radiative Power (FRP)"],
        "country": [
            {"label": name, "value": data["code"]}
            for name, data in json.load(open(extents_path)).items()
        ],
    }
    visualization_tags = ["wildfire", "fire", "map"]
    visualization_description = ""
    visualization_group = "Wildfire Visualizer"
    visualization_label = "Map"
    visualization_type = "map"
    _user_parameters = []

    def __init__(
        self, satellite, days, date, color_code, country, metadata=None, **kwargs
    ):
        self.satellite = satellite
        self.days = days
        self.date = date
        self.color_code = color_code
        self.country = country
        super().__init__(metadata=metadata)

    def read(self):
        token = os.environ["FIRMS_API_TOKEN"]

        parsed_date = pd.to_datetime(self.date).date()
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        raw_data = self.fetch_api_data(token, date=formatted_date)
        geojson_data, legend = self.convert_api_to_geojson(raw_data)

        wildfire_layer = {
            "configuration": {
                "type": "VectorLayer",
                "props": {
                    "name": "Wildfires",
                    "source": {
                        "type": "GeoJSON",
                        "props": {},
                        "geojson": geojson_data,
                    },
                },
                "style": {
                    "version": 8,
                    "sources": {"Wildfires": {"type": "geojson"}},
                    "layers": [
                        {
                            "id": "confidence-frp-style",
                            "type": "circle",
                            "source": "Wildfires",
                            "filter": ["==", "$type", "Point"],
                            "paint": {
                                "circle-radius": 8,
                                "circle-color": [
                                    "match",
                                    ["get", "color"],
                                    "#cccccc",
                                    "#cccccc",
                                    "#1f77b4",
                                    "#1f77b4",
                                    "#ff7f0e",
                                    "#ff7f0e",
                                    "#d62728",
                                    "#d62728",
                                    "#33a02c",
                                    "#33a02c",
                                    "#999999",
                                ],
                                "circle-stroke-width": 2,
                                "circle-stroke-color": "#FFFFFF",
                            },
                        }
                    ],
                },
            },
        }

        if legend:
            wildfire_layer["legend"] = {
                "items": [
                    {
                        "color": color,
                        "label": label,
                        "symbol": "circle",
                    }
                    for label, color in legend["legend_data"].items()
                ],
                "title": legend["title"],
            }

        return {
            "baseMap": "https://server.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer",
            "layers": [wildfire_layer],
            "map_extent": {"extent": self.get_box_by_code()},
            "layerControl": True,
        }

    def get_box_by_code(self):
        country_extents = json.load(open(extents_path))
        for country, info in country_extents.items():
            if info["code"] == self.country:
                return ",".join(str(x) for x in info["box"])

    def fetch_api_data(self, token, date):
        url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{token}/{self.satellite}/{self.country}/{self.days}/{date}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print("Error fetching data:", e)
            return b""

    def convert_api_to_geojson(self, data):
        df = pd.read_csv(StringIO(data))

        has_no_data_color = False

        geojson = {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "EPSG:4326"  # Use 4326 for latitude/longitude; 3857 is for projected meters
                },
            },
        }
        legend = {}
        features = []

        for _, row in df.iterrows():
            wildfire = {
                "type": "Feature",
                "properties": self.format_wildfire_metadata(row),
                "geometry": {
                    "type": "Point",
                    "coordinates": [row.get("longitude"), row.get("latitude")],
                },
            }

            if self.color_code == "Confidence":
                wildfire["properties"]["color"] = self.get_color_from_confidence(
                    row.get("confidence")
                )
                if isinstance(row.get("confidence"), str):
                    type_of_confidence = "string"
                else:
                    type_of_confidence = "numeric"

            elif self.color_code == "Fire Radiative Power (FRP)":
                wildfire["properties"]["color"] = self.get_color_from_frp(
                    row.get("frp")
                )

            if wildfire["properties"]["color"] == "#cccccc":
                has_no_data_color = True

            features.append(wildfire)

        if features:
            legend_data_options = {
                "Confidence": {
                    "string": {
                        "Low": "#1f77b4",
                        "Nominal": "#ff7f0e",
                        "High": "#d62728",
                    },
                    "numeric": {"<30": "#1f77b4", "<80": "#ff7f0e", ">=80": "#d62728"},
                },
                "Fire Radiative Power (FRP)": {
                    "<10": "#33a02c",
                    "<30": "#1f77b4",
                    "<50": "#ff7f0e",
                    ">=50": "#d62728",
                },
            }

            if self.color_code == "Confidence":
                legend_data = legend_data_options[self.color_code][type_of_confidence]
            else:
                legend_data = legend_data_options[self.color_code]

            if has_no_data_color:
                legend_data["N/A"] = "#cccccc"

            legend_title = self.color_code
            legend = {
                "title": legend_title,
                "legend_data": legend_data,
            }

        geojson["features"] = features
        return geojson, legend

    def format_wildfire_metadata(self, data):
        metadata = {}
        if data.get("acq_date") is not None:
            metadata["Acquisition Date"] = data.get("acq_date")
        if data.get("acq_time") is not None:
            acq_time = str(data.get("acq_time"))
            acq_time = acq_time[:-2] + ":" + acq_time[-2:]
            metadata["Acquisition Time"] = acq_time
        if data.get("satellite") is not None:
            metadata["Satellite"] = data.get("satellite")
        if data.get("instrument") is not None:
            metadata["Instrument"] = data.get("instrument")
        if data.get("confidence") is not None:
            if isinstance(data.get("confidence"), str):
                confidence = str(data.get("confidence")).lower()
                if confidence == "l":
                    metadata["Confidence"] = "Low"
                elif confidence == "n":
                    metadata["Confidence"] = "Nominal"
                elif confidence == "h":
                    metadata["Confidence"] = "High"
            else:
                confidence = data.get("confidence")
                metadata["Confidence"] = confidence
        if data.get("frp") is not None:
            metadata["Fire Radiative Power (FRP)"] = data.get("frp")
        if data.get("bright_ti4") is not None:
            metadata["Brightness Temperatrue I4"] = data.get("bright_ti4")
        if data.get("bright_ti5") is not None:
            metadata["Brightness Temperature I5"] = data.get("bright_ti5")
        if data.get("scan") is not None:
            metadata["Scan"] = data.get("scan")
        if data.get("track") is not None:
            metadata["Track"] = data.get("track")
        if data.get("version") is not None:
            metadata["Version"] = data.get("version")
        if data.get("daynight") is not None:
            if data.get("daynight").lower() == "d":
                metadata["Day/Night"] = "Day"
            elif data.get("daynight").lower() == "n":
                metadata["Day/Night"] = "Night"

        return metadata

    def get_color_from_confidence(self, confidence):
        if pd.isna(confidence):
            return "#cccccc"

        if isinstance(confidence, str):
            confidence = confidence.lower()
            if confidence == "l":
                return "#1f77b4"
            elif confidence == "n":
                return "#ff7f0e"
            elif confidence == "h":
                return "#d62728"

        elif isinstance(confidence, (int, float)):
            if confidence < 30:
                return "#1f77b4"
            elif confidence < 80:
                return "#ff7f0e"
            else:
                return "#d62728"

        return "#cccccc"

    def get_color_from_frp(self, frp):
        if pd.isna(frp):
            return "#cccccc"
        elif frp < 10:
            return "#33a02c"
        elif frp < 30:
            return "#1f77b4"
        elif frp < 50:
            return "#ff7f0e"
        else:
            return "#d62728"
