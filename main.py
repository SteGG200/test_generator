from handler import get_exam_content, create_exam_document, convert_to_QTI
from datetime import datetime
import os

def main():
	path = f"./dist/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
	if not os.path.exists(path):
		os.makedirs(path)
	# Get exam content from API
	print("Đang tạo nội dung đề thi...")
	exam_content = get_exam_content(path)
	
	# Create QTI file
	print("Đang tạo tài liệu QTI...")
	convert_to_QTI(path, exam_content)

	# Create document
	print("Đang tạo tài liệu...")
	create_exam_document(path, exam_content)

if __name__ == "__main__":
	main()