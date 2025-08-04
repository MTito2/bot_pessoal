from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import DIET_MODULE_PATH

def save_last_suggestion(last_suggestion):
    path = DIET_MODULE_PATH / "files" / "last_suggestion.txt"

    with open (path, "w", encoding= "utf-8") as file:
        file.write(last_suggestion)

def read_last_suggestion():
    path = DIET_MODULE_PATH / "files" / "last_suggestion.txt"
    
    with open (path, "r", encoding= "utf-8") as file:
        content = file.read()

    return content