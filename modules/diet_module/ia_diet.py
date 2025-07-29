import sys
from pathlib import Path
from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import OPENAI_KEY

def receive_message():
    client = OpenAI(api_key=OPENAI_KEY)

    response = client.responses.create(
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_6888d8d8f5d48193bca73099d063261d0fefde0130757dbf",
            "version": "1"
        }
    )

    return response.output_text

