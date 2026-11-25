import os
import zlib
import struct

dat_path = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"

# In Fallout 2 DAT2:
with open(dat_path, "rb") as f:
    f.seek(-8, 2)
    dir_tree_size, dat_size = struct.unpack("<II", f.read(8))
    f.seek(dat_size - dir_tree_size - 8)
    # The dir tree is compressed or uncompressed?
    # Actually in DAT2, the directory tree is zlib-compressed!
    tree_data = f.read(dir_tree_size)
    try:
        decompressed_tree = zlib.decompress(tree_data)
    except:
        decompressed_tree = tree_data

    # Parse directory tree:
    # First 4 bytes: number of files
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
            print(f"Found {fn}: offset={offset}, real_size={real_size}, packed_size={packed_size}, type={type_flag}")
            f.seek(offset)
            raw = f.read(packed_size)
            if type_flag == 1:
                content = zlib.decompress(raw)
            else:
                content = raw
            text = content.decode("cp1251", errors="replace")
            print("--- FULL CONTENT OF custom.msg in rpu_russian.dat ---")
            print(text)
            with open(r"E:\FALLOUT Ult pjt\tools\base_custom_msg.txt", "w", encoding="cp1251") as out:
                out.write(text)
            print(f"Saved to base_custom_msg.txt ({len(text)} bytes)")
            break
