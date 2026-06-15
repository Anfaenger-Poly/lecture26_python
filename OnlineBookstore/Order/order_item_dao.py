class OrderItemDAO:
    def __init__(self):
        self.__orderItemDB = {}
        self.__seq = 1

    def insert_order_item(self, order_id, order_item):
        order_item_id = str(self.__seq)
        self.__seq += 1
        self.__orderItemDB[order_item_id] = (order_id, order_item)
        return order_item_id
    
    def select_order_items_by_order_id(self, order_id):
        result = []
        for oid, item in self.__orderItemDB.values():
            if oid == order_id:
                result.append(item)
        return result

    def select_all_order_items(self):
        return list(self.__orderItemDB.values())
    
    def update_order_item(self, order_item_id, order_item):
        if order_item_id in self.__orderItemDB:
            order_id = self.__orderItemDB[order_item_id][0]
            self.__orderItemDB[order_item_id] = (order_id, order_item)
            return True
        return False
    
    def delete_order_item(self, order_item_id):
        if order_item_id in self.__orderItemDB:
            self.__orderItemDB.pop(order_item_id)
            return True
        return False
    
    def delete_items_by_order_id(self, order_id):
        keys_to_delete = []
        for k, (oid, _) in self.__orderItemDB.items():
            if oid == order_id:
                keys_to_delete.append(k)
        for k in keys_to_delete:
            self.__orderItemDB.pop(k)