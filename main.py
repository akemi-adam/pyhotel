from platform import system as get_os
from os import system

from models import Client, Room, Reservation, Model
from controllers import ClientController, RoomController, ReservationController, ReportController
from validations import ClientRequest, RoomRequest, ReservationRequest, Request
from interfaces import CliInterface


if __name__ == '__main__':
    interface_mode = ''
    while interface_mode.lower() not in ['cli', 'gui']:
        interface_mode = input('Escolha a interface desejada (CLI/GUI): ')
    if interface_mode == 'cli':
        loop: bool = True
        while loop:
            system('cls' if get_os() == 'Windows' else 'clear')
            print('''
            ###############################
            ###         PyHotel         ###
            ###############################

            1 - Módulo de Clientes
            2 - Módulo de Quartos
            3 - Módulo de Reservas
            4 - Módulo de Relatório
            5 - Módulo de Informações
            6 - Sair

            ###############################

            ''')

            option = int(input('Digite a opção desejada: '))

            match option:
                case 1:
                    menu: CliInterface = CliInterface('clientes', Client, ClientController(Client), ClientRequest())
                    menu.show_crud_options()
                    menu.choose_crud_options()
                case 2:
                    menu: CliInterface = CliInterface('quartos', Room, RoomController(Room), RoomRequest())
                    menu.show_crud_options()
                    menu.choose_crud_options()
                case 3:
                    menu: CliInterface = CliInterface('reservas', Reservation, ReservationController(Reservation), ReservationRequest())
                    menu.show_crud_options()
                    menu.choose_crud_options()
                case 4:
                    menu: CliInterface = CliInterface('reservas', Model, ReportController(), Request)
                    menu.show_reports_options()
                    menu.choose_report_options()
                case 5:
                    pass
                case 6:
                    loop = False
                case _:
                    pass
    else:
        pass