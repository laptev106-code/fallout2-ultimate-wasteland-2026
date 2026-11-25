import os
import zlib
import struct

dat_path = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\master.dat"

with open(dat_path, "rb") as f:
    f.seek(-8, 2)
    dir_tree_size, dat_size = struct.unpack("<II", f.read(8))
    f.seek(dat_size - dir_tree_size - 8)
    tree_data = f.read(dir_tree_size)
    try:
        decompressed_tree = zlib.decompress(tree_data)
    except:
        decompressed_tree = tree_data

    num_files = struct.unpack("<I", decompressed_tree[:4])[0]
    pos = 4
    for i in range(num_files):
        fn_len = struct.unpack("<I", decompressed_tree[pos:pos+4])[0]
        pos += 4
        fn = decompressed_tree[pos:pos+fn_len].decode("ascii", errors="ignore")
        pos += fn_len
        type_flag, real_size, packed_size, offset = struct.unpack("<BIII", decompressed_tree[pos:pos+13])
        pos += 13
        if "custom.msg" in fn.lower():
            print(f"Found {fn}: offset={offset}, real_size={real_size}")
            f.seek(offset)
            raw = f.read(packed_size)
            if type_flag == 1:
                content = zlib.decompress(raw)
            else:
                content = raw
            text = content.decode("ascii", errors="replace")
            print("--- ENGLISH custom.msg ---")
            print(text)
            with open(r"E:\FALLOUT Ult pjt\tools\base_custom_msg_en.txt", "w", encoding="ascii") as out:
                out.write(text)
            break
