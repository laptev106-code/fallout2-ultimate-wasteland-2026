with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_highlighting.ssl", "r", encoding="cp1251", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines[:120]):
    print(f"{i+1:3}: {l.rstrip()}")
