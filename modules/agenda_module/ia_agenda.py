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
            "id": "pmpt_6957e3f9d5fc81908e80eb6cf995222008db875d0f5f10f0",
            "version": "1"
        }
    )

    return response.output_text


