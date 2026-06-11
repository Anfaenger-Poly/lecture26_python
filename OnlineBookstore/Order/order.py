from datetime import datetime
from enum import StrEnum
from Order.order_item import OrderItem

# 주문 상태 (매직 스트링 대신 열거형)
class OrderStatus(StrEnum):
    COMPLETED = '주문완료'
    CANCELED = '주문취소'

class Order:
    def __init__(self, order_id, member_id, items, order_date, status):
        self.__order_id = order_id
        self.__member_id = member_id
        self.__items = items
        self.__order_date = order_date
        self.__status = status

    def get_order_id(self):
        return self.__order_id

    def get_member_id(self):
        return self.__member_id

    def get_items(self):
        return self.__items

    def get_order_date(self):
        return self.__order_date

    def get_status(self):
        return self.__status

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_status(self, status):
        self.__status = status

    def __str__(self):
        date_str = self.__order_date.strftime('%Y-%m-%d %H:%M')
        lines = [f'주문번호 {self.__order_id} | 회원 {self.__member_id} | {date_str} | {self.__status}']
        for item in self.__items:
            lines.append(str(item))
        return '\n'.join(lines)

# 단위테스트
if __name__ == '__main__':
    items = [OrderItem('1000', 2), OrderItem('1001', 1)]
    o = Order('1', 'woongseok', items, datetime.now(), OrderStatus.COMPLETED)
    print(o)
    o.set_status(OrderStatus.CANCELED)
    print(o.get_status())
