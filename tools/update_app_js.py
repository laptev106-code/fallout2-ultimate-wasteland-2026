import os

with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\js\mods_data.js", "r", encoding="utf-8") as f:
    mods_code = f.read().strip()

targets = [
    r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\js\app.js",
    r"E:\Fallout2_Ultimate\launcher_nextgen\ui\js\app.js"
]

for p in targets:
    if not os.path.exists(p):
        print("Not found:", p)
        continue
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_idx = content.find("const MODS_DATABASE = [")
    end_idx = content.find("class LauncherApp {")
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + mods_code + "\n\n" + content[end_idx:]
        with open(p, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated:", p)
    else:
        print("Could not find delimiters in:", p)
