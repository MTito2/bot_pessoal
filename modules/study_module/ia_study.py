from openai import OpenAI
from pathlib import Path
import sys, json

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from keys import OPENAI_KEY
from config import FILES_STUDY_MODULE_PATH
from general_functions import actually_date, save_txt, read_txt
from modules.study_module.functions_study import include_study_register

def analyze_study_register_entry(input):
    client = OpenAI(api_key=OPENAI_KEY)
    date = f"\n{actually_date()}"
    input += date
    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_6957e35ff774819091e5b9621cb26cef07bedb26ae47ff97",
            "version": "1"
        }
    )
    
    ia_response = response.output_text

    save_txt(ia_response, FILES_STUDY_MODULE_PATH, "registers_details.txt", )
    return ia_response

def convert_analyze_to_json():
    client = OpenAI(api_key=OPENAI_KEY)
    input = read_txt(FILES_STUDY_MODULE_PATH, "registers_details.txt")

    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_6957e35ff774819091e5b9621cb26cef07bedb26ae47ff97",
            "version": "1"
        }
    )

    ia_response = json.loads(response.output_text) 
    include_study_register(ia_response)
    return ia_response
