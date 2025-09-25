import sys
from pathlib import Path
from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(ROOT_DIR))

from keys import OPENAI_KEY
from general_functions import actually_date

def receive_event(input):
    client = OpenAI(api_key=OPENAI_KEY)
    now = actually_date()
    input += f"\n Data atual: {now}"
    
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=input,
        prompt={
            "id": "pmpt_68d056dcd8748196b28fa4127f8c4dd60b83c7ca8977d533",
            "version": "4"
        }
    )

    return response.output_text


