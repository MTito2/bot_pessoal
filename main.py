from bot import bot
from modules.agenda_module import callbacks_agenda, keyboards_agenda
from modules.diet_module import callbacks_diet, keyboards_diet
from modules.finances_module import callbacks_finances, keyboards_finances 
from modules.study_module import callbacks_study, keyboards_study 
from modules.menu_module import callbacks_menu, handler_menu, keyboards_menu

if __name__ == "__main__":
    print("Bot iniciado ✅")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
