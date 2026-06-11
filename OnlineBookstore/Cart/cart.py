from Cart.cart_item import CartItem

Cart = CartItem

# 단위테스트
if __name__ == '__main__':
    c = Cart('9000', 'woongseok', '1000', 2)
    print(c)
