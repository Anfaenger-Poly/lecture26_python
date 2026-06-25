class GameMallError(Exception):
    '''온라인 게임 코드 쇼핑몰 도메인 공통 예외'''

class NotFoundError(GameMallError):
    '''대상(상품/주문 등)을 찾을 수 없음'''

class InvalidInputError(GameMallError):
    '''입력값이 유효하지 않음'''

class InvalidStateError(GameMallError):
    '''현재 상태에서 허용되지 않는 작업 (예: 이미 취소된 주문을 다시 취소)'''

class PermissionDeniedError(GameMallError):
    '''권한 없음'''

class OutOfStockError(GameMallError):
    '''판매 가능한 코드가 없음 (품절)'''
