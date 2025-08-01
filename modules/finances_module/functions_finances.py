import sys
from pathlib import Path

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

def read_prompt():
    prompt_path = FILES_FINANCES_MODULE_PATH / "prompt.txt"
    
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read()

    return prompt