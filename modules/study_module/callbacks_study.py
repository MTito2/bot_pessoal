import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from general_ia import period_generate
from general_functions import check_period_d_m_y, check_period_m_y
from modules.study_module.keyboards_study import main_study_menu, confirm_study_register_entry_menu
from modules.study_module.ia_study import analyze_study_register_entry, convert_analyze_to_json
from modules.study_module.metrics_study import study_full_report
from modules.study_module.graphics_study import generate_chart_bars, generate_chart_bubble, IMG_BARS_PATH, IMG_BUBBLE_PATH

WAITING_STUDY_REGISTER_ENTRY = "waiting_study_register_entry"
WAITING_STUDY_METRICS_ENTRY = "waiting_study_metrics_entry"
WAITING_STUDY_GRAPHICS_ENTRY = "waiting_study_graphics_entry"

user_states_waiting_study_register_entry = {}
user_states_waiting_study_metrics_entry = {}
user_states_waiting_study_graphics_entry = {}

@bot.callback_query_handler(func=lambda call: call.data == "study_menu")
def show_study_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_study_menu())

@bot.callback_query_handler(func=lambda call: call.data == "study_register")
def receive_click_to_study_register(call):
    user_states_waiting_study_register_entry[call.from_user.id] = WAITING_STUDY_REGISTER_ENTRY
    bot.send_message(call.message.chat.id, "Por favor, envie o registro de estudo: ")

@bot.message_handler(func=lambda m: user_states_waiting_study_register_entry.get(m.from_user.id) == WAITING_STUDY_REGISTER_ENTRY)
def register_study(message):
    """Analisa e registra uma entrada de estudo enviada pelo usuário.

    Recebe o texto digitado, envia para análise pela IA, retorna o resultado
    ao usuário e pergunta se os dados estão corretos.

    Args:
        message (telebot.types.Message): Mensagem contendo os detalhes do estudo.
    """
    
    user_id = message.from_user.id
    user_states_waiting_study_register_entry.pop(user_id)
    input = message.text

    bot.reply_to(message, "Analisando dados, só um instante...")
    response_ia = analyze_study_register_entry(input)

    bot.send_message(message.chat.id, response_ia)
    bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_study_register_entry_menu())

@bot.callback_query_handler(func=lambda call: call.data == "confirm_study_register_yes")
def save_study_register(call):
    bot.send_message(call.message.chat.id, "Salvando dados...")
    convert_analyze_to_json()
    bot.send_message(call.message.chat.id, "Dados salvos com sucesso ✅")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_study_register_no")
def show_again_study_menu(call):
    bot.send_message(call.message.chat.id, "Os dados estão corretos?", reply_markup=main_study_menu())

@bot.callback_query_handler(func=lambda call: call.data == "study_metrics")
def receive_click_to_study_metrics(call):
    user_states_waiting_study_metrics_entry[call.from_user.id] = WAITING_STUDY_METRICS_ENTRY
    bot.send_message(call.message.chat.id, "Informe o período:")

@bot.message_handler(func=lambda m: user_states_waiting_study_metrics_entry.get(m.from_user.id) == WAITING_STUDY_METRICS_ENTRY)
def show_metrics(message):
    """Exibe métricas de estudo para o período informado pelo usuário.

    Recebe o período digitado, valida o formato (dd/mm - dd/mm/aaaa) e envia
    o relatório completo de estudo. Se o período for inválido ou não houver dados,
    envia mensagem de aviso.

    Args:
        message (telebot.types.Message): Mensagem contendo o período.
    """

    user_id = message.from_user.id
    user_states_waiting_study_metrics_entry.pop(user_id)
    period = message.text
    period = period_generate(period)
    
    result = check_period_d_m_y(period)

    #Se data for correta
    if result:
        try:
            text = study_full_report(period)
            bot.send_message(message.chat.id, text, parse_mode="Markdown")

        except Exception:
           bot.send_message(message.chat.id, "Nenhum dado encontrado nesse período") 
    
    else:
        bot.send_message(message.chat.id, "Período inválido, tente novamente nesse formato (dd/mm - dd/mm/aaaa):", reply_markup=main_study_menu())

@bot.callback_query_handler(func=lambda call: call.data == "study_graphics")
def receive_click_to_study_graphics(call):
    user_states_waiting_study_graphics_entry[call.from_user.id] = WAITING_STUDY_GRAPHICS_ENTRY
    bot.send_message(call.message.chat.id, "Informe o período:")

@bot.message_handler(func=lambda m: user_states_waiting_study_graphics_entry.get(m.from_user.id) == WAITING_STUDY_GRAPHICS_ENTRY)
def send_graphics(message):
    """Gera e envia gráficos de estudo para o período informado pelo usuário.

    Recebe o período digitado, valida o formato (mm/aaaa) e envia gráficos
    de bolhas e de barras correspondentes. Se o período for inválido, envia
    mensagem de aviso.

    Args:
        message (telebot.types.Message): Mensagem enviada pelo usuário contendo o período.
    """
    
    user_id = message.from_user.id
    user_states_waiting_study_graphics_entry.pop(user_id)
    period = message.text
    result = check_period_m_y(period)

    if result:
        generate_chart_bubble(period)
        generate_chart_bars(period)

        with open(IMG_BUBBLE_PATH, "rb") as img_bubble:
            bot.send_photo(message.chat.id, img_bubble, caption="Gráfico de Bolhas")

        with open(IMG_BARS_PATH, "rb") as img_bars:
            bot.send_photo(message.chat.id, img_bars, caption="Gráfico de Barras")

    else:
        bot.send_message(message.chat.id, "Período inválido, tente novamente nesse formato (mm/aaaa):", reply_markup=main_study_menu())