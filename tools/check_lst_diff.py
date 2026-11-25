import struct, zlib, os

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
                f.seek(offset)
                data = f.read(comp_size if is_compressed else uncomp_size)
                return zlib.decompress(data) if is_compressed else data
    return None

base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"
rpu_lst = extract_file(os.path.join(base, "rpu.dat"), "proto/critters/critters.lst").decode('ascii', errors='ignore').splitlines()
armor_lst = extract_file(os.path.join(base, "npc_armor.dat"), "proto/critters/critters.lst").decode('ascii', errors='ignore').splitlines()
miria_lst = extract_file(os.path.join(base, "DB_Enchanced_Miria.dat"), "proto/critters/critters.lst").decode('ascii', errors='ignore').splitlines()

print(f"Lines in rpu critters.lst: {len(rpu_lst)}")
print(f"Lines in npc_armor critters.lst: {len(armor_lst)}")
print(f"Lines in DB_Enchanced_Miria critters.lst: {len(miria_lst)}")

# Check if any lines in npc_armor are missing in miria_lst
missing_in_miria = [l for l in armor_lst if l and l not in miria_lst]
print(f"Lines in npc_armor missing in miria_lst: {len(missing_in_miria)}")
for l in missing_in_miria[:10]:
    print("  Missing:", l)
