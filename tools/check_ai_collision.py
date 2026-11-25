import os
import struct
import zlib

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

miria_ai = extract_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\DB_Enchanced_Miria.dat", "data/ai.txt")
ecco_ai = extract_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_y_ecco.dat", "data/ai.txt")

if miria_ai:
    print(f"Miria ai.txt size: {len(miria_ai)}")
    has_miria_in_miria = b"Miria" in miria_ai or b"miria" in miria_ai or b"MIRIA" in miria_ai
    print(f"Has Miria in DB_Enchanced_Miria ai.txt: {has_miria_in_miria}")
else:
    print("No data/ai.txt in DB_Enchanced_Miria.dat")

if ecco_ai:
    print(f"EcCo ai.txt size: {len(ecco_ai)}")
    has_miria_in_ecco = b"Miria" in ecco_ai or b"miria" in ecco_ai or b"MIRIA" in ecco_ai
    print(f"Has Miria in rpu_y_ecco ai.txt: {has_miria_in_ecco}")
