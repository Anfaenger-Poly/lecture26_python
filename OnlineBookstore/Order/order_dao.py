from Order.order import Order
from Order.order_item_dao import OrderItemDAO

# 주문 데이터 접근 (CRUD) : OrderDAO
class OrderDAO:
    def __init__(self):
        self.__orderDB = {}
        self.__order_item_dao = OrderItemDAO()

    def insert_order(self, order):
        order_id = order.get_order_id()
        if order_id in self.__orderDB:
            return False
        self.__orderDB[order_id] = order
        for item in order.get_items():
            self.__order_item_dao.insert_order_item(order_id, item)
        return True

    def select_order_by_id(self, order_id):
        return self.__orderDB.get(order_id)

    def select_all_orders(self):
        return list(self.__orderDB.values())

    def select_orders_by_member(self, member_id):
        return [o for o in self.__orderDB.values() if o.get_member_id() == member_id]

    def update_order(self, order_id, order):
        if order_id in self.__orderDB:
            self.__orderDB[order_id] = order
            return True
        return False

    def delete_order(self, order_id):
        if order_id in self.__orderDB:
            self.__orderDB.pop(order_id)
            self.__order_item_dao.delete_items_by_order_id(order_id)
            return True
        return False