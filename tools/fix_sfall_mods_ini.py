import os

def update_sfall_mods(ini_path):
    if not os.path.exists(ini_path):
        print("Not found:", ini_path)
        return
    
    with open(ini_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    lines = [l.strip() for l in content.splitlines()]
    
    # Check if [Highlighting] exists
    has_section = any(l.lower() == "[highlighting]" for l in lines)
    if not has_section:
        new_content = "[Highlighting]\nKey=0\nCritters=0\nCheckLOS=0\n\n" + content
    else:
        # replace or ensure Key=0
        new_lines = []
        in_high = False
        key_found = False
        for l in content.splitlines():
            if l.strip().lower() == "[highlighting]":
                in_high = True
                new_lines.append(l)
            elif in_high and l.strip().startswith("["):
                if not key_found:
                    new_lines.append("Key=0")
                    key_found = True
                in_high = False
                new_lines.append(l)
            elif in_high and l.strip().lower().startswith("key="):
                new_lines.append("Key=0")
                key_found = True
            else:
                new_lines.append(l)
        if in_high and not key_found:
            new_lines.append("Key=0")
        new_content = "\n".join(new_lines)

    with open(ini_path, "w", encoding="utf-8") as f:
        f.write(new_content.strip() + "\n")
    print("Updated:", ini_path)

for p in [
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\sfall-mods.ini",
    r"E:\Fallout2_Ultimate\Fallout2_HD\mods\sfall-mods.ini",
    r"D:\AG games mods\fallout2-ultimate-wasteland-2026\mods\sfall-mods.ini"
]:
    update_sfall_mods(p)
