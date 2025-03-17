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

Or you can also create a `.env` file and set variable `API_KEY=<OPENROUTER_API_KEY>`

## Usage

To run the tool, use following command:
```bash
python main.py
```

Output:
```yaml
dist/{timeCreated}:
  - content.txt # Response from OpenRouter API
  - qti.zip # QTI file for Canvas
  - dethi.docx # Microsoft Word File
```

Additionally, you can modify default prompt in `prompt.txt` file to change the output format to whatever you want.

## Directory Structure

```yaml
handler:
  - apiHandler # Handler prompting and returning responses from OpenRouter API
  - convertHandler # Handler converting exam content to QTI file
  - docxHandler # Handler generating file docx
main # Entry point
test
```