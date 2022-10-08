import os
import sys

from pprint import pprint

from model.user import User
from model.shopitem import ShopItem
from constants import *

"""
FUNCTIONS TO INTERACT VIA CLI
"""


def pretty_print(headers: list = [], values: list = [], is_needed_header: bool = True):
    """
    Function to print pretty-ish table
    """
    if is_needed_header:
        print("".join(["{:<14}" * len(headers)]).format(*headers))
    if len(values):
        print("".join(["{:<14}" * len(values)]).format(*list(map(str, values))))


"""
Inserting data
"""


def add_user(orm):

    print("Введите имя пользователя: ")
    name = str(input())
    id = list(orm.users.keys())[-1] + 1
    orm.users[id] = User(id, name)
    print("Пользователь успешно создан!")


def add_item(orm):
    print("Введите название товара:")
    name = str(input())
    print("Введите цену товара:")
    price = int(input())
    print("Введите коротенькое описание:")
    description = str(input())
    print("Введите теги по одному слову через пробел:")
    tags = list(map(str, input()))

    id = list(orm.items.keys())[-1] + 1

    orm.items[id] = ShopItem(id, price, name, description, tags)


def make_order(orm):
    print("Введите ID пользователя, на которого оформить заказ:")
    u_id = 0

    while True:
        u_id = int(input())
        try:
            tmp = orm.users[u_id]
            break
        except KeyError:
            print("Не был найден такой пользователь, введите другой ID:")
            continue



    print("Введите id предметов через пробел, которые необходимо добавить в заказ:")
    items = list(map(int, input().split()))
    for _, item in enumerate(items):
        try:
            tmp = orm.items[item]
        except KeyError:

            while True:
                print(f"Не найдено предмета с ID {item}. Попробуйте его заменить:")
                new_item = int(input())
                try:
                    tmp = orm.items[new_item]
                    break
                except KeyError:
                    continue


            items[_] = new_item

    order = orm.make_order(u_id, items)
    print(f"Успешно сделан заказ: {order}")


"""
Printing data
"""


def print_users(orm):
    pretty_print(list(orm.users.values())[0].__dict__.keys())
    for user in orm.users.values():
        pretty_print(values=user.__dict__.values(), is_needed_header=False)

    while True:
        print("""
          Введите ID пользователя, чтобы увидеть его заказы
          Или введите любую строку, чтобы вернуться в главное меню
          """)
        try:
            id = int(input())
            orders = orm.get_orders_by_user(id)
            pretty_print(list(orm.orders.values())[0].__dict__.keys())
            for order in orders:
                pretty_print(values=order.__dict__.values(), is_needed_header=False)
        except ValueError as err:
            break
        except Exception as ex:
            print(ex)


def print_items(orm):
    pretty_print(list(orm.items.values())[0].__dict__.keys())

    for item in orm.items.values():
        pretty_print(values=item.__dict__.values(), is_needed_header=False)

    while True:
        print("""
    
          Выберите предмет и через пробел номер действия или любую строку, чтобы вернуться в меню.
          Действия:
          
            1 - Установить скидку на предмет
            2 - Удалить скидку, если таковая имеется
            3 - Посчитать кредит на предмет
          """)
        try:
            i_id, action = map(int, input().split())

            try:
                tmp = orm.items[i_id]
            except KeyError:
                print(f"Couldnt't find item with id {i_id}",
                      file=sys.stderr)

            if action == 1:
                print("Введите количество процентов, предоставляемой скидки (целым числом):")
                while True:
                    discount = int(input()) * 0.01
                    if discount > 1 or discount < 0:
                        print("Такую скидку невозможно предоставить!\nВведите другой размер скидки:")
                    else:
                        break

                orm.items[i_id].make_discount(discount)
                print("Успешно применена скидка!")
            elif action == 2:
                orm.items[i_id].delete_discount()
                print("Успешно удалена скидка!")
            elif action == 3:
                print("Введите количество месяцев, на которые рассчитать рассрочку:")
                while True:
                    months = int(input())

                    if months < 0 or months > orm.items[i_id].price < months:
                        print("Не можем рассчитать рассрочку на таких условиях\nВведите другое количество месяцев:")
                    else:
                        break
                payment = orm.items[i_id].count_credit(months)
                print(f"Рассчитали рассрочку на {months} месяцев с ежемесячным платежом {payment}")
        except ValueError:
            break


def print_orders(orm):
    pretty_print(list(orm.orders.values())[0].__dict__.keys())

    for order in orm.orders.values():
        pretty_print(values=order.__dict__.values(), is_needed_header=False)

    while True:
        print("""

              Введите ID заказа, чтобы увидеть товары, входящие в него
              Или введите любую строку, чтобы вернуться в главное меню
              """)
        try:
            id = int(input())
            items = orm.get_items_from_order(id)
            pretty_print(list(orm.items.values())[0].__dict__.keys())
            for item in items:
                pretty_print(values=item.__dict__.values(), is_needed_header=False)
        except ValueError as err:
            break
        except Exception as ex:
            print(ex)


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
            add_user(orm)
        elif answer == 2:
            add_item(orm)
        elif answer == 3:
            make_order(orm)

        # Printing data
        elif answer == 4:
            print_users(orm)
        elif answer == 5:
            print_items(orm)
        elif answer == 6:
            print_orders(orm)


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
