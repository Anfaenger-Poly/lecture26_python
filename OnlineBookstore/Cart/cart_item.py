class CartItem:
    def __init__(self, book_id, quantity):
        self.__book_id = book_id
        self.__quantity = quantity

    def get_book_id(self):
        return self.__book_id

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def __str__(self):
        return f'도서 {self.__book_id} | 수량 {self.__quantity}'
    
# 단위테스트
if __name__ == '__main__':
    c = CartItem('9000', 'woongseok', '1000', 2)
    print(c)   