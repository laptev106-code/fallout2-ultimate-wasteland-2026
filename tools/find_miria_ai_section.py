import os

with open("tools/check_ai_collision.py", "r") as f:
    pass

import struct, zlib

def extract_file(dat_path, inner_name):
    with open(dat_path, "rb") as f:
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
            if fname.lower() == inner_name.lower():
                cur = f.tell()
                f.seek(offset)
                data = f.read(comp_size if is_compressed else uncomp_size)
                if is_compressed:
                    data = zlib.decompress(data)
                return data
    return None

miria_ai = extract_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\DB_Enchanced_Miria.dat", "data/ai.txt").decode('ascii', errors='replace')
ecco_ai = extract_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_y_ecco.dat", "data/ai.txt").decode('ascii', errors='replace')

# Find diff or sections with Miria
lines = miria_ai.splitlines()
miria_section = []
recording = False
for line in lines:
    if "miria" in line.lower() or "custom" in line.lower() or recording:
        miria_section.append(line)
        if len(miria_section) > 50:
            break

print("Lines mentioning Miria in DB_Enchanced_Miria ai.txt:")
for l in lines:
    if "miria" in l.lower():
        print(" ", l)
