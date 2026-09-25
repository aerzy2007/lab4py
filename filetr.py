import asyncio
import json
import os
import re
from pathlib import Path


def split_sentences(text: str):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part for part in parts if part]


async def main():
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        file_name = config["file"]
        target_lang = config["lang"]
        module_name = config["module"].strip().lower()
        output = config["output"].strip().lower()
        sentence_limit = int(config["sentences"])

        path = Path(file_name)

        if not path.exists():
            print("Помилка: файл не знайдено")
            return

        full_text = path.read_text(encoding="utf-8")
        sentences = split_sentences(full_text)
        selected = sentences if sentence_limit <= 0 else sentences[:sentence_limit]
        selected_text = " ".join(selected)

        if module_name in ("gtrans4", "gtrans4_module"):
            from translation_pkg import gtrans4_module as module
            detected = await module.LangDetect(full_text, "lang")
            translated = await module.TransLate(selected_text, "auto", target_lang)
            used_module = "gtrans4_module"

        elif module_name in ("gtrans3", "gtrans3_module"):
            from translation_pkg import gtrans3_module as module
            detected = module.LangDetect(full_text, "lang")
            translated = module.TransLate(selected_text, "auto", target_lang)
            used_module = "gtrans3_module"

        elif module_name in ("deep", "deeptr", "deep_module"):
            from translation_pkg import deep_module as module
            detected = module.LangDetect(full_text, "lang")
            translated = module.TransLate(selected_text, "auto", target_lang)
            used_module = "deep_module"

        else:
            print("Помилка: невідомий модуль у config.json")
            return

        print("Назва файлу:", file_name)
        print("Розмір файлу:", os.path.getsize(path), "байт")
        print("Кількість символів:", len(full_text))
        print("Кількість речень:", len(sentences))
        print("Мова тексту:", detected)

        if translated.startswith("Помилка"):
            print(translated)
            return

        if output == "screen":
            print("\nМова перекладу:", module.CodeLang(target_lang))
            print("Модуль:", used_module)
            print("Переклад:")
            print(translated)

        elif output == "file":
            code = target_lang.lower()
            if len(code) > 3:
                converted = module.CodeLang(target_lang)
                if len(converted) <= 3:
                    code = converted

            new_name = f"{path.stem}_{code}{path.suffix}"
            Path(new_name).write_text(translated, encoding="utf-8")
            print("Ok")
            print("Створено файл:", new_name)

        else:
            print("Помилка: output повинен бути screen або file")

    except Exception as error:
        print("Помилка:", error)

asyncio.run(main())
