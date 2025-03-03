# Exam Generator Tool

Exam Generator is a python tool for generating exam

This tool uses API from [OpenRouter](https://openrouter.ai/)

## Table of Contents
- [Installation](#installation)
- [Basic usage](#basic-usage)
- [Customizing the prompt](#customizing-the-prompt)

## Installation

**Requirements tool**: 
- python 3.8+

You can optionally create a virtual environment for project by using `virtualenv` or `venv` before installation step.

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
$env:API_KEY=<OPENROUTER_API_KEY>
```

Or you can also create a `.env` file and set variable `API_KEY=<OPENROUTER_API_KEY>`

## Basic usage

To run the tool, use following command:
```bash
python main.py
```

This is the output:
```yaml
dist/{timeCreated}:
  - content.txt # Response from OpenRouter API
  - qti.zip # QTI file for Canvas
  - dethi.docx # Microsoft Word File
```

## Customizing the prompt

You can modify default prompt in `prompt.txt` file to change the output content to whatever you want. 

However, you must ensure that the `content.txt` file follows the format below (assuming that option b is the correct answer):

```txt
[Question number]. [Question content]
a) [Option a]
*b) [Option b]
c) [Option c]
d) [Option d]
```

A correct answer always begins with a asterisk (*). Each question is separated by a blank line.

For example:

```txt
1. Thuộc tính CSS nào được sử dụng để thay đổi màu chữ của một phần tử?
a) font-color
*b) color
c) text-color
d) foreground-color

2. Thẻ HTML nào được sử dụng để tạo một danh sách không có thứ tự?
a) `<ol>`
b) `<li>`
*c) `<ul>`
d) `<dl>`
```

### Comment in prompt:

Use `//` or `/**/` syntax to comment in your prompt.

```txt
// This line isn't included in the prompt

/*
This is also comment 
and isn't included.
*/
```

## Directory Structure

```yaml
handler:
  - apiHandler # Handler prompting and returning responses from OpenRouter API
  - convertHandler # Handler converting exam content to QTI file
  - docxHandler # Handler generating file docx
main # Entry point
test
```