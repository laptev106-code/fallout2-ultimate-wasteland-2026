import struct
import zlib
import os

def extract_from_dat(dat_path, target_names, out_dir):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        file_size = f.tell() + 8
        dir_size, _ = struct.unpack('<II', f.read(8))
        dir_offset = file_size - dir_size - 8
        f.seek(dir_offset)
        num_files = struct.unpack('<I', f.read(4))[0]
        
        for _ in range(num_files):
            name_len = struct.unpack('<I', f.read(4))[0]
            fname = f.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
            is_c, usize, csize, offset = struct.unpack('<BIII', f.read(13))
            
            for t in target_names:
                if t.lower() in fname.lower():
                    cur_pos = f.tell()
                    f.seek(offset)
                    raw = f.read(csize)
                    data = zlib.decompress(raw) if is_c else raw
                    dest = os.path.join(out_dir, os.path.basename(fname))
                    with open(dest, 'wb') as out_f:
                        out_f.write(data)
                    print(f"Extracted {fname} -> {dest}")
                    f.seek(cur_pos)

if __name__ == '__main__':
    rpu = r'E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat'
    out = r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\extracted_rpu'
    os.makedirs(out, exist_ok=True)
    extract_from_dat(rpu, ['ecpariah.int', 'vckuri', 'tribe02'], out)
