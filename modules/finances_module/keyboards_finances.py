import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from telebot import types

def main_finances_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Analisar Cupom", callback_data="analyze_coupon")
    btn2 = types.InlineKeyboardButton("Inserir Despesas", callback_data="entry_expenses")
    btn3 = types.InlineKeyboardButton("Ver Métricas", callback_data="expenses_metrics")
    btn4 = types.InlineKeyboardButton("Voltar ⬅️", callback_data="previous_page")

    markup.add(btn1, btn2, btn3, btn4)

    return markup

def confirm_information_coupon_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Sim", callback_data="confirm_information_coupon_yes")
    btn2 = types.InlineKeyboardButton("Não", callback_data="confirm_information_coupon_no")

    markup.add(btn1, btn2)

    return markup

def confirm_manual_expense_entry_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Sim", callback_data="confirm_entry_expenses_yes")
    btn2 = types.InlineKeyboardButton("Não", callback_data="confirm_entry_expenses_no")

    markup.add(btn1, btn2)

    return markup