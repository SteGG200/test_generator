import text2qti.config
import text2qti.qti
import text2qti.quiz

def convert_to_QTI(path: str, content: str, source_name = 'content.txt'):
	text2qti_config = text2qti.config.Config()
	filename = source_name.split(".")[0] + ".zip"
	quiz = text2qti.quiz.Quiz(content, config=text2qti_config, source_name=f'{path}/{source_name}')
	qti = text2qti.qti.QTI(quiz)
	qti.save(f'{path}/{filename}')
