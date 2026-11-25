import struct, zlib, os

def extract_all_matching(dat_path, prefix, out_base):
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
            if any(fname.lower().startswith(p.lower()) for p in prefix):
                cur = f.tell()
                f.seek(offset)
                data = f.read(comp_size if is_compressed else uncomp_size)
                if is_compressed:
                    data = zlib.decompress(data)
                target = os.path.join(out_base, fname.replace('/', os.sep))
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "wb") as out_f:
                    out_f.write(data)
                print(f"Extracted: {fname} -> {target} ({len(data)} bytes)")
                f.seek(cur)

miria_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\DB_Enchanced_Miria.dat"

for p in [r"E:\Fallout2_Ultimate\Fallout2_Gameplay", r"E:\Fallout2_Ultimate\Fallout2_HD"]:
    out_dir = os.path.join(p, "mods", "rpu_russian_uncensored.dat")
    extract_all_matching(miria_dat, ["data/party.txt", "proto/critters/"], out_dir)
