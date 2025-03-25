import text2qti.config
import text2qti.qti
import text2qti.quiz
from rich import print

from handlers.const import CONTENT_FILE, QTI_FILE


def convert_to_QTI(path: str, content: str):
    text2qti_config = text2qti.config.Config()
    quiz = text2qti.quiz.Quiz(
        content, config=text2qti_config, source_name=f"{path}/{CONTENT_FILE}"
    )
    qti = text2qti.qti.QTI(quiz)
    qti.save(f"{path}/{QTI_FILE}")
    print(
        "[blue]│   └── [/blue]"
        "[green]Đã tạo file zip QTI thành công: [/green]"
        f"[white]{path}/{QTI_FILE}[/white]"
    )
