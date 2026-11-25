import os

# Let's inspect define_extra.h around OBJ_DATA_SID
with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\headers\define_extra.h", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines[455:485]):
    print(f"{i+456:3}: {l.rstrip()}")
