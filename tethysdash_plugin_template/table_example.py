from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class TableExample(TethysDashPlugin):
    name = "table_example"
    args = {}
    group = "Example"
    label = "Table Example"
    type = "table"
    tags = [
        "example",
        "table",
    ]
    description = "An example plugin for the table visualization"

    def run(self):
        """
        Return table data
        """

        data = [
            {
                "name": "Alice Johnson",
                "age": 28,
                "occupation": "Engineer",
            },
            {
                "name": "Bob Smith",
                "age": 34,
                "occupation": "Designer",
            },
            {
                "name": "Charlie Brown",
                "age": 22,
                "occupation": "Teacher",
            },
        ]
        title = "User Information"
        subtitle = "Some Subtitle"

        return {"title": title, "subtitle": subtitle, "data": data}
