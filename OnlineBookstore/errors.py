# 도메인 예외 정의
class BookstoreError(Exception):
    '''온라인 북스토어 도메인 공통 예외'''

class NotFoundError(BookstoreError):
    '''대상(책/주문/배송 등)을 찾을 수 없음'''

class OutOfStockError(BookstoreError):
    '''재고가 부족함'''

class InvalidInputError(BookstoreError):
    '''입력값이 유효하지 않음'''

class InvalidStateError(BookstoreError):
    '''현재 상태에서 허용되지 않는 작업 (예: 이미 취소된 주문을 다시 취소)'''

class PermissionDeniedError(BookstoreError):
    '''권한 없음'''
