from typing import List
from datetime import date

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


def today():
  return date.today()
    

def cast_date(date_to_cast: str):
  parts: List[str] = []
  for part in date_to_cast.split('/'):
    valid_part: int = int(part if not part.startswith('0') else part.replace('0', ''))
    parts.append(valid_part)
  return date(parts[2], parts[1], parts[0])


def date_is_in_range(start_date, end_date, target_date = None):
  if not target_date:
    target_date = today()
  return cast_date(start_date) <= target_date <= cast_date(end_date)


def remove_last_char(word: str):
  return word.rstrip(word[-1])


def count_days_from_interval(start_date: str, end_date: str):
  return (cast_date(end_date) - cast_date(start_date)).days


def number_format(number: int|float) -> str:
  integer_part, decimal_part = f'{number:,.2f}'.split('.')
  integer_part = integer_part.replace(',', '.')
  return f'{integer_part},{decimal_part}'