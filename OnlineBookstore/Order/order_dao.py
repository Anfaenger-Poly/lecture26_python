from Order.order import Order

# 주문 데이터 접근 (CRUD) : OrderDAO
class OrderDAO:
    def __init__(self):
        self.__orderDB: dict[str, Order] = {}

    def insert_order(self, order: Order) -> bool:
        order_id = order.get_order_id()
        if order_id in self.__orderDB:
            return False
        self.__orderDB[order_id] = order
        return True

    def select_order_by_id(self, order_id: str) -> Order | None:
        return self.__orderDB.get(order_id)

    def select_all_orders(self) -> list[Order]:
        return list(self.__orderDB.values())

    def select_orders_by_member(self, member_id: str) -> list[Order]:
        return [o for o in self.__orderDB.values() if o.get_member_id() == member_id]

    def update_order(self, order_id: str, order: Order) -> bool:
        if order_id in self.__orderDB:
            self.__orderDB[order_id] = order
            return True
        return False

    def delete_order(self, order_id: str) -> bool:
        if order_id in self.__orderDB:
            self.__orderDB.pop(order_id)
            return True
        return False
