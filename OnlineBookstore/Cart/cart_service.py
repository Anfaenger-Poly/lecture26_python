from Cart.cart_dao import CartDAO
from Cart.cart import Cart
from Cart.cart_item import CartItem
from errors import InvalidInputError

# 장바구니 관리 서비스
class CartService:
    cart_id_seq = 1000

    def __init__(self, cart_dao):
        self.__dao = cart_dao

    def create_cart(self, member_id, book_id, quantity):
        if quantity <= 0:
            raise InvalidInputError('수량은 1 이상이어야 합니다.')
        cart_id = str(CartService.cart_id_seq)
        CartService.cart_id_seq += 1
        cart = Cart(cart_id, member_id)
        cart.add_item(CartItem(book_id, quantity))
        self.__dao.insert_cart(cart)
        return cart

    def view_cart(self, member_id):
        return self.__dao.select_cart_by_member(member_id)

    def delete_cart(self, cart_id):
        return self.__dao.delete_cart(cart_id)

# 단위테스트
if __name__ == '__main__':
    cs = CartService(CartDAO())
    cs.create_cart('woongseok', '1000', 2)
    for c in cs.view_cart('woongseok'):
        print(c)
