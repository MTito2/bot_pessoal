from openai import OpenAI
from pathlib import Path
import sys, json

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from keys import OPENAI_KEY
from config import FILES_FINANCES_MODULE_PATH
from general_functions import actually_date, read_txt
from modules.finances_module.functions_finances import encode_image, include_expenses

client = OpenAI(api_key=OPENAI_KEY)

def analyze_image():
    image_path = FILES_FINANCES_MODULE_PATH / "img.jpeg"
    base64_image = encode_image(image_path)
    prompt = read_txt(FILES_FINANCES_MODULE_PATH, "prompt.txt")
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
    date = actually_date()
    input += f"\n{date}"

    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_6957e394c2208197899c125a3ef6f8b303d18114f7f7e6db",
            "version": "1"
        }
    )
    
    return response.output_text

def convert_analyze_to_json(input):
    client = OpenAI(api_key=OPENAI_KEY)

    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_6957e3b03a74819591a7392ea6ee759605974d8951b7b6da",
            "version": "1"
        }
    )

    ia_response = json.loads(response.output_text) 
    include_expenses(ia_response)
