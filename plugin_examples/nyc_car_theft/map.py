from intake.source import base
import json
import os
from datetime import datetime
from .utilities import run_query

script_dir = os.path.dirname(os.path.abspath(__file__))
boundaries_path = os.path.join(script_dir, "borough_boundaries.geojson")
extents_path = os.path.join(script_dir, "borough_extents.json")


class Map(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "nyc_car_theft_map"
    visualization_args = {
        "borough": list(json.load(open(extents_path)).keys()),
        "start": "date",
        "end": "date",
        "group_by": ["Time of day", "Day of week", "Month"],
    }
    visualization_tags = ["nyc", "car", "theft", "map"]
    visualization_description = ""
    visualization_group = "NYC Car Theft"
    visualization_label = "NYC Map"
    visualization_type = "map"
    _user_parameters = []

    def __init__(self, borough, start, end, group_by, metadata=None, **kwargs):
        self.borough = borough
        self.start_date = start
        self.end_date = end
        self.group_by = group_by
        super().__init__(metadata=metadata)

    def read(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the full path to the file
        file_path = os.path.join(script_dir, "borough_boundaries.geojson")

        # Load GeoJSON data
        with open(file_path) as f:
            geojson_data = json.load(f)

        theft_data = self.search_form()
        theft_geojson = {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "EPSG:4326"  # Use 4326 for latitude/longitude; 3857 is for projected meters
                },
            },
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "borough": item["borough"],
                        "date": item["date"],
                        "time": item["time"],
                        "color": item["color"],
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(item["longitude"]),
                            float(item["latitude"]),
                        ],
                    },
                }
                for item in theft_data["results"]
            ],
        }

        return {
            "baseMap": "https://server.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer",
            "layers": [
                {
                    "configuration": {
                        "type": "VectorLayer",
                        "props": {
                            "name": "Borough Boundaries",
                            "source": {
                                "type": "GeoJSON",
                                "props": {},
                                "geojson": geojson_data,
                            },
                        },
                    },
                },
                {
                    "configuration": {
                        "type": "VectorLayer",
                        "props": {
                            "name": "Theft Data",
                            "source": {
                                "type": "GeoJSON",
                                "props": {},
                                "geojson": theft_geojson,
                            },
                        },
                        "style": {
                            "version": 8,
                            "sources": {"Theft Data": {"type": "geojson"}},
                            "layers": [
                                {
                                    "id": "points-layer",
                                    "type": "circle",
                                    "source": "Theft Data",
                                    "filter": ["==", "$type", "Point"],
                                    "paint": {
                                        "circle-radius": 5,
                                        "circle-color": [
                                            "match",
                                            ["get", "color"],
                                            "blue",
                                            "#0000FF",
                                            "green",
                                            "#008000",
                                            "red",
                                            "#FF0000",
                                            "yellow",
                                            "#FFFF00",
                                            "orange",
                                            "#FFA500",
                                            "purple",
                                            "#800080",
                                            "pink",
                                            "#FFC0CB",
                                            "lightblue",
                                            "#ADD8E6",
                                            "lightgreen",
                                            "#90EE90",
                                            "darkblue",
                                            "#00008B",
                                            "brown",
                                            "#A52A2A",
                                            "darkgreen",
                                            "#006400",
                                            "gray",
                                            "#808080",
                                            "cyan",
                                            "#00FFFF",
                                            "#999999",
                                        ],
                                    },
                                }
                            ],
                        },
                    },
                    "legend": {
                        "items": [
                            {
                                "color": color,
                                "label": f"{label} ({count})",
                                "symbol": "circle",
                            }
                            for label, (color, count) in theft_data["legend"].items()
                        ],
                        "title": "Thefts",
                    },
                },
            ],
            "map_extent": {"extent": self.get_map_extent()},
            "layerControl": True,
        }

    def get_map_extent(self):
        return json.load(open(extents_path))[self.borough]

    def search_form(self):
        # Run the query and color code the results based on the selected grouping option
        query_results = run_query(self.borough, self.start_date, self.end_date)
        color_coded_results = self.color_code_results(query_results)

        return color_coded_results

    def color_code_results(self, results):
        """Color code the results based on the selected grouping option."""
        # Define color options for each grouping option and intialize counts to display in the legend
        reference_options = {
            "Time of day": {
                "Morning": ["blue", 0],
                "Afternoon": ["green", 0],
                "Evening": ["red", 0],
            },
            "Day of week": {
                "Monday": ["blue", 0],
                "Tuesday": ["green", 0],
                "Wednesday": ["yellow", 0],
                "Thursday": ["orange", 0],
                "Friday": ["red", 0],
                "Saturday": ["purple", 0],
                "Sunday": ["pink", 0],
            },
            "Month": {
                "January": ["lightblue", 0],
                "February": ["lightgreen", 0],
                "March": ["yellow", 0],
                "April": ["darkblue", 0],
                "May": ["red", 0],
                "June": ["purple", 0],
                "July": ["pink", 0],
                "August": ["brown", 0],
                "September": ["darkgreen", 0],
                "October": ["orange", 0],
                "November": ["gray", 0],
                "December": ["cyan", 0],
            },
        }

        reference = reference_options[self.group_by]
        if self.group_by == "Time of day":
            for result in results["results"]:
                time = datetime.strptime(result["time"], "%H:%M:%S")
                if time < datetime.strptime("12:00:00", "%H:%M:%S"):
                    # Color code the individual result based on the time of day
                    result["color"] = reference["Morning"][0]
                    # Increment the count for the time of day
                    reference["Morning"][1] += 1
                elif time < datetime.strptime("17:00:00", "%H:%M:%S"):
                    # Color code the individual result based on the time of day
                    result["color"] = reference["Afternoon"][0]
                    # Increment the count for the time of day
                    reference["Afternoon"][1] += 1
                else:
                    # Color code the individual result based on the time of day
                    result["color"] = reference["Evening"][0]
                    # Increment the count for the time of day
                    reference["Evening"][1] += 1

        elif self.group_by == "Day of week":
            for result in results["results"]:
                date = datetime.strptime(result["date"], "%m/%d/%Y")
                day_of_week = date.strftime("%A")

                # Color code the individual result based on the day of the week
                result["color"] = reference[day_of_week][0]
                # Increment the count for the day of the week
                reference[day_of_week][1] += 1

        elif self.group_by == "Month":
            for result in results["results"]:
                date = datetime.strptime(result["date"], "%m/%d/%Y")
                month = date.strftime("%B")

                # Color code the individual result based on the month
                result["color"] = reference[month][0]
                # Increment the count for the month
                reference[month][1] += 1

        # Add the legend data to the results
        results["legend"] = reference

        return results
