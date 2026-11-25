import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory

mods_dir = r"E:\Games\Fallout 2 (Expansion Version)\mods"
for f in os.listdir(mods_dir):
    p = os.path.join(mods_dir, f)
    if os.path.isfile(p) and f.lower().endswith(".dat"):
        d = read_dat2_directory(p)
        print(f"=== {f} ({len(d)} files) ===")
        for k in sorted(d.keys())[:15]:
            print(f"  {k} ({d[k]['real_size']} bytes)")
