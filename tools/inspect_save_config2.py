with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\main.py", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find("# 1. f2_res.ini")
if idx != -1:
    print(text[idx:idx+2500])
