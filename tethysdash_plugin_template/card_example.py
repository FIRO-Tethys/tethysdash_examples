from intake.source import base


class CardExample(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "card_example"
    visualization_args = {}
    visualization_group = "Example"
    visualization_label = "Card Example"
    visualization_type = "card"
    visualization_tags = [
        "example",
        "card",
    ]
    visualization_description = "An example plugin for the card visualization"

    def __init__(self, metadata=None):
        super(CardExample, self).__init__(metadata=metadata)

    def read(self):
        """
        Return the data for the cards
        """

        data = [
            {
                "color": "#ff0000",  # Background color for the icon (in hex format)
                "label": "Total Sales",  # Title or label for the statistic
                "value": "1,500",  # Value of the statistic
                "icon": "BiMoney",  # Icon to display
            },
            {
                "color": "#00ff00",
                "label": "New Customers",
                "value": "350",
                "icon": "BiFace",
            },
            {
                "color": "#0000ff",
                "label": "Refund Requests",
                "value": "5",
                "icon": "BiArrowFromRight",
            },
        ]

        return {"title": "Company Statistics", "data": data}
