with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/foxx_full_changelog.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['выживан', 'голод', 'жажд', 'сна', 'сон', 'survival', 'внешност', 'appearance', 'инсталлятор', 'опци']):
        print(f"{i+1}: {l.strip()}")
