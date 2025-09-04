import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.finances_module.ia_finances import analyze_image, convert_analyze_to_json, analyze_manual_expense_entry
from modules.finances_module.functions_finances import save_photo, save_txt, read_txt
from modules.finances_module.keyboards_finances import main_finances_menu, confirm_information_coupon_menu, confirm_manual_expense_entry_menu

user_states_waiting_photo = {}
user_states_waiting_manual_expense_entry = {}

WAITING_COUPON_PHOTO = "waiting_coupon_photo"
WAITING_EXPENSE_ENTRY = "waiting_expense_entry"

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