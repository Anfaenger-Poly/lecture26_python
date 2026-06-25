from Cart.cart_dao import CartDAO
from Cart.cart import Cart
from Product.product_dao import ProductDAO
from errors import InvalidInputError, NotFoundError

class CartService:
    cart_id_seq = 9000

    def __init__(self, cart_dao: CartDAO, product_dao: ProductDAO):
        self.__dao = cart_dao
        self.__product_dao = product_dao

    def add_to_cart(self, owner_key: str, product_id: str, quantity: int) -> Cart:
        if quantity <= 0:
            raise InvalidInputError('수량은 1 이상이어야 합니다.')
        product = self.__product_dao.select_product_by_id(product_id)
        if not product:
            raise NotFoundError('없는 상품입니다.')
        existing = self.__dao.select_cart_by_owner(owner_key)
        already = sum(c.get_quantity() for c in existing if c.get_product_id() == product_id)
        if already + quantity > product.available_count():
            raise InvalidInputError(f'재고가 부족합니다. (재고: {product.available_count()}, 담긴 수량: {already})')
        cart_id = str(CartService.cart_id_seq)
        CartService.cart_id_seq += 1
        cart = Cart(cart_id, owner_key, product_id, quantity)
        self.__dao.insert_cart(cart)
        return cart

    def view_cart(self, owner_key: str) -> list[Cart]:
        return self.__dao.select_cart_by_owner(owner_key)

    def delete_cart_item(self, cart_id: str) -> bool:
        return self.__dao.delete_cart(cart_id)

    def clear_cart(self, owner_key: str) -> int:
        return self.__dao.delete_cart_by_owner(owner_key)

if __name__ == '__main__':
    from Product.product_dao import ProductDAO
    cs = CartService(CartDAO(), ProductDAO())
    cs.add_to_cart('woongseok', 'P001', 1)
    cs.add_to_cart('woongseok', 'P002', 2)
    for c in cs.view_cart('woongseok'):
        print(c)
    cs.clear_cart('woongseok')
    print('비운 후:', cs.view_cart('woongseok'))