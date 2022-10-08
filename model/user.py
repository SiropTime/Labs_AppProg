import typing

from constants import USER


class User:
    """
    Serialized in XML
    """

    type = USER

    def __init__(self, id: int = 0, name: str = "", orders: typing.List[int] = []):
        self.id = id
        self.name = name
        self.orders = orders

    def __repr__(self) -> str:
        return f"<User: {self.id}, {self.name}>"
