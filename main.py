import os
from datetime import datetime

from clize import run
from termcolor import colored

from handler import convert_to_QTI, create_exam_document, get_exam_content


def main(*, path="", shuffle=False):
    """
    Generate a contest from prompts.

    :param p,path: Path to output.
    :param shuffle: Generated problems are shuffled, e.g. when there are multiple prompts.
    """

    path = f"./dist/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(f"{path}/logs"):
        os.makedirs(f"{path}/logs")

    print(colored(f"Đang tạo đề thi tại {path}...", "yellow"))

    # Get exam content from API
    print(colored("├── ", "blue") + colored("Đang tạo nội dung đề thi...", "yellow"))
    exam_content = get_exam_content(path, shuffle)

    # Create QTI file
    print(colored("├── ", "blue") + colored("Đang tạo file zip QTI...", "yellow"))
    convert_to_QTI(path, exam_content)

    # Create document
    print(colored("└── ", "blue") + colored("Đang tạo file docx...", "yellow"))
    create_exam_document(path, exam_content)

    print()


if __name__ == "__main__":
    run(main)
