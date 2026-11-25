import struct
import zlib
import os

# 1. Extract original door.msg from rpu_russian.dat
dat_path = r'E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat'
out_path_gameplay = r'E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\text\russian\dialog\door.msg'
out_path_hd = r'E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat\text\russian\dialog\door.msg'

with open(dat_path, 'rb') as f:
    f.seek(-8, os.SEEK_END)
    file_size = f.tell() + 8
    dir_size, _ = struct.unpack('<II', f.read(8))
    dir_offset = file_size - dir_size - 8
    f.seek(dir_offset)
    num_files = struct.unpack('<I', f.read(4))[0]
    
    door_text = None
    for _ in range(num_files):
        name_len = struct.unpack('<I', f.read(4))[0]
        fname = f.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
        is_c, usize, csize, offset = struct.unpack('<BIII', f.read(13))
        if fname.lower() == 'text/russian/dialog/door.msg':
            cur = f.tell()
            f.seek(offset)
            raw = f.read(csize)
            door_text = zlib.decompress(raw).decode('cp1251', errors='ignore') if is_c else raw.decode('cp1251', errors='ignore')
            break

if door_text:
    print(f"Extracted door.msg ({len(door_text)} chars)")
    
    # Add AleSiS Crowbar Fix lines:
    # 601: Already unlocked
    # 620: Crowbar destroyed (player)
    # 621: Crowbar destroyed (companion)
    fix_lines = (
        "\n# AleSiS Crowbar Fix 2026\n"
        "{601}{}{Замок уже открыт.}\n"
        "{620}{}{Монтировка погнулась и пришла в негодность.}\n"
        "{621}{}{ ломает монтировку.}\n"
    )
    door_text += fix_lines
    
    for p in [out_path_gameplay, out_path_hd]:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='cp1251') as out_f:
            out_f.write(door_text)
        print("Installed fixed door.msg into:", p)
else:
    print("ERROR: door.msg not found in rpu_russian.dat")
