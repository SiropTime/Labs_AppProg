import os

from pprint import pprint

"""
TYPES CONSTANTS
"""
ORDER = ".ord"
USER = ".usr"
ITEM = ".itm"


"""
FUNCTIONS TO INTERACT VIA CLI
"""

# Inserting data
def add_user(orm):
    pass

def add_item(orm):
    pass

def make_order(orm):
    pass

# Printing data
def print_users(orm):
    for user in orm.users.values():
        pprint(user.__dict__, depth=1)
    
    print("""
          
          Введите ID пользователя, чтобы увидеть его заказы
          Или введите любую строку, чтобы вернуться в главное меню
          """)
    while True:
        try:
            id = int(input())
            orders = orm.get_orders_by_user(id)
            pprint(orders)
        except ValueError:
            break

def print_items(orm):
    for item in orm.items.values():
        pprint(item.__dict__, depth=2)

def print_orders(orm):
    for order in orm.orders.values():
        pprint(order.__dict__, depth=1)

def main_cli(orm) -> None:
    print("""
          Лаба 1. Прикладное программирование
          ИДБ 21-10 Мальцев Тимофей
          Вариант 5

          Магазинчик
          """)
    
    while True:
        print(
            """
          Интерфейс:
            0 - Выход из программы
            
            1 - Добавить пользователя
            2 - Добавить предметe
            3 - Сделать заказ
            
            4 - Вывод пользователей
            5 - Вывод товаров
            6 - Вывод сделанных заказов

          """
        )
        answer = int(input())

        if not answer:
            break

        # Inserting data
        elif answer == 1:
            pass
        elif answer == 2:
            pass
        elif answer == 3:
            pass

        # Printing data
        elif answer == 4:
            pass
        elif answer == 5:
            pass
        elif answer == 6:
            pass


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
