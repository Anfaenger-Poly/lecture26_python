from enum import StrEnum

class CodeStatus(StrEnum):
    AVAILABLE = '판매가능'
    SOLD      = '판매완료'

class GameCode:
    def __init__(self, serial: str, status: CodeStatus = CodeStatus.AVAILABLE):
        self.__serial = serial
        self.__status = status

    def get_serial(self) -> str:
        return self.__serial

    def get_status(self) -> CodeStatus:
        return self.__status

    def set_status(self, status: CodeStatus) -> None:
        self.__status = status

    def __str__(self) -> str:
        return f'{self.__serial} ({self.__status})'

class Product:
    def __init__(self, product_id: str | None, name: str, platform: str,
                 price: int, codes: list[GameCode] | None = None):
        self.__product_id = product_id
        self.__name       = name
        self.__platform   = platform
        self.__price      = price
        # 코드 목록은 외부에서 주입하거나 빈 리스트로 시작
        self.__codes: list[GameCode] = codes if codes is not None else []

    def get_product_id(self) -> str | None:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_platform(self) -> str:
        return self.__platform

    def get_price(self) -> int:
        return self.__price

    def get_codes(self) -> list[GameCode]:
        return self.__codes

    def set_product_id(self, product_id: str) -> None:
        self.__product_id = product_id

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_platform(self, platform: str) -> None:
        self.__platform = platform

    def set_price(self, price: int) -> None:
        self.__price = price

    def available_count(self) -> int:
        '''판매 가능한 코드 수 (재고)'''
        return sum(1 for c in self.__codes if c.get_status() == CodeStatus.AVAILABLE)

    def pop_available_code(self) -> GameCode | None:
        for code in self.__codes:
            if code.get_status() == CodeStatus.AVAILABLE:
                code.set_status(CodeStatus.SOLD)
                return code
        return None

    def stock_label(self) -> str:
        cnt = self.available_count()
        return '품절' if cnt == 0 else f'잔여 {cnt}개'

    def __str__(self) -> str:
        return (f'[{self.__product_id}] {self.__name} / {self.__platform} / '
                f'{self.__price:,}원 / {self.stock_label()}')

# 단위테스트
if __name__ == '__main__':
    p = Product('P001', '사이버펑크 2077', 'Steam', 39000,
                [GameCode('CYBER-AAAA-1111'), GameCode('CYBER-BBBB-2222')])
    print(p)
    code = p.pop_available_code()
    print(f'발급된 코드: {code}')
    print(p)
