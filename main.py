import os
from datetime import datetime
from pathlib import Path

from termcolor import colored

from handler import convert_to_QTI, create_exam_document, get_exam_content


def main():
    for prompt_dir in sorted(Path("prompts").iterdir()):
        print(colored(f"Đang xử lí prompt {prompt_dir.stem}...", "yellow"))

        path = f"./dist/{prompt_dir.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not os.path.exists(path):
            os.makedirs(path)

        # Get exam content from API
        print(
            colored("├── ", "blue") + colored("Đang tạo nội dung đề thi...", "yellow")
        )
        exam_content = get_exam_content(path, str(prompt_dir))

        # Create QTI file
        print(colored("├── ", "blue") + colored("Đang tạo file zip QTI...", "yellow"))
        convert_to_QTI(path, exam_content)

        # Create document
        print(colored("└── ", "blue") + colored("Đang tạo file docx...", "yellow"))
        create_exam_document(path, exam_content)

        print()


if __name__ == "__main__":
    main()
