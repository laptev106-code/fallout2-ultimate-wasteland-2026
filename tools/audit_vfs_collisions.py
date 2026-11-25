import os
import struct

base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"
with open(os.path.join(base, "mods_order.txt"), "r") as f:
    order = [line.strip() for line in f if line.strip() and not line.startswith(";")]

# Track all files inside data/ and proto/
file_locations = {}

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
            fname = df.read(name_len).decode('ascii', errors='ignore').replace('\\', '/').lower()
            df.seek(13, os.SEEK_CUR)
            if fname.startswith("data/") or fname.startswith("proto/"):
                if fname not in file_locations:
                    file_locations[fname] = []
                file_locations[fname].append(dat)

print("=== VFS SYSTEM FILES COLLISION AUDIT (data/ & proto/) ===")
collisions = {k: v for k, v in file_locations.items() if len(v) > 1}
for f, dats in sorted(collisions.items()):
    print(f"File: {f} present in {len(dats)} DATs: -> OVERRIDDEN BY: {dats[-1]}")
    for d in dats:
        print(f"    - {d}")
