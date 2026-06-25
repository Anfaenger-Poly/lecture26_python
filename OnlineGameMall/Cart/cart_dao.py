from Cart.cart import Cart

class CartDAO:
    def __init__(self):
        self.__cartDB: dict[str, Cart] = {}

    def insert_cart(self, cart: Cart) -> bool:
        cart_id = cart.get_cart_id()
        if cart_id in self.__cartDB:
            return False
        self.__cartDB[cart_id] = cart
        return True

    def select_cart_by_id(self, cart_id: str) -> Cart | None:
        return self.__cartDB.get(cart_id)

    def select_cart_by_owner(self, owner_key: str) -> list[Cart]:
        # 컬렉션 조회는 없을 때 None 이 아니라 빈 리스트를 반환한다.
        result = []
        for c in self.__cartDB.values():
            if c.get_owner_key() == owner_key:
                result.append(c)
        return result

    def select_all_carts(self) -> list[Cart]:
        return list(self.__cartDB.values())

    def delete_cart(self, cart_id: str) -> bool:
        if cart_id in self.__cartDB:
            self.__cartDB.pop(cart_id)
            return True
        return False

    def delete_cart_by_owner(self, owner_key: str) -> int:
        targets = [c.get_cart_id() for c in self.__cartDB.values()
                   if c.get_owner_key() == owner_key]
        for cid in targets:
            self.__cartDB.pop(cid)
        return len(targets)
