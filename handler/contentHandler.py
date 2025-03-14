import os
import random
from pathlib import Path

import dotenv
import toml
from openai import OpenAI
from termcolor import colored
from toml import TomlDecodeError

dotenv.load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/"
MODEL = "google/gemini-2.0-pro-exp-02-05:free"


def get_prompt(prompt_dir: str):
    # Read prompt content from file at prompt_dir
    prompt_file = open(prompt_dir, "r")
    prompt_content = prompt_file.read()

    # Remove comments from prompt content
    stack_comment_symbols = []
    buffer_comment_symbols = ""
    parsed_prompt_content = ""
    for index, char in enumerate(prompt_content):
        if len(stack_comment_symbols) > 0:
            if stack_comment_symbols[-1] == "//":
                if char == "\n":
                    parsed_prompt_content += "\n"
                    stack_comment_symbols.pop()
                continue
            elif stack_comment_symbols[-1] == "/*":
                if char == "/" and index - 1 >= 0 and prompt_content[index - 1] == "*":
                    stack_comment_symbols.pop()
                continue
            else:
                raise SyntaxError(
                    f"Invalid comment syntax: {stack_comment_symbols[-1]}"
                )
        if char == "/":
            if buffer_comment_symbols == "/":
                stack_comment_symbols.append("//")
                buffer_comment_symbols = ""
            elif buffer_comment_symbols == "":
                buffer_comment_symbols = "/"
            else:
                raise BufferError(
                    f"Invalid comment syntax in buffer: {buffer_comment_symbols}"
                )
        elif char == "*":
            if buffer_comment_symbols == "/":
                stack_comment_symbols.append("/*")
                buffer_comment_symbols = ""
            elif buffer_comment_symbols == "":
                parsed_prompt_content += char
            else:
                raise BufferError(
                    f"Invalid comment syntax in buffer: {buffer_comment_symbols}"
                )
        else:
            if buffer_comment_symbols == "/":
                parsed_prompt_content += buffer_comment_symbols
                parsed_prompt_content += char
                buffer_comment_symbols = ""
            elif buffer_comment_symbols == "":
                parsed_prompt_content += char
            else:
                raise BufferError(
                    f"Invalid comment syntax in buffer: {buffer_comment_symbols}"
                )

    prompt_file.close()

    return parsed_prompt_content


def toml_to_dict(content_toml: str):
    lines = content_toml.splitlines()
    if lines[0] == "```toml" and lines[-1] == "```":
        content_dict = toml.loads("\n".join(lines[1:-1]))
    else:
        content_dict = toml.loads(content_toml)
    return content_dict


def dict_to_qti_compatible(content_dict: dict, shuffle: bool):
    def _get_indented_multiline_str(s: str):
        lines = [line.strip() for line in s.splitlines()]
        result = lines[0]
        for line in lines[1:]:
            result += f"\n        {line}"  # Should be enough
        return result

    content = ""
    problems = [value for _, value in sorted(content_dict.items())]
    if shuffle:
        random.shuffle(problems)

    for i, problem in enumerate(problems):
        content += f"{i + 1}. {_get_indented_multiline_str(problem['question'])}\n"
        for j, choice in enumerate(problem["choices"]):
            choice_prefix = (
                f"{'*' if j == problem['correct_index'] else ''}{chr(ord('a') + j)})"
            )
            content += f"{choice_prefix} {_get_indented_multiline_str(choice)}\n"
        content += "\n"

    return content


def get_exam_content(path: str, shuffle: bool):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    content_dict = {}

    for prompt_dir in sorted(Path("prompts").iterdir()):
        prompt_name = prompt_dir.stem

        print(
            colored("│   ├── ", "blue")
            + colored(f"Đang xử lí prompt {prompt_name}...", "yellow")
        )

        content_curr_dict = {}

        n_attempts = 0
        succeeded = False
        while not succeeded:
            n_attempts += 1

            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": get_prompt(prompt_dir)}],
            )

            content_curr_raw = response.choices[0].message.content
            assert content_curr_raw is not None

            with open(
                f"{path}/logs/content_{prompt_name}_{n_attempts}.toml",
                "w+",
            ) as log:
                log.write(content_curr_raw)

            try:
                content_curr_dict = toml_to_dict(content_curr_raw)
                succeeded = True
            except TomlDecodeError as error_msg:
                print(
                    colored("│   │   ├── ", "blue")
                    + colored(f"Lần chạy #{n_attempts} gặp lỗi!", "red")
                )
                print(
                    colored("│   │   │   ├── ", "blue")
                    + colored("Thông báo lỗi: ", "red")
                    + f"{error_msg}"
                )
                print(
                    colored("│   │   │   ├── ", "blue")
                    + colored(
                        "Xin hãy kiểm tra nội dung đề thi định dạng TOML AI-generated đã được tạo ở: ",
                        "red",
                    )
                    + f"{path}/logs_failed/content_{prompt_name}_{n_attempts}.toml",
                )
                print(
                    colored("│   │   │   └── ", "blue")
                    + colored("Đang thử lại...", "yellow")
                )

        content_dict.update(
            {f"{prompt_name}_{key}": value for key, value in content_curr_dict.items()}
        )

        print(
            colored("│   │   └── ", "blue")
            + colored(
                f"Đã đọc nội dung đề thi từ prompt {prompt_name} thành công.",
                "green",
            )
        )

    with open(f"{path}/content.txt", "w+") as log:
        log.write(dict_to_qti_compatible(content_dict, shuffle))

    print(
        colored("│   └── ", "blue")
        + colored(
            f"Đã tạo nội dung đề thi định dạng QTI-compatible thành công: {path}/content.txt",
            "green",
        )
    )

    with open(f"{path}/content.txt", "r") as log:
        return log.read()
