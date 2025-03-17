from handler import create_exam_document

def test():
	path = "./dist/20250303_144235"
	with open(f"{path}/content.txt", "r") as file:
		content = file.read()
		print("Đang tạo tài liệu...")
		create_exam_document(path, content)

if __name__ == "__main__":
	test()