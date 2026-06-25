#======================
# 데이터 모델 정의 : Member
class Member:
    def __init__(self, id: str, password: str, name: str, email: str, phone: str):
        self.__id = id
        self.__password = password
        self.__name = name
        self.__email = email
        self.__phone = phone

    def get_id(self) -> str:
        return self.__id

    def get_password(self) -> str:
        return self.__password

    def get_name(self) -> str:
        return self.__name

    def get_email(self) -> str:
        return self.__email

    def get_phone(self) -> str:
        return self.__phone

    def set_password(self, password: str) -> None:
        self.__password = password

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_email(self, email: str) -> None:
        self.__email = email

    def set_phone(self, phone: str) -> None:
        self.__phone = phone

    def __str__(self) -> str:
        return f'{self.__id}\t{self.__name}\t{self.__email}\t{self.__phone}'

# 단위테스트
if __name__ == '__main__':
    m = Member('woongseok', '1234', '최웅석', 'cws@test.com', '010-0000-0000')
    print(m)
