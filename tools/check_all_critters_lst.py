import struct, os

def check_lst(dat_path):
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
            f.seek(13, os.SEEK_CUR)
            if "critters.lst" in fname.lower():
                print(f"Found critters.lst in: {dat_path}")

base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"
for file in os.listdir(base):
    if file.endswith(".dat") and os.path.isfile(os.path.join(base, file)):
        check_lst(os.path.join(base, file))
