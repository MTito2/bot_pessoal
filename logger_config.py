import logging
import sys

# Configuração do log
logging.basicConfig(
    filename="bot.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Captura erros não tratados no Python inteiro
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Exceção não tratada", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception