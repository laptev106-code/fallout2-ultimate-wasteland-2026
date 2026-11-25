with open("tools/check_proto_diff.py", "r", encoding="utf-8-sig") as f:
    code = f.read()

import struct, zlib, os

def extract_file(dat_path, inner_name):
    with open(dat_path, "rb") as f:
        f.seek(-8, os.SEEK_END)
        file_size = f.tell() + 8
        dir_size, data_size = struct.unpack('<II', f.read(8))
        f.seek(file_size - dir_size - 8)
        num_files = struct.unpack('<I', f.read(4))[0]
        for _ in range(num_files):
            name_len = struct.unpack('<I', f.read(4))[0]
            fname = f.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
            is_compressed, uncomp_size, comp_size, offset = struct.unpack('<BIII', f.read(13))
            if fname.lower() == inner_name.lower():
                f.seek(offset)
                data = f.read(comp_size if is_compressed else uncomp_size)
                return zlib.decompress(data) if is_compressed else data
    return None

base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"
p_miria = extract_file(os.path.join(base, "DB_Enchanced_Miria.dat"), "data/party.txt").decode('ascii', errors='ignore')
print("Miria party.txt entries:")
for l in p_miria.splitlines():
    if "miria" in l.lower() or "maria" in l.lower():
        print(" ", l)
