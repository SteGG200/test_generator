import os

import dotenv
import toml
from openai import OpenAI

dotenv.load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/"
MODEL = "google/gemini-2.0-pro-exp-02-05:free"


def get_prompt(prompt_dir: str):
    # Read prompt content from file prompt.txt
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


def toml_to_qti_compatible(content_toml: str):
    content_dict = toml.loads(content_toml)
    content = ""

    def _get_indented_multiline_str(s: str):
        lines = s.splitlines()
        result = lines[0]
        for line in lines[1:]:
            result += f"\n    {line}"
        return result

    for i, problem in content_dict.items():
        content += f"{i}. {_get_indented_multiline_str(problem['question'])}\n"
        for j, choice in enumerate(problem["choices"]):
            choice_prefix = (
                f"{'*' if j == problem['correct_index'] else ''}{chr(ord('a') + j)})"
            )
            content += f"{choice_prefix} {_get_indented_multiline_str(choice)}\n"
        content += "\n"

    return content


def get_exam_content(path: str, prompt_dir: str):
    toml_to_qti_compatible("")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    response = client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": get_prompt(prompt_dir)}]
    )
    content_toml = response.choices[0].message.content
    assert content_toml != None

    with open(f"{path}/content.toml", "w+") as log:
        log.write(content_toml)
        log.close()

    content_qti_compatible = toml_to_qti_compatible(content_toml)

    with open(f"{path}/content.txt", "w+") as log:
        log.write(content_qti_compatible)
        log.close()

    return content_qti_compatible
