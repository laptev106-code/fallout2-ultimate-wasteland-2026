# -*- coding: utf-8 -*-
import os, struct, zlib

def search_dat(dat_path, query):
    if not os.path.exists(dat_path):
        return
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        dir_size, _ = struct.unpack('<II', f.read(8))
        f.seek(- (dir_size + 8), os.SEEK_END)
        num_files = struct.unpack('<I', f.read(4))[0]
        for _ in range(num_files):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            packed, real_size, pack_size, offset = struct.unpack('<BIII', f.read(13))
            if query.lower() in name.lower():
                print(f"Found in {os.path.basename(dat_path)}: {name}")

for d in [
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\master.dat",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"
]:
    search_dat(d, "yellow")
    search_dat(d, "dog")
