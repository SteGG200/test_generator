from handler import create_exam_document

def test():
	with open("./dist/20250217_152828/content.md", "r") as file:
		content = file.read()
		try:
			print("Đang tạo tài liệu...")
			create_exam_document(content)
		except Exception as err:
			print(err)

if __name__ == "__main__":
	test()