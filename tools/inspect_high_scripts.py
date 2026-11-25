import struct
import os
import re

def extract_strings(b):
    return [s.decode("ascii") for s in re.findall(b"[\x20-\x7e]{4,}", b)]

# Check gl_g_highlighting in fo2tweaks.dat
def extract_from_dat(dat_path, target_file):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        tree_size, file_size = struct.unpack('<II', f.read(8))
        f.seek(-tree_size - 8, os.SEEK_END)
        file_count = struct.unpack('<I', f.read(4))[0]
        for _ in range(file_count):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            is_compressed, real_size, packed_size, offset = struct.unpack('<BIII', f.read(13))
            if name.lower().replace('\\', '/') == target_file.lower().replace('\\', '/'):
                f.seek(offset)
                import zlib
                raw = f.read(packed_size)
                if is_compressed:
                    data = zlib.decompress(raw)
                else:
                    data = raw
                return data
    return None

data_fo2 = extract_from_dat(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\fo2tweaks.dat", "scripts/gl_g_highlighting.int")
if data_fo2:
    print("Found scripts/gl_g_highlighting.int in fo2tweaks.dat!")
    for s in extract_strings(data_fo2):
        if any(w in s.lower() for w in ["toggle", "hold", "mode", "key", "press", "release", "hook", "action"]):
            print("  fo2tweaks:", s)

data_sfall = extract_from_dat(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\sfall.dat", "scripts/gl_highlighting.int")
if data_sfall:
    print("\nFound scripts/gl_highlighting.int in sfall.dat!")
    for s in extract_strings(data_sfall):
        if any(w in s.lower() for w in ["toggle", "hold", "mode", "key", "press", "release", "hook", "action", "is"]):
            print("  sfall:", s)
