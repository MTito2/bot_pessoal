import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.agenda_module.ia_agenda import receive_event
from modules.agenda_module.functions_agenda import create_event, delete_event, format_response_ia, events
from modules.agenda_module.keyboards_agenda import main_agenda_menu, confirm_entry_event_menu
from general_functions import save_txt, read_txt
from config import FILES_AGENDA_MODULE_PATH

user_states_waiting_event = {}
user_states_id_event = {}

WAITING_COUPON_EVENT = "waiting_coupon_event"
WAITING_ID_EVENT = "waiting_id_event"

@bot.callback_query_handler(func=lambda call: call.data == "agenda_menu")
def handle_diet_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_agenda_menu())

@bot.callback_query_handler(func=lambda call: call.data == "create_event_agenda")
def receive_click_create_event(call):
    user_states_waiting_event[call.from_user.id] = WAITING_COUPON_EVENT
    bot.send_message(call.message.chat.id, "Por favor, envie as informaçoes do evento:")

@bot.message_handler(func=lambda m: user_states_waiting_event.get(m.from_user.id) == WAITING_COUPON_EVENT)
def show_event_input(message):  
    user_id = message.from_user.id
    user_states_waiting_event.pop(user_id)

    input = message.text
    bot.reply_to(message, "Vou analisar os dados, só um minuto...")         
    bot.send_chat_action(message.chat.id, "typing")

    response = receive_event(input)
    save_txt(response, FILES_AGENDA_MODULE_PATH, "response_ia.txt")

    response_formated = format_response_ia(response)
    bot.send_message(message.chat.id, response_formated)

    bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_entry_event_menu())
    
@bot.callback_query_handler(func=lambda call: call.data == "confirm_entry_event_yes")
def save_event(call):
    event = read_txt(FILES_AGENDA_MODULE_PATH, "response_ia.txt")
    try:
        create_event(event)
        bot.send_message(call.message.chat.id, "Evento criado com sucesso ✅")

    except:
        bot.send_message(call.message.chat.id, "Erro ao criar evento ❌")


@bot.callback_query_handler(func=lambda call: call.data == "confirm_entry_event_no")
def show_menu_again(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_agenda_menu())

    
@bot.callback_query_handler(func=lambda call: call.data == "delete_event_agenda")
def receive_click_delete_event(call):
    user_states_id_event[call.from_user.id] = WAITING_ID_EVENT
    bot.send_message(call.message.chat.id, "Por favor, envie o id que será apagado:")

@bot.message_handler(func=lambda m: user_states_id_event.get(m.from_user.id) == WAITING_ID_EVENT)
def delete_event_with_id(message):  
    user_id = message.from_user.id
    user_states_id_event.pop(user_id)

    input = message.text

    try:
        delete_event(input)
        bot.send_message(message.chat.id, f"Evento com ID {input} foi apagado com sucesso ✅")

    except:
        bot.send_message(message.chat.id, f"Erro ao apagar evento id {input} ❌")

@bot.callback_query_handler(func=lambda call: call.data == "show_event_agenda")
def show_events(call):
    bot.send_message(call.message.chat.id, events())
    

    