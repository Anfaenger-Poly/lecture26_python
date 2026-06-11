class Book:
    def __init__(self, book_id, title, author, price, stock):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__price = price
        self.__stock = stock

    def get_book_id(self):
        return self.__book_id

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def set_book_id(self, book_id):
        self.__book_id = book_id

    def set_title(self, title):
        self.__title = title

    def set_author(self, author):
        self.__author = author

    def set_price(self, price):
        self.__price = price

    def set_stock(self, stock):
        self.__stock = stock
    
    def to_list_str(self):
        return f'[{self.__book_id}] {self.__title} / {self.__author}'

    def __str__(self):
        return f'[{self.__book_id}] {self.__title} / {self.__author} / {self.__price:,}원 / 재고 {self.__stock}'

# 단위테스트
if __name__ == '__main__':
    b = Book('1000', '점프 투 파이썬', '박응용', 22000, 5)
    print(b)
