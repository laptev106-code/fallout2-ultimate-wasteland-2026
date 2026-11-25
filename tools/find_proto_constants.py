with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\headers\sfall.h", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "PROTO_" in line:
            print(line.strip())
