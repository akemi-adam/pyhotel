from os import path
from sys import modules
from typing import Type

from pickle import dump, load
from tabulate import tabulate

from utils import translate_column_name, date_is_in_range, cast_date, remove_last_char
from exceptions import ModelNotFoundedException

class Model:
    table_name = ''
    columns = []
    uniques = {}
    invisible_columns = ['deleted']
    validations = {}
    foreign_keys = []
    relationships = {}


    @classmethod
    def cast_dict_to_model(cls, id: int, row: dict):
        model = cls()
        model.__setattr__('id', id)
        for column, value in row.items():
            model.__setattr__(column, value)
        return model
    

    def cast_model_to_dict(self):
        model_dict: dict = {'deleted': False}
        for column in self.columns:
            model_dict[column[0]] = getattr(self, column[0])
        return model_dict


    @classmethod
    def save(cls, model: dict):
        database = get_connection()
        model['deleted'] = False
        database[cls.table_name].append(model)
        save_tables(get_database_path(), database)
        return cls.cast_dict_to_model(len(database[cls.table_name]) - 1, model)


    @classmethod
    def find_all(cls):
        database = get_connection()
        models: list = []
        for id, row in enumerate(database[cls.table_name]):
            models.append(cls.cast_dict_to_model(id, row))
        return models

    # 11 e 4
    @classmethod
    def find(cls, id: int):
        database = get_connection()
        for index, row in enumerate(database[cls.table_name]):
            if index == id and not row['deleted']:
                return cls.cast_dict_to_model(id, row)
        raise ModelNotFoundedException(id)

    def update(self, data: dict):
        for column, value in data.items():
            self.__setattr__(column, value)
        database: dict = get_connection()
        database[self.table_name][self.id] = self.cast_model_to_dict()
        save_tables(get_database_path(), database)
        return self

    
    def delete(self):
        database: dict = get_connection()
        database[self.table_name][self.id]['deleted'] = True
        save_tables(get_database_path(), database)
        return True

    
    def __str__(self) -> str:
        row = [['ID'], [self.id]]
        for column in self.columns:
            row[0].append(translate_column_name(column[0]))
            row[1].append(getattr(self, column[0]))
        return tabulate(row, headers='firstrow', tablefmt='rounded_grid')



class Client(Model):
    table_name = 'clients'
    columns = [
        ("name", "str"),
        ("email", "str"),
        ("phone", "str")
    ]
    uniques = [
        "email",
    ]
    
    
    def reservations(self):
        return [reservation for reservation in Reservation.find_all() if reservation.client_id == self.id]


class Room(Model):
    table_name = 'rooms'
    columns = [
        ("number", "int"),
        ("maximum_capacity", "int"),
        ("diary_price", "float"),
    ]
    uniques = [
        "number"
    ]
    relationships = {
        "has_many": ["Reservation"]
    }
    
    
    def is_reservated(self) -> bool:
        for reservation in self.reservations():
            if date_is_in_range(reservation.check_in_date, reservation.check_out_date):
                return True
        return False
    
    
    def reservations(self):
        return [reservation for reservation in Reservation.find_all() if reservation.room_id == self.id]


class Reservation(Model):
    table_name = 'reservations'
    columns = [
        ("client_id", "int"),
        ("room_id", "int"),
        ("check_in_date", "date"),
        ("check_out_date", "date"),
    ]
    
    def client(self):
        return Client.find(self.client_id)
    
    def room(self):
        return Room.find(self.room_id)
    


def load_tables(file_name) -> dict:
  with open(file_name, 'rb') as file:
    tables = load(file)
  return tables


def save_tables(file_name, tables) -> None:
  with open(file_name, 'wb') as file:
    dump(tables, file)


def get_database_path() -> str:
    return './database.dat'


def get_connection() -> dict:
    database_struct: dict = { "clients": [], "rooms": [], "reservations": [] }
    database_path = get_database_path()
    return load_tables(database_path) if path.isfile(database_path) else database_struct