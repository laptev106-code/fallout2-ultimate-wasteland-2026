# -*- coding: utf-8 -*-
import os, struct, zlib

def get_file(dat_path, target_rel):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        dir_size, _ = struct.unpack('<II', f.read(8))
        f.seek(- (dir_size + 8), os.SEEK_END)
        num_files = struct.unpack('<I', f.read(4))[0]
        for _ in range(num_files):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            packed, real_size, pack_size, offset = struct.unpack('<BIII', f.read(13))
            if name.lower().replace('\\', '/') == target_rel.lower().replace('\\', '/'):
                f.seek(offset)
                raw = f.read(pack_size)
                return zlib.decompress(raw) if packed else raw
    return None

raw = get_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat", "scripts/kcyellow.int")
if not raw:
    raw = get_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\master.dat", "scripts/kcyellow.int")

with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "wb") as f:
    f.write(raw)
print("Saved kcyellow.int, size:", len(raw))
