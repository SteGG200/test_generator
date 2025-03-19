# Exam Generator Tool

Exam Generator is a python tool for generating exam.

This tool uses API from [OpenRouter](https://openrouter.ai/).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Customizing the prompt](#customizing-the-prompt)

## Installation

### Python

Requires `python` 3.8+.

Install dependencies with the following command.

- For Unix systems:

    ```bash
    python -m venv venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    ```

    [devenv](https://devenv.sh/) users can simply clone this repository then run
    `devenv shell` to drop into a virtual environment with the necessary
    dependencies.

- For Windows Powershell:

    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

### OpenRouter API key

Create a file `.env` at the root of the project and set the following variables.

```env
API_KEY='<YOUR_OPENROUTER_API_KEY>'
MODEL='<OPENROUTER_MODEL>'
```

**Note**:

- `API_KEY` is required, `MODEL` is optional.
- If you don't set the `MODEL` variable, the tool will automatically use the
  `google/gemini-2.0-pro-exp-02-05:free` model.

## Usage

For basic usage, simply run `python main.py` (legacy) or
`python main.py -m "generated_toml"` (for prompts that generate questions in
TOML format).

Find all options by running `python main.py --help`.

```
$ python main.py --help
python main.py -h
Usage: main.py [OPTIONS]

Generate a contest from prompts.

Options:
  -m, --mode=STR     How content.txt should be prepared. One of generated_qti, generated_toml, manual. (default: generated_qti)
  -p, --path=STR     Path to output. (default: )
  -a, --prefer-llm   (Only in generated_qti or generated_toml mode) If not, always ask before sending request to LLM.
  -s, --shuffle      (Only in generated_toml mode) Generated problems are shuffled. Useful when there are multiple prompts.

Other actions:
  -h, --help         Show the help
```

Prompts should be put under the path `prompts`. Their output will be merged into
one contest.

The default output path is `dist/{datetime}`. The directory structure is as
follows.

- `generated_toml` mode:

    ```
    dist
    ├── {datetime}:
    │     ├── logs
    │     │     ├── content_{name of prompt #1}_1.toml # Output of prompt #1 in TOML format.
    │     │     └── ...
    │     ├── content.txt # Contest problems in QTI-compatible format.
    │     ├── dethi.docx # Contest problems in DOCX format.
    │     └── qti.zip # QTI file for Canvas.
    └── ...
    ```

- `generated_qti` mode:

    ```
    dist
    ├── {datetime}:
    │     ├── logs
    │     │     ├── content_{name of prompt #1}_1.txt # Output of prompt #1 in QTI-compatible format.
    │     │     └── ...
    │     ├── content.txt # Contest problems in QTI-compatible format.
    │     ├── dethi.docx # Contest problems in DOCX format.
    │     └── qti.zip # QTI file for Canvas.
    └── ...
    ```

- `manual` mode:

    ```
    dist
    ├── {datetime}:
    │     ├── content.txt # (MANUALLY PROVIDED NOT GENERATED) Contest problems in QTI-compatible format.
    │     ├── dethi.docx # Contest problems in DOCX format.
    │     └── qti.zip # QTI file for Canvas.
    └── ...
    ```

For more information, consult the following section.

## Customizing the prompt

### `generated_toml` mode

The prompt should print out problems in the following TOML format.

```toml
[<Số thứ tự câu>]
question = """Đây là nội dung câu hỏi. \
Có thể gồm nhiều dòng."""
choices = [
    """Đây là nội dung phương án A. \
        Có thể gồm nhiều dòng.""",
    """Đây là nội dung phương án B. \
        Có thể gồm nhiều dòng.""",
    """Đây là nội dung phương án C. \
        Có thể gồm nhiều dòng.""",
    """Đây là nội dung phương án D. \
        Có thể gồm nhiều dòng."""
]
correct_index = 2 # Biểu thị đáp án đúng là C (các đáp án được đánh số từ 0 đến 3)
```

There should be example prompts under `prompts` for reference.

### `generated_qti` mode

You must ensure that the `content.txt` file, which is the response from model
API, follows the format below (assuming that option b is the correct answer):

```txt
[Number]. [Question]
a) [Option a]
*b) [Option b]
c) [Option c]
d) [Option d]
```

A correct answer always begins with a asterisk (\*).

About multi-line question or multi-line answer:

```txt
|
| /* Indentation:
| Question or answer that oppucies more than 1 line
| must have at least this indentation*/
| |
1. [Question]
| |
| [Question continued, so indentation]
| |
a) [Possible answer]
| |
| [Possible answer continued, so indentation]
| |
*b) [Correct answer]
|
...
```

For example:

````txt
1. Thuộc tính CSS nào được sử dụng để thay đổi màu chữ của một phần tử?
a) `font-color`
*b) `color`
c) `text-color`
d) `foreground-color`

2. Đoạn mã:
    ```
    <ol type="A" start="3">
            <li>Item 1</li>
            <li>Item 2</li>
    </ol>
    ```
    Kết quả hiển thị sẽ như thế nào?
a) 1. Item 1
    2. Item 2
b) A. Item 1
    B. Item 2
*c) C. Item 1
    D. Item 2
d) 3. Item 1
    4. Item 2

**Note**: code block like HTML tags should be put in backticks to ensure QTI
output is correct.

### Comment in prompt:

Use `//` or `/**/` syntax to comment in your prompt.

```txt
// This line isn't included in the prompt

/*
This is also comment
and isn't included.
*/
```
````
