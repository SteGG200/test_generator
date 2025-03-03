from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://openrouter.ai/api/v1/'
MODEL = 'google/gemini-2.0-pro-exp-02-05:free'

PROMPT = """
Generate a 50-question exam with HTML and CSS questions in Vietnamese with one example:

1. Định dạng CSS nào sau đây được sử dụng để đặt màu nền của phần tử <p> là màu xám?
*a) p {background-color: gray;}
b) p {bg-color: gray;}
c) p {color: gray;}
d) p {background: gray;}

Note: the answer has the star is the correct answer.

Requirements:
- No other text but question content should be included
- Questions about CSS properties, HTML tags, layout
- At least 5 questions about iframes
- Correct answers should be randomly distributed
- Each answer must be different.
- Must generate text exactly from below format, not markdown or HTML:

Each question's format (for example Option 2 is the correct answer):
X. [Question]
a) [Option 1]
*b) [Option 2]
c) [Option 3]
d) [Option 4]

- Add a asterisk symbol before correct answer.
- Every code block (HTML tag, CSS code) must be put in backticks.
- No indentation in the question format.
- Each question must be separated by a blank line.
"""

	# return """
	# Hãy tạo một đề thi trắc nghiệm 50 câu về HTML và CSS với định dạng sau cho mỗi câu hỏi phải chính xác như sau:

	# **Câu X**: [Nội dung câu hỏi]
	# **A**. [Lựa chọn A]
	# **B**. [Lựa chọn B] 
	# **C**. [Lựa chọn C]
	# **D**. [Lựa chọn D]
	
	# Yêu cầu của đầu ra:
	# - Không được ghi gì khác ngoài nội dung các câu hỏi
	# - Câu hỏi về thuộc tính CSS, thẻ HTML, layout
	# - Có ít nhất 5 câu về iframe
	# - Đáp án đúng phân bố ngẫu nhiên
	# - Giữ nguyên định dạng markdown cho mỗi câu hỏi như mẫu trên
	# """

def get_exam_content(path: str):
	client = OpenAI(
		api_key=API_KEY,
		base_url=BASE_URL
	)
	
	response = client.chat.completions.create(
		model=MODEL,
		messages=[
			{"role": "user", "content": PROMPT}
		]
	)
	content = response.choices[0].message.content
	
	log_name = "content.txt"
	log = open(f"{path}/{log_name}", "w+")

	log.write(content)

	log.close()

	return content