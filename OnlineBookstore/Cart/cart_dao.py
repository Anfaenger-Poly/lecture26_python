from Cart.cart_item_dao import CartItemDAO

# 장바구니 관리 DAO

class CartDAO:
    def __init__(self):
        self.__cartDB = {}
        self.__cart_item_dao = CartItemDAO()

    def insert_cart(self, cart):
        cart_id = cart.get_cart_id()
        if cart_id in self.__cartDB:
            return False
        self.__cartDB[cart_id] = cart
        for item in cart.get_cart_items():
            self.__cart_item_dao.insert_cart(cart_id, item)
        return True

    def select_cart_by_member(self, member_id):
        return [c for c in self.__cartDB.values() if c.get_member_id() == member_id]

    def select_all_carts(self):
        return list(self.__cartDB.values())

    def delete_cart(self, cart_id):
        if cart_id in self.__cartDB:
            self.__cartDB.pop(cart_id)
            self.__cart_item_dao.delete_cart(cart_id)
            return True
        return False