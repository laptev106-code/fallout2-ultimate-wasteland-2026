import os, struct, zlib, re

def read_dat(dat_path):
    files = {}
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        dir_size, total_size = struct.unpack('<II', f.read(8))
        f.seek(-(dir_size + 8), os.SEEK_END)
        file_count = struct.unpack('<I', f.read(4))[0]
        for _ in range(file_count):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            packed, real_size, pack_size, offset = struct.unpack('<BIII', f.read(13))
            key = name.lower().replace('/', '\\')
            files[key] = {
                'name': name,
                'packed': packed,
                'real_size': real_size,
                'pack_size': pack_size,
                'offset': offset,
                'archive': dat_path
            }
    return files

def get_data(info):
    with open(info['archive'], 'rb') as f:
        f.seek(info['offset'])
        data = f.read(info['pack_size'] if info['packed'] else info['real_size'])
        if info['packed']:
            return zlib.decompress(data)
        return data

def parse_msg(text):
    entries = {}
    pattern = re.compile(r'\{(\d+)\}\s*\{([^}]*)\}\s*\{([^}]*)\}')
    for m in pattern.finditer(text):
        num = int(m.group(1))
        sound = m.group(2)
        val = m.group(3)
        entries[num] = (sound, val)
    return entries

ecco_dat = r'E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_y_ecco.dat'
ecco_files = read_dat(ecco_dat)

import sys
sys.path.insert(0, '.')
import tools.engine_full_audit as efa
vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')

diffs = []
ecco_ru_dialogs = [k for k in ecco_files if k.startswith('text\\russian\\dialog\\') and k.endswith('.msg')]

for k in ecco_ru_dialogs:
    e_data = get_data(ecco_files[k]).decode('cp1251', errors='ignore')
    e_entries = parse_msg(e_data)
    
    v_info = vfs.get(k)
    if not v_info:
        diffs.append((k, 'MISSING_IN_VFS', len(e_entries), []))
        continue
    v_data, enc = efa.read_vfs_text(v_info)
    v_entries = parse_msg(v_data) if v_data else {}
    
    missing_in_vfs = set(e_entries.keys()) - set(v_entries.keys())
    diff_source = v_info['source']
    if missing_in_vfs:
        diffs.append((k, diff_source, len(missing_in_vfs), sorted(list(missing_in_vfs))))

print(f"Total EcCo Russian dialogs: {len(ecco_ru_dialogs)}")
print(f"Files with missing lines in VFS: {len(diffs)}")
for k, src, count, lines in diffs:
    base_src = os.path.basename(src)
    print(f"  {k} (overridden by {base_src}): missing {count} lines: {lines[:8]} ... (total {count})")
