import os, struct

def list_all(dat_path):
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

for f in list_all("E:/Fallout2_Ultimate/Fallout2_Gameplay/mods/sfall.dat"):
    print(" ", f)
