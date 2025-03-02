from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://openrouter.ai/api/v1/'
MODEL = 'google/gemini-2.0-flash-lite-preview-02-05:free'

def create_exam_prompt():
	return"""
	Generate a 50-question exam with HTML and CSS questions in Vietnamese with one example:
	
	**Câu 1**: Định dạng CSS nào sau đây được sử dụng để đặt màu nền của phần tử <p> là màu xám?
	**A**. p {background-color: gray;}
	**B**. p {bg-color: gray;}
	**C**. p {color: gray;}
	**D**. p {background: gray;}

  Requirements:
  - No other text but question content should be included
  - Questions about CSS properties, HTML tags, layout
  - At least 5 questions about iframes
  - Correct answers should be randomly distributed
	- Just generate text from below format, not HTML
  
	Each question's format:
	**Câu X**: [Question]
  **A**. [Option 1]
  **B**. [Option 2]
  **C**. [Option 3]
  **D**. [Option 4]
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
			{"role": "user", "content": create_exam_prompt()}
		]
	)
	content = response.choices[0].message.content
	
	log_name = "content.md"
	log = open(f"{path}/{log_name}", "w+")

	log.write(content)

	log.close()

	return content