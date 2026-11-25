import os

def extract_strings(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    import re
    strings = re.findall(b"[\x20-\x7e]{4,}", data)
    return [s.decode("ascii") for s in strings]

p = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_highlighting.int"
if os.path.exists(p):
    print("Strings in tools/gl_highlighting.int:")
    for s in extract_strings(p):
        if any(k in s.lower() for k in ["ini", "key", "highlight", "critter", "los", "sfall"]):
            print(" ", s)
