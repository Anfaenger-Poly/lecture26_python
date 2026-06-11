from Member.member import Member

# 회원 데이터 관리 DAO
class MemberDAO:
    def __init__(self):
        self.__memberDB = {}

    def insert_member(self, member):
        if member.get_id() in self.__memberDB:
            return False
        self.__memberDB[member.get_id()] = member
        return True

    def select_member_by_id(self, id):
        return self.__memberDB.get(id)

    def select_all_members(self): # 전체 회원 조회 후 리스트로 반환
        return list(self.__memberDB.values())

    def update_member(self, id, member):
        if id in self.__memberDB:
            self.__memberDB[id] = member
            return True
        return False

    def delete_member(self, id):
        if id in self.__memberDB:
            self.__memberDB.pop(id)
            return True
        return False

# 단위테스트
if __name__ == '__main__':
    dao = MemberDAO()
    dao.insert_member(Member('woongseok', '1234', '최웅석', '수원', '010'))
    print(dao.select_member_by_id('woongseok'))
    print(dao.insert_member(Member('woongseok', '1', 'dup', 'b', 'c')))
    print(dao.select_all_members())
    print(dao.delete_member('woongseok'))
