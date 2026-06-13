from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Account.account import Account
from Account.account_dao import AccountDAO
from Account.account_service import AccountService

class ConsoleBank:
    start_menu = ['종료', '로그인', '회원가입']
    banking_menu = ['로그아웃', '계좌목록', '입금', '출금', '계좌생성', '계좌해지', '내정보']
    member_myinfo_menu = ['돌아가기', '비밀번호수정', '회원탈퇴']
    admin_menu = ['로그아웃', '회원관리', '계좌관리']
    admin_account_menu = ['돌아가기', '전체계좌목록', '회원별계좌목록']
    admin_member_menu = ['돌아가기', '회원목록', '회원정보조회', '회원강퇴']

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.asv = AccountService(AccountDAO())

    def main(self):
        self.show_welcome()
        self.run_start_menu()
        self.say_goodbye()        

    # 시작 메뉴
    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)
            if menu == 0: # 종료
                break
            elif menu == 1: # 로그인
                self.menu_login()
            elif menu == 2: # 회원가입
                self.menu_join()
            else:
                print('없는 메뉴입니다.')

    def show_welcome(self):
        print('=' * 60)
        title = 'Woongseok Console Bank'
        print(f'{title:^60}')
        print('=' * 60)

    def say_goodbye(self):
        print('이용해 주셔서 감사합니다.')

    # 메뉴 선택
    def select_menu(self, menu_list):
        print('-' * 60)
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}')
        print(f'0. {menu_list[0]}')
        print('-' * 60)
        try:
            num = int(input('>> 원하시는 메뉴를 입력하세요. : '))
        except ValueError:
            return -1
        return num
    
    # 회원가입
    def menu_join(self):
        print('=' * 60)
        title = '회원가입'
        print(f'{title:^60}')
        print('=' * 60)
        user_id = input('>> 아이디 : ')
        password = input('>> 비밀번호 : ')
        name = input('>> 이름 : ')
        if self.msv.join(Member(user_id, password, name)):
            print('회원가입이 완료되었습니다.')
        else:
            print('이미 존재하는 아이디입니다.')
    
    # 로그인
    def menu_login(self):
        print('=' * 60)
        title = '로그인'
        print(f'{title:^60}')
        print('=' * 60)
        user_id = input('>> 아이디 : ')
        password = input('>> 비밀번호 : ')
        if self.msv.login(user_id, password):
            member = self.msv.view_member_info(self.msv.current_user)  # Member 객체 조회
            print(f'{member.get_name()}님, 환영합니다.')
            if self.msv.current_user == MemberService.ADMIN_ID:
                self.run_admin_menu()
            else:
                self.run_banking_menu()
        else:
            print('아이디 또는 비밀번호가 올바르지 않습니다.')

    # 로그아웃
    def menu_logout(self):
        self.msv.logout()

    # 회원 메뉴(은행 업무)
    def run_banking_menu(self):
        print('=' * 60)
        title = '은행 업무 메뉴'
        print(f'{title:^60}')
        print('=' * 60)
        while True:
            menu = self.select_menu(ConsoleBank.banking_menu)
            if menu == 0: # 로그아웃
                self.msv.logout()
                break
            elif menu == 1: # 계좌목록
                self.menu_list_my_accounts()
            elif menu == 2: # 입금
                self.menu_deposit()
            elif menu == 3: # 출금
                self.menu_withdraw()
            elif menu == 4: # 계좌 생성
                self.menu_create_account()
            elif menu == 5: # 계좌 해지
                self.menu_delete_account()
            elif menu == 6: # 내 정보
                self.menu_myinfo()
            else:
                print('없는 메뉴입니다.')

    # 계좌 목록
    def menu_list_my_accounts(self):
        self.menu_list_member_accounts(self.msv.current_user)

    # 계좌 목록 
    def menu_list_member_accounts(self, user):
        account_list = self.asv.get_members_accounts(user)
        print('=' * 60)
        if account_list:
            for account in account_list:
                print(account)
        else:
            print('등록된 계좌가 없습니다.')
        print('=' * 60)

    # 입금
    def menu_deposit(self):
        print('=' * 60)
        title = '입금'
        print(f'{title:^60}')
        print('=' * 60)
        self.menu_list_member_accounts(self.msv.current_user)
        account_no = input('>> 계좌번호 : ')
        amount = int(input('>> 입금액 : '))
        result = self.asv.deposit(account_no, amount)
        if result:
            print(f'계좌번호 {account_no}에 {amount:,}원을 입금했습니다.')
            balance = self.asv.get_account_balance(account_no)
            if balance >= 0:
                print(f'>> 잔액 : {balance:,}')
        else:
            print('입금을 할 수 없습니다.')
    
    # 출금
    def menu_withdraw(self):
        print('=' * 60)
        title = '출금'
        print(f'{title:^60}')
        print('=' * 60)
        self.menu_list_member_accounts(self.msv.current_user)
        account_no = input('>> 계좌번호 : ')
        amount = int(input('>> 출금액 : '))
        password = input('>> 비밀번호 : ')
        try:
            self.asv.withdraw(self.msv.current_user, account_no, amount, password)
        except ValueError:
            print('잔액이 부족합니다.')
        except LookupError:
            print('없는 계좌번호입니다.')
        except KeyError:
            print('출금을 할 수 없습니다.')
        else:
            print(f'계좌번호 {account_no}에서 {amount:,}원을 출금했습니다.')
            balance = self.asv.get_account_balance(account_no)
            print(f'잔액 : {balance:,}')

    # 계좌 생성
    def menu_create_account(self):
        print('=' * 60)
        title = '계좌 생성'
        print(f'{title:^60}')
        print('=' * 60)
        password = input('>> 비밀번호 : ')
        balance = int(input('>> 최초 입금액 : '))
        if self.asv.create_account(Account(0, self.msv.current_user, balance, password)):
            print('계좌를 생성했습니다.')
            self.menu_list_member_accounts(self.msv.current_user)
        else:
            print('계좌 생성에 실패했습니다.')
    
    # 계좌 해지
    def menu_delete_account(self):
        print('=' * 60)
        title = '계좌 해지'
        print(f'{title:^60}')
        print('=' * 60)
        self.menu_list_member_accounts(self.msv.current_user)
        account_no = input('>> 계좌번호 : ')
        password = input('>> 비밀번호 : ')
        try:
            self.asv.delete_account(self.msv.current_user, account_no, password)
        except ValueError:
            balance = self.asv.get_account_balance(account_no)
            print(f'잔액 {balance:,}원이 있습니다. 모두 출금 후 계좌를 해지해주세요.')
        except LookupError:
            print('없는 계좌번호입니다.')
        except KeyError:
            print('계좌 해지를 할 수 없습니다.')

        else:
            print(f'계좌번호 {account_no}을 해지했습니다.')

    # 내 정보
    def menu_myinfo(self):
        self.run_my_info_menu()

    # 내 정보 메뉴
    def run_my_info_menu(self):
        print('=' * 60)
        title = '내 정보 메뉴'
        print(f'{title:^60}')
        print('=' * 60)
        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 비밀번호 수정
                self.menu_update_password()
            elif menu == 2: # 회원탈퇴
                self.menu_delete_membership()
                break
            else:
                print('없는 메뉴입니다.')

    # 현재 로그인한 회원 정보
    def menu_view_myinfo(self):
        member = self.msv.view_member_info(self.msv.current_user)
        if member:
            print(member)

    # 비밀번호 수정
    def menu_update_password(self):
        print('=' * 60)
        title = '비밀번호 변경'
        print(f'{title:^60}')
        print('=' * 60)
        org_password = input('>> 기존 비밀번호 : ')
        new_password = input('>> 새 비밀번호 : ')
        if self.msv.update_member_password(self.msv.current_user, org_password, new_password):
            print('비밀번호를 변경했습니다.')
        else:
            print('비밀번호 변경에 실패했습니다.')

    # 회원 탈퇴
    def menu_delete_membership(self):
        if self.msv.remove_member(self.msv.current_user):
            print('탈퇴 처리되었습니다.')
            self.msv.logout()
        else:
            print('탈퇴 처리에 실패했습니다.')

    # 관리자 메뉴
    def run_admin_menu(self):
        print('=' * 60)
        title = '관리자 메뉴'
        print(f'{title:^60}')
        print('=' * 60)
        while True:
            menu = self.select_menu(ConsoleBank.admin_menu)
            if menu == 0: # 로그아웃
                self.msv.logout()
                break
            elif menu == 1: # 회원관리
                self.menu_manage_members()
            elif menu == 2: # 계좌관리
                self.menu_manage_accounts()
            else:
                print('없는 메뉴입니다.')
    
    # 회원 관리
    def menu_manage_members(self):
        self.run_admin_member_menu()

    # 계좌 관리
    def menu_manage_accounts(self):
        self.run_admin_account_menu()
    
    # 관리자 계좌 관리 메뉴
    def run_admin_account_menu(self):
        print('=' * 60)
        title = '계좌 관리 메뉴'
        print(f'{title:^60}')
        print('=' * 60)
        while True:
            menu = self.select_menu(ConsoleBank.admin_account_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 전체 계좌 목록
                self.menu_list_all_accounts()
            elif menu == 2: # 회원별 계좌 목록
                self.menu_list_member_accounts_admin() # 관리자용
            else:
                print('없는 메뉴입니다.')

    # 전체 계좌 목록
    def menu_list_all_accounts(self):
        account_list = self.asv.get_all_accounts()
        print('=' * 60)
        if account_list:
            for account in account_list:
                print(account)
        else:
            print('등록된 계좌가 없습니다.')
        print('=' * 60)
       
    # 회원별 계좌 목록(관리자용)
    def menu_list_member_accounts_admin(self):
        user_id = input('>> 조회하실 회원 아이디를 입력하세요 : ')
        self.menu_list_member_accounts(user_id)
    
    # 관리자 회원 관리 메뉴
    def run_admin_member_menu(self):
        print('=' * 60)
        title = '회원 관리 메뉴'
        print(f'{title:^60}')
        print('=' * 60)
        while True:
            menu = self.select_menu(ConsoleBank.admin_member_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 회원 목록
                self.menu_list_members()
            elif menu == 2: # 회원 정보 조회
                self.menu_view_member_info()
            elif menu == 3: # 회원 강퇴
                self.menu_delete_member()
            else:
                print('없는 메뉴입니다.')

    # 관리자 회원 목록
    def menu_list_members(self):
        member_list = self.msv.list_members()
        print('=' * 60)
        if member_list:
            for member in member_list:
                print(member)
        else:
            print('가입한 회원이 없습니다.')
        print('=' * 60)
    
    # 회원 정보 조회
    def menu_view_member_info(self):
        user_id = input('>> 조회하실 회원 아이디를 입력하세요 : ')
        member = self.msv.view_member_info(user_id)
        if member:
            print(member)
        else:
            print('존재하지 않는 회원입니다')

    # 회원 강퇴
    def menu_delete_member(self):
        user_id = input('>> 강퇴하실 회원 아이디를 입력하세요 : ')
        if user_id == MemberService.ADMIN_ID:
            print('관리자 계정은 강퇴할 수 없습니다.')
        if self.msv.remove_member(user_id) and MemberService.ADMIN_ID != user_id:
            print('강퇴 처리되었습니다.')
        else:
            print('강퇴 처리에 실패했습니다.')


if __name__ == '__main__':
    app = ConsoleBank()
    app.main()