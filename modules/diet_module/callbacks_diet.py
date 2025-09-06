import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.diet_module.ia_diet import receive_message
from modules.diet_module.keyboards_diet import main_diet_menu

@bot.callback_query_handler(func=lambda call: call.data == "diet_menu")
def handle_diet_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_diet_menu())

@bot.callback_query_handler(func=lambda call: call.data == "suggest_diet")
def suggest_diet(call):
    bot.send_message(call.message.chat.id, "Gerando sugestão, só um instante...")
    response_ia = receive_message()
    bot.send_message(call.message.chat.id, response_ia)

