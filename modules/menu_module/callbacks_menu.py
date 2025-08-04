import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.menu_module.keyboards_menu import main_menu_page_1, main_menu_page_2

@bot.callback_query_handler(func= lambda call:True)
def callback_query(call):
    if call.data == "next_page":
        bot.send_message(call.message.chat.id, "Escolha uma opção:",  reply_markup=main_menu_page_2())

    elif call.data == "previous_page":
        bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_menu_page_1())