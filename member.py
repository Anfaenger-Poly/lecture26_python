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