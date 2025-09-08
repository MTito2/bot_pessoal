import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_FINANCES_MODULE_PATH
from general_functions import read_json, export_json
import base64

def encode_image(image_path):
    with open (image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def save_photo(downloaded_photo):
    image_path = FILES_FINANCES_MODULE_PATH / "img.jpeg"
   
    with open(image_path, "wb") as file:
        file.write(downloaded_photo)

def include_expenses(new_expenses):
    expenses = read_json(FILES_FINANCES_MODULE_PATH, "expenses.json")

    for new_expense in new_expenses:
        expenses.append(new_expense)

    export_json(expenses, FILES_FINANCES_MODULE_PATH, "expenses.json")
