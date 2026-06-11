from datetime import datetime
from Delivery.delivery_dao import DeliveryDAO
from Delivery.delivery import Delivery, DeliveryStatus
from errors import NotFoundError

# 배송 관리 서비스 로직
class DeliveryService:
    delivery_id_seq = 5000 # 배송번호 시퀀스

    def __init__(self, delivery_dao: DeliveryDAO):
        self.__dao = delivery_dao

    def create_delivery(self, order_id, member_id, address):
        delivery_id = str(DeliveryService.delivery_id_seq)
        DeliveryService.delivery_id_seq += 1
        delivery = Delivery(delivery_id, order_id, member_id, address, DeliveryStatus.PREPARING)
        self.__dao.insert_delivery(delivery)
        return delivery

    def get_delivery(self, delivery_id):
        return self.__dao.select_delivery_by_id(delivery_id)

    def get_delivery_by_order(self, order_id):
        return self.__dao.select_by_order(order_id)

    def get_delivery_by_member(self, member_id):
        return self.__dao.select_by_member(member_id)

    def list_deliveries(self):
        return self.__dao.select_all_deliveries()

    def update_status(self, delivery_id, status):
        delivery = self.__dao.select_delivery_by_id(delivery_id) # 배송 id 로 배송 정보를 가져옴
        if not delivery: # 배송 정보가 없을 때
            raise NotFoundError('없는 배송입니다.')
        delivery.set_status(status) # 배송 상태 변경
        if status == DeliveryStatus.DELIVERED: # 배송 상태가 배송 완료로 변경되었을 때
            delivery.set_delivery_date(datetime.now()) # 배송 완료 날짜를 현재 날짜로 설정
        self.__dao.update_delivery(delivery_id, delivery) # 변경된 배송 정보를 DAO에 없데이트

# 단위테스트
if __name__ == '__main__':
    ds = DeliveryService(DeliveryDAO())
    d = ds.create_delivery('1', 'woongseok', '성남시')
    print(d)
    ds.update_status(d.get_delivery_id(), DeliveryStatus.DELIVERED)
    print(ds.get_delivery(d.get_delivery_id()))