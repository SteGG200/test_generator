from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://openrouter.ai/api/v1/'
MODEL = 'google/gemini-2.0-flash-lite-preview-02-05:free'

def create_exam_prompt():
	return """
	Hãy tạo một đề thi trắc nghiệm 50 câu về HTML và CSS với định dạng sau cho mỗi câu hỏi phải chính xác như sau:

	**Câu X**: [Nội dung câu hỏi]
	**A**. [Lựa chọn A]
	**B**. [Lựa chọn B] 
	**C**. [Lựa chọn C]
	**D**. [Lựa chọn D]
	
	Yêu cầu của đầu ra:
	- Không được ghi gì khác ngoài nội dung các câu hỏi
	- Câu hỏi về thuộc tính CSS, thẻ HTML, layout
	- Có ít nhất 5 câu về iframe
	- Đáp án đúng phân bố ngẫu nhiên
	- Giữ nguyên định dạng markdown cho mỗi câu hỏi như mẫu trên
	"""

def get_exam_content():
	client = OpenAI(
		api_key=API_KEY,
		base_url=BASE_URL
	)
	
	try:
		response = client.chat.completions.create(
			model=MODEL,
			messages=[
				{"role": "user", "content": create_exam_prompt()}
			]
		)
		content = response.choices[0].message.content

		log = open("./dist/content.md", "w+")

		log.write(content)

		log.close()

		return content
	except Exception as e:
		raise Exception(f"Lỗi khi gọi API: {str(e)}")