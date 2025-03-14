# Exam Generator Tool

Exam Generator is a python tool for generating exam.

This tool uses API from [OpenRouter](https://openrouter.ai/).

## Table of Contents

- [Installation](#installation)
- [Basic usage](#basic-usage)
- [Customizing the prompt](#customizing-the-prompt)

## Installation

### Python

Requires `python` 3.8+.

Install dependencies with the following command.

```bash
pip install -r requirements.txt
```

You can optionally create a virtual environment for project by using
`virtualenv` or `venv` before installing dependencies.

[devenv](https://devenv.sh/) users can simply clone this repository then run
`devenv shell` to drop into a virtual environment with the necessary
dependencies.

### OpenRouter API key

Set environment variable `API_KEY` to your OpenRouter API key.

- For Linux:

```bash
export API_KEY=<OPENROUTER_API_KEY>
```

- For Windows Powershell:

```powershell
$env:API_KEY=<OPENROUTER_API_KEY>
```

You can also create a `.env` file containing `API_KEY=<OPENROUTER_API_KEY>`.

## Basic usage

Simply run `python main.py`. Find all options by running
`python main.py --help`.

```
$ python main.py --help
Usage: main.py [OPTIONS]

Generate a contest from prompts.

Options:
  --path=STR   Path to output. (default: )
  --shuffle    Generated problems are shuffled, e.g. when there are multiple prompts.

Other actions:
  -h, --help   Show the help
```

Prompts should be put under the path `prompts`. Their output will be merged into
one exam.

The default output path is `dist/{datetimeCreated}`. The directory structure is
as follows.

```
dist
├── {datetime}:
│   ├── logs
│   │   ├── content_{name of prompt #1}_1.toml # Output of prompt #1 in TOML format.
│   │   ├── content_{name of prompt #2}_1.toml # The first attempt at generating content from prompt #2 failed...
│   │   ├── content_{name of prompt #2}_2.toml # ...but the second one succeeded.
│   │   ├── content_{name of prompt #3}_1.toml
│   │   └── ...
│   ├── content.txt # Contest problems in QTI-compatible format.
│   ├── dethi.docx # Contest problems in DOCX format.
│   └── qti.zip # QTI file for Canvas.
└── ...
```

## Customizing the prompt

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

> [!NOTE]
> The rest of this subsection is deprecated since the QTI-compatible
> syntax has been covered by `contestHandler.py`.

You must ensure that the `content.txt` file follows the format below (assuming
that option b is the correct answer):

```txt
[Number]. [Question]
a) [Option a]
*b) [Option b]
c) [Option c]
d) [Option d]
```

A correct answer always begins with a asterisk (\*). Each question is separated
by a blank line.

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
````

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
