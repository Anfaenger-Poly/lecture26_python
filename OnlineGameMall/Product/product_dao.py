from Product.product import Product

class ProductDAO:
    def __init__(self):
        self.__productDB: dict[str, Product] = {}

    def insert_product(self, product: Product):
        pid = product.get_product_id()
        if pid in self.__productDB:
            return False
        self.__productDB[pid] = product
        return True

    def select_product_by_id(self, product_id):
        return self.__productDB.get(product_id)

    def select_all_products(self) -> list[Product]:
        # 컬렉션 조회는 없을 때 None 이 아니라 빈 리스트를 반환한다.
        return list(self.__productDB.values())

    def update_product(self, product_id, product: Product):
        if product_id in self.__productDB:
            self.__productDB[product_id] = product
            return True
        return False

    def delete_product(self, product_id):
        if product_id in self.__productDB:
            self.__productDB.pop(product_id)
            return True
        return False

# 단위테스트
if __name__ == '__main__':
    from Product.product import GameCode
    dao = ProductDAO()
    p = Product('P001', '사이버펑크 2077', 'Steam', 39000,
                [GameCode('CYBER-AAAA-1111')])
    dao.insert_product(p)
    print(dao.select_product_by_id('P001'))
    print(dao.select_all_products())
    print(dao.delete_product('P001'))
