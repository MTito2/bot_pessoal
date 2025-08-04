from bot import bot
from modules.diet_module import callbacks_diet, keyboards_diet
from modules.finances_module import callbacks_finances, keyboards_finances
from modules.menu_module import callbacks_menu, handler_menu, keyboards_menu


if __name__ == "__main__":
    print("Bot iniciado ✅")
    bot.infinity_polling()

#terminar callbacks do finace module
