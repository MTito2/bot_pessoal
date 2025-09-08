
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
            "id": "pmpt_68bb00d19ac48195ad78053a678ad0a60f6cb57682ac7e0f",
            "version": "1"
        }
    )

    ia_response = response.output_text

    return ia_response 