import os

with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\fo2tweaks_v15\mods\fo2tweaks.ini", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "sfall-mods" in line:
            print(line)
