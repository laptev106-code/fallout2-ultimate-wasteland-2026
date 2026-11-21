import os, sys, struct
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import build_profile_vfs, read_dat2_directory, read_vfs_text, extract_dat2_file

print('=== AUDIT: MAPS & PROTOTYPES SCRIPT REFERENCES ===')

def check_references(pname, pdir):
    vfs, collisions, order, stats = build_profile_vfs(pdir)
    master_entries = read_dat2_directory(os.path.join(pdir, 'master.dat'))
    
    # 1. Build map of script_id -> script_filename from scripts.lst
    slst_info = vfs.get(r'scripts\scripts.lst')
    txt, _ = read_vfs_text(slst_info)
    script_id_to_name = {}
    line_idx = 0
    for line in txt.splitlines():
        line = line.strip()
        if line and not line.startswith(';'):
            sname = line.split()[0].lower()
            if sname.endswith('.int'):
                sname = sname[:-4]
            script_id_to_name[line_idx] = sname
            line_idx += 1
            
    print(f'[{pname}] Total mapped script IDs: {len(script_id_to_name)}')
    
    # 2. Check all .pro files for script IDs
    pro_files = [k for k in vfs.keys() if k.startswith('proto\\') and k.endswith('.pro')]
    print(f'[{pname}] Total .pro files in VFS: {len(pro_files)}')
    
    missing_pro_scripts = []
    for pk in pro_files:
        info = vfs[pk]
        if info['is_disk']:
            with open(info['disk_path'], 'rb') as f:
                data = f.read()
        else:
            data = extract_dat2_file(info)
        
        # PRO format in Fallout:
        # offset 0x20 is usually script ID (signed int32)
        if len(data) >= 0x24:
            script_id = struct.unpack('>i', data[0x20:0x24])[0]
            if script_id != -1 and script_id != 0:
                # script_id is 1-based or 0-based? In fallout pro files, script_id is typically 1-based index or direct index
                # Let's check if script_id is in script_id_to_name or script_id-1
                # Actually, in PRO format: scriptId is PID or script index
                pass
                
    # 3. Check all .map files in VFS
    map_files = [k for k in vfs.keys() if k.startswith('maps\\') and k.endswith('.map')]
    print(f'[{pname}] Total .map files in VFS: {len(map_files)}')
    
    # Let's verify each .map file header
    corrupt_maps = []
    for mk in map_files:
        info = vfs[mk]
        if info['is_disk']:
            sz = os.path.getsize(info['disk_path'])
        else:
            sz = info['real_size']
        if sz < 100:
            corrupt_maps.append((mk, sz))
    print(f'[{pname}] Corrupt/empty maps: {len(corrupt_maps)}')
    if corrupt_maps:
        print('  Corrupt maps:', corrupt_maps)

check_references('Gameplay', r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
check_references('HD', r'E:\Fallout2_Ultimate\Fallout2_HD')
