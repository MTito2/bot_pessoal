import sys, json, re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_STUDY_MODULE_PATH
from general_functions import read_json, export_json

def include_study_register(new_registers):
    registers = read_json(FILES_STUDY_MODULE_PATH, "registers.json")

    for new_register in new_registers:
        registers.append(new_register)

    export_json(registers, FILES_STUDY_MODULE_PATH, "registers.json")


