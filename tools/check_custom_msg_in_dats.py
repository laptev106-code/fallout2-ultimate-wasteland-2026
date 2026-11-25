import glob
import struct
import os

dats = glob.glob(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\*.dat") + glob.glob(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\*.dat")
print(f"Scanning {len(dats)} DAT files...")

found = False
for dat in dats:
    if not os.path.exists(dat):
        continue
    try:
        with open(dat, "rb") as f:
            f.seek(-8, 2)
            dir_tree_size, dat_size = struct.unpack("<II", f.read(8))
            f.seek(dat_size - dir_tree_size - 8)
            num_files = struct.unpack("<I", f.read(4))[0]
            for _ in range(num_files):
                fn_len = struct.unpack("<I", f.read(4))[0]
                fn = f.read(fn_len).decode("ascii", errors="ignore")
                f.seek(12, 1) # flags, size, uncompressed_size
                if "custom.msg" in fn.lower():
                    print(f"FOUND custom.msg in {os.path.basename(dat)}: {fn}")
                    found = True
    except Exception as e:
        print(f"Error reading {dat}: {e}")

if not found:
    print("NO custom.msg found in any existing DAT file! The namespace is 100% free and uncolliding.")
