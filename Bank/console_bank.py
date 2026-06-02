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
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_login()
            elif menu == 2:
                self.menu_join()
            else:
                print('없는 메뉴입니다.')
        self.say_goodbye()

    def show_welcome(self):
        print('========== Woongseok Console Bank ==========')

    def say_goodbye(self):
        print('이용해 주셔서 감사합니다.')

    def select_menu(self, menu_list):
        print('========== 메뉴 ==========')
        for index, menu in enumerate(menu_list[1:], start=1):
            print(f'{index}. {menu}')
        print(f'0. {menu_list[0]}')
        print('==========================')
        try:
            num = int(input('>> 메뉴 : '))
        except ValueError:
            return -1
        return num

    def run_start_menu(self):
        pass

    def menu_join(self):
        print('========== 회원가입 ==========')
        user_id = input('아이디 : ')
        password = input('비밀번호 : ')
        name = input('이름 : ')
        if self.msv.join(Member(user_id, password, name)):
            print('회원가입이 완료되었습니다.')
        else:
            print('이미 존재하는 아이디입니다.')

    def menu_login(self):
        print('========== 로그인 ==========')
        user_id = input('아이디 : ')
        password = input('비밀번호 : ')
        if self.msv.login(user_id, password):
            member = self.msv.view_member_info(self.msv.current_user)  # Member 객체 조회
            print(f'{member.get_name()}님, 환영합니다.')
            if self.msv.current_user == MemberService.ADMIN_ID:
                self.run_admin_menu()
            else:
                self.run_banking_menu()
        else:
            print('아이디 또는 비밀번호가 올바르지 않습니다.')

    def menu_logout(self):
        self.msv.logout()

    def run_banking_menu(self):
        print('========== 은행 업무 메뉴 ==========')
        while True:
            menu = self.select_menu(ConsoleBank.banking_menu)
            if menu == 0:
                self.msv.logout()
                break
            elif menu == 1:
                self.menu_list_my_accounts()
            elif menu == 2:
                self.menu_deposit()
            elif menu == 3:
                self.menu_withdraw()
            elif menu == 4:
                self.menu_create_account()
            elif menu == 5:
                self.menu_delete_account()
            elif menu == 6:
                self.menu_myinfo()
            else:
                print('없는 메뉴입니다.')

    def menu_list_my_accounts(self):
        self.menu_list_member_accounts(self.msv.current_user)

    def menu_list_member_accounts(self, user):
        account_list = self.asv.get_members_accounts(user)
        print('========================================')
        if account_list:
            for account in account_list:
                print(account)
        else:
            print('등록된 계좌가 없습니다.')
        print('========================================')

    def menu_deposit(self):
        print('========== 입금 ==========')
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

    def menu_withdraw(self):
        print('========== 출금 ==========')
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

    def menu_create_account(self):
        print('========== 계좌 생성 ==========')
        password = input('>> 비밀번호 : ')
        balance = int(input('>> 최초 입금액 : '))
        if self.asv.create_account(Account(0, self.msv.current_user, balance, password)):
            print('계좌를 생성했습니다.')
            self.menu_list_member_accounts(self.msv.current_user)
        else:
            print('계좌 생성에 실패했습니다.')

    def menu_delete_account(self):
        print('========== 계좌 해지 ==========')
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

    def menu_myinfo(self):
        self.run_my_info_menu()

    def run_my_info_menu(self):
        print('========== 내 정보 ==========')
        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_update_password()
            elif menu == 2:
                self.menu_delete_membership()
                break
            else:
                print('없는 메뉴입니다.')

    def menu_view_myinfo(self):
        pass

    def menu_view_member_info(self):
        pass

    def menu_update_password(self):
        pass

    def menu_delete_membership(self):
        pass

    def menu_delete_member(self):
        pass

    def run_admin_menu(self):
        pass

    def menu_manage_members(self):
        pass

    def menu_manage_accounts(self):
        pass

    def run_admin_account_menu(self):
        pass

    def menu_list_all_accounts(self):
        pass

    def run_admin_member_menu(self):
        pass

    def menu_list_members(self):
        pass


if __name__ == '__main__':
    app = ConsoleBank()
    app.main()