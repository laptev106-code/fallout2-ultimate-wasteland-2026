import os
import struct

def find_in_dats(inner_file):
    base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"
    with open(os.path.join(base, "mods_order.txt"), "r") as f:
        order = [line.strip() for line in f if line.strip() and not line.startswith(";")]
    for dat in order:
        full = os.path.join(base, dat)
        if not os.path.isfile(full): continue
        with open(full, "rb") as df:
            df.seek(-8, os.SEEK_END)
            file_size = df.tell() + 8
            dir_size, _ = struct.unpack('<II', df.read(8))
            df.seek(file_size - dir_size - 8)
            num_files = struct.unpack('<I', df.read(4))[0]
            for _ in range(num_files):
                name_len = struct.unpack('<I', df.read(4))[0]
                fname = df.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
                df.seek(13, os.SEEK_CUR)
                if fname.lower() == inner_file.lower():
                    print(f"Found {inner_file} in: {dat}")

find_in_dats("data/party.txt")
find_in_dats("data/ai.txt")
