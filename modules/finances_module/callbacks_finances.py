import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.finances_module.metrics_finances import expenses_full_report
from modules.finances_module.graphics_finances import generate_chart_daily_bars, generate_chart_pie, IMG_BARS_PATH, IMG_PIE_PATH
from modules.finances_module.ia_finances import analyze_image, convert_analyze_to_json, analyze_manual_expense_entry, period_generate
from modules.finances_module.functions_finances import save_photo, save_txt, read_txt, check_period_d_m_y, check_period_m_y
from modules.finances_module.keyboards_finances import main_finances_menu, confirm_information_coupon_menu, confirm_manual_expense_entry_menu

user_states_waiting_photo = {}
user_states_waiting_manual_expense_entry = {}
user_states_waiting_expenses_metrics_entry = {}
user_states_waiting_expenses_graphics_entry = {}

WAITING_COUPON_PHOTO = "waiting_coupon_photo"
WAITING_EXPENSE_ENTRY = "waiting_expense_entry"
WAITING_EXPENSES_METRICS_ENTRY = "waiting_expenses_metrics_entry"
WAITING_EXPENSES_GRAPHICS_ENTRY = "waiting_expenses_metrics_entry"

@bot.callback_query_handler(func=lambda call: call.data == "finances_menu")
def handle_finance_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_finances_menu())

@bot.callback_query_handler(func= lambda call: call.data == "analyze_coupon")
def receive_click_analyze_coupon(call):
    user_states_waiting_photo[call.from_user.id] = WAITING_COUPON_PHOTO
    bot.send_message(call.message.chat.id, "Por favor, envie uma foto do cupom fiscal:")

@bot.message_handler(content_types=["photo"])
def start_analyze_coupon(message):
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
        save_txt("coupon_details.txt", analysis_response)

        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, analysis_response)
        bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_information_coupon_menu())

@bot.callback_query_handler(func=lambda call: call.data == "confirm_information_coupon_yes")
def save_analysis_img(call):
    bot.send_message(call.message.chat.id, "Salvando dados...")
    analysis_response = read_txt("coupon_details.txt")
    convert_analyze_to_json(analysis_response)
    bot.send_message(call.message.chat.id, "Dados salvos com sucesso ✅")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_information_coupon_no")
def show_again_finances_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_finances_menu())

@bot.callback_query_handler(func=lambda call: call.data == "entry_expenses")
def receive_click_manual_expense_entry(call):
    user_states_waiting_manual_expense_entry[call.from_user.id] = WAITING_EXPENSE_ENTRY
    bot.send_message(call.message.chat.id, "Por favor, envie os detalhes das despesas:")

@bot.message_handler(func=lambda m: user_states_waiting_manual_expense_entry.get(m.from_user.id) == WAITING_EXPENSE_ENTRY)
def start_analyze_manual_expense_entry(message):
    user_id = message.from_user.id
    user_states_waiting_manual_expense_entry.pop(user_id)

    input = message.text
    bot.reply_to(message, "Vou analisar os dados, só um minuto...")

    bot.send_chat_action(message.chat.id, "typing")
    analyze_response = analyze_manual_expense_entry(input)
    bot.send_message(message.chat.id, analyze_response)
    bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_manual_expense_entry_menu())

    save_txt("expense_details.txt", analyze_response)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_entry_expenses_yes")
def save_analysis_manual_expense_entry(call):
    bot.send_message(call.message.chat.id, "Salvando dados...")
    analysis_response = read_txt("expense_details.txt")
    convert_analyze_to_json(analysis_response)
    bot.send_message(call.message.chat.id, "Dados salvos com sucesso ✅")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_entry_expenses_no")
def show_again_finances_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_finances_menu())

#Após clique no botão de métricas aguarda usuário digitar período
@bot.callback_query_handler(func=lambda call: call.data == "expenses_metrics")
def receive_click_to_expenses_metrics(call):
    user_states_waiting_expenses_metrics_entry[call.from_user.id] = WAITING_EXPENSES_METRICS_ENTRY
    bot.send_message(call.message.chat.id, "Informe o período:")

#Recebe o período e verifica se ele está no formato correto
@bot.message_handler(func=lambda m: user_states_waiting_expenses_metrics_entry.get(m.from_user.id) == WAITING_EXPENSES_METRICS_ENTRY)
def show_metrics(message):
    user_id = message.from_user.id
    user_states_waiting_expenses_metrics_entry.pop(user_id)

    period = message.text
    period = period_generate(period)

    result = check_period_d_m_y(period)

    #Se data for correta
    if result:
        try:
            text = expenses_full_report(period)
            bot.send_message(message.chat.id, text, parse_mode="Markdown")

        except Exception:
            bot.send_message(message.chat.id, "Nenhum dado econtrado nesse período.")
    
    else:
        bot.send_message(message.chat.id, "Período inválido, tente novamente nesse formato (dd/mm - dd/mm/aaaa):", reply_markup=main_finances_menu())

#Após clique no botão de visualizar gráfico aguarda usuário digitar período
@bot.callback_query_handler(func=lambda call: call.data == "expenses_graphics")
def receive_click_to_study_graphics(call):
    user_states_waiting_expenses_graphics_entry[call.from_user.id] = WAITING_EXPENSES_GRAPHICS_ENTRY
    bot.send_message(call.message.chat.id, "Informe o período:")

#Recebe o período e verifica se ele está no formato correto
@bot.message_handler(func=lambda m: user_states_waiting_expenses_graphics_entry.get(m.from_user.id) == WAITING_EXPENSES_GRAPHICS_ENTRY)
def send_graphics(message):
    user_id = message.from_user.id
    user_states_waiting_expenses_graphics_entry.pop(user_id)
    period = message.text
    result = check_period_m_y(period)

    #Se data for correta
    if result:
        generate_chart_daily_bars(period)
        generate_chart_pie(period)

        with open(IMG_BARS_PATH, "rb") as img_bars:
            bot.send_photo(message.chat.id, img_bars, caption="Gráfico de Barras")

        with open(IMG_PIE_PATH, "rb") as img_pie:
            bot.send_photo(message.chat.id, img_pie, caption="Gráfico de Pizza")

    else:
        bot.send_message(message.chat.id, "Período inválido, tente novamente nesse formato (mm/aaaa):", reply_markup=main_finances_menu())