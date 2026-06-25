#======================
# 데이터 모델 정의 : Cart
# 비회원도 장바구니를 사용할 수 있으므로 member_id 는 str | None 허용.
# 비회원 session_key 는 UI 에서 생성해 전달한다.
class Cart:
    def __init__(self, cart_id: str, owner_key: str, product_id: str, quantity: int):
        self.__cart_id    = cart_id
        self.__owner_key  = owner_key   # 회원 id 또는 비회원 세션키
        self.__product_id = product_id
        self.__quantity   = quantity

    def get_cart_id(self) -> str:
        return self.__cart_id

    def get_owner_key(self) -> str:
        return self.__owner_key

    def get_product_id(self) -> str:
        return self.__product_id

    def get_quantity(self) -> int:
        return self.__quantity

    def set_cart_id(self, cart_id: str) -> None:
        self.__cart_id = cart_id

    def set_quantity(self, quantity: int) -> None:
        self.__quantity = quantity

    def __str__(self) -> str:
        return f'장바구니 {self.__cart_id} | 상품 {self.__product_id} | 수량 {self.__quantity}'

# 단위테스트
if __name__ == '__main__':
    c = Cart('9000', 'woongseok', 'P001', 2)
    print(c)
