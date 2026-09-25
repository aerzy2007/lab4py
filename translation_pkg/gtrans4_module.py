import sys
import asyncio
from googletrans import Translator, LANGUAGES

PYTHON_ERROR = "Помилка: googletrans 4.0.2 потребує Python 3.13 або вище"

POPULAR_LANGUAGES = {
    "uk": "Ukrainian",
    "en": "English",
    "pl": "Polish",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
}

_cache = {}


def _language_code(lang: str):
    lang = lang.strip().lower()
    if lang == "auto":
        return "auto"
    if lang in LANGUAGES:
        return lang
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return None


async def _translate(text: str, src: str, dest: str) -> str:
    key = (text, src, dest)
    if key in _cache:
        return _cache[key]

    last_error = None
    for attempt in range(3):
        try:
            async with Translator() as translator:
                result = await translator.translate(text, src=src, dest=dest)
            _cache[key] = result.text
            return result.text
        except Exception as error:
            last_error = error
            await asyncio.sleep(2 + attempt * 2)

    raise last_error


async def TransLate(text: str, scr: str, dest: str) -> str:
    if sys.version_info < (3, 13):
        return PYTHON_ERROR
    try:
        src = _language_code(scr)
        dst = _language_code(dest)
        if src is None:
            return "Помилка: невідома мова початкового тексту"
        if dst is None or dst == "auto":
            return "Помилка: невідома мова перекладу"
        return await _translate(text, src, dst)
    except Exception as error:
        return "Помилка перекладу: " + str(error)


async def LangDetect(text: str, set: str = "all") -> str:
    if sys.version_info < (3, 13):
        return PYTHON_ERROR
    try:
        async with Translator() as translator:
            result = await translator.detect(text)

        set = set.strip().lower()
        if set == "lang":
            return result.lang
        if set == "confidence":
            return str(result.confidence)
        if set == "all":
            return f"Мова: {result.lang}, confidence: {result.confidence}"
        return "Помилка: set повинен бути lang, confidence або all"
    except Exception as error:
        return "Помилка визначення мови: " + str(error)


def CodeLang(lang: str) -> str:
    lang = lang.strip().lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang].capitalize()
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Помилка: мову не знайдено"


async def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        out = out.strip().lower()
        if out not in ("screen", "file"):
            return "Помилка: out повинен бути screen або file"

        if text:
            rows = [f"{'Код':<8}{'Мова':<15}{'Переклад'}"]
            for code, name in POPULAR_LANGUAGES.items():
                translated = await TransLate(text, "auto", code)
                rows.append(f"{code:<8}{name:<15}{translated}")
                await asyncio.sleep(1)
        else:
            rows = [f"{'Код':<8}{'Мова':<15}"]
            for code, name in POPULAR_LANGUAGES.items():
                rows.append(f"{code:<8}{name:<15}")

        table = "\n".join(rows)

        if out == "screen":
            print(table)
        else:
            with open("languages_gtrans4.txt", "w", encoding="utf-8") as file:
                file.write(table)

        return "Ok"
    except Exception as error:
        return "Помилка: " + str(error)
