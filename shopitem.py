import typing

from utility import ITEM


class ShopItem:
    """
    Parent class for all items in shop.
    Serializes in JSON.
    """

    type = ITEM

    def __init__(self, id: int = 0, price: int = 0, name: str = "", description: str = "", tags: typing.List[str] = []):
        self.id = id
        self.price = price
        self._price = price  # Initial price of item
        self.name = name
        self.description = description
        self.tags = tags

    def __repr__(self) -> str:
        return f"<ShopItem: {self.id}, {self.name}, {self.price}>"

    def count_credit(self, months: int = 4) -> int:
        """
        Counts price for each month if client wants to take credit on this item
        months: int, by default equals 4
        :return: Returns monthly payment
        """
        return int(self.price / months)

    def make_discount(self, discount: float) -> None:
        """
        Changes price of
        discount: float, size of discount
        :return: Void
        """
        self.price = int(self.price - self.price * discount)

    def delete_discount(self):
        self.price = self._price
