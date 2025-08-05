import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from telebot import types

def main_finances_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Analisar Cupom", callback_data="analyze_coupon")
    btn2 = types.InlineKeyboardButton("Voltar ⬅️", callback_data="previous_page")

    markup.add(btn1, btn2)

    return markup

def confirm_information_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Sim", callback_data="confirm_information_finances_yes")
    btn2 = types.InlineKeyboardButton("Não", callback_data="confirm_information_finances_no")

    markup.add(btn1, btn2)

    return markup