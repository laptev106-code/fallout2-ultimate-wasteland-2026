import os
import sys

sys.path.insert(0, r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools")
from audit_all_texts import read_dat

dat_path = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\resurrection_interface.dat"
files = read_dat(dat_path)
print(f"resurrection_interface.dat contains {len(files)} files:")
for f in sorted(files):
    print(" ", f)

# Also check fo2_interface_upscaled.dat
upscaled = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\fo2_interface_upscaled.dat"
if os.path.exists(upscaled):
    ufiles = read_dat(upscaled)
    print(f"\nfo2_interface_upscaled.dat contains {len(ufiles)} files (first 20):")
    for f in sorted(ufiles)[:20]:
        print(" ", f)
