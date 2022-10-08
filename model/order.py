import datetime, typing

from constants import ORDER


class Order:
    """
    Serialized in JSON
    """
    type = ORDER

    def __init__(self, id: int = 0, items: typing.List[int] = []):
        self.id = id
        self.date = str(datetime.datetime.now())
        self.items = items

    def __repr__(self) -> str:
        return f"<Order: {self.id}, {self.date}>"

