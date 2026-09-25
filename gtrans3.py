import sys
from translation_pkg.gtrans3_module import TransLate, LangDetect, CodeLang, LanguageList, VERSION_ERROR

def main():
    print("=== googletrans 3.1.0a0 ===")
    print("Python:", sys.version.split()[0])

    if sys.version_info >= (3, 13):
        print(VERSION_ERROR)
        return

    text = "Добрий день. Як справи?"
    print("Початковий текст:", text)

    print("\nLangDetect:")
    print(LangDetect(text, "all"))

    print("\nTransLate:")
    print(TransLate(text, "auto", "en"))

    print("\nCodeLang:")
    print("English ->", CodeLang("English"))
    print("en ->", CodeLang("en"))

    print("\n6 популярних мов з перекладом:")
    print(LanguageList("screen", text))

    print("\nЗапис тієї самої таблиці у файл:")
    print(LanguageList("file", text))
    print("Створено файл languages_gtrans3.txt")

main()
