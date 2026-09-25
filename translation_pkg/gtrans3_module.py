import sys
import time

VERSION_ERROR = (
    "Помилка: googletrans==3.1.0a0 потрібно запускати з Python 3.11. "
    "Поточна версія Python 3.13 або вище."
)

POPULAR_LANGUAGES = {
    "uk": "Ukrainian",
    "en": "English",
    "pl": "Polish",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
}

if sys.version_info >= (3, 13):
    Translator = None
    LANGUAGES = {}
else:
    try:
        from googletrans import Translator, LANGUAGES
    except Exception:
        Translator = None
        LANGUAGES = {}


def _version_ok():
    return (3, 11) <= sys.version_info < (3, 13)


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


def TransLate(text: str, scr: str, dest: str) -> str:
    if not _version_ok():
        return VERSION_ERROR
    if Translator is None:
        return "Помилка: googletrans==3.1.0a0 не встановлено"

    try:
        src = _language_code(scr)
        dst = _language_code(dest)
        if src is None:
            return "Помилка: невідома мова початкового тексту"
        if dst is None or dst == "auto":
            return "Помилка: невідома мова перекладу"
        return Translator().translate(text, src=src, dest=dst).text
    except Exception as error:
        return "Помилка перекладу: " + str(error)


def LangDetect(text: str, set: str = "all") -> str:
    if not _version_ok():
        return VERSION_ERROR
    if Translator is None:
        return "Помилка: googletrans==3.1.0a0 не встановлено"

    try:
        result = Translator().detect(text)
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
    if not _version_ok():
        return VERSION_ERROR
    if Translator is None:
        return "Помилка: googletrans==3.1.0a0 не встановлено"

    lang = lang.strip().lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang].capitalize()
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Помилка: мову не знайдено"


def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        out = out.strip().lower()
        if out not in ("screen", "file"):
            return "Помилка: out повинен бути screen або file"

        if text:
            rows = [f"{'Код':<8}{'Мова':<15}{'Переклад'}"]
            for code, name in POPULAR_LANGUAGES.items():
                translated = TransLate(text, "auto", code)
                rows.append(f"{code:<8}{name:<15}{translated}")
                time.sleep(1)
        else:
            rows = [f"{'Код':<8}{'Мова':<15}"]
            for code, name in POPULAR_LANGUAGES.items():
                rows.append(f"{code:<8}{name:<15}")

        table = "\n".join(rows)
        if out == "screen":
            print(table)
        else:
            with open("languages_gtrans3.txt", "w", encoding="utf-8") as file:
                file.write(table)
        return "Ok"
    except Exception as error:
        return "Помилка: " + str(error)
