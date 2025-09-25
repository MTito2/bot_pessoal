import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from telebot import types

def main_agenda_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Criar Evento", callback_data="create_event_agenda")
    btn2 = types.InlineKeyboardButton("Apagar Evento", callback_data="delete_event_agenda")
    btn3 = types.InlineKeyboardButton("Visualizar Eventos", callback_data="show_event_agenda")
    btn4 = types.InlineKeyboardButton("Voltar ⬅️", callback_data="previous_page")

    markup.add(btn1, btn2, btn3, btn4)

    return markup

def confirm_entry_event_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Sim", callback_data="confirm_entry_event_yes")
    btn2 = types.InlineKeyboardButton("Não", callback_data="confirm_entry_event_no")

    markup.add(btn1, btn2)

    return markup
