import sys
sys.path.insert(0, r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools")
from audit_all_texts import read_dat

files = read_dat(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\talking_heads_that_rpu_map_update_patch.dat")
maps = [f for f in files if f.lower().endswith(".map")]
print(f"Total maps in talking_heads_that_rpu_map_update_patch.dat: {len(maps)}")
for m in sorted(maps):
    print(" ", m)
