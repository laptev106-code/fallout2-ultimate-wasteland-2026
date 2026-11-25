import struct, os, zlib

def extract_file(dat_path, target_file, out_path):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        tree_size, file_size = struct.unpack('<II', f.read(8))
        f.seek(-tree_size - 8, os.SEEK_END)
        file_count = struct.unpack('<I', f.read(4))[0]
        for _ in range(file_count):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            is_compressed, real_size, packed_size, offset = struct.unpack('<BIII', f.read(13))
            if name.lower() == target_file.lower():
                cur_pos = f.tell()
                f.seek(offset)
                data = f.read(packed_size)
                if is_compressed:
                    data = zlib.decompress(data)
                with open(out_path, 'wb') as out:
                    out.write(data)
                print(f"Extracted {name} ({len(data)} bytes) to {out_path}")
                return
    print(f"File {target_file} not found")

extract_file("E:/Fallout2_Ultimate/Fallout2_Gameplay/mods/fo2tweaks.dat", "scripts\\gl_g_auto_reload.int", "D:/AG games mods/fallout2-ultimate-wasteland-2026/tools/gl_g_auto_reload.int")
