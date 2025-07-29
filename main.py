from bot import bot
from modules.diet_module import handler_diet
from handlers import general_handlers

if __name__ == "__main__":
    print("Bot iniciado")
    bot.infinity_polling()