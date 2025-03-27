import os
from datetime import datetime
from pathlib import Path

import tomli
from clize import ArgumentError, run
from rich import print

from handlers import content_handler, docx_handler, qti_handler

CONFIG_FILE = "config.toml"
PROMPTS_DIR = "prompts"


def generate(
    *,
    config: "c" = "config.toml",
    output: "o" = None,
    raw_content_only: "r" = False,
    always_use_llm: "a" = False,
):
    """
    Generate a contest from prompts.

    :param config: Path to config file.
    :param output: Path to output. Will be created if not exists. (default: dist/{datetime})
    :param raw_content_only: docx and QTI zip files will not be generated.
    :param always_use_llm: Always use LLM to generate content instead of asking each time.
    """

    if not os.path.isfile(config):
        os.makedirs(config, exist_ok=True)

    if output is None:
        output = os.path.join("dist", datetime.now().strftime("%Y%m%d_%H%M%S"))
    elif not os.path.isdir(output):
        raise ArgumentError(f"Not a directory: {output}")

    with open(config, "r", encoding="utf-8") as log:
        config_all = tomli.loads(log.read())

    print(f"[green]Đã đọc config file tại [white]{config}[/white] thành công.[/green]")

    keys_global = ["shuffle", "back_handler"]
    keys_per_prompt = ["prompt", "n_problems", "front_handler"]

    config_global = config_all.get("global", {})

    for key in keys_global:
        if key not in config_global:
            raise KeyError(f"{key} is not specified.")

    config_per_prompt = {}
    if "batch" not in config_all:
        print(
            "[green]Không tìm thấy \[\[batch]] trong config file. Sẽ xử lí lần lượt tất cả prompts được tìm thấy.[/green]"
        )

        for key in keys_per_prompt:
            if key not in config_global:
                raise KeyError(f"{key} is not specified.")

        prompt_dirs = sorted(Path("prompts").iterdir())
        for prompt_dir in prompt_dirs:
            config_per_prompt_curr = {
                key: value
                for key, value in config_global.items()
                if key in keys_per_prompt
            }
            prompt_name = prompt_dir.stem
            config_per_prompt_curr.update({"prompt": prompt_name})
            config_per_prompt[f"batch_{prompt_name}"] = config_per_prompt_curr
    else:
        for i, config_per_prompt_curr_from_file in enumerate(config_all["batch"]):
            config_per_prompt_curr = {
                key: value
                for key, value in config_global.items()
                if key in keys_per_prompt
            }
            config_per_prompt_curr.update(config_per_prompt_curr_from_file)
            config_per_prompt[f"batch_{i}"] = config_per_prompt_curr

            for key in keys_per_prompt:
                if key not in config_per_prompt_curr:
                    raise KeyError(f"Batch {i}: {key} is not specified anywhere.")

    path = output
    if path == "":
        path = f"./dist/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(os.path.join(path, "assets")):
        os.makedirs(os.path.join(path, "assets"))
    if not os.path.exists(os.path.join(path, "logs")):
        os.makedirs(os.path.join(path, "logs"))
    if not os.path.exists(os.path.join(path, "prompts")):
        os.makedirs(os.path.join(path, "prompts"))

    print(f"[yellow]Đang tạo đề thi tại [white]{path}[/white]...[/yellow]")

    print("[blue]├── [/blue][yellow]Đang tạo nội dung đề thi...[/yellow]")

    content_handler(path, config_global, config_per_prompt, always_use_llm)

    if raw_content_only:
        print(
            "[blue]└── [/blue][green]File zip QTI và file docx sẽ không được tạo.[/green]"
        )
    else:
        print("[blue]├── [/blue][yellow]Đang tạo file zip QTI...[/yellow]")
        qti_handler(path)

        print("[blue]└── [/blue][yellow]Đang tạo file docx...[/yellow]")
        docx_handler(path)


if __name__ == "__main__":
    run(generate)
