import re

with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\headers\sfall.h", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if any(w in line.lower() for w in ["script", "scenery", "proto_sc", "proto_"]):
            if "#define" in line:
                print(line.strip())
