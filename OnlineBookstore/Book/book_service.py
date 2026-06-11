from Book.book_dao import BookDAO
from Book.book import Book
from errors import InvalidInputError

# 도서 관리 서비스
class BookService:
    book_id_seq = 1000 # 도서 ID 시퀀스

    def __init__(self, book_dao):
        self.__dao = book_dao

    def add_book(self, book):
        if not book.get_title().strip():
            raise InvalidInputError('제목은 비어 있을 수 없습니다.') # 제목이 비어 있을 때
        if book.get_price() < 0 or book.get_stock() < 0:
            raise InvalidInputError('가격과 재고는 0 이상이어야 합니다.') # 가격과 재고가 음수 일 때
        book.set_book_id(str(BookService.book_id_seq))
        BookService.book_id_seq += 1
        self.__dao.insert_book(book)
        return book

    def update_book(self, book_id, book):
        if book.get_price() < 0 or book.get_stock() < 0:
            raise InvalidInputError('가격과 재고는 0 이상이어야 합니다.') # 가격과 재고가 음수 일 때
        return self.__dao.update_book(book_id, book)

    def remove_book(self, book_id):
        return self.__dao.delete_book(book_id)

    def get_book(self, book_id):
        return self.__dao.select_book_by_id(book_id)

    def list_books(self):
        return self.__dao.select_all_books()

# 단위테스트
if __name__ == '__main__':
    bs = BookService(BookDAO())
    bs.add_book(Book(None, '파이썬', '박응용', 22000, 5))
    bs.add_book(Book(None, '자바', '남궁성', 30000, 3))
    for b in bs.list_books():
        print(b)
    try:
        bs.add_book(Book(None, '', '저자', -1, 5))
    except InvalidInputError as e:
        print('검증 통과:', e)
