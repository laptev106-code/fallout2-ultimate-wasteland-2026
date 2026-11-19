import struct
import os

def list_dat2(dat_path):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        tree_size, file_size = struct.unpack('<II', f.read(8))
        f.seek(-tree_size - 8, os.SEEK_END)
        file_count = struct.unpack('<I', f.read(4))[0]
        files = []
        for _ in range(file_count):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            is_compressed, real_size, packed_size, offset = struct.unpack('<BIII', f.read(13))
            files.append(name)
        return files

for dat_name in ["sfall.dat", "rpu.dat", "f2_res.dat"]:
    p = os.path.join("E:/Fallout2_Ultimate/Fallout2_Gameplay/mods", dat_name)
    if os.path.exists(p):
        try:
            files = list_dat2(p)
            print(f"=== {dat_name} ({len(files)} files) ===")
            for name in files:
                if any(k in name.lower() for k in ['blur', 'glass', 'footstep', 'key', 'pixote', 'mutant', 'head', 'shader', 'overlay']):
                    print(" ", name)
        except Exception as e:
            print(f"Error {dat_name}: {e}")
