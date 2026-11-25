import struct, zlib, os

def extract_file(dat_path, inner_name):
    if not os.path.isfile(dat_path): return None
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

files_to_check = ["data/maps.txt", "data/quests.txt", "data/worldmap.txt"]
dats_to_check = ["rpu.dat", "rpu_enhanced_worldmap.dat", "rpu_y_ecco.dat", "rpu_russian.dat"]

for inner in files_to_check:
    print("="*50)
    print("CHECKING:", inner)
    for d in dats_to_check:
        dat_full = os.path.join(base, d)
        data = extract_file(dat_full, inner)
        if data:
            print(f"  In {d}: {len(data)} bytes, {len(data.splitlines())} lines")
        else:
            print(f"  In {d}: None")
