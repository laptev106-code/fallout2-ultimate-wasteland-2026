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

rpu_rus_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"
loose_base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\russian\dialog"

for fname in ["mccornel.msg", "mcmiria.msg", "vccasidy.msg", "vcdrtroy.msg", "kcdunton.msg", "kctorr.msg"]:
    loose_path = os.path.join(loose_base, fname)
    dat_content = get_msg_from_dat(rpu_rus_dat, f"text/russian/dialog/{fname}")
    if not dat_content:
        continue
    
    with open(loose_path, 'r', encoding='cp1251', errors='ignore') as lf:
        loose_lines = [l.strip() for l in lf.readlines() if l.strip()]
    
    dat_lines = [l.strip() for l in dat_content.decode('cp1251', errors='ignore').splitlines() if l.strip()]
    
    # find lines in loose that are not in dat
    added = [l for l in loose_lines if l not in dat_lines]
    print(f"\n*** {fname} *** (added in loose: {len(added)} lines)")
    for l in added[:10]:
        print("  ", l)
