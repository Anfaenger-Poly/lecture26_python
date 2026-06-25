from datetime import datetime
from enum import StrEnum

#======================
# 주문 상태 (매직 스트링 대신 열거형)
class OrderStatus(StrEnum):
    COMPLETED = '주문완료'
    CANCELED  = '주문취소'

#======================
# 데이터 모델 정의 : Order
# order_date 는 표시용 문자열이 아니라 datetime 으로 보관하고, 출력 시 포맷한다.
# issued_code 는 주문 완료 시 발급된 게임 코드 시리얼. 취소 시에도 기록은 남긴다.
class Order:
    def __init__(self, order_id: str, owner_key: str, product_id: str,
                 quantity: int, total_price: int, order_date: datetime,
                 status: OrderStatus, issued_code: str = ''):
        self.__order_id    = order_id
        self.__owner_key   = owner_key    # 회원 id 또는 비회원 세션키
        self.__product_id  = product_id
        self.__quantity    = quantity
        self.__total_price = total_price  # 실 결제 금액 (할인 적용 후)
        self.__order_date  = order_date
        self.__status      = status
        self.__issued_code = issued_code  # 발급된 게임 코드 (이메일 발송은 미구현)

    def get_order_id(self) -> str:
        return self.__order_id

    def get_owner_key(self) -> str:
        return self.__owner_key

    def get_product_id(self) -> str:
        return self.__product_id

    def get_quantity(self) -> int:
        return self.__quantity

    def get_total_price(self) -> int:
        return self.__total_price

    def get_order_date(self) -> datetime:
        return self.__order_date

    def get_status(self) -> OrderStatus:
        return self.__status

    def get_issued_code(self) -> str:
        return self.__issued_code

    def set_order_id(self, order_id: str) -> None:
        self.__order_id = order_id

    def set_status(self, status: OrderStatus) -> None:
        self.__status = status

    def __str__(self) -> str:
        date_str = self.__order_date.strftime('%Y-%m-%d %H:%M')
        return (f'주문번호 {self.__order_id} | 상품 {self.__product_id} | '
                f'수량 {self.__quantity} | {self.__total_price:,}원 | '
                f'{date_str} | {self.__status}')

# 단위테스트
if __name__ == '__main__':
    o = Order('1', 'woongseok', 'P001', 1, 35100,
              datetime.now(), OrderStatus.COMPLETED, 'CYBER-AAAA-1111')
    print(o)
