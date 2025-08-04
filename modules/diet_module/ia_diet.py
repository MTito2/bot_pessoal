import sys
from pathlib import Path
from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
from modules.diet_module.functions_diet import save_last_suggestion, read_last_suggestion

sys.path.insert(0, str(ROOT_DIR))

from keys import OPENAI_KEY

def receive_message():
    client = OpenAI(api_key=OPENAI_KEY)
    last_suggestion = read_last_suggestion() 

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"{last_suggestion}",
        prompt={
            "id": "pmpt_6888d8d8f5d48193bca73099d063261d0fefde0130757dbf",
            "version": "2"
        }
    )

    save_last_suggestion(response.output_text)
    return response.output_text

