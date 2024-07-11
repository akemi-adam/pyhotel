from abc import ABC
from typing import Type

from models import Model, Reservation, Room
from exceptions import ReserveRoomAlreadyReservedException


class Controller(ABC):
    def __init__(self, model_class: Type[Model]) -> None:
        self.model_class = model_class


    def create(self, data: dict):
        return self.model_class.save(data)


    def find_all(self):
        return self.model_class.find_all()


    def find(self, id: int):
        return self.model_class.find(id)


    def update(self, data: dict, model: Model):
        return model.update(data)


    def delete(self, model: Model):
        return model.delete()


class ClientController(Controller):
    pass


class RoomController(Controller):
    pass


class ReservationController(Controller):
    def create(self, data: dict):
        room: Room = Room.find(data['room_id'])
        if room.is_reservated():
           raise ReserveRoomAlreadyReservedException(room.number)
        reservation: Reservation = Reservation.save(data)
        return reservation
    

    def update(self, data: dict, reservation: Reservation):
        if (room_id := data.get('room_id')) and room_id != reservation.room_id:
            room: Room = Room.find(room_id)
            if room.is_reservated():
                raise ReserveRoomAlreadyReservedException(room_id)
        return reservation.update(data)
            
            
            
            