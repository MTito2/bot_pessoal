import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.study_module.keyboards_study import main_study_menu, confirm_study_register_entry_menu
from modules.study_module.ia_study import analyze_study_register_entry, convert_analyze_to_json
from modules.study_module.functions_study import save_txt, read_txt, check_period_d_m_y, check_period_m_y
from modules.study_module.metrics_config import study_full_report
from modules.study_module.graphics_config import generate_chart_bars, generate_chart_bubble, IMG_BARS_PATH, IMG_BUBBLE_PATH


WAITING_STUDY_REGISTER_ENTRY = "waiting_study_register_entry"
WAITING_STUDY_METRICS_ENTRY = "waiting_study_metrics_entry"
WAITING_STUDY_GRAPHICS_ENTRY = "waiting_study_graphics_entry"

user_states_waiting_study_register_entry = {}
user_states_waiting_study_metrics_entry = {}
user_states_waiting_study_graphics_entry = {}

#Envia o menu de estudos
@bot.callback_query_handler(func=lambda call: call.data == "study_menu")
def show_study_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_study_menu())

#Recebe clique no botão de registro de estudos
@bot.callback_query_handler(func=lambda call: call.data == "study_register")
def receive_click_to_study_register(call):
    user_states_waiting_study_register_entry[call.from_user.id] = WAITING_STUDY_REGISTER_ENTRY
    bot.send_message(call.message.chat.id, "Por favor, envie o registro de estudo: ")

#Recebe dados do que foi estudado e envia prévia ao usuário e botão perguntando se dados estão corretos
@bot.message_handler(func=lambda m: user_states_waiting_study_register_entry.get(m.from_user.id) == WAITING_STUDY_REGISTER_ENTRY)
def register_study(message):
    user_id = message.from_user.id
    user_states_waiting_study_register_entry.pop(user_id)
    input = message.text

    bot.reply_to(message, "Analisando dados, só um instante...")
    response_ia = analyze_study_register_entry(input)

    bot.reply_to(message, response_ia)
    bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_study_register_entry_menu())

#Se usuário apertar sim no botão de dados corretos ele salva os dados
@bot.callback_query_handler(func=lambda call: call.data == "confirm_study_register_yes")
def save_study_register(call):
    bot.send_message(call.message.chat.id, "Salvando dados...")
    convert_analyze_to_json()
    bot.send_message(call.message.chat.id, "Dados salvos com sucesso ✅")

#Se usuário apertar não no botão de dados corretos ele reenvia o menu
@bot.callback_query_handler(func=lambda call: call.data == "confirm_study_register_no")
def show_again_study_menu(call):
    bot.send_message(call.message.chat.id, "Os dados estão corretos?", reply_markup=main_study_menu())

#Após clique no botão de métricas aguarda usuário digitar período
@bot.callback_query_handler(func=lambda call: call.data == "study_metrics")
def receive_click_to_study_metrics(call):
    user_states_waiting_study_metrics_entry[call.from_user.id] = WAITING_STUDY_METRICS_ENTRY
    bot.send_message(call.message.chat.id, "Informe o período:")

#Recebe o período e verifica se ele está no formato correto
@bot.message_handler(func=lambda m: user_states_waiting_study_metrics_entry.get(m.from_user.id) == WAITING_STUDY_METRICS_ENTRY)
def show_metrics(message):
    user_id = message.from_user.id
    user_states_waiting_study_metrics_entry.pop(user_id)
    input = message.text
    result = check_period_d_m_y(input)

    #Se data for correta
    if result:
        text = study_full_report(input)
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    else:
        bot.send_message(message.chat.id, "Período inválido, tente novamente nesse formato (dd/mm - dd/mm/aaaa):", reply_markup=main_study_menu())

#Após clique no botão de visualizar gráfico aguarda usuário digitar período
@bot.callback_query_handler(func=lambda call: call.data == "study_graphics")
def receive_click_to_study_graphics(call):
    user_states_waiting_study_graphics_entry[call.from_user.id] = WAITING_STUDY_GRAPHICS_ENTRY
    bot.send_message(call.message.chat.id, "Informe o período:")

#Recebe o período e verifica se ele está no formato correto
@bot.message_handler(func=lambda m: user_states_waiting_study_graphics_entry.get(m.from_user.id) == WAITING_STUDY_GRAPHICS_ENTRY)
def send_graphics(message):
    user_id = message.from_user.id
    user_states_waiting_study_graphics_entry.pop(user_id)
    period = message.text
    result = check_period_m_y(period)

    #Se data for correta
    if result:
        generate_chart_bubble(period)
        generate_chart_bars(period)

        with open(IMG_BUBBLE_PATH, "rb") as img_bubble:
            bot.send_photo(message.chat.id, img_bubble, caption="Gráfico de Bolhas")

        with open(IMG_BARS_PATH, "rb") as img_bars:
            bot.send_photo(message.chat.id, img_bars, caption="Gráfico de Barras")

    else:
        bot.send_message(message.chat.id, "Período inválido, tente novamente nesse formato (mm/aaaa):", reply_markup=main_study_menu())