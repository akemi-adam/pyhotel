from abc import ABC, abstractmethod
from re import match
from pprint import pprint
from datetime import datetime

from models import get_connection
from utils import translate_column_name


class Request(ABC):
    def validate(self, data: dict, mode: str) -> list:
        validation = self.create_validation() if mode == 'create' else self.update_validation()
        errors = []
        for field, rules in validation.items():
            for rule in rules:
                if rule.startswith('exists_in:'):
                    if (value := data.get(field)) and not self.exists_in(rule.split(':')[1], value):
                        errors.append(self.get_errors_message(field)['exists_in'])
                else:
                    validated = getattr(self, rule)
                    if mode == 'update':
                        if (value := data.get(field)) and not validated(value):
                            errors.append(self.get_errors_message(field)[rule])
                    else:
                        if not validated(data.get(field)):
                            errors.append(self.get_errors_message(field)[rule])
        return errors

    
    @abstractmethod
    def create_validation(self) -> dict:
        pass

    
    @abstractmethod
    def update_validation(self) -> dict:
        pass


    @staticmethod
    def cast_data_type(type: str, data):
        match type.lower():
            case 'int':
                return int(data)
            case 'float':
                return float(data)
            case 'date' | 'str':
                return data
            case 'bool':
                return data.lower() in ['sim', 'yes']


    def get_errors_message(self, field: str) -> dict:
        pprint(field)
        field = translate_column_name(field)
        return {
            'is_phone': f'O campo {field} não é um número de telefone válido',
            'is_integer': f'O campo {field} não é um número inteiro',
            'is_str': f'O campo {field} não é um texto',
            'is_data': f'O campo {field} não é uma data válida',
            'is_float': f'O campo {field} não é um número decimal',
            'is_positive': f'O campo {field} não é um número positivo',
            'is_required': f'O campo {field} é obrigatório',
            'is_email': f'O campo {field} não é um e-mail válido',
            'is_date': f'O campo {field} não é uma data válida',
            'exists_in': f'O identificador para {field} não foi encontrado na base de dados'
        }


    def is_phone(self, value) -> bool:
        return isinstance(value, str) and len(value) == 9 and value.isdigit()

    
    def is_integer(self, value) -> bool:
        return isinstance(value, int)

    
    def is_str(self, value) -> bool:
        return isinstance(value, str)

    
    def is_date(self, value) -> bool:
        if not isinstance(value, str) or len(value) != 10:
            return False
        try:
            datetime.strptime(value, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    
    def is_float(self, value) -> bool:
        return isinstance(value, float)

    
    def is_positive(self, value) -> bool:
        return isinstance(value, (int, float)) and value > 0

    
    def is_required(self, value) -> bool:
        return value is not None and value != ''
    
    
    def is_email(self, value) -> bool:
        return match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', value)
    

    def exists_in(self, table: str, value: int) -> bool:
        tables = get_connection()
        if table not in tables:
            return False
        table_data = tables[table]
        return 0 <= value < len(table_data) and not table_data[value].get('deleted', False)


class ClientRequest(Request):
    def create_validation(self) -> dict:
        return {
            'name': ['is_required', 'is_str'],
            'email': ['is_required', 'is_email', 'is_str'],
            'phone': ['is_required', 'is_phone'],
        }
    
    def update_validation(self) -> dict:
        return {
            'name': ['is_str'],
            'email': ['is_email', 'is_str'],
            'phone': ['is_phone']
        }


class RoomRequest(Request):
    def create_validation(self) -> dict:
        return {
            'number': ['is_required', 'is_integer', 'is_positive'],
            'maximum_capacity': ['is_required', 'is_integer', 'is_positive'],
            'diary_price': ['is_required', 'is_float', 'is_positive'],
        }
    
    def update_validation(self) -> dict:
        return {
            'number': ['is_integer', 'is_positive'],
            'maximum_capacity': ['is_integer', 'is_positive'],
            'diary_price': ['is_float', 'is_positive'],
        }


class ReservationRequest(Request):
    def create_validation(self) -> dict:
        return {
            'client_id': ['is_required', 'exists_in:clients', 'is_integer'],
            'room_id': ['is_required', 'exists_in:rooms', 'is_integer'],
            'check_in_date': ['is_required', 'is_date'],
            'check_out_date': ['is_required', 'is_date'],
        }
    

    def update_validation(self) -> dict:
        return {
            'client_id': ['exists_in:clients', 'is_integer'],
            'room_id': ['exists_in:rooms', 'is_integer'],
            'check_in_date': ['is_date'],
            'check_out_date': ['is_date'],
        }