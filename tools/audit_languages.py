import os
import sys
import struct
import zlib

def unpack_file(dat_path, file_info):
    with open(dat_path, 'rb') as f:
        f.seek(file_info['offset'])
        data = f.read(file_info['pack_size'])
        if file_info['packed']:
            data = zlib.decompress(data)
        return data

def read_dat(dat_path):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        dir_size, total_size = struct.unpack('<II', f.read(8))
        f.seek(- (dir_size + 8), os.SEEK_END)
        file_count = struct.unpack('<I', f.read(4))[0]
        files = []
        for _ in range(file_count):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            packed, real_size, pack_size, offset = struct.unpack('<BIII', f.read(13))
            files.append({
                'name': name,
                'packed': packed,
                'real_size': real_size,
                'pack_size': pack_size,
                'offset': offset
            })
        return files

dats = [
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\resurrection_interface.dat"
]

for p in dats:
    if os.path.exists(p):
        files = read_dat(p)
        print(f"\n=== DAT: {os.path.basename(p)} ({len(files)} files) ===")
        for f in files:
            fl = f['name'].lower()
            if "door.msg" in fl:
                print("  File:", f['name'])
                data = unpack_file(p, f)
                lines = [l for l in data.decode("latin1", errors="ignore").splitlines() if any(k in l for k in ["601", "620", "621"])]
                print("    Target lines:", lines)
            elif "intrface" in fl or "art/intrface" in fl:
                if "resurrection" in p.lower():
                    print("  Resurrection FRM:", f['name'])
