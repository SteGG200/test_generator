from handler import convert_to_QTI
# from module import getLatestPath
def main():
	path = input("name of folder including content: ")
	path = "./dist/" + path + "/content.txt"
	txt_file = open(path, 'r', encoding="utf-8")
	file_content = txt_file.read()
	txt_file.close()
	convert_to_QTI(path, file_content)
if __name__ == "__main__":
	main()