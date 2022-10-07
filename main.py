from order import OrdersManager

if __name__ == '__main__':
    print("Maltsev Timofey IDB-21-10\n\n")
    
    orm = OrdersManager()

    print(orm.orders)
    print(orm.items)
    print([user.__dict__ for user in orm.users.values()])
