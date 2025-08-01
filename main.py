from bot import bot
from modules.diet_module import handler_diet
from modules.finances_module import handler_finances
from modules.menu_module import handler_menu

if __name__ == "__main__":
    print("Bot iniciado")
    bot.infinity_polling()