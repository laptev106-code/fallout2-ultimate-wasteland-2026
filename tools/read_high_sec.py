path = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\fo2tweaks_v15\mods\fo2tweaks.ini"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    in_sec = False
    for line in f:
        if line.strip().startswith("[highlighting]"):
            in_sec = True
        elif line.strip().startswith("[") and in_sec:
            break
        if in_sec:
            print(line.rstrip())
