from Cart.cart import Cart

# 장바구니 관리 DAO
class CartDAO:
    def __init__(self):
        self.__cartDB = {}

    def insert_cart(self, cart):
        cart_id = cart.get_cart_id()
        if cart_id in self.__cartDB:
            return False
        self.__cartDB[cart_id] = cart
        return True

    def select_cart_by_member(self, member_id):
        result = []
        for c in self.__cartDB.values():
            if c.get_member_id() == member_id:
                result.append(c)
        return result

    def select_all_carts(self):
        return list(self.__cartDB.values())

    def delete_cart(self, cart_id):
        if cart_id in self.__cartDB:
            self.__cartDB.pop(cart_id)
            return True
        return False