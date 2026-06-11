from Book.book import Book

# 도서 관리 DAO
class BookDAO:
    def __init__(self):
        self.__bookDB = {}

    def insert_book(self, book):
        book_id = book.get_book_id()
        if book_id in self.__bookDB:
            return False
        self.__bookDB[book_id] = book
        return True

    def select_book_by_id(self, book_id):
        return self.__bookDB.get(book_id)

    def select_all_books(self):
        return list(self.__bookDB.values())

    def update_book(self, book_id, book):
        if book_id in self.__bookDB:
            self.__bookDB[book_id] = book
            return True
        return False

    def delete_book(self, book_id):
        if book_id in self.__bookDB:
            self.__bookDB.pop(book_id)
            return True
        return False

# 단위테스트
if __name__ == '__main__':
    dao = BookDAO()
    dao.insert_book(Book('1000', '파이썬', '박응용', 22000, 5))
    print(dao.select_book_by_id('1000'))
    print(dao.select_all_books())
    print(dao.delete_book('1000'))
