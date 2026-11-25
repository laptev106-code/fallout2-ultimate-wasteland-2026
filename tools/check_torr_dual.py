import os
import struct, zlib

def get_msg_from_dat(dat_path, target_rel):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        dir_size, _ = struct.unpack('<II', f.read(8))
        f.seek(- (dir_size + 8), os.SEEK_END)
        num_files = struct.unpack('<I', f.read(4))[0]
        for _ in range(num_files):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            packed, real_size, pack_size, offset = struct.unpack('<BIII', f.read(13))
            if name.lower().replace('\\', '/') == target_rel.lower().replace('\\', '/'):
                f.seek(offset)
                raw = f.read(pack_size)
                return zlib.decompress(raw) if packed else raw
    return None

RPU_ENG_DAT = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
eng_torr = get_msg_from_dat(RPU_ENG_DAT, "text/english/dialog/kctorr.msg").decode('latin1')
print("English Torr in rpu.dat total lines:", len(eng_torr.splitlines()))

# Check which numbers are in our Russian kctorr.msg
with open(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\russian\dialog\kctorr.msg", "r", encoding="cp1251") as f:
    rus_torr = f.read()

import re
rus_nums = set(re.findall(r"\{(\d+)\}", rus_torr))
eng_nums = set(re.findall(r"\{(\d+)\}", eng_torr))

missing_in_eng = rus_nums - eng_nums
print("Missing in English Torr:", sorted([int(x) for x in missing_in_eng]))
