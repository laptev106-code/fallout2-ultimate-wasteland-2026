import os
import struct
import zlib

rpu = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
with open(rpu, "rb") as f:
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
        if fname.lower() in ["text/english/dialog/tribec7.msg", "text/english/dialog/scelise.msg"]:
            cur = f.tell()
            f.seek(offset)
            data = f.read(comp_size if is_compressed else uncomp_size)
            if is_compressed:
                data = zlib.decompress(data)
            print(f"Found in rpu.dat: {fname} ({len(data)} bytes)")
            out = os.path.join("tools", os.path.basename(fname))
            with open(out, "wb") as o:
                o.write(data)
            f.seek(cur)
