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
rpu_lst = extract_file(os.path.join(base, "rpu.dat"), "proto/critters/critters.lst").decode('ascii', errors='ignore').splitlines()
miria_lst = extract_file(os.path.join(base, "DB_Enchanced_Miria.dat"), "proto/critters/critters.lst").decode('ascii', errors='ignore').splitlines()

print(f"RPU proto critters.lst lines: {len(rpu_lst)}")
print(f"Miria proto critters.lst lines: {len(miria_lst)}")

# Print the last 10 lines of both
print("Last 5 in RPU:")
for l in rpu_lst[-5:]:
    print(" ", l)

print("Last 5 in Miria:")
for l in miria_lst[-5:]:
    print(" ", l)
