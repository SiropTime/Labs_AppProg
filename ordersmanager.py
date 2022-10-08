import sys
import typing

from serialization import SerializingManager
from utility import sort_items
from model.shopitem import ShopItem
from model.user import User
from model.order import Order


class OrdersManager:

    def __init__(self):

        self.serializing_manager = SerializingManager()

        self.orders = {}
        self.users = {}
        self.items = {}

        self.files = sort_items()

        self.load_orders(self.files["orders"])
        self.load_items(self.files["items"])
        self.load_users(self.files["users"])

        del self.files

    def __del__(self):
        """
        Desctructor is needed to save all files when programm is finished correctly.
        """
        self.save_orders()
        self.save_items()
        self.save_users()

        print("\n\n\nSuccessfully serialized everything before end of program")

    """
    Orders section
    """

    def make_order(self, user_id: int, items_id: typing.List[int]) -> Order:
        try:
            user = self.users[user_id]
            try:
                items = []
                for id in items_id:
                    try:
                        item = self.items[id]
                        items.append(id)
                    except KeyError:
                        print(f"Couldn't find item with id {id}.")
                if not len(items) == 0:
                    if not len(self.orders.keys()) == 0:
                        order = Order(list(self.orders.keys())[-1] + 1, items)
                    else:
                        order = Order(1, items)
                    self.users[user_id].orders.append(order.id)
                    self.orders[order.id] = order

                    self.save_users()
                    self.save_orders()

                    return order
                else:
                    raise Exception("Didn't find any of given item. Try to change list of item's ids")

            except Exception as ex:
                print(f"Got error: {ex.args[0]}")

        except KeyError:
            print(f"Couldn't find user with id {user_id}. Try with another id",
                  file=sys.stderr)

        return Order()

    def save_orders(self):
        for order in self.orders.values():
            self.serializing_manager.serialize_json(order)

    def load_orders(self, orders: typing.List[str]):
        for f in orders:
            o = self.serializing_manager.deserialize_json(Order, f)
            self.orders[o.id] = o

    """
    Users section
    """

    def get_orders_by_user(self, user_id: int) -> typing.List[Order]:
        try:
            user = self.users[user_id]
            try:
                return [self.orders[o_id] for o_id in user.orders]
            except KeyError:
                print(f"Couldn't find orders from user.\n Try to change user's orders or initialize files.",
                      file=sys.stderr)
        except KeyError:
            print(f"There is no user with id {user_id}.\n Try another id.",
                  file=sys.stderr)
            raise Exception(f"Didn't find user with id {user_id}")

    def load_users(self, users: typing.List[str]):
        for f in users:
            u = self.serializing_manager.deserialize_xml(User, f)
            self.users[u.id] = u

    def save_users(self):
        for user in self.users.values():
            self.serializing_manager.serialize_xml(user)

    """
    Items section
    """

    def load_items(self, items: typing.List[str]):
        for f in items:
            i = self.serializing_manager.deserialize_json(ShopItem, f)
            self.items[i.id] = i

    def save_items(self):
        for item in self.items.values():
            self.serializing_manager.serialize_json(item)

    def get_items_from_order(self, order_id: int) -> typing.List[ShopItem]:
        try:
            order = self.orders[order_id]
            return [self.items[id] for id in order.items]
        except KeyError:
            print(f"There is no order with id {order_id}\nTry another value!",
                  file=sys.stderr)
            raise Exception(f"Didn't find order with id {order_id}")
