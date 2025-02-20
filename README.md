# Exam Generator Tool

Exam Generator is a python tool for generating exam about HTML and CSS

This tool uses API from [OpenRouter](https://openrouter.ai/)

[Installation](#installation) | [Usage](#usage)

## Installation

**Requirements tool**: 
- python 3.8+

Optionally, you can create a virtual environment for project by using `virtualenv` or `venv` before installation step.

Installation dependencies:
```bash
pip install -r requirements.txt
```

Set environment variable `API_KEY` to your OpenRouter API key

For Linux:
```bash
export API_KEY=<OPENROUTER_API_KEY>
```

For Windows Powershell:
```powershell
$env:API_KEY=<OPENROUTER_API_KEY>w
```

Or you can also create a file `.env` and set variable `API_KEY`

## Usage

To run the tool, use following command:
```bash
python main.py
```

The output file is `de_thi.docx` inside folder `dist/{timeCreated}`. Additionally, there is also a file named `content.md` in the same folder which displays the response from the OpenRouter API.

## Directory Structure

```yaml
handler:
  - apiHandler # Handler prompting and returning responses from OpenRouter API
  - docxHandler # Handler generating file docx
main # Entry point
test
```