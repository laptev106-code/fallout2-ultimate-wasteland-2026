import shutil, os, subprocess

src = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_highlighting.int"
targets = [
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\scripts\gl_highlighting.int",
    r"E:\Fallout2_Ultimate\Fallout2_HD\DATA\scripts\gl_highlighting.int"
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copy2(src, t)
    print(f"Copied {src} -> {t} ({os.path.getsize(t)} bytes)")

# Update fo2tweaks.ini to set highlighting=0
def disable_fo2_high(ini_path):
    if not os.path.exists(ini_path):
        return
    with open(ini_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    new_lines = []
    for l in lines:
        if l.strip().startswith("highlighting="):
            new_lines.append("highlighting=0\n")
        else:
            new_lines.append(l)
    with open(ini_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Set highlighting=0 in {ini_path}")

for root in [r"E:\Fallout2_Ultimate\Fallout2_Gameplay", r"E:\Fallout2_Ultimate\Fallout2_HD", r"D:\AG games mods\fallout2-ultimate-wasteland-2026"]:
    disable_fo2_high(os.path.join(root, "mods", "fo2tweaks.ini"))

# Repack DAT
pack_script = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\pack_dat.py"
if os.path.exists(pack_script):
    subprocess.run(["py", pack_script], check=True)
    print("Repacked DATs successfully!")
