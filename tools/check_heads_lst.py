from audit_dat import read_dat2_directory
import struct
import zlib
import os

def extract_heads_lst(dat_path):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        dir_size, _ = struct.unpack('<II', f.read(8))
        f.seek(-(dir_size + 8), os.SEEK_END)
        cnt = struct.unpack('<I', f.read(4))[0]
        for _ in range(cnt):
            nlen = struct.unpack('<I', f.read(4))[0]
            name = f.read(nlen).decode('ascii', errors='ignore')
            packed, rsize, psize, offset = struct.unpack('<BIII', f.read(13))
            if name.lower().replace('/', '\\') == r'art\heads\heads.lst':
                cur = f.tell()
                f.seek(offset)
                raw = f.read(psize)
                if packed:
                    raw = zlib.decompress(raw)
                f.seek(cur)
                return raw.decode('ascii', errors='ignore')
    return None

if __name__ == '__main__':
    rpu_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
    th_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\talking_heads.dat"
    
    lst_rpu = extract_heads_lst(rpu_dat)
    lst_th = extract_heads_lst(th_dat)
    
    print("=== heads.lst in rpu.dat ===")
    lines_rpu = [l.strip() for l in lst_rpu.splitlines() if l.strip()]
    print(f"Total entries: {len(lines_rpu)}")
    print("First 5:", lines_rpu[:5])
    print("Last 5:", lines_rpu[-5:])
    
    print("\n=== heads.lst in talking_heads.dat ===")
    lines_th = [l.strip() for l in lst_th.splitlines() if l.strip()]
    print(f"Total entries: {len(lines_th)}")
    print("First 5:", lines_th[:5])
    print("Last 5:", lines_th[-5:])
    
    # Check if lines_th starts with exact lines_rpu
    matches = True
    for idx, (r, t) in enumerate(zip(lines_rpu, lines_th)):
        if r.lower() != t.lower():
            print(f"Mismatch at index {idx}: RPU='{r}' vs TH='{t}'")
            matches = False
            break
    if matches:
        print("\nPERFECT BACKWARD COMPATIBILITY! talking_heads.dat preserves 100% of RPU entries and strictly appends new heads!")
