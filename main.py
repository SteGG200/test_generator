import os
import warnings
from datetime import datetime

from clize import ArgumentError, run
from rich import print

from handlers import convert_to_QTI, create_exam_document, get_exam_content


def generate(
    *,
    mode: "m" = "generated_qti",
    path: "p" = "",
    prefer_llm: "a" = False,
    shuffle: "s" = False,
):
    """
    Generate a contest from prompts.

    :param mode: How `content.txt` should be prepared. One of `generated_qti`, `generated_toml`, `manual`.
    :param path: Path to output.
    :param prefer_llm: (Only in `generated_qti` or `generated_toml` mode) If not, always ask before sending request to LLM.
    :param shuffle: (Only in `generated_toml` mode) Generated problems are shuffled. Useful when there are multiple prompts.
    """

    if mode not in ["generated_qti", "generated_toml", "manual"]:
        raise ArgumentError(f"Invalid mode: {mode}")

    if mode != "generated_toml" and shuffle:
        warnings.warn(
            "Not using `generated_toml` mode. Flag `--shuffle` has no effect."
        )

    if mode not in ["generated_qti", "generated_toml"] and prefer_llm:
        warnings.warn(
            "Not using `generated_qti` or `generated_toml` mode. Flag `--prefer-llm` has no effect."
        )

    if mode == "manual" and path == "":
        raise ArgumentError("Using `manual` mode requires parameter `path` to be set.")

    if path == "":
        path = f"./dist/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(f"{path}/logs"):
        os.makedirs(f"{path}/logs")

    print(f"[yellow]Đang tạo đề thi tại [white]{path}[/white]...[/yellow]")

    # Get exam content from API
    print("[blue]├── [/blue][yellow]Đang tạo nội dung đề thi...[/yellow]")
    exam_content = get_exam_content(mode, path, prefer_llm, shuffle)

    # Create QTI file
    print("[blue]├── [/blue][yellow]Đang tạo file zip QTI...[/yellow]")
    convert_to_QTI(path, exam_content)

    # Create document
    print("[blue]└── [/blue][yellow]Đang tạo file docx...[/yellow]")
    create_exam_document(path, exam_content)

    print()


if __name__ == "__main__":
    run(generate)
