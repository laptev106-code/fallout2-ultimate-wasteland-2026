with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/mvk_board.html', 'rb') as f:
    raw = f.read()

text = raw.decode('utf-8', errors='ignore')
print("Decoded length:", len(text))
for line in text.splitlines():
    if any(k in line.lower() for k in ['войти', 'регистрация', 'ошибка', 'обсужд', 'тема', 'fallout', '18']):
        print("Line:", line[:120])
