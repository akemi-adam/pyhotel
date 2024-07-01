from os import path

from pickle import dump, load


class Model:
    columns = {}
    invisible_columns = ["deleted"]
    validations = {}
    foreign_keys = []
    relationships = {}
    
    def __init__(self):
        self.table_name = self.__class__.__name__.lower() + "s"
        database_struct: dict = { "clients": [], "rooms": [], "reservations": [] }
        self.database_path = get_database_path()
        self.database = load_tables(self.database_path) if path.isfile(self.database_path) else database_struct
    
    def save(self, model: dict):
        self.database[self.table_name].append(model)
        save_tables(self.database_path, self.database)


    def update(self, id: int, model: dict):
        self.database[self.table_name][id] = model
        save_tables(self.database_path, self.database)
    

    def get(self):
        return self.database[self.table_name]

    
    def find(self, id: int):
        for index, model in enumerate(self.database[self.table_name]):
            if index == id and not model['deleted']:
                return model
        return {}
        

    def delete(self, id: int):
        self.database[self.table_name][id]['deleted'] = True
        save_tables(self.database_path, self.database)


class Client:
    columns = [
        ("name", "str"),
        ("email", "str"),
        ("phone", "str")
    ]


class Room:
    columns = [
        ("number", "int"),
        ("maximum_capacity", "int"),
        ("diary_price", "float"),
        ("status", "str")
    ]


class Reservation:
    columns = [
        ("client_id", "int"),
        ("room_id", "int"),
        ("check_in_date", "int"),
        ("check_out_date", "date"),
        ("discount", "float")
    ]


def load_tables(file_name) -> dict:
  with open(file_name, 'rb') as file:
    tables = load(file)
  return tables


def save_tables(file_name, tables) -> None:
  with open(file_name, 'wb') as file:
    dump(tables, file)


def get_database_path() -> str:
  return './database.dat'