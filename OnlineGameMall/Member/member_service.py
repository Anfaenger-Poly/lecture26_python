from Member.member_dao import MemberDAO
from Member.member import Member
from errors import InvalidInputError
#==================
# 회원 관리 서비스 로직 : MemberService
class MemberService:
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self, member_dao: MemberDAO):
        self.__dao = member_dao
        self.current_user: str | None = None  # 로그인 상태
        # 관리자 계정 자동 생성
        self.join(Member(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD, '관리자', '-', '-'))

    def join(self, member: Member) -> bool:
        # 입력 불변식은 서비스가 검증한다 (UI 를 믿지 않는다).
        if not member.get_id().strip():
            raise InvalidInputError('아이디는 비어 있을 수 없습니다.')
        if not member.get_password().strip():
            raise InvalidInputError('비밀번호는 비어 있을 수 없습니다.')
        if not member.get_name().strip():
            raise InvalidInputError('이름은 비어 있을 수 없습니다.')
        # 중복 아이디면 insert_member 가 False 반환
        return self.__dao.insert_member(member)

    def login(self, id: str, password: str) -> bool:
        member = self.__dao.select_member_by_id(id)
        if member and member.get_password() == password:
            self.current_user = id
            return True
        return False

    def logout(self) -> None:
        self.current_user = None

    def is_admin(self) -> bool:
        return self.current_user == MemberService.ADMIN_ID

    def list_members(self) -> list[Member]:
        return self.__dao.select_all_members()

    def view_member_info(self, id: str) -> Member | None:
        return self.__dao.select_member_by_id(id)

    def update_member_info(self, id: str, member: Member) -> bool:
        return self.__dao.update_member(id, member)

    def update_password(self, id: str, org_pw: str, new_pw: str) -> bool:
        if self.current_user != id:
            return False
        member = self.__dao.select_member_by_id(id)
        if member and member.get_password() == org_pw:
            member.set_password(new_pw)
            return True
        return False

    def remove_member(self, id: str) -> bool:
        # 본인이거나 관리자만 탈퇴/강퇴 가능
        if self.current_user == id or self.is_admin():
            return self.__dao.delete_member(id)
        return False

# 단위테스트
if __name__ == '__main__':
    ms = MemberService(MemberDAO())
    print(ms.join(Member('woongseok', '1234', '최웅석', 'a@a.com', '010')))
    print(ms.login('woongseok', '1234'), ms.current_user)
    print(ms.update_password('woongseok', '1234', '1111'))
    ms.login(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD)
    print(ms.remove_member('woongseok'))
