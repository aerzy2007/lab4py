from translation_pkg.deep_module import (
    TransLate,
    LangDetect,
    CodeLang,
    LanguageList
)


text = "Добрий день. Як справи?"

print("=== deep-translator / MyMemory ===")
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
print("Створено файл languages_deep.txt")