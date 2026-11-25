import struct, os
from audit_maps_quests import base

th_dat = os.path.join(base, "talking_heads.dat")
with open(th_dat, "rb") as f:
    f.seek(-8, os.SEEK_END)
    file_size = f.tell() + 8
    dir_size, _ = struct.unpack('<II', f.read(8))
    f.seek(file_size - dir_size - 8)
    num_files = struct.unpack('<I', f.read(4))[0]
    for _ in range(num_files):
        name_len = struct.unpack('<I', f.read(4))[0]
        fname = f.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
        f.seek(13, os.SEEK_CUR)
        if "torr" in fname.lower():
            print(f"Torr in TH: {fname}")
