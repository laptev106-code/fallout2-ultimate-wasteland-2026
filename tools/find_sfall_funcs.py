import os, re

headers_dir = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\headers"

for root, dirs, files in os.walk(headers_dir):
    for f in files:
        if f.endswith(".h"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as h:
                for i, line in enumerate(h):
                    if "sfall_func" in line and any(w in line.lower() for w in ["script", "sid", "scenery", "action", "use", "click"]):
                        print(f"{f}:{i+1} -> {line.strip()}")
