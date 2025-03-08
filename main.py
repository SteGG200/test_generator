import os
from datetime import datetime
from pathlib import Path

from handler import convert_to_QTI, create_exam_document, get_exam_content


def main():
    for prompt_dir in sorted(Path("prompts").iterdir()):
        print(f"Đang xử lí prompt {prompt_dir.stem}...")

        path = f"./dist/{prompt_dir.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not os.path.exists(path):
            os.makedirs(path)

        # Get exam content from API
        print("Đang tạo nội dung đề thi...")
        exam_content = get_exam_content(path, str(prompt_dir))

        # Create QTI file
        print("Đang tạo tài liệu QTI...")
        convert_to_QTI(path, exam_content)

        # Create document
        print("Đang tạo tài liệu...")
        create_exam_document(path, exam_content)

        print()


if __name__ == "__main__":
    main()
