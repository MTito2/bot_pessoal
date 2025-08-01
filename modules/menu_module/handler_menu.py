import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from bot import bot

@bot.message_handler(commands=["comandos", "start"])
def send_commands(message):
    bot.reply_to(
        message,
        """
/comandos - Para ver os comandos disponíveis
/sugerir_refeicao - Para receber uma sugestão de refeição
/status - Para verificar o status do bot
/analisar_cupom - Analisa a imagem do cupom fiscal
"""
    )

@bot.message_handler(commands=["status"])
def send_commands(message):
    bot.reply_to(message, "Estou online e funcionando corretamente ✅")