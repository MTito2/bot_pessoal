import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from config import FILES_FINANCES_MODULE_PATH
from general_functions import save_txt, read_txt, check_period_d_m_y, check_period_m_y
from general_ia import period_generate
from modules.finances_module.metrics_finances import expenses_full_report
from modules.finances_module.graphics_finances import generate_chart_daily_bars, generate_chart_pie, IMG_BARS_PATH, IMG_PIE_PATH
from modules.finances_module.ia_finances import analyze_image, convert_analyze_to_json, analyze_manual_expense_entry
from modules.finances_module.functions_finances import save_photo
from modules.finances_module.keyboards_finances import main_finances_menu, confirm_information_coupon_menu, confirm_manual_expense_entry_menu

user_states_waiting_photo = {}
user_states_waiting_manual_expense_entry = {}
user_states_waiting_expenses_metrics_entry = {}
user_states_waiting_expenses_graphics_entry = {}

WAITING_COUPON_PHOTO = "waiting_coupon_photo"
WAITING_EXPENSE_ENTRY = "waiting_expense_entry"
WAITING_EXPENSES_METRICS_ENTRY = "waiting_expenses_metrics_entry"
WAITING_EXPENSES_GRAPHICS_ENTRY = "waiting_expenses_graphics_entry"

@bot.callback_query_handler(func=lambda call: call.data == "finances_menu")
def handle_finance_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_finances_menu())

@bot.callback_query_handler(func= lambda call: call.data == "analyze_coupon")
def receive_click_analyze_coupon(call):
    user_states_waiting_photo[call.from_user.id] = WAITING_COUPON_PHOTO
    bot.send_message(call.message.chat.id, "Por favor, envie uma foto do cupom fiscal:")

@bot.message_handler(content_types=["photo"])
def start_analyze_coupon(message):
    """Processa a foto de um cupom, salva a análise e pergunta ao usuário se os dados estão corretos.

    A função só age se o usuário estiver no estado de envio de cupom. 
    Salva a imagem, realiza a análise, armazena o resultado em 'coupon_details.txt' 
    e pergunta ao usuário se os dados extraídos estão corretos.

    Args:
        message (telebot.types.Message): Mensagem contendo a foto enviada pelo usuário.
    """

    user_id = message.from_user.id
    if user_states_waiting_photo.get(user_id) == WAITING_COUPON_PHOTO:
        bot.reply_to(message, "Foto recebida ✅")
        bot.reply_to(message, "Vou analisar o cupom fiscal, só um instante...")
        user_states_waiting_photo.pop(user_id)

        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        downloaded_photo = bot.download_file(photo_info.file_path)
        save_photo(downloaded_photo)

        analysis_response = analyze_image()
        save_txt(analysis_response, FILES_FINANCES_MODULE_PATH, "coupon_details.txt")

        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, analysis_response)
        bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_information_coupon_menu())

@bot.callback_query_handler(func=lambda call: call.data == "confirm_information_coupon_yes")
def save_analysis_img(call):
    bot.send_message(call.message.chat.id, "Salvando dados...")
    analysis_response = read_txt(FILES_FINANCES_MODULE_PATH, "coupon_details.txt")
    convert_analyze_to_json(analysis_response)
    bot.send_message(call.message.chat.id, "Dados salvos com sucesso ✅")

@bot.callback_query_handler(func=lambda call: call.data in ("confirm_information_coupon_no", "confirm_entry_expenses_no"))
def show_again_finances_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_finances_menu())

@bot.callback_query_handler(func=lambda call: call.data == "entry_expenses")
def receive_click_manual_expense_entry(call):
    user_states_waiting_manual_expense_entry[call.from_user.id] = WAITING_EXPENSE_ENTRY
    bot.send_message(call.message.chat.id, "Por favor, envie os detalhes das despesas:")

@bot.message_handler(func=lambda m: user_states_waiting_manual_expense_entry.get(m.from_user.id) == WAITING_EXPENSE_ENTRY)
def start_analyze_manual_expense_entry(message):
    """Analisa despesas enviadas pelo usuário e solicita confirmação.

    A função processa o texto da despesa, formata os dados via IA, 
    envia o resultado ao usuário e pergunta se os dados estão corretos.
    Também salva a análise em 'expense_details.txt'.

    Args:
        message (telebot.types.Message): Mensagem enviada pelo usuário contendo a despesa.
    """

    user_id = message.from_user.id
    user_states_waiting_manual_expense_entry.pop(user_id)

    input = message.text
    bot.reply_to(message, "Vou analisar os dados, só um minuto...")

    bot.send_chat_action(message.chat.id, "typing")
    analyze_response = analyze_manual_expense_entry(input)
    bot.send_message(message.chat.id, analyze_response)
    bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_manual_expense_entry_menu())

    save_txt(analyze_response, FILES_FINANCES_MODULE_PATH, "expense_details.txt")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_entry_expenses_yes")
def save_analysis_manual_expense_entry(call):
    bot.send_message(call.message.chat.id, "Salvando dados...")
    analysis_response = read_txt(FILES_FINANCES_MODULE_PATH, "expense_details.txt")
    convert_analyze_to_json(analysis_response)
    bot.send_message(call.message.chat.id, "Dados salvos com sucesso ✅")

@bot.callback_query_handler(func=lambda call: call.data == "expenses_metrics")
def receive_click_to_expenses_metrics(call):
    user_states_waiting_expenses_metrics_entry[call.from_user.id] = WAITING_EXPENSES_METRICS_ENTRY
    bot.send_message(call.message.chat.id, "Informe o período:")

@bot.message_handler(func=lambda m: user_states_waiting_expenses_metrics_entry.get(m.from_user.id) == WAITING_EXPENSES_METRICS_ENTRY)
def show_metrics(message):
    """Exibe métricas de despesas para o período informado pelo usuário.

    Recebe o período digitado, valida o formato e envia o relatório de despesas.
    Caso o período seja inválido ou não haja dados, envia mensagem de aviso.

    Args:
        message (telebot.types.Message): Mensagem enviada pelo usuário contendo o período.
    """
    
    user_id = message.from_user.id
    user_states_waiting_expenses_metrics_entry.pop(user_id)

    period = message.text
    period = period_generate(period)

    result = check_period_d_m_y(period)

    if result:
        try:
            text = expenses_full_report(period)
            bot.send_message(message.chat.id, text, parse_mode="Markdown")

        except Exception:
            bot.send_message(message.chat.id, "Nenhum dado econtrado nesse período.")
    
    else:
        bot.send_message(message.chat.id, "Período inválido, tente novamente nesse formato (dd/mm - dd/mm/aaaa):", reply_markup=main_finances_menu())

@bot.callback_query_handler(func=lambda call: call.data == "expenses_graphics")
def receive_click_to_study_graphics(call):
    user_states_waiting_expenses_graphics_entry[call.from_user.id] = WAITING_EXPENSES_GRAPHICS_ENTRY
    bot.send_message(call.message.chat.id, "Informe o período:")

@bot.message_handler(func=lambda m: user_states_waiting_expenses_graphics_entry.get(m.from_user.id) == WAITING_EXPENSES_GRAPHICS_ENTRY)
def send_graphics(message):
    """Gera e envia gráficos de despesas para o período informado.

    Recebe o período digitado pelo usuário, valida o formato (mm/aaaa) 
    e envia gráficos de barras e pizza correspondentes. Se o período for inválido, 
    envia mensagem de aviso.

    Args:
        message (telebot.types.Message): Mensagem enviada pelo usuário contendo o período.
    """
    
    user_id = message.from_user.id
    user_states_waiting_expenses_graphics_entry.pop(user_id)
    period = message.text
    result = check_period_m_y(period)

    if result:
        generate_chart_daily_bars(period)
        generate_chart_pie(period)

        with open(IMG_BARS_PATH, "rb") as img_bars:
            bot.send_photo(message.chat.id, img_bars, caption="Gráfico de Barras")

        with open(IMG_PIE_PATH, "rb") as img_pie:
            bot.send_photo(message.chat.id, img_pie, caption="Gráfico de Pizza")

    else:
        bot.send_message(message.chat.id, "Período inválido, tente novamente nesse formato (mm/aaaa):", reply_markup=main_finances_menu())