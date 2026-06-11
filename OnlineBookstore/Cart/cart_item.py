class CartItem:
    def __init__(self, cart_id, member_id, book_id, quantity):
        self.__cart_id = cart_id
        self.__member_id = member_id
        self.__book_id = book_id
        self.__quantity = quantity

    def get_cart_id(self):
        return self.__cart_id
    
    def get_member_id(self):
        return self.__member_id
    
    def get_book_id(self):
        return self.__book_id
    
    def get_quantity(self):
        return self.__quantity
    
    def set_cart_id(self, cart_id):
        self.__cart_id = cart_id

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def __str__(self):
        return f'장바구니 {self.__cart_id} | 도서 {self.__book_id} | 수량 {self.__quantity}'
    
# 단위테스트
if __name__ == '__main__':
    c = CartItem('9000', 'woongseok', '1000', 2)
    print(c)   