import logging
import sys
from config import LOGS_PATH

path = LOGS_PATH / "bot.log"

logging.basicConfig(
    filename=path,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Exceção não tratada", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception