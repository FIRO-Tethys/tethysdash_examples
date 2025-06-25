from intake.source import base


class TableExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "table_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Table Example"
    visualization_type = "table"
    visualization_tags = [
        "example",
        "table",
    ]
    visualization_description = "An example plugin for the table visualization"

    def __init__(self, metadata=None):
        super().__init__(metadata=metadata)

    def read(self):
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
