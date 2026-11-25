import sys
sys.path.insert(0, r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools")
from audit_all_texts import read_dat

for name in ["mods/rpu.dat", "mods/rpu_russian.dat"]:
    files = read_dat(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\\" + name.replace('/', '\\'))
    matches = [f for f in files if "tribec7" in f.lower()]
    print(f"{name}: {matches}")
