import os
import struct

dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_y_ecco.dat"
with open(dat, "rb") as f:
    f.seek(-8, os.SEEK_END)
    file_size = f.tell() + 8
    dir_size, data_size = struct.unpack('<II', f.read(8))
    dir_offset = file_size - dir_size - 8
    f.seek(dir_offset)
    num_files = struct.unpack('<I', f.read(4))[0]
    for _ in range(num_files):
        name_len = struct.unpack('<I', f.read(4))[0]
        fname = f.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
        is_compressed, uncomp_size, comp_size, offset = struct.unpack('<BIII', f.read(13))
        if fname.lower().endswith(".ini") or fname.lower().endswith(".txt") or fname.lower().endswith(".cfg"):
            print(f"EcCo config: {fname} ({uncomp_size} bytes)")
