from openai import OpenAI
from pathlib import Path
import sys, json

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from keys import OPENAI_KEY
from modules.study_module.functions_study import include_study_register, actually_date, save_txt, read_txt

client = OpenAI(api_key=OPENAI_KEY)

def analyze_study_register_entry(input):
    client = OpenAI(api_key=OPENAI_KEY)
    date = f"\n{actually_date()}"
    input += date
    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_6899facef23881968fae854ac094e76d0dce3b2008d1832d",
            "version": "4"
        }
    )
    
    ia_response = response.output_text

    save_txt("registers_details.txt", ia_response)
    return ia_response

def convert_analyze_to_json():
    client = OpenAI(api_key=OPENAI_KEY)
    input = read_txt("registers_details.txt")

    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_689a309cc838819389434795286307050063297886ade225",
            "version": "3"
        }
    )

    ia_response = json.loads(response.output_text) 
    include_study_register(ia_response)
    return ia_response

def period_generate(input):
    client = OpenAI(api_key=OPENAI_KEY)
    date = actually_date()

    input += f"\nData atual: {date}"

    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_68bb00d19ac48195ad78053a678ad0a60f6cb57682ac7e0f",
            "version": "1"
        }
    )

    ia_response = response.output_text

    return ia_response 