import os, sys, struct
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import build_profile_vfs, read_dat2_directory, read_vfs_text, extract_dat2_file

print('=== AUDIT: CRITTER ANIMATION INTEGRITY (OFFSET 0x08) ===')

def check_critter_art(pname, pdir):
    vfs, collisions, order, stats = build_profile_vfs(pdir)
    crit_entries = read_dat2_directory(os.path.join(pdir, 'critter.dat'))
    
    clst_info = vfs.get(r'art\critters\critters.lst') or crit_entries.get(r'art\critters\critters.lst')
    if not clst_info:
        print(f'[{pname}] critters.lst not found!')
        return
    txt, _ = read_vfs_text(clst_info)
    critter_models = [l.strip().split(',')[0].strip().lower() for l in txt.splitlines() if l.strip() and not l.startswith(';')]
    print(f'[{pname}] critters.lst has {len(critter_models)} registered model prefixes.')
    
    crit_pros = [k for k in vfs.keys() if k.startswith('proto\\critters\\') and k.endswith('.pro')]
    print(f'[{pname}] Total critter prototypes in VFS: {len(crit_pros)}')
    
    missing_models = []
    for cp in crit_pros:
        info = vfs[cp]
        if info['is_disk']:
            with open(info['disk_path'], 'rb') as f:
                data = f.read()
        else:
            data = extract_dat2_file(info)
            
        if len(data) >= 0x0C:
            # FID in critter proto is at offset 0x08
            fid = struct.unpack('>I', data[0x08:0x0C])[0]
            model_id = fid & 0x0FFF
            if model_id >= len(critter_models):
                missing_models.append((cp, model_id, len(critter_models)))
            else:
                prefix = critter_models[model_id]
                has_any = any(k.startswith(f'art\\critters\\{prefix}') for k in vfs) or any(k.startswith(f'art\\critters\\{prefix}') for k in crit_entries)
                if not has_any:
                    missing_models.append((cp, model_id, prefix))
                        
    print(f'[{pname}] Critters with missing/invalid animations: {len(missing_models)}')
    if missing_models:
        print('  Invalid critters:', missing_models[:10])

check_critter_art('Gameplay', r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
check_critter_art('HD', r'E:\Fallout2_Ultimate\Fallout2_HD')
