import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot
from modules.diet_module.ia_diet import receive_message

@bot.message_handler(commands=["sugerir_refeicao"])
def send_diet(message):
    response_ia = receive_message()
    bot.reply_to(message, response_ia)

