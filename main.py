from handler import get_exam_content
from handler import create_exam_document
import dotenv

def main():
	dotenv.load_dotenv()

	try:
		# Get exam content from API
		print("Đang tạo nội dung đề thi...")
		exam_content = get_exam_content()
		
		# Create document
		print("Đang tạo tài liệu...")
		doc = create_exam_document(exam_content)
		
		# Save document
		filename = "./dist/de_thi.docx"
		doc.save(filename)
		print(f"Đã tạo đề thi thành công và lưu với tên: {filename}")
		
	except Exception as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()