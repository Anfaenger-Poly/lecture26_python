from Cart.cart_item import CartItem

class CartItemDAO:
    def __init__(self):
        self.__cartItemDB = {}

    def insert_cart(self, cart_id, cart_item):
        if cart_id not in self.__cartItemDB:
            self.__cartItemDB[cart_id] = []
        self.__cartItemDB[cart_id].append(cart_item)
        return True
    
    def select_cart_by_member(self, member_id):
        return list(self.__cartItemDB.values())
    
    def select_all_carts(self):
        return list(self.__cartItemDB.values())
    
    def delete_cart(self, cart_id):
        if cart_id in self.__cartItemDB:
            self.__cartItemDB.pop(cart_id)
            return True
        return False