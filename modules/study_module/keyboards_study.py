import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from telebot import types

def main_study_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Registrar Estudo", callback_data="study_register")
    btn2 = types.InlineKeyboardButton("Voltar ⬅️", callback_data="previous_page")

    markup.add(btn1, btn2)

    return markup

def confirm_study_register_entry_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Sim", callback_data="confirm_study_register_yes")
    btn2 = types.InlineKeyboardButton("Não", callback_data="confirm_study_register_no")

    markup.add(btn1, btn2)

    return markup