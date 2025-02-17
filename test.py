from handler import create_exam_document

def test():
	with open("content.md", "r") as file:
		content = file.read()
		try:
			print("Đang tạo tài liệu...")
			doc = create_exam_document(content)

			filename = "./dist/de_thi.docx" 
			doc.save(filename)
			print(f"Đã tạo đề thi thành công và lưu với tên: {filename}")
		except Exception as err:
			print(err)

if __name__ == "__main__":
	test()