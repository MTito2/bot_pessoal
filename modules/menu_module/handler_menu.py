import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from modules.menu_module.keyboards_menu import main_menu_page_1
from general_functions import check_user
from bot import bot

@bot.message_handler(commands=["comandos", "start"])
def send_commands(message):
    if check_user(message):
        bot.reply_to(
            message,
            """
    /comandos - Para ver os comandos disponíveis
    /status - Para verificar o status do bot
    /menu - Para ver o menu
    /cls - Limpar o chat
    """
        )

@bot.message_handler(commands=["status"])
def send_commands(message):
    if check_user(message):
        bot.reply_to(message, "Estou online e funcionando corretamente ✅")

@bot.message_handler(commands=["menu"])
def menu(message):
    if check_user(message):
        bot.send_message(message.chat.id, "Escolha uma opção:", reply_markup=main_menu_page_1())

@bot.message_handler(commands=["cls"])
def send_commands(message):
    if check_user(message):
        for i in range(11):
            bot.send_message(message.chat.id, "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ")