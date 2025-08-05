import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.finances_module.ia_finances import analyze_image, convert_analyze_image_to_json
from modules.finances_module.functions_finances import save_photo, save_txt, read_txt
from modules.finances_module.keyboards_finances import main_finances_menu, confirm_information_menu

user_states = {}
WAITING_COUPON_PHOTO = "waiting_coupon_photo"

@bot.callback_query_handler(func=lambda call: call.data == "finances_menu")
def handle_diet_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_finances_menu())

@bot.callback_query_handler(func= lambda call: call.data == "analyze_coupon")
def start_analysis(call):
    user_states[call.from_user.id] = WAITING_COUPON_PHOTO
    bot.send_message(call.message.chat.id, "Por favor, envie uma foto do cupom fiscal.")

@bot.message_handler(content_types=["photo"])
def receive_img(message):
    user_id = message.from_user.id
    if user_states.get(user_id) == WAITING_COUPON_PHOTO:
        bot.reply_to(message, "Foto recebida ✅")
        bot.reply_to(message, "Vou analisar o cupom fiscal, só um instante...")
        user_states.pop(user_id)

        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        downloaded_photo = bot.download_file(photo_info.file_path)
        save_photo(downloaded_photo)

        analysis_response = analyze_image()
        save_txt("coupon_details.txt", analysis_response)
        bot.reply_to(message, analysis_response)
        bot.send_message(message.chat.id, "Os dados estão corretos?", reply_markup=confirm_information_menu())

@bot.callback_query_handler(func=lambda call: call.data == "confirm_information_finances_yes")
def save_analysis(call):
    bot.send_message(call.message.chat.id, "Salvando dados...")
    analysis_response = read_txt("coupon_details.txt")
    convert_analyze_image_to_json(analysis_response)
    bot.send_message(call.message.chat.id, "Dados salvos com sucesso ✅")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_information_finances_no")
def show_again_finances_menu(call):
    bot.send_message(call.message.chat.id, "Escolha uma opção:", reply_markup=main_finances_menu())