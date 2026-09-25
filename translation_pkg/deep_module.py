import time
from deep_translator import MyMemoryTranslator
from langdetect import detect, detect_langs


POPULAR_LANGUAGES = {
    "uk": ("Ukrainian", "uk-UA"),
    "en": ("English", "en-GB"),
    "pl": ("Polish", "pl-PL"),
    "de": ("German", "de-DE"),
    "fr": ("French", "fr-FR"),
    "es": ("Spanish", "es-ES")
}


def _language_code(lang, text=""):
    lang = lang.lower()

    if lang == "auto":
        detected = detect(text)

        if detected in POPULAR_LANGUAGES:
            return POPULAR_LANGUAGES[detected][1]

        return None

    if lang in POPULAR_LANGUAGES:
        return POPULAR_LANGUAGES[lang][1]

    for code, data in POPULAR_LANGUAGES.items():
        name = data[0]

        if lang == name.lower():
            return data[1]

    return None


def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        source = _language_code(scr, text)
        target = _language_code(dest)

        if source is None:
            return "Помилка: невідома початкова мова"

        if target is None:
            return "Помилка: невідома мова перекладу"

        if source == target:
            return text

        result = MyMemoryTranslator(
            source=source,
            target=target
        ).translate(text)

        return result

    except Exception as error:
        return "Помилка перекладу: " + str(error)


def LangDetect(text: str, set: str = "all") -> str:
    try:
        result = detect_langs(text)[0]

        lang = result.lang
        confidence = result.prob

        if set == "lang":
            return lang

        if set == "confidence":
            return str(confidence)

        if set == "all":
            return f"Мова: {lang}, confidence: {confidence}"

        return "Помилка: невірний параметр set"

    except Exception as error:
        return "Помилка визначення мови: " + str(error)


def CodeLang(lang: str) -> str:
    lang = lang.lower()

    if lang in POPULAR_LANGUAGES:
        return POPULAR_LANGUAGES[lang][0]

    for code, data in POPULAR_LANGUAGES.items():
        name = data[0]

        if lang == name.lower():
            return code

    return "Помилка: мову не знайдено"


def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        rows = []

        if text:
            rows.append(f"{'Код':<8}{'Мова':<15}{'Переклад'}")

            detected = detect(text)

            if detected not in POPULAR_LANGUAGES:
                return "Помилка: мову тексту не підтримано"

            source = POPULAR_LANGUAGES[detected][1]

            for code, data in POPULAR_LANGUAGES.items():
                name = data[0]
                target = data[1]

                if source == target:
                    translated = text
                else:
                    translated = MyMemoryTranslator(
                        source=source,
                        target=target
                    ).translate(text)

                rows.append(
                    f"{code:<8}{name:<15}{translated}"
                )

                time.sleep(1)

        else:
            rows.append(f"{'Код':<8}{'Мова':<15}")

            for code, data in POPULAR_LANGUAGES.items():
                rows.append(
                    f"{code:<8}{data[0]:<15}"
                )

        result_text = "\n".join(rows)

        if out == "screen":
            print(result_text)

        elif out == "file":
            with open(
                "languages_deep.txt",
                "w",
                encoding="utf-8"
            ) as file:
                file.write(result_text)

        else:
            return "Помилка: out повинен бути screen або file"

        return "Ok"

    except Exception as error:
        return "Помилка: " + str(error)