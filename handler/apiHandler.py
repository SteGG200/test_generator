from module import getLatestPath
from openai import OpenAI
# from __init__ import get_latest_path
import os
import dotenv
dotenv.load_dotenv()

API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://openrouter.ai/api/v1/'
MODEL = 'google/gemini-2.0-flash-lite-001'

def get_prompt():
	# Read prompt content from file prompt.txt
	prompt_file = open('prompt.txt', 'r', encoding="utf-8")
	prompt_content = prompt_file.read()
	prompt_file.close()
	return prompt_content
def get_exam_content(path: str, log_name = "content.txt"):
	client = OpenAI(
		api_key=API_KEY,
		base_url=BASE_URL
	)
	
	response = client.chat.completions.create(
		model=MODEL,
		messages=[
			{"role": "user", "content": get_prompt()}
		]
	)
	content = response.choices[0].message.content
	
	# Save response from OpenRouter API to file content.txt
	log = open(f"{path}/{log_name}", "w+", encoding="utf-8")
	log_latest = open(getLatestPath() + "/" + log_name, "w+", encoding="utf-8")

	log.write(content)
	log_latest.write(content)

	log.close()
	log_latest.close()

	return content