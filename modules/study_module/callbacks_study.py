import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.study_module.keyboards_study import main_study_menu, confirm_study_register_entry_menu
from modules.study_module.ia_study import analyze_study_register_entry, convert_analyze_to_json
from modules.study_module.functions_study import save_txt, read_txt


WAITING_STUDY_REGISTER_ENTRY = "waiting_study_register_entry"
user_states_waiting_study_register_entry = {}

@bot.callback_query_handler(func=lambda call: call.data == "study_menu")
def show_study_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_study_menu())

@bot.callback_query_handler(func=lambda call: call.data == "study_register")
def receive_click_to_study_register(call):
    user_states_waiting_study_register_entry[call.from_user.id] = WAITING_STUDY_REGISTER_ENTRY
    bot.send_message(call.message.chat.id, "Por favor, envie o registro de estudo: ")

@bot.message_handler(func=lambda m: user_states_waiting_study_register_entry.get(m.from_user.id) == WAITING_STUDY_REGISTER_ENTRY)
def register_study(message):
    user_id = message.from_user.id
    user_states_waiting_study_register_entry.pop(user_id)
    input = message.text

    bot.reply_to(message, "Analisando dados, só um instante...")
    response_ia = analyze_study_register_entry(input)

    bot.reply_to(message, response_ia)
    bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_study_register_entry_menu())

@bot.callback_query_handler(func=lambda call: call.data == "confirm_study_register_yes")
def save_study_register(call):
    bot.send_message(call.message.chat.id, "Salvando dados...")
    convert_analyze_to_json()
    bot.send_message(call.message.chat.id, "Dados salvos com sucesso ✅")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_study_register_no")
def show_again_study_menu(call):
    bot.send_message(call.message.chat.id, "Os dados estão corretos?", reply_markup=main_study_menu())
