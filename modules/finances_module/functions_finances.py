import sys, json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_FINANCES_MODULE_PATH
import base64

def encode_image(image_path):
    with open (image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def save_photo(downloaded_photo):
    image_path = FILES_FINANCES_MODULE_PATH / "img.jpeg"
   
    with open(image_path, "wb") as file:
        file.write(downloaded_photo)

def read_txt(file_name):
    path = FILES_FINANCES_MODULE_PATH / file_name
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    return content

def save_txt(file_name, content):
    path = FILES_FINANCES_MODULE_PATH / file_name
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

def read_json(file_name):
    path = FILES_FINANCES_MODULE_PATH / file_name
    
    with open(path, "r", encoding="utf-8") as file:
        content = json.load(file)

    return content

def actually_date():
    date = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")
    return date

def export_json(file_name, content):
    path = FILES_FINANCES_MODULE_PATH / file_name
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

def include_expenses(new_expenses):
    expenses = read_json("expenses.json")

    for new_expense in new_expenses:
        expenses.append(new_expense)

    export_json("expenses.json", expenses)
