from bot import bot

@bot.message_handler(commands=["comandos", "start"])
def send_commands(message):
    bot.reply_to(message, "/comandos - Para ver os comandos disponíveis\n/sugerir_refeicao - Para receber um sugestão de refeicao\n/status - Para verificar o status do bot")

@bot.message_handler(commands=["status"])
def send_commands(message):
    bot.reply_to(message, "Estou online e funcionando corretamente")