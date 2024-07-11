class ReserveRoomAlreadyReservedException(Exception):
    def __init__(self, room_number: int):
        self.message = f'O quarto número {room_number} está reservado no momento!'
        super().__init__(self.message)

    
    def __str__(self):
        return self.message
    

class ModelNotFoundedException(Exception):
    def __init__(self, id: int):
        self.message = f'Nenhum registro com o ID {id} foi encontrado'
        super().__init__(self.message)

    
    def __str__(self) -> str:
        return self.message