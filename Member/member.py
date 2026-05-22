#======================
# 데이터 모델 정의 : Member
class Member:
    def __init__(self, id, password, name):
        self.__member_no = 0 # 회원번호는 회원가입 시 자동으로 부여되므로 초기값은 0
        self.__id = id
        self.__password = password
        self.__name = name

    def get_member_no(self):
        return self.__member_no
    
    def get_id(self):
        return self.__id
    
    def get_password(self):
        return self.__password
    
    def get_name(self):
        return self.__name
    
    def set_password(self, password):
        self.__password = password
    
    def __str__(self):
        return f'{self.__member_no}\t{self.__id}\t{self.__name}\t{self.__password}'   

#==================
# 회원 관리 서비스 로직 (Controller) : MemberService
class MemberService:
    def __init__(self, memberDao):
        self.__dao = memberDao # MemberDAO 객체를 받아 멤버 변수로 저장

    def join(self, member):
        # 이미 있는 아이디인지 확인, 있으면 False, 없으면 회원가입 후 True 반환
        if self.__dao.is_exist(member.get_id()):
            return False
        self.__dao.insert_member(member)
        return True

    def login(self, id, password):
        member = self.__dao.get_member_info(id)
        if member:
            if password == member.get_password():
                return member
        return None
    
    def list_members(self):
        member_list = self.__dao.get_all_members()
        return member_list
    
    def get_member_info(self, id):
        return self.__dao.get_member_info(id)
    
    def delete_member(self, id):
        return self.__dao.delete_member(id)
    
    def update_member(self, member):
        return self.__dao.update_member(member)

#====================
# 회원 데이터 접근 (CRUD) : MemberDAO 클래스 CRUD -> Create, Read, Update, Delete
class MemberDAO:
    def __init__(self):
        self.__memberDB = {} # 회원번호를 key로, Member 객체를 value로 저장하는 딕셔너리
    
    def insert_member(self, member):
        self.__memberDB[member.get_id()] = member

    def is_exist(self, id):
        if id in self.__memberDB.keys() : return True
        return False
    
    def get_member_info(self, id):
        if self.is_exist(id):
            return self.__memberDB[id]
        else:
            return None
        
    def get_all_members(self):
        return list(self.__memberDB.values()) # 회원번호, Member 객체 반환하는 리스트
    
    def update_member(self, member):
        if self.is_exist(member.get_id()):
            self.__memberDB[member.get_id()] = member
            return True
        return False
        
    def delete_member(self, id):
        if self.is_exist(id):
            del self.__memberDB[id]
            return True
        return False
    
