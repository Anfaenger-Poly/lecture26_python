class Member:
    def __init__(self, id, password, name, address, phone):
        self.__id = id
        self.__password = password
        self.__name = name
        self.__address = address
        self.__phone = phone

    def get_id(self):
        return self.__id

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_phone(self):
        return self.__phone

    def set_password(self, password):
        self.__password = password

    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    def set_phone(self, phone):
        self.__phone = phone

    def __str__(self):
        return f'{self.__id}\t{self.__name}\t{self.__address}\t{self.__phone}'

# 단위테스트
if __name__ == '__main__':
    m = Member('woongseok', '1234', '최웅석', '성남시', '010-1234-1234')
    print(m)
