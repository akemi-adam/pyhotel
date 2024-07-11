from datetime import date, datetime

def translate_column_name(column_name: str) -> str:
  match column_name:
    case 'name':
      return 'Nome'
    case 'email':
      return 'E-mail'
    case 'phone':
      return 'Telefone'
    case 'status':
      return 'Status (Ocupado/Desocupado)'
    case 'number':
      return 'Número'
    case 'maximum_capacity':
      return 'Capacidade Máxima'
    case 'diary_price':
      return 'Preço Diário'
    case 'check_in_date':
      return 'Data de Check-In'
    case 'check_out_date':
      return 'Data de Check-Out'
    case 'discount':
      return 'Desconto'
    case 'room_id':
      return 'Identificação do Quarto'
    case 'client_id':
      return 'Identificação do Cliente'
    case _:
      return ''
    

def cast_date(date_to_cast: str):
  return datetime.strptime(date_to_cast, '%d/%m/%Y').date()


def date_is_in_range(start_date, end_date, target_date = None):
  if not target_date:
    target_date = date.today()
  return cast_date(start_date) <= target_date <= cast_date(end_date)


def remove_last_char(word: str):
  return word.rstrip(word[-1])