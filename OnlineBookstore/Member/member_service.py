from Member.member_dao import MemberDAO
from Member.member import Member

# 회원 관리 서비스
class MemberService:
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self, member_dao):
        self.__dao = member_dao
        self.current_user = None # 로그인 상태
        # 관리자 계정 자동 생성
        self.join(Member(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD, '관리자', '-', '-'))

    def join(self, member):
        return self.__dao.insert_member(member) # 중복 아이디면 False 반환

    def login(self, id, password):
        member = self.__dao.select_member_by_id(id)
        if member and member.get_password() == password:
            self.current_user = id
            return True
        return False

    def logout(self):
        self.current_user = None

    def is_admin(self):
        return self.current_user == MemberService.ADMIN_ID

    def list_members(self):
        return self.__dao.select_all_members()

    def view_member_info(self, id):
        return self.__dao.select_member_by_id(id)

    def update_member_info(self, id, member):
        return self.__dao.update_member(id, member)

    def update_password(self, id, org_pw, new_pw):
        if self.current_user != id:
            return False
        member = self.__dao.select_member_by_id(id)
        if member and member.get_password() == org_pw:
            member.set_password(new_pw)
            return True
        return False

    def remove_member(self, id):
        # 본인 또는 관리자만 탈퇴/강퇴 가능
        if self.current_user == id or self.is_admin():
            return self.__dao.delete_member(id)
        return False

# 단위테스트
if __name__ == '__main__':
    ms = MemberService(MemberDAO())
    print(ms.join(Member('woongseok', '1234', '최웅석', '성남시', '010')))
    print(ms.login('woongseok', '1234'), ms.current_user)
    print(ms.update_password('woongseok', '1234', '1111'))
    ms.login(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD)
    print(ms.remove_member('woongseok'))