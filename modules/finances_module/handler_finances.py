import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.finances_module.ia_finances import analyze_image
from modules.finances_module.functions_finances import save_photo


user_states = {}
WAITING_COUPON_PHOTO = "waiting_coupon_photo"

@bot.message_handler(commands=["analisar_cupom"])
def start_analysis(message):
    user_states[message.from_user.id] = WAITING_COUPON_PHOTO
    bot.reply_to(message, "Por favor, envie uma foto do cupom fiscal.")

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
        bot.reply_to(message, analysis_response)

        

