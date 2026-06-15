class Cart:
    def __init__(self, cart_id, member_id):
        self.__cart_id = cart_id
        self.__member_id = member_id
        self.__cart_items = []

    def add_item(self, cart_item):
        self.__cart_items.append(cart_item)

    def get_cart_id(self):
        return self.__cart_id

    def get_member_id(self):
        return self.__member_id

    def get_cart_items(self):
        return self.__cart_items

    def __str__(self):
        result = f'장바구니 {self.__cart_id}\n'
        for item in self.__cart_items:
            result += str(item) + '\n'
        return result
    
# 단위테스트
if __name__ == '__main__':
    c = Cart('9000', 'woongseok')
    print(c)