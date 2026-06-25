import uuid
from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Product.product import Product, GameCode
from Product.product_dao import ProductDAO
from Product.product_service import ProductService
from Order.order_dao import OrderDAO
from Order.order_service import OrderService
from Cart.cart_dao import CartDAO
from Cart.cart_service import CartService
from errors import GameMallError

class ConsoleGameMall:
    start_menu = ['종료', '로그인', '회원가입', '상품 목록 조회']
    member_menu = ['로그아웃', '주문 조회', '주문 목록 조회', '상품 목록 조회', '장바구니 보기', '내 정보', '회원 탈퇴']
    cart_menu = ['돌아가기', '주문하기', '상품 삭제', '장바구니 확인']
    myinfo_menu = ['돌아가기', '내 정보 보기', '비밀번호 수정', '회원정보 수정']
    admin_menu = ['로그아웃', '상품 관리', '주문 관리', '회원 관리']
    product_admin_menu = ['돌아가기', '상품 추가', '상품 수정', '상품 삭제', '상품 목록 조회', '상품 정보 조회']
    order_admin_menu = ['돌아가기', '주문 조회', '주문 목록 조회', '주문 취소']
    member_admin_menu = ['돌아가기', '회원 목록 조회', '회원 강퇴']

    def __init__(self):
        # 의존성 주입: DAO 객체를 각 Service 에 전달
        product_dao = ProductDAO()
        self.ms = MemberService(MemberDAO())
        self.ps = ProductService(product_dao)
        self.os = OrderService(OrderDAO(), product_dao)
        self.cs = CartService(CartDAO(), product_dao)
        # 비회원 세션키 — 로그아웃 상태에서 장바구니를 유지하기 위한 임시 키
        self._guest_key = self._new_guest_key()
        self._seed_products()

    def _seed_products(self):
        data = [
            ('사이버펑크 2077', 'Steam', 39000, ['CYBER-AAAA-1111', 'CYBER-BBBB-2222', 'CYBER-CCCC-3333']),
            ('엘든 링', 'Steam', 59000, ['ELDEN-AAAA-1111', 'ELDEN-BBBB-2222']),
            ('피파 25', 'PSN', 69000, ['FIFA-AAAA-1111', 'FIFA-BBBB-2222', 'FIFA-CCCC-3333']),
            ('헤일로 인피닛', 'Xbox', 49000, ['HALO-AAAA-1111', 'HALO-BBBB-2222']),
            ('마인크래프트', 'PC', 29000, ['MINE-AAAA-1111', 'MINE-BBBB-2222', 'MINE-CCCC-3333']),
        ]
        for name, platform, price, codes in data:
            p = self.ps.add_product(Product(None, name, platform, price))
            self.ps.add_codes(p.get_product_id(), codes)

    def _new_guest_key(self):
        return f'guest_{uuid.uuid4().hex[:8]}'

    def _owner_key(self):
        if self.ms.current_user:
            return self.ms.current_user
        else:
            self._guest_key

    def main(self):
        self.show_welcome()
        self.run_start_menu()
        self.say_goodbye()

    def show_welcome(self):
        self.print_title('Woongseok Online Game Mall')

    def say_goodbye(self):
        print('이용해 주셔서 감사합니다.')

    def print_title(self, title):
        print('=' * 60)
        print(f'{title:^60}')
        print('=' * 60)

    def input_int(self, prompt):
        try:
            return int(input(prompt))
        except ValueError:
            return None

    def select_menu(self, menu_list: list[str]) -> int:
        print('-' * 60)
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}')
        print(f'0. {menu_list[0]}')
        print('-' * 60)
        num = self.input_int('>> 원하시는 메뉴를 입력하세요. : ')
        if num is not None:
            return num
        else:
            return -1

    # 시작메뉴
    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleGameMall.start_menu)
            if menu == 0:
                break
            elif menu == 1: # 로그인
                self.menu_login()
            elif menu == 2: # 회원가입
                self.menu_join()
            elif menu == 3: # 상품 목록 조회
                self.menu_list_products()
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
        email = input('>> 이메일 : ')
        phone = input('>> 연락처 : ')
        try:
            if self.ms.join(Member(user_id, password, name, email, phone)):
                print('회원가입이 완료되었습니다.')
            else:
                print('이미 존재하는 아이디입니다.')
        except GameMallError as e:
            print(e)
            
    # 상품 목록
    def menu_list_products(self):
        self.print_title('상품 목록')
        product_list = self.ps.list_products()
        if not product_list:
            print('등록된 상품이 없습니다.')
            print('=' * 60)
            return
        for p in product_list:
            print(p)
        print('=' * 60)
        if self.ms.is_admin():
            return
        print('1. 장바구니 담기')
        print('2. 즉시구매')
        print('0. 돌아가기')
        print('-' * 60)
        menu = self.input_int('>> ')
        if menu == 1: # 장바구니 담기
            self._add_to_cart()
        elif menu == 2: # 즉시 주문
            self._instant_order()

    # 상품 카트에 담기
    def _add_to_cart(self):
        product_id = input('>> 담을 상품 번호 : ')
        if not self.ps.get_product(product_id):
            print('없는 상품입니다.')
            return
        quantity = self.input_int('>> 수량 : ')
        if quantity is None:
            print('수량은 숫자로 입력해주세요.')
            return
        try:
            self.cs.add_to_cart(self._owner_key(), product_id, quantity)
            print('장바구니에 담았습니다.')
        except GameMallError as e:
            print(e)

    # 즉시구매 — 1번에 1개 상품만 주문 가능
    def _instant_order(self): 
        product_id = input('>> 구매할 상품 번호 : ')
        product = self.ps.get_product(product_id)
        if not product:
            print('없는 상품입니다.')
            return
        is_member = bool(self.ms.current_user) and not self.ms.is_admin()
        # 즉시구매는 할인 없이 정가 결제
        print(f'상품명 : {product.get_name()}')
        print(f'결제금액 : {product.get_price():,}원')
        confirm = input('>> 구매하시겠습니까? (y/n) : ')
        if confirm.lower() != 'y':
            print('구매가 취소되었습니다.')
            return
        try:
            order = self.os.create_order(
                self._owner_key(), product_id, 1,
                is_member=is_member, use_discount=False)
            print(f'구매 완료 (주문번호 {order.get_order_id()}) | 결제 {order.get_total_price():,}원')
        except GameMallError as e:
            print(e)

    # 상품 
    def menu_product_info(self):
        product_id = input('>> 조회할 상품 번호 : ')
        product = self.ps.get_product(product_id)
        if product:
            print('=' * 60)
            print(f'상품번호 : {product.get_product_id()}')
            print(f'상품명 : {product.get_name()}')
            print(f'플랫폼 : {product.get_platform()}')
            print(f'가격 : {product.get_price():,}원')
            print(f'재고 : {product.stock_label()}')
            print('=' * 60)
        else:
            print('없는 상품입니다.')

    # 회원 메뉴
    def run_member_menu(self):
        self.print_title('회원 메뉴')
        while True:
            menu = self.select_menu(ConsoleGameMall.member_menu)
            if menu == 0:
                self.ms.logout()
                # 로그아웃 시 비회원 세션키 갱신 (장바구니 초기화)
                self._guest_key = self._new_guest_key()
                break
            elif menu == 1: # 주문 조회
                self.menu_view_order()
            elif menu == 2: # 주문 목록 조회
                self.menu_list_orders()
            elif menu == 3: # 상품 목록 조회
                self.menu_list_products()
            elif menu == 4: # 장바구니 메뉴
                self.run_cart_menu()
            elif menu == 5: # 내 정보 메뉴
                self.run_myinfo_menu()
            elif menu == 6: # 회원 탈퇴
                self.menu_quit_membership()
                break
            else:
                print('없는 메뉴입니다.')

    def menu_view_order(self):
        order_id = input('>> 조회할 주문번호 : ')
        order = self.os.get_order(order_id)
        if order and order.get_owner_key() == self.ms.current_user:
            print(order)
            if order.get_issued_code():
                print(f'발급 코드 : {order.get_issued_code()}')
        else:
            print('주문을 찾을 수 없습니다.')

    def menu_list_orders(self):
        self.print_title('내 주문 목록')
        order_list = self.os.list_orders_by_owner(self.ms.current_user)
        if order_list:
            for order in order_list:
                print(order)
        else:
            print('주문 내역이 없습니다.')
        print('=' * 60)

    def menu_quit_membership(self):
        if self.ms.remove_member(self.ms.current_user):
            print('탈퇴 처리되었습니다.')
            self.ms.logout()
            self._guest_key = self._new_guest_key()
        else:
            print('탈퇴 처리에 실패했습니다.')

    # 장바구니 메뉴
    def run_cart_menu(self):
        self.print_title('장바구니')
        while True:
            menu = self.select_menu(ConsoleGameMall.cart_menu)
            if menu == 0:
                break
            elif menu == 1: # 주문하기
                self.menu_order_from_cart()
            elif menu == 2: # 상품 삭제
                self.menu_delete_cart_item()
            elif menu == 3: # 장바구니 확인
                self.menu_view_cart()
            else:
                print('없는 메뉴입니다.')

    # 장바구니 담기
    def menu_add_to_cart(self):
        self.menu_list_products()
        product_id = input('>> 담을 상품 번호 : ')
        if not self.ps.get_product(product_id):
            print('없는 상품입니다.')
            return
        quantity = self.input_int('>> 수량 : ')
        if quantity is None:
            print('수량은 숫자로 입력해주세요.')
            return
        try:
            self.cs.add_to_cart(self._owner_key(), product_id, quantity)
            print('장바구니에 담았습니다.')
        except GameMallError as e:
            print(e)

    # 장바구니 확인
    def menu_view_cart(self):
        self.print_title('장바구니 확인')
        cart_list = self.cs.view_cart(self._owner_key())
        if not cart_list:
            print('장바구니가 비어 있습니다.')
            print('=' * 60)
            return
        total = 0
        for cart in cart_list:
            product = self.ps.get_product(cart.get_product_id())
            if product:
                subtotal = product.get_price() * cart.get_quantity()
                total += subtotal
                print(f'[{cart.get_cart_id()}] {product.get_name()} '
                      f'/ {cart.get_quantity()}개 / {subtotal:,}원')
            else:
                print(f'[{cart.get_cart_id()}] 상품 정보 없음')
        print(f'합계 : {total:,}원')
        if self.ms.current_user and not self.ms.is_admin():
            print(f'회원 할인 적용 시 : {int(total * 0.9):,}원 (10% 할인)')
        print('=' * 60)

    # 장바구니에서 상품 삭제
    def menu_delete_cart_item(self):
        self.menu_view_cart()
        cart_id = input('>> 삭제할 장바구니 번호 : ')
        print('삭제되었습니다.' if self.cs.delete_cart_item(cart_id)
              else '삭제에 실패했습니다.')

    # 장바구니에 담은 상품 주문
    def menu_order_from_cart(self):
        self.menu_view_cart()
        cart_list = self.cs.view_cart(self._owner_key())
        if not cart_list:
            return
        is_member = bool(self.ms.current_user) and not self.ms.is_admin()
        confirm = input('>> 장바구니 전체를 주문하시겠습니까? (y/n) : ')
        if confirm.lower() != 'y':
            print('주문이 취소되었습니다.')
            return
        success, fail = 0, 0
        for cart in cart_list:
            try:
                order = self.os.create_order(
                    self._owner_key(), cart.get_product_id(),
                    cart.get_quantity(), is_member=is_member, use_discount=True)
                print(f'주문 완료 (주문번호 {order.get_order_id()}) '
                      f'| 결제 {order.get_total_price():,}원'
                      f' | 코드: {order.get_issued_code()}')
                success += 1
            except GameMallError as e:
                print(f'주문 실패 [{cart.get_product_id()}]: {e}')
                fail += 1
        # 성공한 항목만 장바구니에서 제거
        if success > 0:
            self.cs.clear_cart(self._owner_key())
            print(f'주문 {success}건 완료, {fail}건 실패.')

    # 내 정보 메뉴
    def run_myinfo_menu(self):
        self.print_title('내 정보')
        while True:
            menu = self.select_menu(ConsoleGameMall.myinfo_menu)
            if menu == 0:
                break
            elif menu == 1: # 내 정보 보기
                self.menu_view_myinfo()
            elif menu == 2: # 비밀번호 수정
                self.menu_update_password()
            elif menu == 3: # 회원정보 수정
                self.menu_update_member_info()
            else:
                print('없는 메뉴입니다.')

    # 내 정보 보기
    def menu_view_myinfo(self):
        member = self.ms.view_member_info(self.ms.current_user)
        if member:
            print('=' * 60)
            print(f'아이디 : {member.get_id()}')
            print(f'이름 : {member.get_name()}')
            print(f'이메일 : {member.get_email()}')
            print(f'연락처 : {member.get_phone()}')
            print('=' * 60)

    # 비밀번호 수정
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
        self.print_title('회원정보 수정')
        member = self.ms.view_member_info(self.ms.current_user)
        if not member:
            print('회원 정보를 찾을 수 없습니다.')
            return
        print('(변경하지 않을 항목은 그냥 Enter)')
        name = input(f'>> 이름 [{member.get_name()}] : ')  or member.get_name()
        email = input(f'>> 이메일 [{member.get_email()}] : ') or member.get_email()
        phone = input(f'>> 연락처 [{member.get_phone()}] : ') or member.get_phone()
        updated = Member(member.get_id(), member.get_password(), name, email, phone)
        if self.ms.update_member_info(member.get_id(), updated):
            print('회원정보를 수정했습니다.')
        else:
            print('회원정보 수정에 실패했습니다.')

    # 관리자 메뉴
    def run_admin_menu(self):
        self.print_title('관리자 메뉴')
        while True:
            menu = self.select_menu(ConsoleGameMall.admin_menu)
            if menu == 0:
                self.ms.logout()
                break
            elif menu == 1: # 상품 관리 메뉴
                self.run_product_admin_menu()
            elif menu == 2: # 주문 관리 메뉴
                self.run_order_admin_menu()
            elif menu == 3: # 회원 관리 메뉴
                self.run_member_admin_menu()
            else:
                print('없는 메뉴입니다.')

    # 상품 관리(관리자)
    def run_product_admin_menu(self):
        self.print_title('상품 관리')
        while True:
            menu = self.select_menu(ConsoleGameMall.product_admin_menu)
            if menu == 0:
                break
            elif menu == 1: # 상품 추가
                self.menu_add_product()
            elif menu == 2: # 상품 수정
                self.menu_update_product()
            elif menu == 3: # 상품 삭제
                self.menu_delete_product()
            elif menu == 4: # 상품 목록 조회
                self.menu_list_products()
            elif menu == 5: # 상품 정보 조회
                self.menu_product_info()
            else:
                print('없는 메뉴입니다.')

    # 상품 추가
    def menu_add_product(self):
        self.print_title('상품 추가')
        name = input('>> 게임명 : ')
        platform = input('>> 플랫폼 (Steam/PSN/Xbox 등) : ')
        price = self.input_int('>> 가격 : ')
        if price is None:
            print('가격은 숫자로 입력해주세요.')
            return
        try:
            product = self.ps.add_product(Product(None, name, platform, price))
        except GameMallError as e:
            print(e)
            return
        print(f'상품을 추가했습니다. (상품번호 {product.get_product_id()})')
        # 코드 등록 여부 문의
        add_code = input('>> 지금 바로 코드(시리얼)를 등록하시겠습니까? (y/n) : ')
        if add_code.lower() == 'y':
            self._input_codes(product.get_product_id())


    def _input_codes(self, product_id):
        print('코드를 한 줄에 하나씩 입력하세요. (빈 줄 입력 시 종료)')
        serials = []
        while True:
            s = input('>> 코드 : ').strip()
            if not s:
                break
            serials.append(s)
        if serials:
            try:
                cnt = self.ps.add_codes(product_id, serials)
                print(f'{cnt}개의 코드를 등록했습니다.')
            except GameMallError as e:
                print(e)

    # 상품 수정
    def menu_update_product(self):
        product_id = input('>> 수정할 상품 번호 : ')
        product = self.ps.get_product(product_id)
        if not product:
            print('없는 상품입니다.')
            return
        print('(변경하지 않을 항목은 그냥 Enter)')
        name = input(f'>> 게임명 [{product.get_name()}] : ') or product.get_name()
        platform = input(f'>> 플랫폼 [{product.get_platform()}] : ') or product.get_platform()
        price_in = input(f'>> 가격 [{product.get_price()}] : ')
        try:
            price = int(price_in) if price_in else product.get_price()
        except ValueError:
            print('가격은 숫자로 입력해주세요.')
            return
        try:
            ok = self.ps.update_product(
                product_id,
                Product(product_id, name, platform, price, product.get_codes()))
        except GameMallError as e:
            print(e)
            return
        print('상품을 수정했습니다.' if ok else '상품 수정에 실패했습니다.')
        # 코드 추가 여부 문의
        add_code = input('>> 코드(시리얼)를 추가 등록하시겠습니까? (y/n) : ')
        if add_code.lower() == 'y':
            self._input_codes(product_id)

    # 상품 삭제
    def menu_delete_product(self):
        product_id = input('>> 삭제할 상품 번호 : ')
        print('상품을 삭제했습니다.' if self.ps.remove_product(product_id)
              else '상품 삭제에 실패했습니다.')

    # 주문 관리 메뉴(관리자)
    def run_order_admin_menu(self):
        self.print_title('주문 관리')
        while True:
            menu = self.select_menu(ConsoleGameMall.order_admin_menu)
            if menu == 0:
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
            if order.get_issued_code():
                print(f'발급 코드 : {order.get_issued_code()}')
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
            self.os.cancel_order(order_id, is_admin=True)
        except GameMallError as e:
            print(e)
            return
        print('주문이 취소되었습니다.')

    # 회원 관리(관리자)
    def run_member_admin_menu(self):
        self.print_title('회원 관리')
        while True:
            menu = self.select_menu(ConsoleGameMall.member_admin_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_list_members()
            elif menu == 2:
                self.menu_delete_member()
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

    # 회원 강퇴
    def menu_delete_member(self):
        user_id = input('>> 강퇴할 회원 아이디 : ')
        if user_id == MemberService.ADMIN_ID:
            print('관리자 계정은 강퇴할 수 없습니다.')
            return
        print('강퇴 처리되었습니다.' if self.ms.remove_member(user_id)
              else '강퇴 처리에 실패했습니다.')


if __name__ == '__main__':
    app = ConsoleGameMall()
    app.main()
