import sys, json
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_STUDY_MODULE_PATH

def read_txt(file_name):
    path = FILES_STUDY_MODULE_PATH / file_name
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    return content

def save_txt(file_name, content):
    path = FILES_STUDY_MODULE_PATH / file_name
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

def read_json(file_name):
    path = FILES_STUDY_MODULE_PATH / file_name
    
    with open(path, "r", encoding="utf-8") as file:
        content = json.load(file)

    return content

def export_json(file_name, content):
    path = FILES_STUDY_MODULE_PATH / file_name
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

def include_study_register(new_registers):
    registers = read_json("registers.json")

    for new_register in new_registers:
        registers.append(new_register)

    export_json("registers.json", registers)

def actually_date():
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return date

