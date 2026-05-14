class Member:
    def __init__(self, user_no, user_id, pw, name, phone, address):
        self.__user_no = user_no
        self.__id = user_id
        self.__pw = pw
        self.__name = name
        self.__phone = phone
        self.__address = address

    def get_user_no(self): return self.__user_no
    def get_id(self): return self.__id
    def get_pw(self): return self.__pw
    def get_name(self): return self.__name
    def get_phone(self): return self.__phone
    def get_address(self): return self.__address

    def member_update(self, name, pw, phone, address):
        self.__name = name
        self.__pw = pw
        self.__phone = phone
        self.__address = address
    
    def __str__(self):
        return f'----------------------\n아이디: {self.__id}\n비밀번호: {self.__pw}\n이름: {self.__name}\n전화번호: {self.__phone}\n주소: {self.__address}'
    

    

# 회원 관리 기능
class MemberService:
    def __init__(self):
        self.__member_list = []

    # 회원가입
    def register_member(self, user_no, user_id, pw, name, phone, address):
        member = Member(user_no, user_id, pw, name, phone, address)
        self.__member_list.append(member)
        return True
    
    # 회원목록
    def member_list(self):
        return self.__member_list
    
    # 회원상세정보
    def info_member(self, user_no):
        for member in self.__member_list:
            if member.get_user_no() == user_no:
                return member
        return None
    
    # 회원정보수정
    def edit_member(self, user_no, pw, name, phone, address):
        for member in self.__member_list:
            if member.get_user_no() == user_no:
                if member.get_pw() != pw:
                    return False
                member.member_update(name, pw, phone, address)
                return True
        return False
            
    # 회원탈퇴
    def del_member(self, user_no, pw):
        for member in self.__member_list:
            if member.get_user_no() == user_no:
                if member.get_pw() != pw:
                    return False
                self.__member_list.remove(member)
                return True
        return False
    

# 메뉴와 사용자 interaction에 따른 서비스 호출
def select_menu():
    print('======================================================================================')
    print(' 1. 회원가입 | 2. 회원목록 | 3. 회원상세정보 | 4. 회원정보수정 | 5. 회원탈퇴 | 0. 종료')
    print('======================================================================================')
    menu = int(input('>> 메뉴 선택'))
    return menu


mservice = MemberService()

print()
print('=====================회원관리=====================')

while True:
    menu = select_menu()
    if menu == 0: break
    elif menu == 1:
        # 회원번호, 아이디, 비밀번호, 이름, 전화번호, 주소 입력받아 회원가입
        user_no = int(input('> 회원번호 : '))
        user_id = input('> 아이디 : ')
        pw = input('> 비밀번호 : ')
        name = input('> 이름 : ')
        phone = (input('> 전화번호 : '))
        address = input('> 주소 : ')
        if mservice.register_member(user_no, user_id, pw, name, phone, address):
            print('결과 : 회원가입이 완료되었습니다')

    # 회원목록
    elif menu == 2:
        member_list = mservice.member_list()
        for member in member_list:
            print(member)

    # 회원상세정보
    elif menu == 3:
        user_no = int(input('> 회원번호 : '))
        member = mservice.info_member(user_no)
        if member:
            print(member)
        else:
            print('결과 : 회원번호에 해당하는 회원이 없습니다')

    # 회원정보수정
    elif menu == 4:
        user_no = int(input('> 회원번호 : '))
        pw = input('> 현재 비밀번호 : ')
        name = input('> 새 이름 : ')
        phone = input('> 새 전화번호 : ')
        address = input('> 새 주소 : ')
        if mservice.edit_member(user_no, pw, name, phone, address):
            print('결과 : 회원정보가 수정되었습니다')
        else:
            print('결과 : 존재하지 않는 회원 이거나 비밀번호가 일치하지 않습니다')

    # 회원탈퇴
    elif menu == 5:
        user_no = int(input('> 회원번호 :'))
        member = mservice.info_member(user_no)
        if member is None:
            print('결과 : 존재하지 않는 회원입니다')
        else:
            pw = input('> 비밀번호 : ')
            if mservice.del_member(user_no, pw):
                print('결과 : 회원탈퇴가 완료되었습니다')
            else:
                print('결과 : 존재하지 않는 회원 이거나 비밀번호가 일치하지 않습니다')


print('==================이용해 주셔서 감사합니다==================')