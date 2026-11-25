import struct, zlib, os

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

rpu_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
rpu_rus = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"

eng_msg = get_msg_from_dat(rpu_dat, 'text/english/dialog/tribec7.msg')
rus_msg = get_msg_from_dat(rpu_rus, 'text/russian/dialog/tribec7.msg')

print("English 2000-2002:")
for l in eng_msg.decode('latin1').splitlines():
    if any(k in l for k in ["{2000}", "{2001}", "{2002}"]):
        print(" ", l)

print("Russian 2000-2002:")
for l in rus_msg.decode('cp1251').splitlines():
    if any(k in l for k in ["{2000}", "{2001}", "{2002}"]):
        print(" ", l)
