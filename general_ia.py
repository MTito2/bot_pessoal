
from openai import OpenAI
from general_functions import actually_date
from keys import OPENAI_KEY

def period_generate(input):
    client = OpenAI(api_key=OPENAI_KEY)
    date = actually_date()

    input += f"\nData atual: {date}"

    response = client.responses.create(
        input=input,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_6957e30f286081968e2f852364c2126a0dd1f3fc5bb6da32",
            "version": "1"
        }
    )

    ia_response = response.output_text

    return ia_response 