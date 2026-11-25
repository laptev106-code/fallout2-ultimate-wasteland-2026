import sys
sys.path.insert(0, r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools")
from audit_all_texts import read_dat

files = read_dat(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat")
maps = [f for f in files if f.lower().endswith(".map")]
print(f"Total maps in rpu.dat: {len(maps)}")
for m in sorted(maps):
    if any(k in m.lower() for k in ["epa", "tribe"]):
        print(" ", m)
