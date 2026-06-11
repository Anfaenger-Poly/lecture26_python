from datetime import datetime
from Order.order_dao import OrderDAO
from Order.order import Order, OrderStatus
from Order.order_item import OrderItem
from Book.book_dao import BookDAO
from errors import NotFoundError, OutOfStockError, InvalidInputError, InvalidStateError, PermissionDeniedError

# 주문 관리 서비스
class OrderService:
    order_id_seq = 1 # 주문번호 시퀀스

    def __init__(self, order_dao, book_dao):
        self.__dao = order_dao
        self.__book_dao = book_dao

    def create_order(self, member_id, cart_list):
        if not cart_list:
            raise InvalidInputError('주문할 도서가 없습니다.')
        for cart in cart_list:
            if cart.get_quantity() <= 0:
                raise InvalidInputError('수량은 1 이상이어야 합니다.')
            book = self.__book_dao.select_book_by_id(cart.get_book_id())
            if not book:
                raise NotFoundError(f'없는 도서입니다. (도서 번호 {cart.get_book_id()})')
            if book.get_stock() < cart.get_quantity():
                raise OutOfStockError(f'재고가 부족합니다. (도서번호 {cart.get_book_id()}, 현재 재고 {book.get_stock()})')
        
        # 재고 차감
        items = []
        for cart in cart_list:
            book = self.__book_dao.select_book_by_id(cart.get_book_id())
            book.set_stock(book.get_stock() - cart.get_quantity())
            self.__book_dao.update_book(cart.get_book_id(), book)
            items.append(OrderItem(cart.get_book_id(), cart.get_quantity()))

        order_id = str(OrderService.order_id_seq)
        OrderService.order_id_seq += 1
        order = Order(order_id, member_id, items, datetime.now(), OrderStatus.COMPLETED)
        self.__dao.insert_order(order)
        return order
    
    def get_order(self, order_id):
        return self.__dao.select_order_by_id(order_id)

    def list_orders(self):
        return self.__dao.select_all_orders()

    def list_orders_by_member(self, member_id):
        return self.__dao.select_orders_by_member(member_id)

    def cancel_order(self, order_id, requester_id, is_admin):
        order = self.__dao.select_order_by_id(order_id)
        if not order:
            raise NotFoundError('없는 주문입니다.')
        if not is_admin and order.get_member_id() != requester_id: # 관리자가 아니고 주문자가 아닐 때
            raise PermissionDeniedError('본인 주문만 취소할 수 있습니다.')
        if order.get_status() == OrderStatus.CANCELED: # 주문이 취소되었을 때
            raise InvalidStateError('이미 취소된 주문입니다.')
        # 재고 복구
        for item in order.get_items():
            book = self.__book_dao.select_book_by_id(item.get_book_id())
            if book:
                book.set_stock(book.get_stock() + item.get_quantity())
                self.__book_dao.update_book(book.get_book_id(), book)
        order.set_status(OrderStatus.CANCELED)
        self.__dao.update_order(order_id, order)

# 단위테스트
if __name__ == '__main__':
    from Book.book import Book

    book_dao = BookDAO()
    book_dao.insert_book(Book('1000', '파이썬', '박응용', 22000, 5))
    book_dao.insert_book(Book('1001', '자바', '남궁성', 30000, 3))

    class FakeCart:
        def __init__(self, book_id, qty):
            self._book_id = book_id
            self._qty = qty
        def get_book_id(self): return self._book_id
        def get_quantity(self): return self._qty
        def get_cart_id(self): return '99'

    os = OrderService(OrderDAO(), book_dao)
    order = os.create_order('woongseok', [FakeCart('1000', 2), FakeCart('1001', 1)])
    print(order)
    print('파이썬 재고:', book_dao.select_book_by_id('1000').get_stock())  # 3
    print('자바 재고:', book_dao.select_book_by_id('1001').get_stock())    # 2
    os.cancel_order(order.get_order_id(), 'woongseok', is_admin=False)
    print('취소 후 파이썬 재고:', book_dao.select_book_by_id('1000').get_stock())  # 5
    print('취소 후 자바 재고:', book_dao.select_book_by_id('1001').get_stock())   # 3