import os

"""
TYPES CONSTANTS
"""
ORDER = ".ord"
USER = ".usr"
ITEM = ".itm"


def sort_items() -> dict:
    """
    Function for sorting serialized objects in data folder.
    Returns dictionary with keys called by classes and values by names of files.
    """
    data = os.listdir("data/")
    items = list(filter(lambda i: ITEM in i, data))
    orders = list(filter(lambda o: ORDER in o, data))
    users = list(filter(lambda u: USER in u, data))

    return {"items": items, "orders": orders, "users": users}
