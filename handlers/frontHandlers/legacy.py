import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL") or "https://openrouter.ai/api/v1/"
MODEL = os.environ.get("MODEL") or "google/gemini-2.0-pro-exp-02-05:free"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def handler(prompt_content: str, n_problems: int):
    response = (
        client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt_content,
                }
            ],
        )
        .choices[0]
        .message.content
    )
    assert response is not None

    return {"response": response}
