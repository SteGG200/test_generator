import importlib.util
import json
import os
import random
import shutil

import dotenv
from rich import print
from rich.prompt import Confirm

dotenv.load_dotenv()


def load_handler(handler_type: str, handler_name: str):
    handler_path = os.path.join("handlers", handler_type, f"{handler_name}.py")

    if not os.path.exists(handler_path):
        raise ImportError(f"Module {handler_name} not found at {handler_path}.")

    module_name = f"handlers.{handler_type}.{handler_name.replace('/', '.')}"

    spec = importlib.util.spec_from_file_location(module_name, handler_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "handler"):
        raise ImportError(f"Module {handler_name} does not define function handler.")

    return module.handler


def content_handler(
    path: str, config_global: dict, config_per_prompt: dict, always_use_llm: bool
):
    content_dir = os.path.join(path, "content.txt")

    if os.path.isfile(content_dir):
        do_overwrite = Confirm.ask(
            (
                "[yellow]Bạn có muốn ghi đè lên nội dung đề thi định dạng QTI-compatible tại [/yellow]"
                f"[white]{content_dir}[/white]"
                "[yellow]?[/yellow]"
            )
        )
        if not do_overwrite:
            print(
                (
                    "[blue]│   └── [/blue]"
                    "[green]Đã đọc nội dung đề thi định dạng QTI-compatible thành công: [/green]"
                    f"[white]{content_dir}[/white]"
                )
            )

            with open(content_dir, "r", encoding="utf-8") as log:
                return log.read()

    content_dict = {}
    n_prompts = len(config_per_prompt)
    for i, (key, config_per_prompt_curr) in enumerate(config_per_prompt.items()):
        prompt_name = config_per_prompt_curr["prompt"]

        print(
            (
                "[blue]│   ├── [/blue]"
                f"[yellow]Đang xử lí batch {i + 1}/{n_prompts} (prompt: [white]{prompt_name}[/white])..."
            )
        )

        prompt_dir = os.path.join("prompts", f"{prompt_name}.txt")
        prompt_copy_dir = os.path.join(path, prompt_dir)
        os.makedirs(os.path.dirname(prompt_copy_dir), exist_ok=True)
        shutil.copy(prompt_dir, os.path.join(path, prompt_dir))

        content_curr_dict = {}

        n_attempts = 0
        succeeded = False
        while not succeeded:
            n_attempts += 1

            print(
                f"[blue]│   │   ├── [/blue][yellow]Lần chạy #{n_attempts}...[/yellow]"
            )

            do_use_llm = always_use_llm or Confirm.ask(
                "[yellow]Bạn có muốn dùng LLM để sinh mới nội dung?[/yellow]"
            )

            log_dir = os.path.join(path, "logs", f"{key}.json")

            try:
                if do_use_llm:
                    front_handler = load_handler(
                        "frontHandlers", config_per_prompt_curr["front_handler"]
                    )
                    n_problems = config_per_prompt_curr["n_problems"]

                    prompt_dir = os.path.join("prompts", f"{prompt_name}.txt")
                    with open(prompt_dir, "r", encoding="utf-8") as log:
                        prompt_content = log.read()

                    content_curr_dict = front_handler(prompt_content, n_problems)

                    with open(log_dir, "w+", encoding="utf-8") as log:
                        json.dump(content_curr_dict, log, ensure_ascii=False, indent=4)
                else:
                    with open(log_dir, "r", encoding="utf-8") as log:
                        content_curr_dict = json.load(log)
                succeeded = True

            except Exception as error_msg:
                print(
                    (
                        "[blue]│   │   │   ├── [/blue]"
                        f"[red]Thông báo lỗi: [/red]"
                        f"[white]{error_msg}[/white]"
                    )
                )
                print(
                    (
                        "[blue]│   │   │   ├── [/blue]"
                        f"[red]Xin hãy kiểm tra nội dung đề thi định dạng JSON tại: [/red]"
                        f"[white]{log_dir}[/white]"
                    )
                )
                print("[blue]│   │   │   └── [/blue][yellow]Đang thử lại...[/yellow]")

        content_dict.update(
            {f"{key}_{_key}": _value for _key, _value in content_curr_dict.items()}
        )

        print(
            (
                "[blue]│   │   └── [/blue]"
                + f"[green]Đã đọc nội dung đề thi được sinh bởi prompt [white]{prompt_name}[/white] thành công.[/green]"
            )
        )

    do_shuffle = config_global["shuffle"]
    if do_shuffle:
        content_dict_items = list(content_dict.items())
        random.shuffle(content_dict_items)
        content_dict = dict(content_dict_items)

    back_handler = load_handler("backHandlers", config_global["back_handler"])
    content = back_handler(content_dict, path)

    content_dir = os.path.join(path, "content.txt")
    with open(content_dir, "w+", encoding="utf-8") as log:
        log.write(content)

    print(
        (
            "[blue]│   └── [/blue]"
            "[green]Đã tạo nội dung đề thi định dạng QTI-compatible thành công: [/green]"
            f"[white]{content_dir}[/white]"
        )
    )
