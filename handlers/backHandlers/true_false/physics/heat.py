import io
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def get_images(problem):
    variables = problem["variables"]
    temperature = variables["temperature"]
    time = variables["time"]

    plt.figure(figsize=(8, 5))
    for i in range(len(time) - 1):
        plt.plot([time[i], time[i + 1]], [temperature[i], temperature[i + 1]], "r-")

    plt.scatter(
        time,
        [t if t is not None else np.nan for t in temperature],
        color="b",
        zorder=2,
    )
    plt.xlabel("Thời gian (phút)")
    plt.ylabel("Nhiệt độ (°C)")
    plt.grid(True)

    return [fig2img(plt)]


def handler(content_dict: dict, path: str) -> str:
    """
    Takes in dict 'content_dict' where keys are the prompts and values are the respective LLM responses.
    Generates images under 'path' if needed.
    Returns text in QTI-compatible format.
    """

    def _get_indented_multiline_str(s: str):
        lines = [line.strip() for line in s.splitlines()]
        result = lines[0]
        for line in lines[1:]:
            result += f"\n        {line}"  # Should be enough
        return result

    content = ""

    for i, (key, problem) in enumerate(content_dict.items()):
        question = f"{problem['question']}\n\n"
        for j, image in enumerate(get_images(problem)):
            image_dir_relative = os.path.join(
                "assets",
                f"{key}_{j}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            )
            image_dir = os.path.join(path, image_dir_relative)
            image.save(image_dir)
            question += f"![{key}_{j}]({image_dir_relative})\n\n"
        content += f"{i + 1}. {_get_indented_multiline_str(question)}\n"

        content = "\n".join([line.strip() for line in content.splitlines()])  # temp

        is_true = problem["is_true"]
        for j, statement_pair in enumerate(problem["statements"]):
            statement = (
                statement_pair["true"] if is_true[j] else statement_pair["false"]
            )
            # statement_prefix = f"[{'*' if is_true[j] else ' '}]"
            statement_prefix = f"[{'ĐÚNG' if is_true[j] else 'SAI'}]"  # temp
            content += (
                f"{statement_prefix} {_get_indented_multiline_str(statement)}\n\n"
            )

    for i, (key, problem) in enumerate(content_dict.items()):
        solution = problem["solution"].replace("\n", "\n\n")
        content += f"{i + 1}. Lời giải\n\n{solution}\n\n"  # temp

    return content
