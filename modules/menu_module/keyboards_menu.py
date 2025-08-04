import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from telebot import types

def main_menu_page_1():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Finanças", callback_data="finances_menu")
    btn2 = types.InlineKeyboardButton("Dieta", callback_data="diet_menu")
    btn3 = types.InlineKeyboardButton("Agenda", callback_data="agenda_menu")
    btn4 = types.InlineKeyboardButton("Livros", callback_data="books_menu")
    btn5 = types.InlineKeyboardButton("Próximo ➡️", callback_data="next_page")

    markup.add(btn1, btn2, btn3, btn4, btn5)

    return markup

def main_menu_page_2():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Estudos", callback_data="study_menu")
    btn2 = types.InlineKeyboardButton("Corrida", callback_data="run_menu")
    btn3 = types.InlineKeyboardButton("Voltar ⬅️", callback_data="previous_page")

    markup.add(btn1, btn2, btn3)

    return markup