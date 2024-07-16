from pprint import pprint
from typing import Type, List

from tabulate import tabulate

from models import Model, Room
from controllers import Controller
from validations import Request
from utils import translate_column_name, number_format



class CliInterface:
    def __init__(self, module: str, model: Type[Model], controller: Controller, request: Request):
        self.module = module
        self.model = model
        self.controller = controller
        self.request = request

    def show_message(self, message: str, wait_for_next_action: bool = False) -> None:
        print(message)
        if wait_for_next_action:
            input("Aperte <Enter> para prosseguir")

    
    def show_table(self, table, wait_for_next_action = True) -> None:
        self.show_message(tabulate(table, headers='firstrow', tablefmt='rounded_grid'), wait_for_next_action)


    def read_line(self, message: str) -> str:
        return input(message)
    

    def show_crud_options(self) -> None:
        print(f'''
        ###########################
                {self.module.capitalize()}
        ###########################
                
        1 - Cadastrar {self.module}
        2 - Consultar {self.module}s
        3 - Editar {self.module}
        4 - Deletar {self.module}
        ''')
        
        
    def show_reports_options(self) -> None:
        print(f'''
        ###########################
                Relatórios
        ###########################
                
        1 - Relatório de receitas
        2 - Relatório de quartos ocupados
        3 - Relatório de quartos desocupados
        ''')

    
    def choose_crud_options(self) -> None:
        match int(self.read_line('Escolha a operação: ')):
            case 1:
                self.create_option()
            case 2:
                self.find_all_option()
            case 3:
                self.update_option()
            case 4:
                self.delete_option()
            case _:
                self.show_message('Opção inválida!', True)
                
    
    def choose_report_options(self) -> None:
        match int(self.read_line('Escolha a operação: ')):
            case 1:
                self.balance_option()
            case 2:
                self.rooms_currently_reserved_option()
            case 3:
                self.rooms_currently_free_option()
            case _:
                self.show_message('Opção inválida!', True)

    
    def validate_input(self, data: dict, mode: str = 'create'):
        for column in self.model.columns:
            answer = input(f'{translate_column_name(column[0])}: ')
            if mode == 'create' or not (answer is None or answer == ''):
                data[column[0]] = Request.cast_data_type(column[1], answer)
        errors: list = self.request.validate(data, mode)
        if errors:
            self.show_message(f'Algo deu errado! Os seguintes erros foram encontrados:')
            for index, error in enumerate(errors, 1):
                self.show_message(f'{index}. {error}')
            self.show_message('Por favor, realize insira os dados novamente')
            return False
        return True


    def create_option(self):
        data: dict = {}
        if self.validate_input(data):
            try:
                model = self.controller.create(data)
                self.show_message(f'\n{model}\n\n{self.module} cadastrado com sucesso!', True)
            except Exception as e:
                self.show_message(f'Um erro ocorreu: {e}', True)
        else:
            return self.create_option()
        

    def find_all_option(self):
        self.show_message(f'# Lista de {self.module}s\n')
        models: list = self.controller.find_all()
        data = [['ID']]
        for column in self.model.columns:
            data[0].append(translate_column_name(column[0]))
        for index, model in enumerate(models):
            if not model.deleted:
                row = [str(index)]
                for column in model.columns:
                    if column[0] not in self.model.invisible_columns:
                        row.append(getattr(model, column[0]))
                data.append(row)
        self.show_table(data)


    def update_option(self):
        try:
            data: dict = {}
            model: Model = self.controller.find(int(self.read_line(f'Informe o Identificador (ID) do registro que deseja atualizar: ')))
            self.show_message(f'Registro encontrado: \n{model}\n\n', True)
            if self.validate_input(data, 'update'):
                model = self.controller.update(data, model)
                self.show_message(f'\n{model}\n\n{self.module} atualizado com sucesso!', True)
            else:
                return self.update_option()
        except Exception as e:
            self.show_message(f'Um erro ocorreu: {e}', True)


    def delete_option(self):
        try:
            model: Model = self.controller.find(int(self.read_line(f'Informe o Identificador (ID) do registro que deseja deletar: ')))
            self.show_message(f'Registro encontrado: \n{model}\n\n')
            self.controller.delete(model)
            self.show_message(f'{self.module} deletado com sucesso!', True)
        except Exception as e:
            self.show_message(f'Um erro ocorreu: {e}', True)
        
        
    def balance_option(self):
        self.show_message('Receitas geradas pelas reservas')
        table: list = [['ID', 'Receita']]
        data: dict = self.controller.get_total_balance()
        for reservation in data['reservations']:
            table.append([reservation.id, f'R$ {number_format(reservation.get_balance())}'])
        self.show_table(table, False)
        self.show_message(f'Receita total: R$ {number_format(data['total_balance'])}', True)
    
    
    def _show_rooms(self, message: str, rooms: List[Room]):
        self.show_message(message)
        table: list = [[translate_column_name(column[0]) for column in Room.columns]]
        table[0].insert(0, 'ID')
        rooms: List[Room] = rooms
        for id, room in enumerate(rooms):
            row: list = [id]
            for column in room.columns:
                row.append(getattr(room, column[0]))
            table.append(row)
        self.show_table(table)
    
    
    def rooms_currently_reserved_option(self):
        self._show_rooms('Quartos reservados no momento', self.controller.get_rooms_currently_reserved())
    
    
    def rooms_currently_free_option(self):
        self._show_rooms('Quartos livres no momento', self.controller.get_rooms_currently_free())
        

class GuiInterface:
    pass