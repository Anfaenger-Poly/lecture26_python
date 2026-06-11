from Delivery.delivery import Delivery

# 배송 관리 DAO
class DeliveryDAO:
    def __init__(self):
        self.__deliveryDB= {}

    def insert_delivery(self, delivery):
        delivery_id = delivery.get_delivery_id()
        if delivery_id in self.__deliveryDB:
            return False
        self.__deliveryDB[delivery_id] = delivery
        return True

    def select_delivery_by_id(self, id):
        return self.__deliveryDB.get(id)

    def select_by_order(self, order_id):
        for delivery in self.__deliveryDB.values():
            if delivery.get_order_id() == order_id:
                return delivery
        return None

    def select_by_member(self, member_id):
        return [d for d in self.__deliveryDB.values() if d.get_member_id() == member_id]

    def select_all_deliveries(self):
        return list(self.__deliveryDB.values())

    def update_delivery(self, id, delivery):
        if id in self.__deliveryDB:
            self.__deliveryDB[id] = delivery
            return True
        return False
