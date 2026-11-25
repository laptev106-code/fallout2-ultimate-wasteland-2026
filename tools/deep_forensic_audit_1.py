import os, sys, struct, re
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import build_profile_vfs, read_vfs_text, read_dat2_directory

print('--- DEEP FORENSIC AUDIT PASS ---')

gp_dir = r'E:\Fallout2_Ultimate\Fallout2_Gameplay'
hd_dir = r'E:\Fallout2_Ultimate\Fallout2_HD'

# 1. Check all global scripts (gl_*.int) in both profiles
for pname, pdir in [('Gameplay', gp_dir), ('HD', hd_dir)]:
    vfs, collisions, order, stats = build_profile_vfs(pdir)
    gl_scripts = {k: v for k, v in vfs.items() if k.startswith('scripts\\gl_') and k.endswith('.int')}
    print(f'[{pname}] Total global scripts (gl_*.int): {len(gl_scripts)}')
    for k in sorted(gl_scripts.keys()):
        src = gl_scripts[k]['source']
        sz = gl_scripts[k].get('real_size', 0)
        if sz == 0:
            print(f'  [ERROR ZERO BYTE SCRIPT] {k} from {src}')

# 2. Check all heads in heads.lst: verify that art assets exist in VFS
for pname, pdir in [('Gameplay', gp_dir), ('HD', hd_dir)]:
    vfs, collisions, order, stats = build_profile_vfs(pdir)
    heads_lst = vfs.get(r'art\heads\heads.lst')
    if heads_lst:
        txt, _ = read_vfs_text(heads_lst)
        lines = [l.strip() for l in txt.splitlines() if l.strip() and not l.startswith(';')]
        missing_art = []
        for line in lines:
            parts = line.split(',')
            head_dir = parts[0].strip()
            # check art\heads\<head_dir>
            matches = [k for k in vfs.keys() if k.lower().startswith(f'art\\heads\\{head_dir.lower()}')]
            if not matches:
                missing_art.append(head_dir)
        print(f'[{pname}] heads.lst checked: {len(lines)} heads. Missing art directories: {len(missing_art)}')
        if missing_art:
            print(f'  Missing head art folders: {missing_art[:10]}')

# 3. Check map files: check for invalid script IDs or missing script mappings
# Let's inspect scripts.lst
for pname, pdir in [('Gameplay', gp_dir), ('HD', hd_dir)]:
    vfs, collisions, order, stats = build_profile_vfs(pdir)
    slst_info = vfs.get(r'scripts\scripts.lst')
    scripts_lst_entries = {}
    if slst_info:
        txt, _ = read_vfs_text(slst_info)
        for idx, line in enumerate(txt.splitlines()):
            line = line.strip()
            if line and not line.startswith(';'):
                parts = line.split()
                sname = parts[0].lower()
                if sname.endswith('.int'):
                    sname = sname[:-4]
                scripts_lst_entries[sname] = idx
    print(f'[{pname}] scripts.lst has {len(scripts_lst_entries)} valid script names.')
    
    missing_int = []
    for sname in scripts_lst_entries:
        int_key = f'scripts\\{sname}.int'
        if int_key not in vfs:
            missing_int.append(int_key)
    print(f'[{pname}] Scripts in scripts.lst missing .int in VFS: {len(missing_int)}')
    if missing_int:
        print(f'  Missing .int files (sample): {missing_int[:10]}')
