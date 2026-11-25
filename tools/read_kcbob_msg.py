import struct, os

def get_file_from_dat(dat_path, target_file):
    with open(dat_path, 'rb') as f:
        f.seek(-8, 2)
        dir_tree_size, dat_size = struct.unpack('<II', f.read(8))
        f.seek(dat_size - dir_tree_size - 8)
        num_files = struct.unpack('<I', f.read(4))[0]
        for _ in range(num_files):
            fname_len = struct.unpack('<I', f.read(4))[0]
            fname = f.read(fname_len).decode('ascii', errors='ignore').replace('\\', '/')
            is_comp, real_sz, comp_sz, offset = struct.unpack('<BIII', f.read(13))
            if target_file.lower() in fname.lower():
                cur = f.tell()
                f.seek(offset)
                data = f.read(comp_sz)
                if is_comp:
                    import zlib
                    data = zlib.decompress(data)
                f.seek(cur)
                return data
    return None

data = get_file_from_dat(r'E:\Fallout2_Ultimate\Fallout2_Gameplay\master.dat', 'kcbob.msg')
if data:
    for line in data.decode('cp1251', errors='ignore').splitlines()[:30]:
        print(line)
