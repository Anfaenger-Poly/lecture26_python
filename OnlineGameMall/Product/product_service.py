from Product.product_dao import ProductDAO
from Product.product import Product, GameCode
from errors import InvalidInputError, NotFoundError

class ProductService:
    product_id_seq = 1000  # 상품 ID 시퀀스

    def __init__(self, product_dao: ProductDAO):
        self.__dao = product_dao

    def add_product(self, product: Product) -> Product:
        if not product.get_name().strip():
            raise InvalidInputError('상품명은 비어 있을 수 없습니다.')
        if not product.get_platform().strip():
            raise InvalidInputError('플랫폼은 비어 있을 수 없습니다.')
        if product.get_price() < 0:
            raise InvalidInputError('가격은 0 이상이어야 합니다.')
        product.set_product_id(str(ProductService.product_id_seq))
        ProductService.product_id_seq += 1
        self.__dao.insert_product(product)
        return product

    def update_product(self, product_id: str, product: Product) -> bool:
        if product.get_price() < 0:
            raise InvalidInputError('가격은 0 이상이어야 합니다.')
        return self.__dao.update_product(product_id, product)

    def remove_product(self, product_id: str) -> bool:
        return self.__dao.delete_product(product_id)

    def get_product(self, product_id: str) -> Product | None:
        return self.__dao.select_product_by_id(product_id)

    def list_products(self) -> list[Product]:
        return self.__dao.select_all_products()

    def add_codes(self, product_id: str, serials: list[str]) -> int:
        '''기존 상품에 코드를 추가한다. 추가된 개수를 반환.'''
        product = self.__dao.select_product_by_id(product_id)
        if not product:
            raise NotFoundError('없는 상품입니다.')
        for s in serials:
            s = s.strip()
            if s:
                product.get_codes().append(GameCode(s))
        return len(serials)

# 단위테스트
if __name__ == '__main__':
    ps = ProductService(ProductDAO())
    p = ps.add_product(Product(None, '사이버펑크 2077', 'Steam', 39000))
    print(p)
    ps.add_codes(p.get_product_id(), ['CYBER-AAAA-1111', 'CYBER-BBBB-2222'])
    print(ps.get_product(p.get_product_id()))
