path = r"d:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_temple_hints.ssl"
with open(path, "r", encoding="cp1251", errors="ignore") as f:
    text = f.read()

text = text.replace("Hold Shift to highlight gear, traps, and containers", "Press Caps Lock for permanent highlighting (or hold Shift)")
text = text.replace("Зажми клавишу Shift, чтобы подсветить вещи, ловушки и сундуки", "Нажми Caps Lock для постоянной подсветки (или зажми Shift)")

with open(path, "w", encoding="cp1251", errors="ignore") as f:
    f.write(text)

print("Updated hints text!")
