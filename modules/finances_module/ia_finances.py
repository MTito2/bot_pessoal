from openai import OpenAI
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from keys import OPENAI_KEY
from config import FILES_FINANCES_MODULE_PATH
from modules.finances_module.functions_finances import encode_image, read_prompt

client = OpenAI(api_key=OPENAI_KEY)

def analyze_image():
    image_path = FILES_FINANCES_MODULE_PATH / "img.jpeg"
    base64_image = encode_image(image_path)
    prompt = read_prompt()
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
