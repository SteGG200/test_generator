import text2qti.config
import text2qti.qti
import text2qti.quiz

def convert_to_QTI(path: str, content: str):
	text2qti_config = text2qti.config.Config()
	source_name = 'content.txt'
	filename = 'qti.zip'
	quiz = text2qti.quiz.Quiz(content, config=text2qti_config, source_name=f'{path}/{source_name}')
	qti = text2qti.qti.QTI(quiz)
	qti.save(f'{path}/{filename}')
	print(f"Đã tạo file zip QTI thành công: {path}/{filename}")
