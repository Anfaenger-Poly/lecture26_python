from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Book.book import Book
from Book.book_dao import BookDAO
from Book.book_service import BookService
from Order.order_dao import OrderDAO
from Order.order_service import OrderService
from Delivery.delivery import DeliveryStatus
from Delivery.delivery_dao import DeliveryDAO
from Delivery.delivery_service import DeliveryService
from Cart.cart_dao import CartDAO
from Cart.cart_service import CartService
from errors import BookstoreError

class ConsoleBookstore:
    start_menu = ['종료', '로그인', '회원가입', '도서 목록 조회',]
    member_menu = ['로그아웃', '주문 조회', '주문 목록 조회', '주문 취소', '도서 목록 조회', '장바구니 보기', '내 정보', '배송 조회', '회원 탈퇴']
    myinfo_menu = ['돌아가기', '내 정보 보기', '비밀번호 수정', '회원 정보 수정']
    book_browse_menu = ['돌아가기', '도서 정보 조회', '장바구니 담기']
    cart_view_menu = ['돌아가기', '주문하기', '도서 삭제']
    admin_menu = ['로그아웃', '도서 관리', '주문 관리', '배송 관리', '회원 관리']
    book_admin_menu = ['돌아가기', '도서 추가', '도서 수정', '도서 삭제', '도서 목록 조회', '도서 정보 조회']
    order_admin_menu = ['돌아가기', '주문 조회', '주문 목록 조회', '주문 취소']
    delivery_admin_menu = ['돌아가기', '배송 조회', '배송 상태 수정']
    member_admin_menu = ['돌아가기', '회원 목록 조회', '회원 탈퇴']

    def __init__(self):
        # 의존성 주입 DAO 객체를 각 Service 에 전달
        book_dao = BookDAO()
        self.ms = MemberService(MemberDAO())
        self.bs = BookService(book_dao)
        self.os = OrderService(OrderDAO(), book_dao) # 재고 차감 위해 book_dao 공유
        self.ds = DeliveryService(DeliveryDAO())
        self.cs = CartService(CartDAO())

    def main(self):
        self.show_welcome()
        self.run_start_menu()
        self.say_goodbye()

    def show_welcome(self):
        self.print_title('Woongseok Online Bookstore')

    def say_goodbye(self):
        print('이용해 주셔서 감사합니다.')

    def print_title(self, title):
        print('=' * 60)
        print(f'{title:^60}')
        print('=' * 60)

    # 숫자 입력 처리 (예외 처리)
    def input_int(self, prompt):
        try:
            return int(input(prompt))
        except ValueError:
            return None
        
    # 메뉴 선택
    def select_menu(self, menu_list):
        print('-' * 60)
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}')
        print(f'0. {menu_list[0]}')
        print('-' * 60)
        try:
            num = int(input('>> 원하시는 메뉴를 입력하세요. :'))
        except ValueError:
            return -1
        return num

    # 시작 메뉴
    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleBookstore.start_menu)
            if menu == 0: # 종료
                break
            elif menu == 1: # 로그인
                self.menu_login()
            elif menu == 2: # 회원가입
                self.menu_join()
            elif menu == 3: # 도서 목록 조회
                self.menu_list_books()
            else:
                print('없는 메뉴입니다.')

    # 로그인
    def menu_login(self):
        self.print_title('로그인')
        user_id = input('>> 아이디 : ')
        password = input('>> 비밀번호 : ')
        if self.ms.login(user_id, password):
            member = self.ms.view_member_info(self.ms.current_user)
            print(f'{member.get_name()}님, 환영합니다.')
            if self.ms.is_admin():
                self.run_admin_menu()
            else:
                self.run_member_menu()
        else:
            print('아이디 또는 비밀번호가 올바르지 않습니다.')

    # 회원가입
    def menu_join(self):
        self.print_title('회원가입')
        user_id = input('>> 아이디 : ')
        password = input('>> 비밀번호 : ')
        name = input('>> 이름 : ')
        address = input('>> 주소 : ')
        phone = input('>> 연락처 : ')
        if self.ms.join(Member(user_id, password, name, address, phone)):
            print('회원가입이 완료되었습니다.')
        else:
            print('이미 존재하는 아이디입니다.')

    # 도서 목록 조회
    def menu_list_books(self):
        self.print_title('도서 목록')
        book_list = self.bs.list_books()
        if book_list:
            for book in book_list:
                print(book.to_list_str())
        else:
            print('등록된 도서가 없습니다.')
        print('=' * 60)

    # 도서 정보 조회
    def menu_book_info(self):
        book_id = input('>> 조회할 도서 번호 : ')
        book = self.bs.get_book(book_id)
        if book:
            print(book)
        else:
            print('없는 도서입니다.')

    # 로그아웃
    def menu_logout(self):
        self.ms.logout()

    # 회원 메뉴
    def run_member_menu(self):
        self.print_title('회원 메뉴')
        while True:
            menu = self.select_menu(ConsoleBookstore.member_menu)
            if menu == 0: # 로그아웃
                self.ms.logout()
                break
            elif menu == 1: # 주문 조회
                self.menu_view_order()
            elif menu == 2: # 주문 목록 조회
                self.menu_list_orders()
            elif menu == 3: # 주문 취소
                self.menu_cancel_order()
            elif menu == 4: # 도서 목록 조회
                self.run_book_browse_menu()
            elif menu == 5: # 장바구니 보기
                self.run_cart_view_menu()
            elif menu == 6: # 내 정보
                self.run_myinfo_menu()
            elif menu == 7: # 배송 조회
                self.menu_view_delivery()
            elif menu == 8: # 회원 탈퇴
                self.menu_quit_membership()
                break
            else:
                print('없는 메뉴입니다.')

    # 도서 목록 조회 메뉴(회원)
    def run_book_browse_menu(self):
        self.menu_list_books()
        while True:
            menu = self.select_menu(ConsoleBookstore.book_browse_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 도서 정보 조회
                self.menu_book_info()
            elif menu == 2: # 장바구니 담기
                self.menu_add_to_cart()
            else:
                print('없는 메뉴입니다.')

    # 장바구니 담기
    def menu_add_to_cart(self):
        book_id = input('>> 장바구니에 담을 도서 번호 : ')
        if not self.bs.get_book(book_id):
            print('없는 도서입니다.')
            return
        quantity = self.input_int('>> 수량 : ')
        if quantity is None:
            print('수량은 숫자로 입력해주세요.')
            return
        try:
            self.cs.create_cart(self.ms.current_user, book_id, quantity)
        except BookstoreError as e:
            print(e)
            return
        print('장바구니에 담았습니다.')

    # 주문 조회
    def menu_view_order(self):
        order_id = input('>> 조회할 주문번호 : ')
        order = self.os.get_order(order_id)
        if order and order.get_member_id() == self.ms.current_user:
            print(order)
        else:
            print('주문을 찾을 수 없습니다.')

    # 주문 목록 조회
    def menu_list_orders(self):
        self.print_title('내 주문 목록')
        order_list = self.os.list_orders_by_member(self.ms.current_user)
        if order_list:
            for order in order_list:
                print(order)
        else:
            print('주문 내역이 없습니다.')
        print('=' * 60)

    # 주문 취소
    def menu_cancel_order(self):
        order_id = input('>> 취소할 주문번호 : ')
        try:
            self.os.cancel_order(order_id, self.ms.current_user, is_admin = False)
        except BookstoreError as e:
            print(e)
            return
        self.__cancel_linked_delivery(order_id)
        print('주문이 취소되었습니다.')

    # 주문 취소 시 연결된 배송도 취소
    def __cancel_linked_delivery(self, order_id):
        delivery = self.ds.get_delivery_by_order(order_id)
        if delivery:
            self.ds.update_status(delivery.get_delivery_id(), DeliveryStatus.CANCELED)

    # 배송 조회
    def menu_view_delivery(self):
        self.print_title('배송 조회')
        delivery_list = self.ds.get_delivery_by_member(self.ms.current_user)
        if delivery_list:
            for delivery in delivery_list:
                print(delivery)
        else:
            print('배송 내역이 없습니다.')
        print('=' * 60)

    # 회원 탈퇴
    def menu_quit_membership(self):
        if self.ms.remove_member(self.ms.current_user):
            print('탈퇴 처리되었습니다.')
            self.ms.logout()
        else:
            print('탈퇴 처리에 실패했습니다.')

    # 장바구니 보기 메뉴
    def run_cart_view_menu(self):
        self.menu_view_cart()
        while True:
            menu = self.select_menu(ConsoleBookstore.cart_view_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 주문하기
                self.menu_order_cart()
            elif menu == 2: # 장바구니에서 도서 삭제
                self.menu_delete_cart()
            else:
                print('없는 메뉴입니다.')

    # 장바구니 주문하기
    def menu_order_cart(self):
        cart_list = self.cs.view_cart(self.ms.current_user)
        if not cart_list:
            print('장바구니가 비어 있습니다.')
            return
        address = input('>> 배송 주소 : ')  # 주소는 한 번만 입력받아 모든 배송에 사용
        ordered = 0
        for cart in cart_list:
            try:
                order = self.os.create_order(
                    self.ms.current_user, cart.get_book_id(), cart.get_quantity())
            except BookstoreError as e:
                print(f'[도서 {cart.get_book_id()}] {e}')  # 실패: 장바구니에 그대로 남김
                continue
            delivery = self.ds.create_delivery(
                order.get_order_id(), self.ms.current_user, address)
            self.cs.delete_cart(cart.get_cart_id())  # 성공한 도서만 장바구니에서 제거
            print(f'주문 완료 (주문번호 {order.get_order_id()}, '
                  f'배송번호 {delivery.get_delivery_id()})')
            ordered += 1
        if ordered:
            print(f'총 {ordered}건 주문이 완료되었습니다.')
        else:
            print('주문된 항목이 없습니다.')

    # 도서 삭제(장바구니에서 제거)
    def menu_delete_cart(self):
        self.menu_view_cart()
        cart_id = input('>> 비울 장바구니 번호 : ')
        if self.cs.delete_cart(cart_id):
            print('장바구니에서 삭제했습니다.')
        else:
            print('삭제하지 못했습니다.')

    # 장바구니 확인
    def menu_view_cart(self):
        self.print_title('장바구니 조회')
        cart_list = self.cs.view_cart(self.ms.current_user)
        if cart_list:
            for cart in cart_list:
                print(cart)
        else:
            print('장바구니가 비어있습니다.')
        print('=' * 60)

    # 내 정보 메뉴
    def run_myinfo_menu(self):
        self.print_title('내 정보')
        while True:
            menu = self.select_menu(ConsoleBookstore.myinfo_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 내 정보 보기
                self.menu_view_myinfo()
            elif menu == 2: # 비밀번호 수정
                self.menu_update_password()
            elif menu == 3: # 회원 정보 수정
                self.menu_update_member_info()
            else:
                print('없는 메뉴입니다.')

    # 내 정보 보기
    def menu_view_myinfo(self):
        member = self.ms.view_member_info(self.ms.current_user)
        if member:
            print('=' * 60)
            print(f'아이디 : {member.get_id()}')
            print(f'이름   : {member.get_name()}')
            print(f'주소 : {member.get_address()}')
            print(f'연락처 : {member.get_phone()}')
            print('=' * 60)

    # 비밀번호 변경
    def menu_update_password(self):
        self.print_title('비밀번호 변경')
        org_password = input('>> 기존 비밀번호 : ')
        new_password = input('>> 새 비밀번호 : ')
        if self.ms.update_password(self.ms.current_user, org_password, new_password):
            print('비밀번호를 변경했습니다.')
        else:
            print('비밀번호 변경에 실패했습니다.')

    # 회원 정보 수정
    def menu_update_member_info(self):
        self.print_title('회원 정보 수정')
        member = self.ms.view_member_info(self.ms.current_user)
        if not member:
            print('회원 정보를 찾을 수 없습니다.')
            return
        print('(변경하지 않을 항목은 Enter를 눌러주세요.)')
        name = input(f'>> 이름 [{member.get_name()}] : ') or member.get_name()
        address = input(f'>> 주소 [{member.get_address()}] : ') or member.get_address()
        phone = input(f'>> 연락처 [{member.get_phone()}] : ') or member.get_phone()
        updated = Member(member.get_id(), member.get_password(), name, address, phone)
        if self.ms.update_member_info(member.get_id(), updated):
            print('회원 정보를 수정했습니다.')
        else:
            print('회원 정보 수정에 실패했습니다.')

    # 관리자 메뉴
    def run_admin_menu(self):
        self.print_title('관리자 메뉴')
        while True:
            menu = self.select_menu(ConsoleBookstore.admin_menu)
            if menu == 0: # 로그아웃
                self.ms.logout()
                break
            elif menu == 1: # 도서 관리
                self.run_book_admin_menu()
            elif menu == 2: # 주문 관리
                self.run_order_admin_menu()
            elif menu == 3: # 배송 관리
                self.run_delivery_admin_menu()
            elif menu == 4: # 회원 관리
                self.run_member_admin_menu()
            else:
                print('없는 메뉴입니다.')

    # 도서 관리(관리자)
    def run_book_admin_menu(self):
        self.print_title('도서 관리')
        while True:
            menu = self.select_menu(ConsoleBookstore.book_admin_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 도서 추가
                self.menu_add_book()
            elif menu == 2: # 도서 수정
                self.menu_update_book()
            elif menu == 3: # 도서 삭제
                self.menu_delete_book()
            elif menu == 4: # 도서 목록 조회
                self.menu_list_books()
            elif menu == 5: # 도서 정보 조회
                self.menu_book_info()
            else:
                print('없는 메뉴입니다.')

    # 도서 추가(관리자)
    def menu_add_book(self):
        self.print_title('도서 추가')
        title = input('>> 제목 : ')
        author = input('>> 저자 : ')
        price = self.input_int('>> 가격 : ')
        stock = self.input_int('>> 재고 : ')
        if price is None or stock is None:
            print('가격과 재고는 숫자로 입력해주세요.')
            return
        try:
            book = self.bs.add_book(Book(None, title, author, price, stock))
        except BookstoreError as e:
            print(e)
            return
        print(f'도서를 추가했습니다. (도서 번호 {book.get_book_id()})')

    # 도서 수정(관리자)
    def menu_update_book(self):
        book_id = input('>> 수정할 도서 번호 : ')
        book = self.bs.get_book(book_id)
        if not book:
            print('없는 도서입니다.')
            return
        print('(변경하지 않을 항목은 Enter를 눌러주세요.)')
        title = input(f'>> 제목 [{book.get_title()}] : ') or book.get_title()
        author = input(f'>> 저자 [{book.get_author()}] : ') or book.get_author()
        price_in = input(f'>> 가격 [{book.get_price()}] : ')
        stock_in = input(f'>> 재고 [{book.get_stock()}] : ')
        try:
            price = int(price_in) if price_in else book.get_price()
            stock = int(stock_in) if stock_in else book.get_stock()
        except ValueError:
            print('가격과 재고는 숫자로 입력해주세요.')
            return
        try:
            ok = self.bs.update_book(book_id, Book(book_id, title, author, price, stock))
        except BookstoreError as e:
            print(e)
            return
        if ok:
            print('도서를 수정했습니다.')
        else:
            print('도서 수정에 실패했습니다.')

    # 도서 삭제(관리자)
    def menu_delete_book(self):
        book_id = input('>> 삭제할 도서 번호 : ')
        if self.bs.remove_book(book_id):
            print('도서를 삭제했습니다.')
        else:
            print('도서 삭제에 실패했습니다.')

    # 주문 관리(관리자)
    def run_order_admin_menu(self):
        self.print_title('주문 관리')
        while True:
            menu = self.select_menu(ConsoleBookstore.order_admin_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 주문 조회
                self.menu_view_order_admin()
            elif menu == 2: # 주문 목록 조회
                self.menu_list_orders_admin()
            elif menu == 3: # 주문 취소
                self.menu_cancel_order_admin()
            else:
                print('없는 메뉴입니다.')

    # 주문 조회(관리자)
    def menu_view_order_admin(self):
        order_id = input('>> 조회할 주문번호 : ')
        order = self.os.get_order(order_id)
        if order:
            print(order)
        else:
            print('없는 주문입니다.')

    # 주문 목록 조회(관리자)
    def menu_list_orders_admin(self):
        self.print_title('전체 주문 목록')
        order_list = self.os.list_orders()
        if order_list:
            for order in order_list:
                print(order)
        else:
            print('주문 내역이 없습니다.')
        print('=' * 60)

    # 주문 취소(관리자)
    def menu_cancel_order_admin(self):
        order_id = input('>> 취소할 주문번호 : ')
        try:
            self.os.cancel_order(order_id, self.ms.current_user, is_admin = True)
        except BookstoreError as e:
            print(e)
            return
        self.__cancel_linked_delivery(order_id)
        print('주문이 취소되었습니다.')

    # 배송 관리(관리자)
    def run_delivery_admin_menu(self):
        self.print_title('배송 관리')
        while True:
            menu = self.select_menu(ConsoleBookstore.delivery_admin_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 배송 조회
                self.menu_view_delivery_admin()
            elif menu == 2: # 배송 상태 수정
                self.menu_update_delivery_status()
            else:
                print('없는 메뉴입니다.')

    # 배송 조회(관리자)
    def menu_view_delivery_admin(self):
        self.print_title('전체 배송 목록')
        delivery_list = self.ds.list_deliveries()
        if delivery_list: # 배송목록이 비어있지 않으면 배송목록 출력, 비어있으면 메시지 출력
            for delivery in delivery_list:
                print(delivery)
        else:
            print('배송 내역이 없습니다.')
        print('=' * 60)

    # 배송 상태 수정(관리자)
    def menu_update_delivery_status(self):
        self.menu_view_delivery_admin()
        delivery_id = input('>> 상태를 변경할 배송번호 : ')
        valid = ' / '.join(s.value for s in DeliveryStatus)
        print(f'상태: {valid}')
        try:
            status = DeliveryStatus(input('>> 새 배송 상태 : '))
        except ValueError:
            print('올바른 배송 상태가 아닙니다.')
            return
        try:
            self.ds.update_status(delivery_id, status)
        except BookstoreError as e:
            print(e)
            return
        print('배송 상태를 변경했습니다.')

    # 회원 관리(관리자)
    def run_member_admin_menu(self):
        self.print_title('회원 관리')
        while True:
            menu = self.select_menu(ConsoleBookstore.member_admin_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 회원 목록 조회
                self.menu_list_members()
            elif menu == 2: # 회원 탈퇴
                self.menu_quit_member_admin()
            else:
                print('없는 메뉴입니다.')

    # 회원 목록 조회(관리자)
    def menu_list_members(self):
        self.print_title('회원 목록')
        member_list = self.ms.list_members()
        if member_list:
            for member in member_list:
                print(member)
        else:
            print('가입한 회원이 없습니다.')
        print('=' * 60)

    # 회원 강퇴(관리자)
    def menu_quit_member_admin(self):
        user_id = input('>> 강퇴할 회원 아이디 : ')
        if user_id == MemberService.ADMIN_ID:
            print('관리자 계정은 강퇴할 수 없습니다.')
            return
        if self.ms.remove_member(user_id):
            print('강퇴 처리되었습니다.')
        else:
            print('강퇴 처리에 실패했습니다.')

if __name__ == '__main__':
    app = ConsoleBookstore()
    app.main()