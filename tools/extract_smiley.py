import os
import struct
import zlib

def extract_from_dat(dat_path, target_names, out_dir):
    os.makedirs(out_dir, exist_ok=True)
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
            base_name = os.path.basename(fname).lower()
            if base_name in target_names:
                cur = f.tell()
                f.seek(offset)
                data = f.read(comp_size if is_compressed else uncomp_size)
                if is_compressed:
                    data = zlib.decompress(data)
                out_path = os.path.join(out_dir, base_name)
                with open(out_path, "wb") as out_f:
                    out_f.write(data)
                print(f"Extracted: {fname} -> {out_path} ({len(data)} bytes)")
                f.seek(cur)

th_patch = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\talking_heads_that_rpu_map_update_patch.dat"
extract_from_dat(th_patch, ["kcsmiley.int", "kcsmiley.msg"], "tools/extracted_smiley_patch")

rpu = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
extract_from_dat(rpu, ["kcsmiley.int", "kcsmiley.msg"], "tools/extracted_smiley_rpu")
