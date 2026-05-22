from member import Member, MemberDAO, MemberService

class MemberManager:
    start_menu = ['종료', '로그인', '회원가입']
    admin_menu = ['관리자로그아웃', '회원목록', '회원정보조회', '회원강퇴']
    member_menu = ['로그아웃', '내정보조회', '내정보수정', '회원탈퇴']
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self):
        # 현재 로그인한 회원 정보를 저장하는 변수
        self.current_user = None
        # MemberService 객체 생성 시 MemberDAO 객체를 전달하여 의존성 주입
        self.ms = MemberService(MemberDAO())

    def main(self):
        self.show_welcome()
        self.ms.join(Member(MemberManager.ADMIN_ID, MemberManager.ADMIN_PASSWORD, None))
        # 관리자 계정 생성

        while True:
            menu = self.select_menu(MemberManager.start_menu)
            if menu == 0: break
            elif menu == 1: # 로그인
                id = input('>> id : ')
                password = input('>> password : ')
                self.current_user = self.ms.login(id, password)
                if self.current_user:
                    if self.current_user.get_id() == MemberManager.ADMIN_ID:
                        self.start_admin_menu()
                    else:
                        self.start_member_menu()
                else:
                    print('로그인에 실패하였습니다.')

            elif menu == 2: # 회원가입
                id = input('>> id : ')
                password = input('>> password : ')
                name = input('>> name : ')
                member = Member(id, password, name)
                if self.ms.join(member):
                    print('회원가입이 완료되었습니다.')
                else:
                    print('회원가입에 실패했습니다.')
            else:
                print('없는 메뉴입니다.')
        self.say_goodbye()

    def start_admin_menu(self):
        print('---------- 관리자 메뉴 ----------')
        while True:
            menu = self.select_menu(MemberManager.admin_menu)
            if menu == 0: break # return으로 바꿔도 됨
            elif menu == 1: # 회원목록
                self.list_all_member()

            elif menu == 2: # 회원정보조회
                id = input('조회할 회원 id : ')
                member = self.ms.get_member_info(id)
                if member:
                    print(f'{member.get_member_no()}\t{member.get_id()}\t{member.get_name()}')
                else:
                    print('존재하지 않는 회원입니다.')

            elif menu == 3: # 회원강퇴
                id = input('강퇴할 회원 id : ')
                if self.ms.delete_member(id):
                    print('회원이 강퇴되었습니다.')
                else:
                    print('존재하지 않는 회원입니다.')
            else:
                print('없는 메뉴입니다.')

    def list_all_member(self):
        if self.current_user.get_id() != MemberManager.ADMIN_ID:
            print('사용 권한이 없습니다.')
            return
        
        member_list = self.ms.list_members()
        if len(member_list) <= 1:
            print('가입한 회원이 없습니다.')
        else:
            for member in member_list: # 관리자 계정은 제외하고 출력
                if member.get_id() != MemberManager.ADMIN_ID:
                    print(f'{member.get_member_no()}\t{member.get_id()}\t{member.get_name()}')

    def start_member_menu(self):
        print('---------- 회원 메뉴 ----------')
        while True:
            menu = self.select_menu(MemberManager.member_menu)
            if menu == 0: break
            elif menu == 1: # 내정보조회
                print(self.current_user)

            elif menu == 2: # 내정보수정
                new_password = input('새 비밀번호를 입력해주세요 : ')
                self.current_user.set_password(new_password)
                self.ms.update_member(self.current_user)
                print('비밀번호가 변경되었습니다.')

            elif menu == 3: # 회원탈퇴
                if self.ms.delete_member(self.current_user.get_id()):
                    print('회원 탈퇴가 완료되었습니다.')
                    self.current_user = None
                    break
            else:
                print('없는 메뉴입니다.')

    def show_welcome(self):
        print('=' * 50)
        title = 'Member Manager'
        print(f'{title:^50}')
        print('=' * 50)

    def say_goodbye(self):
        print('안녕히 가세요')

    def print_menu(self, menu_list):
        print('-' * 40)
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}')
        print(f'0. {menu_list[0]}')
        print('-' * 40)

    def select_menu(self, menu_list):
        self.print_menu(menu_list)
        try:
            menu = int(input('메뉴 선택 : '))
            return menu
        except ValueError:
            return -1

if __name__ == '__main__':
    app = MemberManager()
    app.main()