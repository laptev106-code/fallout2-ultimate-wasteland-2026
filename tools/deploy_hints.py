import shutil, os
import subprocess

src = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_temple_hints.int"
targets = [
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\scripts\gl_temple_hints.int",
    r"E:\Fallout2_Ultimate\Fallout2_HD\DATA\scripts\gl_temple_hints.int"
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copy2(src, t)
    print(f"Copied to {t} ({os.path.getsize(t)} bytes)")

# Also update inside rpu_russian_uncensored.dat using pack_dat.py
pack_script = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\pack_dat.py"
if os.path.exists(pack_script):
    subprocess.run(["py", pack_script], check=True)
    print("Repacked into rpu_russian_uncensored.dat")
