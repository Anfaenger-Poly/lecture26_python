from datetime import datetime
from enum import StrEnum

# 배송 상태 (매직 스트링 대신 열거형)
class DeliveryStatus(StrEnum):
    PREPARING = '배송준비중'
    SHIPPING = '배송중'
    DELIVERED = '배송완료'
    CANCELED = '배송취소'

class Delivery:
    def __init__(self, delivery_id, order_id, member_id,
                 address, status, delivery_date = None): # 배송 날짜는 배송완료 때 설정 -> None 값으로 설정
        self.__delivery_id = delivery_id
        self.__order_id = order_id
        self.__member_id = member_id
        self.__address = address
        self.__status = status
        self.__delivery_date = delivery_date

    def get_delivery_id(self):
        return self.__delivery_id

    def get_order_id(self):
        return self.__order_id

    def get_member_id(self):
        return self.__member_id

    def get_address(self):
        return self.__address

    def get_status(self):
        return self.__status

    def get_delivery_date(self):
        return self.__delivery_date

    def set_status(self, status):
        self.__status = status

    def set_delivery_date(self, delivery_date):
        self.__delivery_date = delivery_date

    def __str__(self):
        if self.__delivery_date:
            date_str = self.__delivery_date.strftime('%Y-%m-%d %H:%M')
        else:
            date_str = '-'
        return (f'배송번호 {self.__delivery_id} | 주문 {self.__order_id} | '
                f'{self.__address} | {self.__status} | {date_str}')

# 단위테스트
if __name__ == '__main__':
    d = Delivery('5000', '1', 'woongseok', '성남시', DeliveryStatus.PREPARING)
    print(d)
