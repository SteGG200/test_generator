from handler import get_exam_content
from handler import create_exam_document
from datetime import datetime
import os

def main():
	try:
		path = f"./dist/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
		if not os.path.exists(path):
			os.makedirs(path)
		# Get exam content from API
		print("Đang tạo nội dung đề thi...")
		exam_content = get_exam_content(path)
		
		# Create document
		print("Đang tạo tài liệu...")
		create_exam_document(path, exam_content)
	except Exception as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()