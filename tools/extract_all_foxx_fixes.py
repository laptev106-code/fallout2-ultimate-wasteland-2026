with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/foxx_full_changelog.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
lines = text.splitlines()
print(f"Total lines: {len(lines)}")
print("=== All script / quest / fix mentions in Foxx's changelog ===")
for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['квест', 'исправлен', 'скрипт', 'ошибк', 'баг', 'диалог', 'скитер', 'мари', 'умбра', 'азос', 'карты', 'пастбищ', 'торр', 'дантон']):
        print(f"L{i+1}: {l.strip()}")
