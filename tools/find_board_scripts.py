with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\headers\scripts.h", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if any(w in line.lower() for w in ["board", "notice", "bulletin", "sign", "poster", "klamat"]):
            print(line.strip())
