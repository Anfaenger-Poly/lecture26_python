from datetime import datetime
from Order.order_dao import OrderDAO
from Order.order import Order, OrderStatus
from Product.product_dao import ProductDAO
from errors import (NotFoundError, OutOfStockError, InvalidInputError,
                    InvalidStateError, PermissionDeniedError)
#==================
# 주문 관리 서비스 로직 : OrderService
# - 비즈니스 규칙(재고/할인/소유권)은 모두 이 계층에서 강제한다. UI 는 규칙을 모른다.
# - 단순 조회 실패는 None, 규칙 위반은 전용 예외로 신호한다.
# - ORDER-002: 회원은 취소 불가, 관리자만 취소 가능.
class OrderService:
    order_id_seq  = 1      # 주문번호 시퀀스
    MEMBER_DISCOUNT = 0.10  # 회원 장바구니 주문 할인율

    def __init__(self, order_dao: OrderDAO, product_dao: ProductDAO):
        self.__dao         = order_dao
        self.__product_dao = product_dao

    def _calc_price(self, unit_price: int, quantity: int, is_member: bool,
                    use_discount: bool) -> int:
        '''결제 금액 계산. 회원 + 장바구니 주문일 때만 10% 할인.'''
        total = unit_price * quantity
        if is_member and use_discount:
            total = int(total * (1 - OrderService.MEMBER_DISCOUNT))
        return total

    def create_order(self, owner_key: str, product_id: str, quantity: int,
                     is_member: bool, use_discount: bool = False) -> Order:
        '''
        owner_key   : 회원 id 또는 비회원 세션키
        is_member   : 회원 여부 (True 면 할인 적용 가능)
        use_discount: 장바구니 주문일 때 True (즉시구매는 False — 정가 결제)
        '''
        if quantity <= 0:
            raise InvalidInputError('수량은 1 이상이어야 합니다.')
        product = self.__product_dao.select_product_by_id(product_id)
        if not product:
            raise NotFoundError('없는 상품입니다.')
        if product.available_count() < quantity:
            raise OutOfStockError(
                f'재고가 부족합니다. (현재 판매 가능 코드 {product.available_count()}개)')

        # 코드 발급 (수량만큼 순서대로 꺼냄)
        issued_serials = []
        for _ in range(quantity):
            code = product.pop_available_code()
            if code:
                issued_serials.append(code.get_serial())

        total_price = self._calc_price(
            product.get_price(), quantity, is_member, use_discount)

        order_id = str(OrderService.order_id_seq)
        OrderService.order_id_seq += 1
        order = Order(
            order_id, owner_key, product_id, quantity, total_price,
            datetime.now(), OrderStatus.COMPLETED,
            ', '.join(issued_serials)  # 이메일 발송은 미구현
        )
        self.__dao.insert_order(order)
        return order

    def get_order(self, order_id: str) -> Order | None:
        return self.__dao.select_order_by_id(order_id)

    def list_orders(self) -> list[Order]:
        return self.__dao.select_all_orders()

    def list_orders_by_owner(self, owner_key: str) -> list[Order]:
        return self.__dao.select_orders_by_owner(owner_key)

    def cancel_order(self, order_id: str, is_admin: bool = False) -> None:
        # ORDER-002: 회원은 취소 불가, 관리자만 취소 가능.
        if not is_admin:
            raise PermissionDeniedError('주문 취소는 관리자만 가능합니다.')
        order = self.__dao.select_order_by_id(order_id)
        if not order:
            raise NotFoundError('없는 주문입니다.')
        if order.get_status() == OrderStatus.CANCELED:
            raise InvalidStateError('이미 취소된 주문입니다.')
        order.set_status(OrderStatus.CANCELED)
        self.__dao.update_order(order_id, order)

# 단위테스트
if __name__ == '__main__':
    from Product.product import Product, GameCode
    product_dao = ProductDAO()
    p = Product('P001', '사이버펑크 2077', 'Steam', 39000,
                [GameCode('CYBER-AAAA-1111'), GameCode('CYBER-BBBB-2222')])
    product_dao.insert_product(p)
    os = OrderService(OrderDAO(), product_dao)
    # 회원 + 장바구니 주문 → 10% 할인
    order = os.create_order('woongseok', 'P001', 1, is_member=True, use_discount=True)
    print(order, '| 발급 코드:', order.get_issued_code())
    try:
        os.cancel_order(order.get_order_id(), is_admin=False)
    except PermissionDeniedError as e:
        print('권한거부:', e)
    os.cancel_order(order.get_order_id(), is_admin=True)
    print('취소 후:', os.get_order(order.get_order_id()).get_status())
