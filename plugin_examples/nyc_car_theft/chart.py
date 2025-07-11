from intake.source import base
import json
import os
from datetime import datetime, timedelta
from sodapy import Socrata
from .utilities import run_query

script_dir = os.path.dirname(os.path.abspath(__file__))
extents_path = os.path.join(script_dir, "borough_extents.json")


class Chart(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "nyc_car_theft_chart"
    visualization_args = {
        "borough": list(json.load(open(extents_path)).keys()),
        "start": "date",
        "end": "date",
        "sort_by": ["Day", "Week", "Month"],
    }
    visualization_tags = ["nyc", "car", "theft", "chart"]
    visualization_description = ""
    visualization_group = "NYC Car Theft"
    visualization_label = "Car Theft Stats Chart"
    visualization_type = "plotly"
    _user_parameters = []

    def __init__(self, borough, start, end, sort_by, metadata=None, **kwargs):
        self.borough = borough
        self.start_date = start
        self.end_date = end
        self.sort_by = sort_by
        super().__init__(metadata=metadata)

    def read(self):
        query_results = run_query(self.borough, self.start_date, self.end_date)
        x_values, y_values = self.group_graph_results(query_results)
        data = [
            {
                "type": "bar",
                "x": x_values,
                "y": y_values,
            },
        ]

        layout = {
            "title": f"Car Theft in {self.borough.capitalize()} from {self.start_date} to {self.end_date}",
            "yaxis": {"title": "Number of Car Thefts"},
        }

        return {"data": data, "layout": layout}

    def group_graph_results(self, results):
        """Group the results of a query by the specified time period."""
        grouped_results = {}

        if self.sort_by == "Week":
            for result in results["results"]:
                date = result["date"]
                date_obj = datetime.strptime(date, "%m/%d/%Y")
                start_of_week = date_obj - timedelta(days=date_obj.weekday())
                end_of_week = start_of_week + timedelta(days=6)

                week_range = f"{start_of_week.strftime('%m/%d/%y')} - {end_of_week.strftime('%m/%d/%y')}"
                if week_range not in grouped_results:
                    grouped_results[week_range] = 0
                grouped_results[week_range] += 1

            time_series = sorted(
                grouped_results.keys(),
                key=lambda x: datetime.strptime(x.split(" - ")[0], "%m/%d/%y"),
            )

        elif self.sort_by == "Month":
            for result in results["results"]:
                date = result["date"]
                month = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m")
                if month not in grouped_results:
                    grouped_results[month] = 0
                grouped_results[month] += 1

            time_series = sorted(grouped_results.keys())

        elif self.sort_by == "Day":
            for result in results["results"]:
                date = result["date"]
                date_str = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
                if date_str not in grouped_results:
                    grouped_results[date_str] = 0
                grouped_results[date_str] += 1

            time_series = sorted(grouped_results.keys())

        else:
            return [], []

        grouped_counts = [grouped_results[period] for period in time_series]
        return time_series, grouped_counts
