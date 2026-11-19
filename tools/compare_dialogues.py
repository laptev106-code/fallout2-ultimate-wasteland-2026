import struct
import zlib
import os

def extract_file_from_dat(dat_path, target_subpath):
    target = target_subpath.lower().replace('/', '\\')
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        dir_size, _ = struct.unpack('<II', f.read(8))
        f.seek(-(dir_size + 8), os.SEEK_END)
        cnt = struct.unpack('<I', f.read(4))[0]
        for _ in range(cnt):
            nlen = struct.unpack('<I', f.read(4))[0]
            name = f.read(nlen).decode('ascii', errors='ignore')
            packed, rsize, psize, offset = struct.unpack('<BIII', f.read(13))
            if name.lower().replace('/', '\\') == target:
                cur = f.tell()
                f.seek(offset)
                raw = f.read(psize)
                if packed:
                    raw = zlib.decompress(raw)
                f.seek(cur)
                return raw
    return None

if __name__ == '__main__':
    dat_patch = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\talking_heads_that_rpu_map_update_patch.dat"
    dat_rpu_ru = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"
    
    test_files = [
        r"text\russian\dialog\DCSmitty.msg",
        r"text\russian\dialog\VCDrTroy.msg",
        r"text\russian\dialog\ACKlint.msg",
        r"text\russian\dialog\mcMiria.msg"
    ]
    
    for tf in test_files:
        raw_patch = extract_file_from_dat(dat_patch, tf)
        raw_rpu = extract_file_from_dat(dat_rpu_ru, tf)
        
        print(f"\n=== Comparing {tf} ===")
        print(f"  In patch: {'Found (' + str(len(raw_patch)) + ' bytes)' if raw_patch else 'Not found'}")
        print(f"  In rpu_ru: {'Found (' + str(len(raw_rpu)) + ' bytes)' if raw_rpu else 'Not found'}")
        
        if raw_patch and raw_rpu:
            if raw_patch == raw_rpu:
                print("  IDENTICAL MATCH!")
            else:
                lines_patch = raw_patch.decode('cp1251', errors='ignore').splitlines()
                lines_rpu = raw_rpu.decode('cp1251', errors='ignore').splitlines()
                print(f"  DIFFERENCE! Lines in patch: {len(lines_patch)}, lines in rpu_ru: {len(lines_rpu)}")
                # Show differences
                set_patch = set(lines_patch)
                set_rpu = set(lines_rpu)
                diff_patch = [l for l in lines_patch if l not in set_rpu and l.strip()]
                diff_rpu = [l for l in lines_rpu if l not in set_patch and l.strip()]
                print(f"  Lines only in patch ({len(diff_patch)}):")
                for d in diff_patch[:5]:
                    print(f"    + {d}")
                print(f"  Lines only in rpu_ru ({len(diff_rpu)}):")
                for d in diff_rpu[:5]:
                    print(f"    - {d}")
