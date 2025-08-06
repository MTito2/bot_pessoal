from openai import OpenAI
from pathlib import Path
import sys, json

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from keys import OPENAI_KEY
from config import FILES_FINANCES_MODULE_PATH
from modules.finances_module.functions_finances import encode_image, read_txt, include_expenses

client = OpenAI(api_key=OPENAI_KEY)

def analyze_image():
    image_path = FILES_FINANCES_MODULE_PATH / "img.jpeg"
    base64_image = encode_image(image_path)
    prompt = read_txt("prompt.txt")
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"{prompt}"},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    }
                ]
            }
        ]
    )

    return response.output_text

def analyze_manual_expense_entry(input):
    client = OpenAI(api_key=OPENAI_KEY)

    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_689215b60a64819092e79038cc1123db0aa90fd02a3e8819",
            "version": "3"
        }
    )
    
    return response.output_text

def convert_analyze_to_json(input):
    client = OpenAI(api_key=OPENAI_KEY)

    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_689113b13cb48196bf154146f5b8727908384ea949f1d6a5",
            "version": "6"
        }
    )

    ia_response = json.loads(response.output_text) 
    include_expenses(ia_response)