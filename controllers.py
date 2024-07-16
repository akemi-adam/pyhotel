from abc import ABC
from typing import Type, List
from pprint import pprint

from models import Model, Reservation, Room
from exceptions import ReserveRoomAlreadyReservedException
from utils import count_days_from_interval


class Controller(ABC):
    pass


class CrudController(Controller, ABC):
    def __init__(self, model_class: Type[Model]) -> None:
        self.model_class = model_class


    def create(self, data: dict) -> Model:
        return self.model_class.save(data)


    def find_all(self) -> list:
        return self.model_class.find_all()


    def find(self, id: int) -> Model:
        return self.model_class.find(id)


    def update(self, data: dict, model: Model) -> Model:
        return model.update(data)


    def delete(self, model: Model) -> bool:
        return model.delete()


class ClientController(CrudController):
    pass


class RoomController(CrudController):
    pass


class ReservationController(CrudController):
    def create(self, data: dict) -> Model:
        room: Room = Room.find(data['room_id'])
        if room.is_reservated():
           raise ReserveRoomAlreadyReservedException(room.number)
        reservation: Reservation = Reservation.save(data)
        return reservation
    

    def update(self, data: dict, reservation: Reservation) -> Model:
        if (room_id := data.get('room_id')) and room_id != reservation.room_id:
            room: Room = Room.find(room_id)
            if room.is_reservated():
                raise ReserveRoomAlreadyReservedException(room_id)
        return reservation.update(data)
    
    
class ReportController(Controller):
    def get_total_balance(self) -> dict:
        total_balance: float = 0
        reservations: List[Reservation] = Reservation.get_paids()
        for reservation in reservations:
            total_balance += reservation.get_balance()
        return {'total_balance': total_balance, 'reservations': reservations}            
    
    
    def get_rooms_currently_reserved(self) -> List[Room]:
        return [room for room in Room.find_all() if room.is_reservated()]
    
    
    def get_rooms_currently_free(self) -> List[Room]:
        return [room for room in Room.find_all() if not room.is_reservated()]
    
    