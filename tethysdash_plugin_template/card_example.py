from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class CardExample(TethysDashPlugin):
    name = "card_example"
    args = {}
    group = "Example"
    label = "Card Example"
    type = "card"
    tags = [
        "example",
        "card",
    ]
    description = "An example plugin for the card visualization"

    def run(self):
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
