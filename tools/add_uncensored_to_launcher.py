import os

p_app = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\js\app.js"
with open(p_app, "r", encoding="utf-8") as f:
    text = f.read()

uncensored_entry = """  },
  {
    id: "uncensored",
    title: "AUTHENTIC UNCENSORED TRANSLATION",
    category: "ПЕРЕВОД",
    badge: "18+ БЕЗ ЦЕНЗУРЫ",
    version: "v2026.1",
    author: "Black Isle, LevCorp, Antigravity",
    desc: "Аутентичный некастрированный перевод Fallout 2 (18+): возвращен живой взрослый язык Пустошей без ханжеской цензуры 1С, исправлен квест Торра и Дантонов, устранены ошибки воровства и непереведенные книги.",
    cancels: "Ханжескую цензуру 1С («негодяи», «шалуны»), английские фразы при неудачной краже, непереведенные книги навыков и иероглифы/каракули.",
    specs: ["Атмосфера: Взрослый канон 1998", "Синхронизация: Talking Heads Lip-Sync", "Кодировка: Windows-1251 ANSI", "Квесты: Торр и Дантоны (Low/High IQ)"]
  }
];"""

target = """  }
];"""

if 'id: "uncensored"' not in text:
    if target in text:
        text = text.replace(target, uncensored_entry, 1)
        with open(p_app, "w", encoding="utf-8") as f:
            f.write(text)
        print("Added uncensored to app.js successfully")
    else:
        print("Target not found in app.js")
else:
    print("uncensored already in app.js")

# Also copy to E:\Fallout2_Ultimate\launcher\ui\js\app.js
p_runtime_app = r"E:\Fallout2_Ultimate\launcher\ui\js\app.js"
if os.path.exists(p_runtime_app):
    with open(p_runtime_app, "w", encoding="utf-8") as f:
        f.write(text)
    print("Copied to runtime launcher app.js")

# Update index.html counters
p_html = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\index.html"
with open(p_html, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("КАТАЛОГ МОДОВ (25)", "КАТАЛОГ МОДОВ (26)")
html = html.replace("МАКСИМАЛЬНОЕ КОЛИЧЕСТВО МОДОВ (25 МОДУЛЕЙ)", "МАКСИМАЛЬНОЕ КОЛИЧЕСТВО МОДОВ (26 МОДУЛЕЙ)")
html = html.replace("ВСЕ (25 МОДОВ)", "ВСЕ (26 МОДОВ)")
html = html.replace("объединяющая 25 модификаций", "объединяющая 26 модификаций")

with open(p_html, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.html counters to 26")

p_runtime_html = r"E:\Fallout2_Ultimate\launcher\ui\index.html"
if os.path.exists(p_runtime_html):
    with open(p_runtime_html, "w", encoding="utf-8") as f:
        f.write(html)
    print("Copied to runtime launcher index.html")
