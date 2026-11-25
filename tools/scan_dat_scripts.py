import os
import struct

def scan_dat(dat_path):
    gl_scripts = []
    try:
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
                if "gl_" in fname.lower() or fname.lower().endswith(".int"):
                    if "gl_" in fname.lower():
                        gl_scripts.append((fname, uncomp_size))
    except Exception as e:
        pass
    return gl_scripts

base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"
for file in os.listdir(base):
    full = os.path.join(base, file)
    if os.path.isfile(full) and file.lower().endswith(".dat"):
        scripts = scan_dat(full)
        if scripts:
            print(f"DAT: {file} ({len(scripts)} gl_ scripts)")
            for s in scripts:
                print(f"  - {s[0]} ({s[1]} bytes)")
