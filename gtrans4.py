import asyncio
from translation_pkg.gtrans4_module import TransLate, LangDetect, CodeLang, LanguageList

async def main():
    text = "Добрий день. Як справи?"

    print("=== googletrans 4.0.2 ===")
    print("Початковий текст:", text)

    print("\nLangDetect:")
    print(await LangDetect(text, "all"))

    print("\nTransLate:")
    print(await TransLate(text, "auto", "en"))

    print("\nCodeLang:")
    print("English ->", CodeLang("English"))
    print("en ->", CodeLang("en"))

    print("\n6 популярних мов з перекладом:")
    print(await LanguageList("screen", text))

    print("\nЗапис тієї самої таблиці у файл:")
    print(await LanguageList("file", text))
    print("Створено файл languages_gtrans4.txt")

asyncio.run(main())
